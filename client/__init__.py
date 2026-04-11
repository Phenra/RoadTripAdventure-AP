"""
Archipelago client for Road Trip Adventure
This is what the player runs from the Archipelago launcher in order to have AP and the game interact with each other.

Like most retro console games, this inherits from AP's CommonClient classes (which handle a lot of functionality for
us, see comments in RTAContext below) and interacts with an emulator (in this case PCSX2, via an API called PINE).

When AP finishes generating a multiworld, it stores any data saved to the 'slot_data' dictionary as part of our
slot on the server (typically done in the world's 'fill_slot_data' function).

Then, when we connect to that slot on the server using our client, it needs to request and store that slot_data.
This is how we pass any necessary information from the generation process to the client (for example, what the
shop purchases have been randomized to, so we can display the new item names in Road Trip).

Before handling items and locations, we first verify that the game either already has the RTA AP patches applied, 
or is in the main menu so they can be applied (since it's a safe place to do so), and then confirm we've connected 
to the correct slot (by comparing its slot_data's save ID to the one stored in our RTA save file).

Once verified, we start handling items and locations.

For items, CommonClient manages a received_items list for us. All we have to do is regularly check it, keep track
of how many of those items we've already handled, and update the game accordingly.

Lastly, for locations, we need to send the server various commands when we complete location checks in game (using
CommonClient's 'send_msgs' function) so it can send out the corresponding item for that location.
"""

# Standard library imports
import asyncio

# AP imports
from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, get_base_parser, logger
from NetUtils import ClientStatus
from Utils import async_start

# Local imports
from .Patches import patch_rta_no_slot_data, patch_rta_post_connect
from .pine import Pine
from .Helpers import *
from ..names import ItemName
from ..ram_data import Addresses

# Shorthand aliases
StorageType = Addresses.StorageType
TableData = Addresses.TableData

# Constants
MINIMUM_RACE_RANK_FOR_COMPLETION = 5 # In RTA's RAM, 0 is 1st place, so this 6th place
WRONG_SAVE_ID_MSG = "The currently loaded save is an AP save, but it is either for a different slot, or a different multiworld!\n" \
                "Please return to the main menu and either load a save associated with this slot, or start a new game."

# Debug
DEBUG_ALLOW_SAVE_MISMATCH = False

class RTACommandProcessor(ClientCommandProcessor):
    pass # Not adding any new commands beyond those provided by CommonClient for now

# CommonContext is how we interact with AP's CommonClient (which is what we're using for the Road Trip client).
#   In our sub-class, we define a few overrides of default functions in CommonContext, include a few pieces
#   of custom data, and create+store an instance of the interface we're using to read from / write to
#   RTA's memory within PCSX2 (see notes on PINE below).
#
# CommonContext contains many default functions that we don't need to override for RTA, and use as-is - see
#   its .py file for more info on those.
class RTAContext(CommonContext):
    command_processor = RTACommandProcessor
    game = "Road Trip Adventure"
    want_slot_data = True

    # No items are handled locally for RTA, all are received from the server.
    # List of options for this bitfield: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/network%20protocol.md#items_handling-flags
    items_handling = 0b111

    # From the slot_data dictionary passed from the AP world to the server, and then to the client on connection:
    filler_amount = 500 # Default, should be overridden once slot_data received
    save_id = None
    shop_strings = [] # List of PartDescriptions
    area_unlock_mode = None
    remove_double_up_stamps = None
    reset_post_connect_patches = False
    quick_patch_check_failed = False

    # Overriding the default run_gui function in order to set the title of the client window.
    # Taken from the Adventure Client. RaC2's client seems to use basically the same function as well.
    def run_gui(self):
        from kvui import GameManager

        class RoadTripManager(GameManager):
            base_title = "Road Trip Client"
            # icon = r"data/icon.png" # TODO: Custom launcher icon?

        self.ui = RoadTripManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    # The default server_auth function in CommonContext doesn't actually connect you to a slot (just the server).
    #   To do that, we first need a slot name (which CommonContext's 'get_username' prompts the user for), and
    #   then we can send a 'Connect' packet to the server (using CommonContext's 'send_connect' function).
    # Taken from the RaC2 AP.
    async def server_auth(self, password_requested: bool = False):
        # First, request a password if needed. The default server_auth function is set up to do this, so we'll just call it here.
        if password_requested and not self.password:
            await super(RTAContext, self).server_auth(password_requested)
        
        await self.get_username()
        await self.send_connect()

    # CommonContext will call this function every time a package is sent to us.
    #   We only need to write custom behavior for extracting the slot data.
    #   The base CommonClient's 'process_server_cmd' function will update the 'items_received' list for us.
    #   There are many more commands we can react to, documentation here: https://alwaysintreble.github.io/Archipelago/network%20protocol.html#server-client
    #
    # TODO: We can actually do away with the args['slot_data'] parsing if we want by using self.slot_data.save_id instead
    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            print("Connected")

            self.filler_amount = args['slot_data']['filler_amount']
            self.save_id = args['slot_data']['save_id']
            self.shop_strings = args['slot_data']['shop_strings']
            self.area_unlock_mode = args['slot_data']['area_unlock_mode']
            self.remove_double_up_stamps = args['slot_data']['remove_double_up_stamps']

            self.reset_post_connect_patches = True

    # -------- Custom definitions (non-overrides) ---------

    # PINE is the API provided by PCSX2 for reading and writing to the memory of its emulated game.
    #   The library in use here was created by the developer of the Ratchet and Clank 2 AP, and is taken
    #   from that game's implementation.
    pine = Pine() 

    class RTAStatus():
        EMU_NOT_RUNNING = 0
        EMU_NOT_RUNNING_RTA = 1
        RTA_MAIN_MENU_NO_SLOT_DATA = 2
        RTA_MAIN_MENU_WITH_SLOT_DATA = 3
        RTA_OTHER_STATE = 4
        RTA_IN_VANILLA_GAME = 5
        RTA_IN_UNPATCHED_AP_GAME = 6
        RTA_IN_AP_GAME_NO_CLIENT_SAVE_ID = 7
        RTA_IN_WRONG_AP_GAME = 8
        RTA_IN_AP_GAME = 9
        
    # Default RTA status
    RTA_status = RTAStatus.EMU_NOT_RUNNING
    prev_RTA_status = RTAStatus.EMU_NOT_RUNNING
    
    def get_save_id_in_game(self) -> bytes:
        return self.pine.read_bytes(Addresses.ap_save_id.address, Addresses.ap_save_id.length) 

    def set_save_id_in_game(self, id : int) -> None:
        data = int_to_bytes(id, Addresses.ap_save_id.length)
        self.pine.write_bytes(Addresses.ap_save_id.address, data)

    def is_game_waiting_for_save_id(self) -> bool:
        data = self.pine.read_bytes(Addresses.ready_for_ap_save_id.address, Addresses.ready_for_ap_save_id.length) 
        return bytes_to_int(data)

    # The RTA function hook that sets the AP index to its default (0x1) also sets a byte to let the
    #   client know that the save ID can be sent to the game now. This resets that byte to 0x0.
    def set_save_id_bool_to_sent(self) -> None:
        self.pine.write_bytes(Addresses.ready_for_ap_save_id.address, bytes([0]))

    # On new game, we save an ID generated for this slot to RTA's save file. This function determines
    #   whether the seed in the save file matches the one for this slot on the server.
    def save_matches_slot(self):
        if DEBUG_ALLOW_SAVE_MISMATCH:
            return True

        if self.save_id == None:
            return False # Seed will not be set until the client connects to a server
        elif self.is_game_waiting_for_save_id():
            self.set_save_id_in_game(self.save_id)
            self.set_save_id_bool_to_sent()
         
        game_save_id = self.get_save_id_in_game()

        # print("Save ID:", game_save_id)
        # print("Save ID as int", bytes_to_int(game_save_id))
        # print("AP stored ID:", self.save_id)
        # print("AP ID as bytes", int.to_bytes(self.save_id, 4).hex())
        # print(self.save_id == bytes_to_int(game_save_id))

        return self.save_id == bytes_to_int(game_save_id)

    # Setter for RTA_status. Will also call print_status to log status updates to the client.
    def set_status(self, status : RTAStatus):
        # Save previous status so we can compare the new one to the previous one
        self.prev_RTA_status = self.RTA_status

        # Set the new status
        self.RTA_status = status

        # If the status changed, inform the player
        if self.prev_RTA_status != self.RTA_status:
            self.print_status()
        
        if self.prev_RTA_status != self.RTAStatus.RTA_MAIN_MENU_WITH_SLOT_DATA and self.RTA_status == self.RTAStatus.RTA_MAIN_MENU_WITH_SLOT_DATA:
            self.reset_post_connect_patches = True # In addition to setting on server connection, setting here to handle re-patching shop strings on game reset

    def print_status(self):
        # First, a couple of special cases.

        # Did we change from EMU_NOT_RUNNING to *any* other state?
        # If we did, we just connected to PCSX2's socket, and should alert the player
        if self.prev_RTA_status == self.RTAStatus.EMU_NOT_RUNNING:
            logger.info("Connected to PCSX2!")
            logger.info("Waiting for Road Trip to start...")

        # Next, if we were previously not running RTA, and are now in *any* other state, alert the player that RTA has started
        if self.prev_RTA_status <= self.RTAStatus.EMU_NOT_RUNNING_RTA and \
            self.RTA_status > self.RTAStatus.EMU_NOT_RUNNING_RTA:
            logger.info("Road Trip loaded!")

        # --------------------------------------

        # Finally, handle each state's messages
        if self.RTA_status == self.RTAStatus.EMU_NOT_RUNNING:
            # Alert user on emulator disconnect
            if self.prev_RTA_status > self.RTAStatus.EMU_NOT_RUNNING:
                logger.info("Lost connection to PCSX2, attempting to reconnect...")
            else:
                pass # We're still waiting to connect
        elif self.RTA_status == self.RTAStatus.EMU_NOT_RUNNING_RTA:
            if self.prev_RTA_status > self.RTAStatus.EMU_NOT_RUNNING_RTA:
                logger.info("Road Trip no longer running, start game again to continue.")
            else:
                pass # Already handled in first conditional of set_status
        elif self.RTA_status == self.RTAStatus.RTA_MAIN_MENU_NO_SLOT_DATA:
            logger.info("RTA is in the main menu. Connect to the server before creating/loading a save!")
        elif self.RTA_status == self.RTAStatus.RTA_MAIN_MENU_WITH_SLOT_DATA:
            logger.info("RTA is in the main menu. Slot data has been received from the server.")
        elif self.RTA_status == self.RTAStatus.RTA_OTHER_STATE:
            print("RTA not in-game or in main menu (possibly non-Adventure mode loaded?)")
        elif self.RTA_status == self.RTAStatus.RTA_IN_VANILLA_GAME:
            #print("RTA is in a vanilla game")
            logger.info("The currently loaded save appears to be a vanilla (non-AP) save file!\n"
            "Please return to the main menu and either load an AP save, or start a new game.")
        elif self.RTA_status == self.RTAStatus.RTA_IN_UNPATCHED_AP_GAME:
            #print("RTA is in an unpatched AP game")
            logger.info("AP save loaded! However, the game's memory has not yet been patched for AP.\n"
            "Please return to the main menu to set up the game for AP.")
        elif self.RTA_status == self.RTAStatus.RTA_IN_AP_GAME_NO_CLIENT_SAVE_ID:
            #print("RTA is in an AP game, but not connected to the server")
            logger.info("RTA is in an AP game, but not connected to the server.\nConnect to your slot from the client to continue.")
        elif self.RTA_status == self.RTAStatus.RTA_IN_WRONG_AP_GAME:
            logger.info(WRONG_SAVE_ID_MSG)
        elif self.RTA_status == self.RTAStatus.RTA_IN_AP_GAME:
            #print("RTA is in an AP game")
            logger.info("AP save loaded, you are ready to play!")
        else:
            print("set_status: Switched to unknown status")

    # Using the emu status, and RTA's memory, determine the current game state. Called on every client update loop.
    def update_RTA_status(self):
        if not self._is_pcsx2_connected():
            self.set_status(self.RTAStatus.EMU_NOT_RUNNING)
            return

        if not self._is_RTA_running():
            self.set_status(self.RTAStatus.EMU_NOT_RUNNING_RTA)
            return

        # Is game in main menu, or loaded? Checking RTA's task queue to find out
        for index in range(Addresses.MAX_TASKS_IN_QUEUE): # For each task in the queue...
            address = Addresses.task_queue_entry.address + (index * Addresses.task_queue_entry.length)
            
            # Get function pointer and status byte stored in this task
            ptr = bytes_to_int(self.pine.read_bytes(address + Addresses.OFFSET_TASK_FUNC_PTR, Addresses.BYTES_IN_A_WORD))
            taskStatus = self.pine.read_bytes(address, 1)[0] # Will be 0 if task is not active
            
            if taskStatus != 0:
                mainMenuPtrs = [
                    Addresses.FUNC_PTR_MAIN_MENU,
                    Addresses.FUNC_PTR_MAIN_MENU_ADVENTURE_MODE_SELECTED,
                    Addresses.FUNC_PTR_NEW_GAME,
                    Addresses.FUNC_PTR_TASK_BETWEEN_NEW_GAME_AND_NAME_INPUT,
                    Addresses.FUNC_PTR_NAME_INPUT,
                    Addresses.FUNC_PTR_CURRENCY_INPUT
                ]
                # Are we past the main menu? (and not in a quick-race, 2P mode, etc?)
                if ptr == Addresses.FUNC_PTR_ADVENTURE_MODE: # TODO: Add president cutscene to check?
                    # Check if currently loaded game save is AP or vanilla (i.e. check if there's an AP index, would be 0x1 at minimum)
                    apIndex = bytes_to_int(self.pine.read_bytes(Addresses.ap_item_index.address, Addresses.ap_item_index.length))
                    if apIndex == 0:
                        self.set_status(self.RTAStatus.RTA_IN_VANILLA_GAME)
                        return
                    else:
                        # Checking all of the patches requires reading quite a bit of data, so we'll just check
                        #   one of the functions per server loop *unless* the quick check previously found a 
                        #   non-matching patch. In that case, we need to run the full check until we confirm
                        #   that the game is fully patched again (at which point, we can go back to the quick check).
                        game_patched = None
                        if self.quick_patch_check_failed:
                            game_patched = self.is_game_patched_full()
                        else:
                            game_patched = self.is_game_patched_quick()

                        if not game_patched:
                            self.set_status(self.RTAStatus.RTA_IN_UNPATCHED_AP_GAME)
                            self.quick_patch_check_failed = True
                            return
                        else:
                            self.quick_patch_check_failed = False
                            if not self.save_matches_slot():
                                if self.save_id == None:
                                    self.set_status(self.RTAStatus.RTA_IN_AP_GAME_NO_CLIENT_SAVE_ID)
                                else:
                                    self.set_status(self.RTAStatus.RTA_IN_WRONG_AP_GAME)
                                return
                            else:
                                self.set_status(self.RTAStatus.RTA_IN_AP_GAME)
                        
                        return
                elif ptr in mainMenuPtrs:
                    if not self.save_id or not self.shop_strings:
                        self.set_status(self.RTAStatus.RTA_MAIN_MENU_NO_SLOT_DATA)
                    else:
                        self.set_status(self.RTAStatus.RTA_MAIN_MENU_WITH_SLOT_DATA)
                    return
            # Else if the task status *is* 0, and the task pointer is a null pointer, that's a blank slot in the task queue
            #   (and presumably the end of the queue)
            elif ptr == 0: # AFAIK there shouldn't be any gaps in the task queue - if we hit a null pointer, that should be it
                self.set_status(self.RTAStatus.RTA_OTHER_STATE)
                return
        
        # If we're here, we checked all tasks in the queue, and every slot in the queue was not null
        self.set_status(self.RTAStatus.RTA_OTHER_STATE)
        if self.prev_RTA_status != self.RTAStatus.RTA_OTHER_STATE:
            print("Task queue is full!")
        return

    def _is_pcsx2_connected(self) -> bool:
        return self.pine.is_connected()

    def _is_RTA_running(self) -> bool:
        try:
            gameId = self.pine.get_game_id()
            if gameId == "SLUS-20398": 
                return True
        except Exception:
            # There doesn't appear to be a function in the PINE library that can test specifically
            #   for whether PCSX2 is running but does NOT currently have a game loaded.
            #   'get_game_id()' actually raises an exception if a game is not loaded.
            #
            # Because of this, the best answer here seems to be to just catch that exception if it happens 
            #   and return False.
            return False
    
    def is_game_patched_full(self) -> bool:       
        # Create a mock Pine object, and have its 'write_bytes' function instead locally store the
        #   bytes being written. Afterward, compare those bytes to those in the game's memory.
        mock = PineMock()
        patch_rta_no_slot_data(mock)
        return mock.compare_writes_to_game_ram(self.pine)
    
    def is_game_patched_quick(self) -> bool:
        # Same as full version, but only verifies one function. Done to reduce performance hit, since this is run every client loop.
        mock = PineMock()
        patch_rta_no_slot_data(mock, True)
        return mock.compare_writes_to_game_ram(self.pine)


# --------- Handle receiving items ---------
def handle_received_items(self : RTAContext):
    if self.RTA_status == self.RTAStatus.RTA_IN_AP_GAME and self.save_matches_slot():
        # print("Index: ", args['index'])
        # print("Length of items arg: ", len(args['items']))

        # Index - 1 is the number of items RTA has received
        # If that's less than the index plus the length of the list, we need to start sending items, starting with the last item in the list
        local_index = bytes_to_int(self.pine.read_bytes(Addresses.ap_item_index.address, Addresses.ap_item_index.length), "little") - 1
        print("local_index: ", local_index)

        if local_index < 0: # Will be -1 if a vanilla save
            assert("handleReceiveItems: We confirmed this is an AP game, but the AP item index is 0x0? This should be impossible.")
        
        if local_index < len(self.items_received):
            # DEBUG - Print all received items
            #msg = f"Received {', '.join([self.item_names.lookup_in_game(item.item) for item in self.items_received])}"
            #print(msg)

            num_items_to_send = len(self.items_received) - local_index

            # The items we need to send are at the end of the list
            items_to_send = self.items_received[-1 * num_items_to_send:]

            for index, item in enumerate(items_to_send):
                item_name = self.item_names.lookup_in_game(item.item) # The 'item' attribute in a NetworkItem object is the item's ID (meaning this is an int)
                msg = f"Received {item_name}"
                print(msg)
            
                # Convert the progressive upgrade to its actual item
                # TODO: Make a 'get progressive item' function
                if "Progressive" in item_name and item_name != ItemName.Progressive_License:
                    # Total number of this prog item received by the player, according to the server
                    # This, however, includes items RTA hasn't actually handled yet
                    total_prog_count = len([x.item for x in self.items_received if x.item == item.item])
                    # Now we subtract this copy of the progressive item, and all copies in the 'items_to_send' list that are AFTER this item, from the count
                    prog_not_yet_counted = len([x.item for x in items_to_send[index:] if x.item == item.item])
                    current_prog_to_send = total_prog_count - prog_not_yet_counted
                    print(f"{item_name} is prog count: ", current_prog_to_send)

                    # Convert the progressive item to its corresponding actual item
                    prog_part_type = item_name.split(" - ")[0] # remove " - Set 2" or " - Set 3" from string 
                    valid_prog_index = False
                    try:
                        item_name_new = progressive_part_order[prog_part_type][current_prog_to_send]
                        valid_prog_index = True
                    except Exception:
                        print("Progressive item index out of range, skipping")

                    if valid_prog_index:
                        print(f"Non-prog actual item: {item_name_new}")
                        update_inventory(self, item_name_new)

                elif item_name == ItemName.Stamp:
                    increment_stamp_count(self)
                else:
                    update_inventory(self, item_name)

            self.pine.write_int16(Addresses.ap_item_index.address, len(self.items_received) + 1)
        
        elif local_index > len(self.items_received):
            print("Local index higher than length of items_received list. Is this a save from a prior playthrough of this AP seed?")

        return

def update_inventory(self : RTAContext, item_name : str):
    pine = self.pine
    MAX_PART_QUANTITY = 5

    if item_name == ItemName.Victory: # Not actually an in-game item, not handled below
        return
    
    # print(Addresses.get_table_data_for_part(itemName).address)
    # print(Addresses.get_bit_to_update(itemName))
    table_data = Addresses.get_table_data_for_part(item_name)
    address = table_data.address
    length = table_data.length

    if table_data.storage_type == StorageType.Bits: # If not licenses or money...
        # Get initial bytes (may be changed if this is a part and RTA already has a copy)
        bytes = pine.read_bytes(address, length)
        bit = Addresses.get_bit_to_update(item_name)

        # If this is a part, we need to figure out how many parts the player has received so we can update
        #     the correct quantity bitfield (RTA stores each copy that the player can have in separate bitfields)
        if table_data != Addresses.inventory_bodies and table_data != Addresses.inventory_collectibles:
            update_my_city_part_shop(self, item_name)
            i = 0
            while i < MAX_PART_QUANTITY:
                bytes = pine.read_bytes(address, length)

                if not is_bit_set(bytes, bit):
                    break # We found it
                else:
                    address += length # Move on to the next bitfield
                    i = i + 1

        bytes = set_bit(bytes, bit)
        print("Writing to address", hex(address))
        write_bytes_and_verify(pine, address, bytes)

    elif item_name == ItemName.Progressive_License:
        bytes = pine.read_bytes(address, length)
        print("Writing to address", hex(address))
        write_bytes_and_verify(pine, address, int_to_bytes(min(bytes[0]+1, 3), length)) # NOTE: Magic number 3 is number of licenses

    elif item_name == ItemName.Filler:
        bytes = pine.read_bytes(address, length)
        money = min(bytes_to_int(bytes) + self.filler_amount, 999999) # NOTE: Setting max money to 999,999. Road Trip can store higher, but can't display higher (except when loading a save)
        bytes = int_to_bytes(money, length)
        write_bytes_and_verify(pine, address, bytes)

    else:
        # NOTE: If something like non-progressive licenses are implemented, there will need to be an additional case added here
        raise Exception(f"update_inventory: Could not handle this item: {item_name}")

def update_my_city_part_shop(self : RTAContext, item_name : str):
    from ..items import BASE_IDS as BASE_ITEM_IDS, item_name_to_base_ID
    pine = self.pine

    if "Billboard" not in item_name: # Shouldn't be able to re-buy billboards
        base_id = item_name_to_base_ID(item_name)

        if base_id:
            part_type_index = -1
            for index, id in enumerate(BASE_ITEM_IDS.get_all_as_list()):
                if base_id == id and id >= BASE_ITEM_IDS.TIRES and id < BASE_ITEM_IDS.COLLECTIBLES:
                    part_type_index = index
                    break

            if part_type_index >= 0:
                # Valid part
                table = Addresses.my_city_part_shop_table
                address = table.address + (table.length * part_type_index)

                bytes = pine.read_bytes(address, table.length)
                bit = Addresses.get_bit_to_update(item_name)
                bytes = set_bit(bytes, bit)
                write_bytes_and_verify(pine, address, bytes)


def increment_stamp_count(self : RTAContext):
    pine = self.pine

    table = Addresses.ap_stamps_received
    
    # Read from PCSX2 memory.
    address = table.address
    num_bytes = table.length
    stamp_count = pine.read_int8(address)

    # Increment and write to PCSX2 memory.
    if stamp_count < 255: # Prevent overflow
        stamp_count = stamp_count + 1
    
    pine.write_int8(address, stamp_count)

# --------- Handle location checks ---------
async def check_race_completions(ctx: RTAContext):
    table = Addresses.race_results
    
    # Read from PCSX2 memory.
    address = table.address
    num_bytes = table.length
    data = ctx.pine.read_bytes(address, num_bytes)

    # Determine which location checks have been completed
    race_completions = []
    for index, val in enumerate(data): # enumerate(data) causes val to be an int
        if val <= MINIMUM_RACE_RANK_FOR_COMPLETION:
            race_completions.append(index + table.base_ID)

    # Send newly completed location checks to the AP server
    if race_completions:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": race_completions}])

async def check_stamp_completions(ctx: RTAContext): 
    table = Addresses.stamp_completions

    # Read from PCSX2 memory
    address = table.address
    num_bytes = table.length
    data = ctx.pine.read_bytes(address, num_bytes)

    # Determine which location checks have been completed
    stamp_completions = []
    victory = False
    for index in range(Addresses.NUM_STAMPS):
        if is_bit_set(data, index, "little"):
            #print(ctx.location_names.lookup_in_game(index + table.baseID))
            stamp_completions.append(index + table.base_ID)

            if index == 99:
                victory = True
    
    # Send newly completed location checks to the AP server
    if stamp_completions:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": stamp_completions}])

    if victory:
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

async def check_shop_purchase_completions(ctx: RTAContext):
    table = Addresses.shop_purchases

    # Read from PCSX2 memory
    address = table.address
    num_bytes = table.length
    data = ctx.pine.read_bytes(address, num_bytes)

    #print("DEBUG SHOP PURCHASES: ", data)

    # Determine which location checks have been completed
    shop_completions = []
    for index in range(num_bytes * BITS_IN_BYTE):
        if is_bit_set(data, index, "little"):
            print(ctx.location_names.lookup_in_game(index + table.base_ID))
            shop_completions.append(index + table.base_ID)

    # Send newly completed location checks to the AP server
    if shop_completions:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": shop_completions}])

async def check_NPC_reward_completions(ctx: RTAContext):
    from ..locations import BASE_IDS as BASE_LOCATION_IDS

    table = Addresses.items_obtained
    id = table.base_ID
    
    # Read from PCSX2 memory
    address = table.address
    num_bytes = table.length
    data = ctx.pine.read_bytes(address, num_bytes)

    #print("DEBUG NPC REWARDS: ", data)

    # Determine which location checks have been completed
    reward_completions = []
    for index in range(num_bytes * BITS_IN_BYTE):
        if is_bit_set(data, index, "little"):
            if ctx.remove_double_up_stamps == True:
                # Test if a double-up stamp location exists for this bit
                # If it does, use it instead
                temp = ctx.location_names.lookup_in_game(index + id + BASE_LOCATION_IDS.COMBINED)
                if "Unknown location" not in temp:
                    index += BASE_LOCATION_IDS.COMBINED
            
            print(ctx.location_names.lookup_in_game(index + id))
        
            reward_completions.append(index + id)

    # Send newly completed location checks to the AP server
    if reward_completions:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": reward_completions}])

async def check_license_completions(ctx: RTAContext):
    table = Addresses.license_completions
    
    # Read from PCSX2 memory
    address = table.address
    num_bytes = table.length
    data = ctx.pine.read_bytes(address, num_bytes)

    #print("DEBUG LICENSE COMPLETIONS: ", data)

    # Determine which location checks have been completed
    license_completions = []

    for index in range(Addresses.NUM_LICENSES):
        if is_bit_set(data, index, "little"):
            print(ctx.location_names.lookup_in_game(index+1 + table.base_ID))
            license_completions.append(index+1 + table.base_ID)

    # Send newly completed location checks to the AP server
    if license_completions:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": license_completions}])

async def check_world_grand_prix_completion(ctx: RTAContext):
    table = Addresses.event_flags

    # Read from PCSX2 memory
    address = table.address
    num_bytes = table.length
    data = ctx.pine.read_bytes(address, num_bytes)

    if is_bit_set(data, 31, "little"): # World GP completion is 31st bit (when bytes are read in reverse order, because little-endian)
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [table.base_ID]}])

# --------- Game loop ---------
# This is the function that both watches Road Trip's memory for updates to send to the server (e.g. newly-checked
#   locations) and updates Road Trip's memory based on any newly-received items (e.g. giving the player new
#   parts, license upgrades, etc.).
async def handle_rta(ctx: RTAContext):
    # Do not patch the game unless we are on the main menu and have received slot data.
    if ctx.RTA_status == ctx.RTAStatus.RTA_MAIN_MENU_WITH_SLOT_DATA:
        if not ctx.is_game_patched_full():
            patch_rta_no_slot_data(ctx.pine)
            logger.info("Road Trip AP memory patch successful! Load an AP save or start a new game to continue.")
        if ctx.reset_post_connect_patches:
            patch_rta_post_connect(ctx.pine, ctx.shop_strings, ctx.area_unlock_mode)
            logger.info("Patches requiring slot data successful!")
            ctx.reset_post_connect_patches = False

    elif ctx.RTA_status == ctx.RTAStatus.RTA_IN_AP_GAME and ctx.save_matches_slot():
        # At this point, we have confirmed all of the following:
        # - PCSX2 is running Road Trip.
        # - The currently loaded save is an AP save, and it is associated with the slot that the client is currently connected to.
        # - The game has been patched (required to get to RTA_IN_AP_GAME state)
        # - We have loaded Adventure Mode.
        #
        # At this point, we can finally handle received items and check for location clears!
        #
        handle_received_items(ctx)
        await check_race_completions(ctx)
        await check_stamp_completions(ctx)
        await check_shop_purchase_completions(ctx)
        await check_NPC_reward_completions(ctx)
        await check_license_completions(ctx)
        await check_world_grand_prix_completion(ctx)

        print() # DEBUG

# This is the client's main loop. If the emulator and RTA are running, it will call handle_rta.
async def pcsx2_loop(ctx: RTAContext):
    logger.info("Attempting to connect to PCSX2 via PINE...")
    ctx.pine.connect()
    
    # While the client is still running...
    while not ctx.exit_event.is_set():
        # Update RTA state
        ctx.update_RTA_status()

        # If the emulator is at least running...
        if ctx.RTA_status > ctx.RTAStatus.EMU_NOT_RUNNING:
            # If the emulator is running Road Trip in any state...
            if ctx.RTA_status > ctx.RTAStatus.EMU_NOT_RUNNING_RTA:
                # If we've confirmed we're both connected to PCSX2 and Road Trip is running...
                await handle_rta(ctx)
                await asyncio.sleep(1) # Wait one second between each poll of the emulator for status updates.
            else:
                await asyncio.sleep(2.5) # Keep waiting for RTA to start
        else:
            # Attempt to reconnect to the emulator.
            ctx.pine.connect()
            await asyncio.sleep(2.5)

        continue

# --------- Launch / Main ---------
def launch():
    # Parts taken from the Adventure Client, RaC2's client, and 'run_as_textclient' in CommonClient.py
    async def main():
        parser = get_base_parser()
        args = parser.parse_args()

        ctx = RTAContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        asyncio.create_task(pcsx2_loop(ctx), name="PCSX2 Update Loop")

        await ctx.exit_event.wait() # Function will wait here until the client exits.
        await ctx.shutdown()

    import colorama
    colorama.just_fix_windows_console()

    asyncio.run(main())

    colorama.deinit()


if __name__ == '__main__':
    launch()