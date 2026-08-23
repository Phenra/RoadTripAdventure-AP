from .pine import Pine
from ..ram_data import Addresses
from .MIPS import *
from .Helpers import int_to_bytes

NOP_BYTES = bytes([0,0,0,0])

# Assembly hook locations in RAM
#
# All of these are written to space normally used by pointer tables to email strings.
#   Since we disable the email system, all of this space can be used as a code cave.
#
# For easier organization, all assembly patches start on an address ending in 00 or 80.
#   This means each patch is always given at least 0x80 (128) bytes of space - and
#   since MIPS instructions are always 4 bytes long, this equals 32 instructions.
#
# Some patches need fewer than 32 instructions, but the additional space allows for
#   easier expansion of the patch later if it ends up needing more functionality.
#
# Some patches need more than 32 instructions, and take up multiple of these 0x80
#   byte 'slots'.
HOOK_ADDR_INIT_AP_ITEM_INDEX = 0x2DA180
HOOK_ADDR_AP_LOCATION_FUNC_READ = 0x2DA200
HOOK_ADDR_AP_LOCATION_FUNC_WRITE = 0x2DA20C
HOOK_ADDR_SHOP_PURCHASES = 0x2DA380
HOOK_ADDR_NPC_REWARDS = 0x2DA400
HOOK_ADDR_IS_LICENSE_CHECK_COMPLETE = 0x2DA480
HOOK_ADDR_WRITE_LICENSE_CHECK = 0x2DA500 # (License checks are not handled by the earlier AP Location hook.)

# NOTE: 0x2DA600 through 0x2DA67F is reserved for custom strings (e.g. AP item classifications, used by the
#   part shop description hook)

HOOK_ADDR_ENFORCE_AREA_ACCESS = 0x2DA680
HOOK_ADDR_AREA_ACCESS_NPCS_AND_ENTRANCES = 0x2DA800
HOOK_ADDR_AREA_ACCESS_Q_COINS = 0x2DA880
HOOK_ADDR_AREA_ACCESS_OVERWORLD_ITEMS = 0x2DA900
HOOK_ADDR_AP_PARTS_SHOP_FULL_NAME_IN_BUY_CONFIRMATION = 0x2DA980
HOOK_ADDR_AP_PARTS_SHOP_DESCRIPTIONS = 0x2DA98C

HOOK_ADDR_NPC_EQUIPS = 0x2DAB80
HOOK_ADDR_PARTS_SHOP_CHECK_IF_LOCATION_COMPLETE = 0x2DAC00
HOOK_ADDR_PARTS_SHOP_OWNED_QUANTITY_STRING_HANDLING = 0x2DAC80

HOOK_ADDR_DISPLAY_AP_STAMP_COUNT = 0x2DAD00
HOOK_ADDR_CONVERT_DIGIT_IN_INT_TO_CHAR = 0x2DAD80
HOOK_ADDR_HANDLE_MY_CITY_PARTS_SHOP_ON_CONTINUE = 0x2DAE00

# NOTE: 0x2DAE80 through 0x2DAEFF also reserved for custom strings

HOOK_ADDR_COST_PERCENTAGE_MODIFIER = 0x2DAF00
HOOK_ADDR_PREVENT_AP_ITEM_REPURCHASE = 0x2DB000
HOOK_ADDR_COINE_PATCH_FOR_Q_COIN_RANDO = 0x2DB080

# ---------------------------------------------------
def closure__patch_rta_no_slot_data():
    # Create a closure around the function that applies the patches that do not require slot data.
    #
    # This is needed entirely for the patch verification system. Every time the RTA client checks
    #   the game's memory to see if anything AP-related has updated, it double-checks that the game is
    #   still patched before sending anything off to the AP server. Since checking every patch on
    #   every client loop would be expensive, we just check one patch per loop.
    # To do this, we keep track of both 1. the index of the patch we're checking (loops back to the
    #    beginning once it checks the last patch), and 2. a cache of the results of the patches, to
    #    greatly speed up the checks.
    # We can safely cache all of these patches since none of them rely on player settings (hence, why
    #    none of them require slot data). This would not hold true for the post-connect patches.
    patch_index = 0
    cached_patches = {}
    
    def patch_rta_no_slot_data(pine : Pine, verification_run : bool = False):
        patches = [
            # Disable the email system
            # This is where we'll store our patches - but in particular, we need to clear
            #   something of this size to store all of the shop strings.
            disable_email_system,

            # Handling AP location checks
            write_ap_location_func,
            hook_shop_purchases,
            hook_npc_rewards,
            patch_npc_dialogue_triggers,
            hook_overworld_item_funcs,
            hook_license_upgrades,

            # For shop strings (this function does not require slot data)
            change_shop_item_quantity_display_to_ap,

            # Other patches
            patch_npc_equips,
            disable_vanilla_my_city_part_shop_handling,
            hook_game_continue_to_reset_my_city_part_shop,
            patch_tin_raceway_requirements,
            disable_func_that_overwrites_ap_save_data,
            # patch_bars_for_ap_hints # TODO
            fix_vanilla_bugs
        ]

        if verification_run:
            # Run only one patch. Used for patch verification, so we're not verifying every function on every client loop.
            nonlocal patch_index, cached_patches
            if cached_patches.get(patch_index) == None:
                patches[patch_index](pine)
                cached_patches[patch_index] = pine
            else:
                vars(pine).update(vars(cached_patches[patch_index])) # Replace passed pine object's data with cached data (instead of running the patch function again)
            
            patch_index += 1
            if patch_index >= len(patches):
                patch_index = 0
        else:
            # Run all patches. Standard use case (i.e. patching the game).
            for patch in patches:
                patch(pine)
    
    return patch_rta_no_slot_data

patch_rta_no_slot_data = closure__patch_rta_no_slot_data()

def patch_rta_post_connect(pine : Pine, shop_strings : list, area_unlock_mode : int, parts_cost_modifier : int, parts_cost_maximum : int, auto_unlock_warps : bool, randomize_q_coins : bool, q_coins_needed_per_coine_reward : int):
    # AP save setup
    hook_currency_input_to_init_ap(pine, auto_unlock_warps)

    # Handle shop strings
    hook_shops_to_display_ap_item_strings(pine, shop_strings)

    # Handle enforcing area access
    enforce_area_access(pine, area_unlock_mode)

    # Apply a percent modifier and/or maximum to the cost of parts
    part_cost_modifiers(pine, parts_cost_modifier, parts_cost_maximum)

    # In Decorations mode, modify the descriptions of items used as keys to note which town they unlock.
    modify_key_descriptions(pine, area_unlock_mode)

    # Modify how Coine rewards work depending on two provided settings
    patch_coine_behavior(pine, randomize_q_coins, q_coins_needed_per_coine_reward)

# ---------------------------------------------------

def disable_email_system(pine : Pine):
    """
    Removes all interactions with the email system from the game. 
    
    This allows us to use the space in memory where email text was stored for our new AP item descriptions in part shops.
    Additionally, this space is so large that we can actually store all of our assembly patches here (which will help
    prevent any other RTA mods from accidentally overwriting our patches for AP).
    """
    # Original ASM line at this address compares whether distance traveled is greater than amount needed to trigger email. 
    # This sets the comparison to always be False instead.
    pine.write_bytes(0x210EE8, mips([
        addiu(a1, zero, 0x0)
    ]))

    # Prevent blinking indicator on the minimap
    # pine.write_bytes(0x249264, NOP_BYTES) # Broken, hides the entire border around the minimap.
    pine.write_bytes(0x2492BC, NOP_BYTES) # NOPing this line instead seems to work?

    # Remove option for email from garage menu.
    pine.write_bytes(0x22CE88, NOP_BYTES)

    # Automatically increment garage menu index by one so that all menu options run the correct tasks.
    # Otherwise, the first option would still open the email inbox, even with its button removed.
    # Also, skip code that handles the email option.
    pine.write_bytes(0x22D118, mips([
        addiu(v1, v1, 0x1),
        beq(zero, zero, 9), # beq zero,zero,0x0022D140
        nop()
    ]))


def hook_currency_input_to_init_ap(pine : Pine, auto_unlock_warps : bool):
    """ 
    Hook RTA to, on New Game, initialize the AP index variable, get the AP save ID, and
    (if Auto Unlock Warps is on) unlock the ability to warp to the Garage.
    This hook runs after currency input is complete, but before the President Forest cutscene begins.
    """
    # Overwrite jal to president Forest cutscene so we can add a hook that runs first
    pine.write_bytes(0x26d650, mips([
        jal(HOOK_ADDR_INIT_AP_ITEM_INDEX)
    ]))
    
    # Hook
    # ---------------------
    # Used only if Auto Unlock Warps is enabled
    additional_garage_asm = [
        # Set garage warp unlock bit
        lui(t1, get_upper_nibble(Addresses.unlocked_warps.address)),
        ori(t1, t1, get_lower_nibble(Addresses.unlocked_warps.address)),
        lbu(t0, 0, t1),
        andi(t0, t0, 0xfe), # Garage warp is the first bit in the bitfield. Unlocked warps bitfield uses 1 to indicate 'not unlocked', so we need to set this bit to 0.
        sb(t0, 0, t1),

        # Set garage visibility bit
        lui(t1, get_upper_nibble(Addresses.my_city_buildings.address)),
        ori(t1, t1, get_lower_nibble(Addresses.my_city_buildings.address)),
        lbu(t0, 0, t1),
        ori(t0, t0, 0x80), # 0x80 is 8th bit set
        sb(t0, 0, t1),
    ]
    # Always used
    asm = [
        # Set AP index to 0x1
        addiu(t0, zero, 0x1),
        lui(t1, get_upper_nibble(Addresses.ap_item_index.address)),
        ori(t1, t1, get_lower_nibble(Addresses.ap_item_index.address)),
        sb(t0, 0, t1),

        # Set boolean (at 0x2DA0F0) to indicate to the server that we are ready to receive the AP save ID to 1
        lui(t1, get_upper_nibble(Addresses.ready_for_ap_save_id.address)),
        ori(t1, t1, get_lower_nibble(Addresses.ready_for_ap_save_id.address)),
        sb(t0, 0, t1),

        # Set boolean (at 0x2DA0F1) to indicate to the server that we're ready to receive the current My City part shop inventory
        sb(t0, 1, t1),

        # Now jump to the president Forest cutscene function (don't jal, our jal into this hook already set the ra register)
        j(0x211708),
        nop()
    ]

    if auto_unlock_warps == True:
        asm = additional_garage_asm + asm

    pine.write_bytes(HOOK_ADDR_INIT_AP_ITEM_INDEX, mips(asm))


def hook_game_continue_to_reset_my_city_part_shop(pine : Pine):
    """
    Hook the function that continues from a saved game to set the 'ready_for_my_city_part_shop_inventory' byte.
    When the client sees this, it will set the parts sold at the My City part shop to the parts the player has
    received so far from the multiworld.
    """
    # Change the jr ra to a j to our hook
    pine.write_bytes(0x26d42c, mips([
        j(HOOK_ADDR_HANDLE_MY_CITY_PARTS_SHOP_ON_CONTINUE)
    ]))

    pine.write_bytes(HOOK_ADDR_HANDLE_MY_CITY_PARTS_SHOP_ON_CONTINUE, mips([
        lui(t0, get_upper_nibble(Addresses.ready_for_my_city_part_shop_inventory.address)),
        ori(t0, t0, get_lower_nibble(Addresses.ready_for_my_city_part_shop_inventory.address)),
        addiu(t1, t1, 0x1),
        sb(t1, 0, t0),
        jr(ra),
        nop()
    ]))
    

def write_ap_location_func(pine : Pine):
    """
    Creates a function that, given an item's part type (in register a0) and item ID (in register a1),
    can read/write whether the AP location associated with obtaining that item is complete.
    """
    # Additional info:
    # There are two AP location tables: One for items received from NPCs, and one for items purchased from a part
    # shop. Both are needed since a few items can be obtained either way, and those are separate AP locations.
    # Example: RS Magnum (Which-Way Maze location != Shop Purchase RS Magnum location)
    #
    # This function will check to see whether we are currently in a part shop. If we are, it reads/writes
    # the shop location table. If not, it reads/writes the NPC location table.
    #
    # These 'AP location completion' tables are saved in (what appears to be) an unused part of the save file.
    # (More specifically, all data from the save file is stored by RTA in one contiguous block of memory.
    # When the game saves, it just writes that big block of memory to the memory card. So we don't write to the
    # memory card here, we're writing to the part of memory that *will get written* to the memory card when
    # the player saves.)
    
    # -----------------------------------------
    # What is 'table_length_table'?
    # The AP location completion tables are bitfields. Each bit corresponds to whether the location for that
    # item has been completed.
    #
    # To determine which bit we need to read/write, we first need to convert the item type + ID to the correct
    # bit. This involves adding the total number of parts of all prior part types, plus the item ID.
    #
    # Example: Engines are part type 2. The RS Magnum is engine index 8. Given this, its bit in the bitfield is #172 because:
    # 0x97 (all 151 bodies) + 0x0D (all 13 tires) + 0x8 (RS Magnum index in engine table) = 0xAC hex, or 172 decimal
    #
    table_length_table = bytes([0x97, 0x0D, 0x0C, 0x05, 0x06, 0x04, 0x04, 0x0F, 0x03, 0x02, 0x03, 0x09, 0x02, 0x0F, 0x0B, 0x30])
    pine.write_bytes(Addresses.ADDR_TABLE_LENGTH_TABLE, table_length_table) # Just prior to all ASM patches

    # ASM Labels
    END = "End"
    SHOP_PURCHASE = "Shop Purchase"

    pine.write_bytes(HOOK_ADDR_AP_LOCATION_FUNC_READ, mips([
        # To read a bit, start here. Set t7 to 1 (checked later).
        addiu(t7, zero, 1),
        beq(zero, zero, 3),
        nop(),

        # To write a bit, start here. Set t7 to 2 (checked later).
        addiu(t7, zero, 2),

        # ---------------------------------------

        # Main function body
        # First, if a2 is not 0, exit the function.
        # a2 appears to always be 0 when the player is receiving a part.
        bne(a2,zero,END),
        nop(),

        # Copy the arguments to temporary registers, instead of mutating directly (they could 
        #   be needed by the vanilla function later)
        addiu(t0, a0, 0),
        addiu(t2, a1, 0),

        # Load the address to the table length table
        lui(t1, get_upper_nibble(Addresses.ADDR_TABLE_LENGTH_TABLE)),
        ori(t1, t1, get_lower_nibble(Addresses.ADDR_TABLE_LENGTH_TABLE)),

        # Loop
        # Add the part totals for each part type until we've reached this part's type.
        beq(t0, zero, 6),
        lbu(t3, 0, t1),
        addu(t2, t2, t3),
        addiu(t1, t1, 1),
        addiu(t0, t0, -1),
        beq(zero, zero, -5),

        # Determine whether we are currently in a shop by testing for several possible shop
        #   task addresses in ra.
        # The first will be in ra during a buy, the second will be in ra while browsing,
        #   and the third will be in ra when verifying that the player does not already
        #   own the maximum number of a part when attempting to buy.
        #   (TODO: this is fragile, really should pass in a variable if possible...)
        # If we are in the shop, set the address to check to the AP shop purchases
        #   bitfield. Otherwise, set it to the AP NPC items received bitfield.
        lui(t3, 0x0026),
        ori(t3, t3, 0x97E0),
        beq(ra, t3, SHOP_PURCHASE),
        nop(),
        lui(t3, 0x0024),
        ori(t3, t3, 0x7244),
        beq(ra, t3, SHOP_PURCHASE),
        nop(),
        lui(t3, 0x26),
        ori(t3, t3, 0x9704),
        beq(ra, t3, SHOP_PURCHASE),
        nop(),

        # Set table to NPC reward table
        lui(t1, get_upper_nibble(Addresses.items_obtained.address)),
        addiu(t1, t1, get_lower_nibble(Addresses.items_obtained.address)),
        beq(zero, zero, 4),
        nop(),

        # Set table to shop purchases table
        label(SHOP_PURCHASE),
        lui(t1, get_upper_nibble(Addresses.shop_purchases.address)),
        addiu(t1, t1, get_lower_nibble(Addresses.shop_purchases.address)),

        # Loop
        # Continue subtracting 8 from the total item count until it would go negative.
        # This is to determine which *byte* contains our bit (since 8 bits are in a byte).
        addiu(t3, t2, -0x8),
        bltz(t3, 6),
        nop(),
        addiu(t2, t2, -0x8),
        addiu(t1, t1, 1),
        beq(zero,zero,-5),
        nop(),

        # Load the byte, and prepare t2 to contain a 1 in the bit we want to read/write, and
        #   0 in all other bits (i.e. create a bit mask)
        lbu(t0, 0, t1),
        addiu(t3, zero, 1),
        sllv(t2, t3, t2),

        # If t7 (read/write enum) is 1, branch to TABLE READ
        slti(t7, t7, 2),
        bne(t7, zero, 5),
        nop(),

        # TABLE WRITE
        or_(t0, t0, t2),
        sb(t0, 0, t1),
        jr(ra),

        # TABLE READ
        and_(t0, t0, t2),
        slti(v0, t0, 1),
        xori(v0, v0, 1),
        label(END),
        jr(ra),
        nop()
    ]))


def hook_shop_purchases(pine : Pine):
    """
    Convert shop purchases to AP locations, instead of giving the player the item purchased - *except* in My City.
    My City's part shop does not contain any locations, and is used exclusively for repurchasing parts you've
    already obtained.
    """
    # At 0x2697d8, change the ASM instruction (which is currently a jump-and-link to the function that handles
    #   updating your inventory) to a jal to our new hook.
    pine.write_bytes(0x2697D8, mips([
        jal(HOOK_ADDR_SHOP_PURCHASES)
    ]))
    
    # In our hook, test if the current region index is 9 (My City).
    #   If it's not, run our AP location check function (defined above).
    #   If it is, jump (not jal) to the normal shop function that updates your inventory.
    pine.write_bytes(HOOK_ADDR_SHOP_PURCHASES, mips([
        lui(t0, get_upper_nibble(Addresses.ADDR_CURRENT_ROOM_TABLE)),
        addiu(t0, t0, get_lower_nibble(Addresses.ADDR_CURRENT_ROOM_TABLE)),
        lbu(t0, 0, t0), # was lb
        addiu(t1, zero, 0x9),
        bne(t0, t1, 4),
        nop(),
        j(0x23D2C0),
        nop(),
        j(HOOK_ADDR_AP_LOCATION_FUNC_WRITE),
        nop()
    ]))

    # Prevent repurchases of AP parts
    pine.write_bytes(0x2696FC, mips([
        jal(HOOK_ADDR_PREVENT_AP_ITEM_REPURCHASE)
    ]))
    pine.write_bytes(HOOK_ADDR_PREVENT_AP_ITEM_REPURCHASE, mips([
        # Run the vanilla 'cannot buy' function if we are in the My City Part Shop
        # TODO: Determining whether we're here should probably be a function, this is done several times throughout the patches
        lui(t0, get_upper_nibble(Addresses.ADDR_CURRENT_ROOM_INDEX)),
        ori(t0, t0, get_lower_nibble(Addresses.ADDR_CURRENT_ROOM_INDEX)),
        lbu(t1, 0, t0),
        addiu(t2, zero, 1),
        bne(t1, t2, 7),
        lbu(t1, 2, t0), # get room table value, 2 bytes away from room index
        addiu(t2, zero, 9),
        bne(t1, t2, 4),
        nop(),
        j(0x23D548),
        nop(),
        j(HOOK_ADDR_AP_LOCATION_FUNC_READ),
        nop()
    ]))
    # 'Already bought AP part!' string
    pine.write_bytes(0x32F308, bytes([0x41, 0x6C, 0x72, 0x65, 0x61, 0x64, 0x79, 0x20, 0x62, 0x6F, 0x75, 0x67, 0x68, 0x74, 0x20, 0x41, 0x50, 0x20, 0x70, 0x61, 0x72, 0x74, 0x21, 0x00]))


def hook_npc_rewards(pine : Pine):
    """
    Convert NPC rewards to AP locations, instead of the vanilla behavior of giving the player an item. 
    Also sets the name of the received item to 'AP Item', instead of the vanilla name.
    """
    # Overwrite the call to the normal 'set inventory' function with our AP location function.
    pine.write_bytes(0x23A0B4, mips([
        jal(HOOK_ADDR_AP_LOCATION_FUNC_WRITE)
    ]))

    # Set all NPC reward item names to 'AP Item'
    # 1. Hook the JAL that would normally get the pointer to the reward's name.
    pine.write_bytes(0x239FE4, mips([
        jal(HOOK_ADDR_NPC_REWARDS)
    ]))

    # 2. In our hook, instead return the address to our new "AP Item" string.
    pine.write_bytes(HOOK_ADDR_NPC_REWARDS, mips([
        lui(v0, get_upper_nibble(Addresses.ADDR_STRING_AP_ITEM)),
        ori(v0, v0, get_lower_nibble(Addresses.ADDR_STRING_AP_ITEM)),
        jr(ra),
        nop()
    ]))

    # 3. Write the 'AP Item' string.
    addr = Addresses.ADDR_STRING_AP_ITEM
    pine.write_bytes(addr, bytes([0x41, 0x50, 0x20, 0x49]))
    pine.write_bytes(addr+4, bytes([0x74, 0x65, 0x6d, 0x00]))

    # Replace 'Body' string used when receiving a body from an NPC with just a double-quote
    #   (since it needs to be there to be used as the opening quote in "AP Item")
    pine.write_bytes(0x3338E8, bytes([0x22, 0x00]))

def hook_overworld_item_funcs(pine : Pine):
    """
    Convert overworld items to AP locations. Also modify the code that decides whether to display them
    to check whether they've been picked up, *not* whether we actually have the item.
    """
    # Overwrite existing set inventory calls to use our AP location handling function instead
    overworld_item_JALs = [
        # Function calls for inventory update
        0x2409E0, # Peach
        0x25C03C, # Wallet 
        0x25C2B4, # Fluffy Mushroom
        0x25C3F0, # Amethyst
        0x25C4D4, # Moonstone
        0x25C608, # Small Bottle
        0x25C6E8, # Black Opal
        0x25C7C8, # Papu Flower
        0x25C904, # Ruby
        0x25CAE8, # Fountain Pen
        0x25CBC8, # Blue Sapphire
        0x25D4A8, # Topaz
        0x25D5B8  # Emerald
    ]
    for address in overworld_item_JALs:
        pine.write_bytes(address, mips([
            jal(HOOK_ADDR_AP_LOCATION_FUNC_WRITE)
        ]))

    # Also modify these functions to prevent overworld items from disappearing when we add that item to our
    #   inventory. (Road Trip uses the status of the item in your inventory to determine whether it should
    #   appear in the overworld.)
    overworld_item_inventory_checks = [
        0x25BF9C, # Wallet 
        0x25C218, # Fluffy Mushroom
        0x25C350, # Amethyst
        0x25C434, # Moonstone
        0x25C568, # Small Bottle
        0x25C648, # Black Opal
        0x25C728, # Papu Flower
        0x25C868, # Ruby
        0x25CA48, # Fountain Pen
        0x25CB28, # Blue Sapphire
        0x25D410, # Topaz
        0x25D520  # Emerald
    ]

    for address in overworld_item_inventory_checks:
        pine.write_bytes(address, mips([
            jal(HOOK_ADDR_AP_LOCATION_FUNC_READ)
        ]))
        
        # All overworld items have a stamp check that will cause the item to not display if the stamp has
        #   been received. For example, the Fountain Pen and Stamp 39, "Found Benji's Fountain Pen".
        # This is done since items like the Fountain Pen are removed from your inventory when completing
        #   the stamp, and the overworld item needs to stay invisible even after that happens.
        # Since these items and their locations are now separate for AP, we need to remove these stamp checks.
        #
        # All of them are four instructions (16 bytes) after the inventory checks.
        pine.write_bytes(address+16, NOP_BYTES)


def hook_license_upgrades(pine : Pine):
    """
    Convert receiving a new license to an AP location (and remove vanilla behavior).
    """
    # Road Trip assumes that the 3 license upgrades will be obtained in order. As a result, it stores
    #   an int representing the current license the player has obtained (unlike with obtained parts and
    #   items, which use bitfields). So C-rank = 0x0, B-rank = 0x1, etc.
    #
    # This creates several problems for AP. For example: What if we obtain all of the license items prior
    #    to completing all B-rank races, and THEN finish all the B-rank races? In this case, the game
    #    won't even check to see whether it needs to award you a new license. This would make that 
    #    license location permanently missable.
    #
    # So we have to do several things here:
    #    1. Modify the game so that it uses the AP license location data to determine whether to run the
    #       check, NOT the actual obtained licenses. (We can skip the check if we've already cleared the
    #       location for that license - otherwise, run it.)
    #    2. When we would normally be awarded a new license by the game, update the AP license location
    #       bitfield instead (as opposed to incrementing the game's license count int, the vanilla behavior).

    # --------------------------------------

    # PART 1 - Modifying the license upgrade check
    
    # The function starting at 0x237508 (NTSC) handles determining whether all of the races that match
    #   the rank of the race just completed are now complete.
    #
    # Here we call our hook to get license upgrades to check against the AP license location bitfield,
    #   instead of the licenses in your inventory.
    pine.write_bytes(0x23757C, mips([
        jal(HOOK_ADDR_IS_LICENSE_CHECK_COMPLETE)
    ]))

    # Hook 1
    pine.write_bytes(HOOK_ADDR_IS_LICENSE_CHECK_COMPLETE, mips([
        # Road Trip has a table containing (among other things) the corresponding rank for each race. 
        # a2 contains a pointer to the entry in that table for this race. Byte 3 contains the race rank.
        # This instruction loads that byte.
        lbu(a3, 3, a2), # was lb

        # Convert rank int to a bitfield index.
        addiu(t7, zero, 1),
        sllv(t7, t7, a3),

        # Load AP license location bitfield
        lui(t6, get_upper_nibble(Addresses.license_completions.address)),
        addiu(t6, t6, get_lower_nibble(Addresses.license_completions.address)),
        lbu(t6, 0, t6), # was lb

        # Bitwise and. Result is 0 if we haven't completed this license location yet, not 0 if we have.
        and_(t6, t6, t7),

        # If 0, return. Setting a3 to the current race rank on line 1 has already tricked the game 
        #   into thinking our current license matches this race, so the remaining check logic should work
        #   (i.e. for the 'you earned a license' text).
        beq(t6, zero, 3),
        nop(),
        # Otherwise, if 1, set a3 to 3 instead. This will cause the function to assume we have all licenses 
        #    already, and it will not check for any license rank completions.
        addiu(a3, zero, 3),

        jr(ra),
        nop()
    ]))

    # ---------------------------------

    # PART 2 - Modifying the function that updates your license count to update the AP license bitfield instead.
    
    # Overwrite existing lines that handle updating license byte in the 'handleRaceResults' function.
    pine.write_bytes(0x2366FC, mips([
        jal(HOOK_ADDR_WRITE_LICENSE_CHECK),
        nop(),
        nop()
    ]))

    # Hook 2 - Updates our AP location byte for license checks
    pine.write_bytes(HOOK_ADDR_WRITE_LICENSE_CHECK, mips([
        beq(v1, zero, 9),           # Skip if no license bit to update
        addiu(v0, zero, 1),         # Init license bit slot to 1
        addiu(v1, v1, -1),          # Number of left shifts to apply to 1 
        sllv(v1, v0, v1),           # Apply shift. Result is the bit that corresponds to this license.
        lui(v0, get_upper_nibble(Addresses.license_completions.address)),
        addiu(v0, v0, get_lower_nibble(Addresses.license_completions.address)),
        lbu(t7, 0, v0), # was lb    # Load current AP license bitfield
        or_(v1, v1, t7),
        sb(v1, 0, v0),              # Store updated AP license bitfield
        jr(ra),
        nop()
    ]))

    # ---------------------------------

    # Additionally, make a small change to the congratulations message in Q's Factory.
    # If you just completed all the A-rank licenses, you'll receive a special message for getting the Super-A license.
    #   Otherwise, you'll get a generic message.
    # Neither of these are necessarily accurate in AP (completing a license check might get you something completely
    #   different), but the Super-A one could be especially confusing since it calls out that license by name.
    # The below changes the function to always use the generic congratulations message (i.e. changes the string pointer).
    pine.write_bytes(0x2a4508, bytes([0x07, 0x27, 0x2f, 0x00]))

    #002f26f0 - Location of generic license message (NTSC)
    # For some reason has several additional characters at the beginning, possibly some kind of opcodes?
    # Actual text starts at 0x2f2707

    #002f1e40 - Location of Super-A license message (NTSC)


def change_shop_item_quantity_display_to_ap(pine : Pine):
    """
    Change the "You (don't) have it" text in part shops to check whether we've purchased the part for AP, *not*
    whether we actually have the item that would be normally bought in that slot.
    """
    # Change the inventory check call to use our own hook instead
    pine.write_bytes(0x24723c, mips([
        jal(HOOK_ADDR_PARTS_SHOP_CHECK_IF_LOCATION_COMPLETE)
    ]))

    # Is this the My City part shop? If so, jump to the normal function. 
    # Otherwise, call the AP location check function
    pine.write_bytes(HOOK_ADDR_PARTS_SHOP_CHECK_IF_LOCATION_COMPLETE, mips([
        lui(t0, get_upper_nibble(Addresses.ADDR_CURRENT_ROOM_INDEX)),
        ori(t0, t0, get_lower_nibble(Addresses.ADDR_CURRENT_ROOM_INDEX)),
        lbu(t1, 0, t0),
        addiu(t2, zero, 1),
        bne(t1, t2, 7),
        lbu(t1, 2, t0), # get room table value, 2 bytes away from room index
        addiu(t2, zero, 9),
        bne(t1, t2, 4),
        nop(),
        j(0x23D488),
        nop(),
        j(HOOK_ADDR_AP_LOCATION_FUNC_READ),
        nop()
    ]))

    # Change the check at this location to jump to our hook, which will prevent the game from displaying 
    #     "You have #" in part shops (except My City), and always display "You [don't] have it" instead.
    #     ("You have #" would not make sense for AP location checks.)
    pine.write_bytes(0x247284, mips([
        nop(),
        jal(HOOK_ADDR_PARTS_SHOP_OWNED_QUANTITY_STRING_HANDLING)
    ]))

    # If this is not the My City part shop, jump to the part of the calling function that makes the
    #     displayed text "You have it" or "You don't have it".
    #     Otherwise, jump to the part that could make it "You have #".
    pine.write_bytes(HOOK_ADDR_PARTS_SHOP_OWNED_QUANTITY_STRING_HANDLING, mips([
        lui(t0, get_upper_nibble(Addresses.ADDR_CURRENT_ROOM_INDEX)),
        ori(t0, t0, get_lower_nibble(Addresses.ADDR_CURRENT_ROOM_INDEX)),
        lbu(t1, 0, t0),
        addiu(t2, zero, 1),
        bne(t1, t2, 9),
        lbu(t1, 2, t0), # get room table value, 2 bytes away from room index
        addiu(t2, zero, 9),
        bne(t1, t2, 6),
        lui(t0, get_upper_nibble(Addresses.ADDR_PART_SELECTION_MENU_STYLE)),
        ori(t0, t0, get_lower_nibble(Addresses.ADDR_PART_SELECTION_MENU_STYLE)),
        lw(v1, 0, t0),
        j(0x2472b0),    # If My City part shop
        nop(),
        j(0x24728c),    # If not My City part shop
        nop()
    ]))


def patch_npc_equips(pine : Pine):
    """
    Prevent NPCs from equipping parts to the player (which could allow them to, at least temporarily, have parts
    when they shouldn't in AP).
    """
    # Write hook in dialogue handler function that only allows your equipped items to be modified
    #   if you are in the Ski Jump lobby (since it should still remove the Flight Wing).
    # All other NPC equips should be disabled. (e.g. Billboards, Wing Set + Propeller)
    pine.write_bytes(0x23B984, mips([
        jal(HOOK_ADDR_NPC_EQUIPS)
    ]))

    pine.write_bytes(HOOK_ADDR_NPC_EQUIPS, mips([
        lui(t0, get_upper_nibble(Addresses.ADDR_CURRENT_ROOM_INDEX)),
        ori(t0, t0, get_lower_nibble(Addresses.ADDR_CURRENT_ROOM_INDEX)),
        lbu(t1, 0, t0),
        addiu(t2, zero, 7),
        bne(t1, t2, 7),
        lbu(t1, 2, t0), # get room table value, 2 bytes away from room index
        addiu(t2, zero, 6),
        bne(t1, t2, 4),
        nop(),
        j(0x23C418),
        nop(),
        jr(ra),
        nop()
    ]))


def patch_npc_dialogue_triggers(pine : Pine):
    """
    Patch some dialogue opcodes that would cause dialogue to be skipped if the player already has an item.
    Not patching these would make some AP locations missable if the player receives the vanilla item for
    that location prior to completing it.
    """
    # Patch Luke's dialogue for the UnbaboDoll. Normally, the dialogue where he would give you the doll
    #   is skipped if you already have the stamp, *or* if you already have the item.
    # This changes the item check to use the collectible index after the final one (the Peach), which is never set.
    pine.write_bytes(0x315FC4, bytes([0x30]))


def patch_tin_raceway_requirements(pine : Pine):
    """
    Make Tin Raceway accessible prior to becoming the president so it can be a location check.
    """
    # Change the license requirement for entering Tin Raceway to the A License.
    #   This does not make Tin Raceway a required race for obtaining the Super A License.
    pine.write_bytes(0x2BDF63, bytes([2]))

    # Also for Tin Raceway, modify the assembly instruction at the below location to be an unconditional branch.
    #   This branch typically checks whether the race you're trying to enter is Tin Raceway. 
    #   If it is, it then checks if you've completed stamp 100 (Became the President), and prevents you from
    #   entering if you haven't (displays "Under construction").
    pine.write_bytes(0x239E12, bytes([0,0x10]))


def disable_func_that_overwrites_ap_save_data(pine : Pine):
    """
    Disable a function call that will, for some reason, reset our AP save data upon recruiting a 2nd teammate.

    I've yet to find any indication in Ghidra that the data this writes is ever read by anything in the game.
    No idea why these 0x0 writes happen - for now, I'm just going to remove this call, run some test multiworlds,
    and see if anything breaks.
    """
    pine.write_bytes(0x23DAF4, mips([
        jr(ra) # (instead of a j to the offending function)
    ]))

def disable_vanilla_my_city_part_shop_handling(pine : Pine):
    """
    Overwrite function that handles vanilla part availability behavior for My City part shop to a jr ra (i.e. do nothing).
    In vanilla, all parts from part shops you have previously visited are available in My City.
    """
    pine.write_bytes(0x267C30, mips([
        jr(ra),
        nop()
    ]))


def encode_as_ascii_code_list(string : str) -> list[int]:
    codes = []
    for char in string:
        try:
            codes.append(list(char.encode('ascii'))[0])
        # If a character is not a valid ASCII character, fall back to a space.
        except Exception:
            if char == "é":
                codes.append(0x65) # Special case for 'é' since it's used throughout Pokémon, replace with 'e'
            else:
                codes.append(0x20) # 0x20 is a space in ASCII
    
    return codes

def hook_shops_to_display_ap_item_strings(pine : Pine, shop_strings : list):
    """
    Write the AP part shop descriptions (item name, player, classification) into the now-unused email text data, and
    add a hook to the part shops to display them instead of the vanilla part descriptions.
    """
    from BaseClasses import ItemClassification

    for description in shop_strings:
        addr = Addresses.ADDR_SHOP_STRINGS + (Addresses.SHOP_STRING_LENGTH * description["vanilla_item_id"])

        # Encode the item name and the name of the player it's for into a list of ASCII codes.
        item_name_bytes = bytes(encode_as_ascii_code_list(description["item_name"]) + [0]) # Add an extra space before the player name for spacing in-game, and the null terminator
        player_bytes = bytes([0x20] + encode_as_ascii_code_list(description["player"]) + [0]) # Add null terminator
        item_classification_addr = []

        match(description["item_classification"]):
            case ItemClassification.progression:
                temp = Addresses.ADDR_PART_SHOP_AP_ITEM_CLASSIFICATIONS
            case ItemClassification.progression_skip_balancing:
                temp = Addresses.ADDR_PART_SHOP_AP_ITEM_CLASSIFICATIONS
            case ItemClassification.useful:
                temp = Addresses.ADDR_PART_SHOP_AP_ITEM_CLASSIFICATIONS + 0x10
            case ItemClassification.filler:
                temp = Addresses.ADDR_PART_SHOP_AP_ITEM_CLASSIFICATIONS + 0x18
            case ItemClassification.trap:
                temp = Addresses.ADDR_PART_SHOP_AP_ITEM_CLASSIFICATIONS + 0x20
            case _:
                temp = Addresses.ADDR_PART_SHOP_AP_ITEM_CLASSIFICATIONS + 0x28
        
        item_classification_addr = list(temp.to_bytes(4))
        item_classification_addr.reverse()
        item_classification_addr = bytes(item_classification_addr)

        pine.write_bytes(addr, item_name_bytes)
        pine.write_bytes(addr+Addresses.OFFSET_SHOP_STRING_PLAYER_NAME, player_bytes)
        pine.write_bytes(addr+Addresses.OFFSET_SHOP_STRING_ITEM_CLASSIFICATION_PTR, item_classification_addr)
        
    # 'Progression' string
    addr = Addresses.ADDR_PART_SHOP_AP_ITEM_CLASSIFICATIONS
    pine.write_bytes(addr, bytes([0x20, 0x50, 0x72, 0x6f]))
    pine.write_bytes(addr+4, bytes([0x67, 0x72, 0x65, 0x73]))
    pine.write_bytes(addr+8, bytes([0x73, 0x69, 0x6f, 0x6e]))
    pine.write_bytes(addr+12, bytes([0x00, 0x00, 0x00, 0x00]))

    # 'Useful' string
    pine.write_bytes(addr+16, bytes([0x20, 0x55, 0x73, 0x65]))
    pine.write_bytes(addr+20, bytes([0x66, 0x75, 0x6c, 0x00]))

    # 'Filler' string
    pine.write_bytes(addr+24, bytes([0x20, 0x46, 0x69, 0x6c]))
    pine.write_bytes(addr+28, bytes([0x6c, 0x65, 0x72, 0x00]))

    # 'Trap' string
    pine.write_bytes(addr+32, bytes([0x20, 0x54, 0x72, 0x61]))
    pine.write_bytes(addr+36, bytes([0x70, 0x00, 0x00, 0x00]))

    # 'Other' string
    pine.write_bytes(addr+40, bytes([0x20, 0x4f, 0x74, 0x68]))
    pine.write_bytes(addr+44, bytes([0x65, 0x72, 0x00, 0x00]))

    # ------------------------------------------

    # Change JAL in func that handles the final buy confirmation to our hook.
    pine.write_bytes(0x268910, mips([
        jal(HOOK_ADDR_AP_PARTS_SHOP_FULL_NAME_IN_BUY_CONFIRMATION)
    ]))

    # Change JAL that would get the address of the vanilla parts description to our hook.
    pine.write_bytes(0x22e9c4, mips([
        jal(HOOK_ADDR_AP_PARTS_SHOP_DESCRIPTIONS) # Same as HOOK_ADDR_AP_PARTS_SHOP_FULL_NAME_IN_BUY_CONFIRMATION + 0xC, see note below
    ]))

    # Write the hook to replace the part descriptions in stores with AP item data
    pine.write_bytes(HOOK_ADDR_AP_PARTS_SHOP_FULL_NAME_IN_BUY_CONFIRMATION, mips([
        # Start here if we want the full part name (set t0 to 1, checked later)
        # This would likely give us too many characters to fit in the part description box,
        #   but is important for the final buy confirmation so the player can see the full
        #   item name somewhere.
        addiu(t0, zero, 0x1),
        beq(zero, zero, 3),
        nop(),

        # Otherwise, start here for a truncated version of the item name that should fit in
        # the part description box (set t0 to 0, checked later)
        # (NOTE: HOOK_ADDR_AP_PARTS_SHOP_DESCRIPTIONS points to here)
        addiu(t0, zero, 0),

        # Check if we are in a part shop. If not, return.
        # (We don't want to modify part descriptions when in other places - for example,
        #   while changing our parts in a Q's Factory.)
        #
        # Load shop type value
        lui(t7, get_upper_nibble(Addresses.ADDR_PART_SELECTION_MENU_STYLE)),
        ori(t7, t7, get_lower_nibble(Addresses.ADDR_PART_SELECTION_MENU_STYLE)),
        lbu(t7, 0, t7),
        addiu(t6, zero, 0x1),

        # Check if shop type value is one, else return
        beq(t7, t6, 4),
        nop(),
        j(0x2DAA9C), # JUMP TO 'PASSTHROUGH' BELOW
        nop(),

        # Check if this is the My City part shop. If so, return
        addiu(t7, zero, 0x9),
        lui(t6, get_upper_nibble(Addresses.ADDR_CURRENT_ROOM_TABLE)),
        ori(t6, t6, get_lower_nibble(Addresses.ADDR_CURRENT_ROOM_TABLE)),
        lbu(t6, 0, t6),
        bne(t7, t6, 4),
        nop(),
        j(0x2DAA9C), # JUMP TO 'PASSTHROUGH' BELOW
        nop(),

        # Init t5 and t6
        addiu(t5, zero, 0),
        addiu(t6, zero, 0),

        # Load address to table_length_table
        lui(t7, get_upper_nibble(Addresses.ADDR_TABLE_LENGTH_TABLE)),
        ori(t7, t7, get_lower_nibble(Addresses.ADDR_TABLE_LENGTH_TABLE)),

        # Iterate through table_length_table and add part counts of all prior part types
        beq(a0, zero, 6),
        addiu(a0, a0, -0x1),
        lbu(t5, 0, t7),
        addu(t6, t5, t6),
        addiu(t7, t7, 0x1),
        beq(zero, zero, -5),
        nop(),

        # Add ID of this part to the total
        addu(t6, t6, a1),

        # Multiply the total by 64 (each part description is 64 bytes)
        sll(t6, t6, 0x6),

        # Get address of part descriptions
        lui(t7, get_upper_nibble(Addresses.ADDR_SHOP_STRINGS)),
        ori(t7, t7, get_lower_nibble(Addresses.ADDR_SHOP_STRINGS)),

        # Add ID * 64 to that address to get the address of this part description
        addu(t7, t7, t6),

        # Test if t0 is not 0. 
        #   t0 == 0 -> Get truncated name
        #   t0 == 1 -> Get full name
        # If 1, jump to 'RETURN FULL NAME' at the end (we don't need the next part).
        bne(t0, zero, 32),
        nop(),

        # If t0 is 0, we're trying to fill the part description box.
        # a2 stores the current line we're trying to print in the part description
        # If it's line 0, get the name of the item.
        # If it's line 1, get the name of the player that item is for.
        # If it's line 2, get the AP item classification for that item (e.g. Progression, Useful, etc.)

        # Test if line 0. Decrement a2 and branch if not.
        bne(a2, zero, 16),

        # Line 0 - Get truncated version of item name
        # Copy characters to the temp address location, return the address to it
        addiu(a2, a2, -0x1),
        lui(t6, get_upper_nibble(Addresses.ADDR_TEMP_SHORTENED_PART_NAME)),
        ori(t6, t6, get_lower_nibble(Addresses.ADDR_TEMP_SHORTENED_PART_NAME)),
        addu(v0, zero, t6),
        addiu(t4, zero, 0x12), # Max character count is 18 (19 total when null terminator added)

        # Loop. Break if char in t5 is null terminator, or if we hit the max character count
        # (i.e. t4 == 0). Otherwise, copy char and increment.
        lbu(t5, 0, t7),
        sb(t5, 0, t6),
        beq(t5, zero, 23),
        sb(zero, 1, t6), # Write null terminator in following char - will get overwritten if we aren't done looping, otherwise sets null terminator
        addiu(t7, t7, 0x1),
        addiu(t6, t6, 0x1),
        beq(t4, zero, 19),
        nop(),
        beq(zero, zero, -8),
        addiu(t4, t4, -0x1),

        # Test if line 1. Decrement a2 and branch if not.
        bne(a2, zero, 5),
        addiu(a2, a2, -0x1),

        # Line 1 - Get name of player this item is for
        addiu(v0, t7, 0x2A), # (add offset to part description address)
        beq(zero, zero, 12),
        nop(),

        # Test if line 2. Decrement a2 and branch if not.
        bne(a2, zero, 6),
        addiu(a2, a2, -0x1),

        # Line 2 - Get the AP item classification
        addiu(t7, t7, 0x3C), # (add offset to part description address)
        lw(v0, 0, t7),
        beq(zero, zero, 6),
        nop(),

        # Line 3 - Return null terminator
        addiu(v0, t7, 0x3F), # (offset of null terminator)

        # Return
        jr(ra),
        nop(),

        # RETURN FULL NAME
        addiu(v0, t7, 0),
        jr(ra),
        nop(),

        # PASSTHROUGH
        # If we've jumped here, it's because we're either not in a part shop, or in the My City part shop.
        # Depending on whether this function was called for a part shop description or for the full part title displayed
        #   just before purchase, we need to now jump to different functions.
        beq(t0, zero, 4),
        nop(),
        j(0x243468),
        nop(),
        j(0x243848),
        nop()
    ]))


def enforce_area_access(pine : Pine, area_unlock_mode : int):
    """
    Create a function in RTA that, while in the overworld, checks every frame to see if the player has access
    to the chunk they are in, given their AP decorations/stamps (depending on the mode the player set in their YAML).
    
    If they don't have access, prevent them from interacting with anything, and display a warning on screen.
    """
    # 1. Check the progression mode
    # 2. If Decorations:
    #    - What chunk are we in?
    #    - Check the reference table for chunk -> region unlock ID
    #    - Do we have that item in our collectibles table?
    #    - If yes, return True, if no, return False
    # 3. If Stamps:
    #    - What chunk are we in?
    #    - Pull the AP stamp count
    #    - Check the reference table for chunk -> required stamp count
    #    - Is AP stamp count >= required stamp count?
    #    - If yes, return True, if no, return False
    # 4. Result:
    #    - If True: great, we can talk to people, enter houses, and pick up overworld items
    #    - If False: we can't do those things, print "No access!" in the top left of the screen

    # Create the chunk -> region unlock ID reference table
    NO_REGION = "None"
    SANDPOLIS = "Sandpolis"
    MY_CITY = "My City"
    CHESTNUT_CANYON = "Chestnut Canyon"
    CHESTNUT_CANYON_TUNNEL = "Chestnut Canyon Tunnel" # Need to handle the tunnel separately because the Q Coin off the highway should be logically part of Sandpolis instead
    FUJI_CITY = "Fuji City"
    MUSHROOM_ROAD = "Mushroom Road"
    PEACH_TOWN = "Peach Town"
    WHITE_MOUNTAIN = "White Mountain"
    WHITE_MOUNTAIN_MAIN = "White Mountain Main" # Need to handle White Mountain proper separately due to Moonstone being in the chunk (which should be in-logic for Mushroom Road)
    WINDMILLS = "Windmills"
    PAPAYA_ISLAND = "Papaya Island"
    CLOUD_HILL = "Cloud Hill"
    chunks = [
        # 0x0 through 0xF
        NO_REGION,NO_REGION,NO_REGION,NO_REGION,
        NO_REGION,SANDPOLIS,SANDPOLIS,SANDPOLIS,
        SANDPOLIS,SANDPOLIS,NO_REGION,MY_CITY,
        MY_CITY,MY_CITY,NO_REGION,NO_REGION,

        # 0x10 through 0x1F
        NO_REGION,NO_REGION,NO_REGION,CHESTNUT_CANYON,
        CHESTNUT_CANYON_TUNNEL,NO_REGION,SANDPOLIS,FUJI_CITY,
        FUJI_CITY,NO_REGION,FUJI_CITY,NO_REGION,
        NO_REGION,NO_REGION,NO_REGION,NO_REGION,

        # 0x20 through 0x2F
        NO_REGION,WHITE_MOUNTAIN,NO_REGION,WHITE_MOUNTAIN_MAIN,
        MUSHROOM_ROAD,WHITE_MOUNTAIN,FUJI_CITY,WINDMILLS,
        FUJI_CITY,PEACH_TOWN,PEACH_TOWN,PEACH_TOWN,
        NO_REGION,PEACH_TOWN,NO_REGION,PAPAYA_ISLAND,

        # 0x30 through 0x3F
        NO_REGION,NO_REGION,WHITE_MOUNTAIN,NO_REGION,
        WHITE_MOUNTAIN,NO_REGION,NO_REGION,NO_REGION,
        NO_REGION,NO_REGION,PEACH_TOWN,NO_REGION,
        PEACH_TOWN,NO_REGION,NO_REGION,NO_REGION,

        # 0x40
        CLOUD_HILL
    ]

    # ASM labels used in both the versions of the patch (decorations and stamps)
    GET_REQUIREMENTS = "Get Requirements"
    ACCESS_DENIED = "Access Denied"
    ACCESS_GRANTED = "Access Granted"
    HANDLE_WHITE_MOUNTAIN = "Handle White Mountain"
    HANDLE_CHESTNUT_CANYON_TUNNEL = "Handle Chestnut Canyon Tunnel"
    TEST_REQUIREMENTS = "Test Requirements"
    
    data = []
    # For decorations mode, the table values should contain the IDs of both
    #   items that can unlock access to the chunk.
    # Items have a table ID and an index in that table, but all decorations
    #   are in the collectibles table (0xF), so only the index is needed.
    if area_unlock_mode == 0: # Decorations
        for chunk in chunks:
            if chunk == NO_REGION:
                data += [0,0]
            elif chunk == PEACH_TOWN:
                data += [0xA, 0xB]
            elif chunk == WINDMILLS:
                data += [0xFF, 0xFF] # Special case
            elif chunk == FUJI_CITY:
                data += [0xC, 0xD]
            elif chunk == MY_CITY:
                data += [0,0]
            elif chunk == SANDPOLIS:
                data += [0xe, 0xf]
            elif chunk == CHESTNUT_CANYON:
                data += [0x10, 0x11]
            elif chunk == CHESTNUT_CANYON_TUNNEL:
                data += [0xFD, 0xFD] # Special case
            elif chunk == MUSHROOM_ROAD:
                data += [0x1, 0x2]
            elif chunk == WHITE_MOUNTAIN:
                data += [0x9, 0x12]
            elif chunk == WHITE_MOUNTAIN_MAIN:
                data += [0xFE, 0xFE] # Special case
            elif chunk == PAPAYA_ISLAND:
                data += [0x13, 0x14]
            elif chunk == CLOUD_HILL:
                data += [0x15, 0x16]
            else:
                raise Exception("enforce_area_access, decorations table: Invalid region?")

        # DECORATIONS MODE PATCH
        pine.write_bytes(HOOK_ADDR_ENFORCE_AREA_ACCESS, mips([
            # Create a stack frame of 4 bytes to store the current return address
            addiu(sp, sp, -0x4),
            sw(ra, 0, sp),
            
            # Get the current world chunk ID
            lui(t0, get_upper_nibble(Addresses.ADDR_CURRENT_WORLD_CHUNK)),
            addiu(t0, t0, get_lower_nibble(Addresses.ADDR_CURRENT_WORLD_CHUNK)),
            lbu(t0, 0, t0),

            # Add the current chunk ID * 2 to ADDR_CHUNK_ACCESS_REQUIREMENTS_TABLE to get
            #   the correct index in the table (since each chunk has two bytes, one for each item ID).
            # Then, store the 1st byte in t1, and the 2nd in t2.
            label(GET_REQUIREMENTS),
            lui(t1, get_upper_nibble(Addresses.ADDR_CHUNK_ACCESS_REQUIREMENTS_TABLE)),
            ori(t1, t1, get_lower_nibble(Addresses.ADDR_CHUNK_ACCESS_REQUIREMENTS_TABLE)),
            addu(t1, t1, t0),
            addu(t1, t1, t0),
            lbu(t2, 1, t1),
            lbu(t1, 0, t1),

            # If the first byte is zero, this means that the chunk has no access requirements.
            #   Jump to the end of the function, where we'll return 1.
            beq(t1, zero, ACCESS_GRANTED),

            # ---- HANDLE WINDMILLS CHUNK ----
            # If the first byte is 0xFF, this means that we're in the Windmills region.
            #   Windmills is a special case, as part of the region has no access requirements,
            #   and part of it has requirements that match White Mountain. (Without physics exploits,
            #   you can't get on top of the waterfall / cliff unless you go through White Mountain).
            ori(t3, zero, 0xFF),
            bne(t1, t3, HANDLE_WHITE_MOUNTAIN),
            nop(),

            # If we're here, we're in Windmills.
            # To figure out which side of Windmills we're on, take the two most significant bytes
            #   of the player's X position and compare them to 0x43B0. If it's less than that, we're
            #   in the White Mountain section. Otherwise, we're in the Peach Town section.
            lui(t3, get_upper_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            ori(t3, t3, get_lower_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            lhu(t3, 2, t3),
            slti(t3, t3, 0x43B0),
            bne(t3, zero, 5),
            nop(),

            # If we're here, we're in the Peach Town section of Windmills
            # t0 is currently expected to contain the current world chunk ID - set it to Peach Town's
            #   (0x2B), then branch back up in order to read from that part of the access requirements
            #   table instead.
            addiu(t0, zero, 0x2B),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            # If we're here, we're in the White Mountain section of Windmills
            # Same as the lines above, but set it to a White Mountain chunk ID that is *not* the main
            #   town (e.g. 0x25), then branch back up.
            # We do *not* want to use the main town ID (0x23) as it *also* is a special case, see below.
            addiu(t0, zero, 0x25),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            # ---- HANDLE WHITE MOUNTAIN TOWN CHUNK ----
            # If the first byte is 0xFE, that means we're in the chunk containing White Mountain proper.
            #   White Mountain is also a special case, as it contains the Moonstone, the gem at
            #   the bottom of the waterfall. ...This is awkward, as IMO most players would expect
            #   the bottom of the waterfall to be considered part of Mushroom Road, not White Mountain.
            #   (Especially since most of the river path leading up to it *is* part of Mushroom Road's chunk.)
            # The code below will redirect us to using Mushroom Road's requirements if we're far
            #   enough south from the town that we could have jumped off the waterfall.
            label(HANDLE_WHITE_MOUNTAIN),
            ori(t3, zero, 0xFE),
            bne(t1, t3, HANDLE_CHESTNUT_CANYON_TUNNEL),
            nop(),

            # If we're here, we're in White Mountain proper
            #   Take the two most significant bytes of the player's Z position and compare it to 0x4310.
            #   If it's less than that, we're too far south, and we're in the Mushroom Road section.
            #   Otherwise, we're in White Mountain.
            lui(t3, get_upper_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            ori(t3, t3, get_lower_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            lhu(t3, 10, t3),
            slti(t3, t3, 0x4310),
            bne(t3, zero, 5),
            nop(),

            # If we're here, we're in the White Mountain part of the chunk.
            # Set t0 to a different White Mountain chunk (such as 0x25) and branch back up.
            addiu(t0, zero, 0x25),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            # If we're here, we're in the Mushroom Road part of the chunk.
            # Set t0 to Mushroom Road's chunk ID (0x24) and branch back up.
            addiu(t0, zero, 0x24),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            # ---- HANDLE CHESTNUT CANYON TUNNEL CHUNK ----
            # If the first byte is 0xFD, that means we're in the chunk containing the Chestnut Canyon tunnel.
            #   There is a Q Coin off of the highway on the cliff beside the ocean in this chunk.
            #   Since it is outside of the tunnel on the Sandpolis side, it should probably be logically
            #   considered part of Sandpolis.
            label(HANDLE_CHESTNUT_CANYON_TUNNEL),
            ori(t3, zero, 0xFD),
            bne(t1, t3, TEST_REQUIREMENTS),
            nop(),

            # If we're here, we're at the Chestnut Canyon tunnel.
            #   Take the two most significant bytes of the player's X position and compare it to 0x44AC.
            #   If it's less than that, we're too far west, and we're in the tunnel.
            #   Otherwise, we're outside of it (or close enough).
            lui(t3, get_upper_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            ori(t3, t3, get_lower_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            lhu(t3, 2, t3),
            slti(t3, t3, 0x44AC),
            beq(t3, zero, 5),
            nop(),

            # If we're here, we're in the Chestnut Canyon part of the chunk.
            # Set t0 to Chestnut Canyon's chunk ID (0x13) and branch back up.
            addiu(t0, zero, 0x13),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            # If we're here, we're in the Sandpolis part of the chunk.
            # Set t0 to Sandpolis's chunk ID (0x7) and branch back up.
            addiu(t0, zero, 0x7),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            # ----------------------------------

            # Store the address for where we'll store the final boolean return value
            #   (1 if the player can access, 0 if they can't)
            # TODO: this could be moved to the section following the next one?
            label(TEST_REQUIREMENTS),
            lui(t3, get_upper_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
            ori(t3, t3, get_lower_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),

            # Call the game's 'has item' function, passing the IDs of the two decoration
            #   items this region is looking for.
            addiu(a0, zero, 0xF), # 0xF is the collectibles category
            addiu(a1, t1, 0), # t1 has the 1st item ID
            jal(0x23D488), # Call vanilla 'has item' function
            addiu(a2, zero, 0), # a2 appears to always be 0 when checking player inventory

            bne(v0, zero, ACCESS_GRANTED), # Jump to end if item was found

            addiu(a0, zero, 0xF),
            addiu(a1, t2, 0), # t2 has the 2nd item ID
            jal(0x23D488),
            addiu(a2, zero, 0),

            bne(v0, zero, ACCESS_GRANTED),
            nop(),

            # If we're here, the player did not have either of the needed decoration items.
            #   Display 'no access', set access bool to 0, and return.
            label(ACCESS_DENIED),
            addiu(a0, zero, 0x11), # Horizontal value in screen space (i.e. how far to the right)
            addiu(a1, zero, 0x7), # Vertical value in screen space (i.e. how far down)
            lui(a2, get_upper_nibble(Addresses.ADDR_STRING_NO_ACCESS)),
            ori(a2, a2, get_lower_nibble(Addresses.ADDR_STRING_NO_ACCESS)),
            addiu(a3, zero, 0x6), # a3 contains the text color, 0x6 is red
            lw(ra, 0, sp), # Load the return address we stored in the stack frame at the beginning back into ra
            addiu(sp, sp, 0x4), # Move the stack pointer back to the position it was in before this function ran
            j(0x203FC8), # Jump to the function that displays text on screen (which will eventually jr(ra) to our return address)
            sb(v0, 0, t3), # Store 0 at ADDR_CHUNK_ACCESS_BOOL 

            # If we're here, the chunk either had no access requirements, or the player had
            #   at least one of the required decoration items. Set access bool to 1 and return.
            label(ACCESS_GRANTED),
            lw(ra, 0, sp), # Load the return address we stored in the stack frame at the beginning back into ra
            addiu(v0, zero, 0x1), # Set return value to 1
            lui(t3, get_upper_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
            ori(t3, t3, get_lower_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
            addiu(sp, sp, 0x4), # Move the stack pointer back to the position it was in before this function ran
            jr(ra), # Return to the calling function
            sb(v0, 0, t3), # Store 1 at ADDR_CHUNK_ACCESS_BOOL
            nop()
        ]))

    elif area_unlock_mode == 1: # Stamps       
        # For stamp mode, the table values should contain the number of AP stamp items
        #   needed to unlock access to the chunk.
        for chunk in chunks:
            if chunk == NO_REGION:
                data += [0,0]
            elif chunk == PEACH_TOWN:
                data += [0, 0]
            elif chunk == WINDMILLS:
                data += [0xFF, 0] # Special case
            elif chunk == FUJI_CITY:
                data += [5, 0]
            elif chunk == MY_CITY:
                data += [0,0]
            elif chunk == SANDPOLIS:
                data += [10, 0]
            elif chunk == CHESTNUT_CANYON:
                data += [15, 0]
            elif chunk == CHESTNUT_CANYON_TUNNEL:
                data += [0xFD, 0] # Special case
            elif chunk == MUSHROOM_ROAD:
                data += [20, 0]
            elif chunk == WHITE_MOUNTAIN:
                data += [25, 0]
            elif chunk == WHITE_MOUNTAIN_MAIN:
                data += [0xFE, 0x0] # Special case
            elif chunk == PAPAYA_ISLAND:
                data += [30, 0]
            elif chunk == CLOUD_HILL:
                data += [35, 0]
            else:
                raise Exception("enforce_area_access, stamp table: Invalid region?")
        
        # STAMP MODE PATCH
        pine.write_bytes(HOOK_ADDR_ENFORCE_AREA_ACCESS, mips([
            # Mostly the same as the decorations mode version of the patch above
            # TODO: Can these be merged in a way that is compatible with the patch verification system?
            # Maybe write decorations patch first, and then re-patch differences in if in stamps mode?
            # Normally, having one patch overwrite another would cause the patch verification system to
            #   return a failure, but I think it would work fine if the two are in the same function?
            addiu(sp, sp, -0x4),
            sw(ra, 0, sp),

            lui(t0, get_upper_nibble(Addresses.ADDR_CURRENT_WORLD_CHUNK)),
            addiu(t0, t0, get_lower_nibble(Addresses.ADDR_CURRENT_WORLD_CHUNK)),
            lbu(t0, 0, t0),
            
            label(GET_REQUIREMENTS),
            lui(t1, get_upper_nibble(Addresses.ADDR_CHUNK_ACCESS_REQUIREMENTS_TABLE)),
            ori(t1, t1, get_lower_nibble(Addresses.ADDR_CHUNK_ACCESS_REQUIREMENTS_TABLE)),
            addu(t1, t1, t0),
            addu(t1, t1, t0),
            nop(),
            lbu(t1, 0, t1),

            beq(t1, zero, ACCESS_GRANTED),

            # ---- HANDLE WINDMILLS CHUNK ----
            nop(), # TODO: remove?
            ori(t3, zero, 0xFF),
            bne(t1, t3, HANDLE_WHITE_MOUNTAIN),
            nop(),

            lui(t3, get_upper_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            ori(t3, t3, get_lower_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            lhu(t3, 2, t3),
            slti(t3, t3, 0x43B0),
            bne(t3, zero, 5),
            nop(),

            addiu(t0, zero, 0x2B),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            addiu(t0, zero, 0x25),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            # ---- HANDLE WHITE MOUNTAIN TOWN CHUNK ----
            label(HANDLE_WHITE_MOUNTAIN),
            ori(t3, zero, 0xFE),
            bne(t1, t3, HANDLE_CHESTNUT_CANYON_TUNNEL),
            nop(),

            lui(t3, get_upper_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            ori(t3, t3, get_lower_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            lhu(t3, 10, t3),
            slti(t3, t3, 0x4310),
            bne(t3, zero, 5),
            nop(),

            addiu(t0, zero, 0x25),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            addiu(t0, zero, 0x24),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            # ---- HANDLE CHESTNUT CANYON TUNNEL CHUNK ----
            label(HANDLE_CHESTNUT_CANYON_TUNNEL),
            ori(t3, zero, 0xFD),
            bne(t1, t3, TEST_REQUIREMENTS),
            nop(),

            lui(t3, get_upper_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            ori(t3, t3, get_lower_nibble(Addresses.ADDR_POSITION_IN_CHUNK)),
            lhu(t3, 2, t3),
            slti(t3, t3, 0x44AC),
            beq(t3, zero, 5),
            nop(),

            addiu(t0, zero, 0x13),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            addiu(t0, zero, 0x7),
            beq(zero, zero, GET_REQUIREMENTS),
            nop(),

            # ------------------------------------
            label(TEST_REQUIREMENTS),
            lui(t3, get_upper_nibble(Addresses.ap_stamps_received.address)),
            ori(t3, t3, get_lower_nibble(Addresses.ap_stamps_received.address)),

            lbu(t3, 0, t3),
            addiu(t3, t3, 0x1),
            slt(v0, t1, t3), # Are the number of AP stamps received less than the number needed to access this region?
            
            lui(t3, get_upper_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
            ori(t3, t3, get_lower_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
            
            bne(v0, zero, ACCESS_GRANTED),
            nop(),

            label(ACCESS_DENIED),
            addiu(a0, zero, 0x11),
            addiu(a1, zero, 0x7),
            lui(a2, get_upper_nibble(Addresses.ADDR_STRING_NO_ACCESS)),
            ori(a2, a2, get_lower_nibble(Addresses.ADDR_STRING_NO_ACCESS)),
            addiu(a3, zero, 0x6),
            lw(ra, 0, sp),
            addiu(sp, sp, 0x4),
            j(0x203FC8),
            sb(v0, 0, t3),

            label(ACCESS_GRANTED),
            lw(ra, 0, sp),
            addiu(v0, zero, 0x1),
            lui(t3, get_upper_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
            ori(t3, t3, get_lower_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
            addiu(sp, sp, 0x4),
            jr(ra),
            sb(v0, 0, t3),
            nop()
        ]))

        # In stamp mode, display the number of AP stamp items received in the Stamps page in the Notebook
        # Part 1 - Write "AP stamps: " string
        addr = Addresses.ADDR_STRING_AP_STAMPS # Ran out of room in the other location, moving lower
        pine.write_bytes(addr+0, bytes([0x41, 0x50, 0x20, 0x53]))
        pine.write_bytes(addr+4, bytes([0x74, 0x61, 0x6d, 0x70]))
        pine.write_bytes(addr+8, bytes([0x73, 0x3a, 0x20]))

        # Part 2 - Jump to our hook instead of returning from notebook stamps page task
        pine.write_bytes(0x265FDC, mips([
            j(HOOK_ADDR_DISPLAY_AP_STAMP_COUNT)
        ]))

        # Part 3 - Hook
        # Takes the AP stamp count, converts the number to a string, concatenates it to the end of
        #    our "AP stamps: " string, and then passes that string's address (+ positioning values
        #    and text color value) to RTA's print text function.
        pine.write_bytes(HOOK_ADDR_DISPLAY_AP_STAMP_COUNT, mips([
            addiu(sp, sp, -0x4),
            sw(ra, 0, sp),
            lui(a0, get_upper_nibble(Addresses.ap_stamps_received.address)),
            ori(a0, a0, get_lower_nibble(Addresses.ap_stamps_received.address)),
            lbu(a0, 0, a0),
            lui(a2, get_upper_nibble(Addresses.ADDR_STRING_AP_STAMPS)),
            ori(a2, a2, get_lower_nibble(Addresses.ADDR_STRING_AP_STAMPS)),
            sb(zero, 0xB, a2),
            jal(HOOK_ADDR_CONVERT_DIGIT_IN_INT_TO_CHAR),
            addiu(a1, zero, 0x64),
            addu(a0, zero, v0),
            jal(HOOK_ADDR_CONVERT_DIGIT_IN_INT_TO_CHAR),
            addiu(a1, zero, 0xA),
            addu(a0, zero, v0),
            jal(HOOK_ADDR_CONVERT_DIGIT_IN_INT_TO_CHAR),
            addiu(a1, zero, 0x1),
            addiu(a0, zero, 0x14),
            addiu(a1, zero, 0x4),
            addiu(a3, zero, 0x0),
            lw(ra, 0, sp),
            j(0x203FC8),
            addiu(sp, sp, 0x4),
            nop(),
        ]))

        # Function extracting a character from a number (sets only one char, for one digit)
        # Called by above
        # a0 - Number to print
        # a1 - Lowest possible value that contains the digit to test against (i.e to get hundreds digit, pass 100, or 0x64)
        # a2 - Address to string, we'll save the char to the end of the string and then add a null terminator after it
        pine.write_bytes(HOOK_ADDR_CONVERT_DIGIT_IN_INT_TO_CHAR, mips([
            addiu(t0, zero, 0),
            addu(t1, zero, a2),
            lbu(t2, 0, t1),
            bne(t2, zero, -0x1),
            addiu(t1, t1, 0x1),
            addu(t2, zero, a0),
            sltu(t3, t2, a1),
            bne(t3, zero, 5),
            nop(),
            addiu(t0, t0, 0x1),
            beq(zero, zero, -4),
            subu(t2, t2, a1),
            addiu(t1, t1, -0x1),
            bne(t0, zero, 11),
            nop(),
            addiu(t4, zero, 0x1),
            beq(t4, a1, 8),
            nop(),
            lbu(t5, -1, t1),
            addiu(t6, zero, 0x20),
            bne(t5, t6, 4),
            nop(),
            beq(zero, zero, 4),
            nop(),
            addiu(t0, t0, 0x30),
            sb(t0, 0, t1),
            sb(zero, 1, t1),
            jr(ra),
            addu(v0, zero, t2),
            nop()
        ]))

    # Write the reference table into the game's memory
    pine.write_bytes(Addresses.ADDR_CHUNK_ACCESS_REQUIREMENTS_TABLE, bytes(data))

    # Write 'No access!' string
    addr = Addresses.ADDR_STRING_NO_ACCESS
    pine.write_bytes(addr, bytes([0x4e, 0x6f, 0x20, 0x61]))
    pine.write_bytes(addr+4, bytes([0x63, 0x63, 0x65, 0x73]))
    pine.write_bytes(addr+8, bytes([0x73, 0x21, 0x00, 0x00]))

    # While in the overworld, if the player doesn't have access to the chunk they're currently in,
    #   display "No access!" in the top-left of the screen.
    # This calls the big patch above every frame, which sets a boolean value that the hooks below
    #   reference to see if they should allow an action or not.
    pine.write_bytes(0x24332C, mips([
        j(HOOK_ADDR_ENFORCE_AREA_ACCESS)
    ]))

    # NPCs and entrances
    pine.write_bytes(0x210EEC, mips([
        jal(HOOK_ADDR_AREA_ACCESS_NPCS_AND_ENTRANCES) # Jump-and-link to hook
    ]))
    # Hook
    pine.write_bytes(HOOK_ADDR_AREA_ACCESS_NPCS_AND_ENTRANCES, mips([
        beq(v0, zero, 8),
        lui(t0, get_upper_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
        ori(t0, t0, get_lower_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
        lbu(t0, 0, t0), # was lb
        beq(t0, zero, 4),
        nop(),
        jr(ra),
        nop(),
        j(0x211100),
        nop()
    ]))

    # Q Coins
    pine.write_bytes(0x241C98, mips([
        jal(HOOK_ADDR_AREA_ACCESS_Q_COINS), # Jump-and-link to hook
        nop()
    ]))
    # Hook
    pine.write_bytes(HOOK_ADDR_AREA_ACCESS_Q_COINS, mips([
        bc1fl(9),
        nop(),
        lui(t0, get_upper_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
        ori(t0, t0, get_lower_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
        lbu(t0, 0, t0), # was lb
        beq(t0, zero, 4),
        nop(),
        jr(ra),
        nop(),
        j(0x241D00),
        nop()
    ]))

    # Overworld items
    # Hook
    pine.write_bytes(HOOK_ADDR_AREA_ACCESS_OVERWORLD_ITEMS, mips([
        addiu(t1, ra, 0),
        lui(t0, get_upper_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
        ori(t0, t0, get_lower_nibble(Addresses.ADDR_CHUNK_ACCESS_BOOL)),
        lbu(t0, 0, t0), # was lb
        bne(t0, zero, 5),
        nop(),
        addiu(ra, ra, 0x10),
        jr(ra),
        nop(),
        jal(0x258E50),
        addiu(ra, t1, 0),
        nop()
    ]))

    # Once the game confirms that the player is colliding with an overworld item, jump to the above area access hook
    overworld_item_collision_checks = [
        0x2409C8, # Peach
        0x25C024, # Wallet 
        0x25C29C, # Fluffy Mushroom
        0x25C3D8, # Amethyst
        0x25C4BC, # Moonstone
        0x25C5F0, # Small Bottle
        0x25C6D0, # Black Opal
        0x25C7B0, # Papu Flower
        0x25C8EC, # Ruby
        0x25CAD0, # Fountain Pen
        0x25CBB0, # Blue Sapphire
        0x25D490, # Topaz
        0x25D5A0  # Emerald
    ]

    for address in overworld_item_collision_checks:
        pine.write_bytes(address+8, mips([
            jal(HOOK_ADDR_AREA_ACCESS_OVERWORLD_ITEMS) # Jump-and-link to hook
        ]))

def part_cost_modifiers(pine : Pine, cost_percent_int : int, cost_max_int : int):
    '''
    Inject a hook into the 'get part cost' function that modifies the returned cost by a 
    provided percentage.
    '''
    # Convert cost_percent_int to two bytes, store in pre-determined location
    # Assumes that int will not be over 100 or below 0
    addr = Addresses.ADDR_AP_PART_COST_MODIFIER
    modifier = list(cost_percent_int.to_bytes(2))
    modifier.reverse()
    modifier = bytes(modifier)
    pine.write_bytes(addr, modifier)

    # Convert cost_max_int to four bytes, store in pre-determined location
    # Assumes that int will not be greater than max 16-bit int
    # If -1, set to max 16-bit int (0xFFFFFFFF)
    addr = Addresses.ADDR_AP_PART_COST_MAXIMUM
    modifier = [0xFF, 0xFF, 0xFF, 0xFF] # default, no maximum
    if cost_max_int >= 0:
        modifier = list(cost_max_int.to_bytes(4))
        modifier.reverse()
    modifier = bytes(modifier)
    pine.write_bytes(addr, modifier)

    # In the function that handles getting the cost of a part/body (0x243670 in NTSC),
    #   Road Trip first loads the type of part, then runs different code depending on
    #   the type of part. This is necessary since the data structures for each part 
    #   differ from each other, so determining where the part cost is actually stored 
    #   in memory is a little different for each part type.
    #
    # After finding the cost, all of these code branches immediately return from the
    #   function. This means that unlike for most functions, where we can patch the
    #   one return call at the end to jump to our hook instead, we need to patch
    #   several return calls, one for each different kind of part.
    cost_return_hooks = [
        0x243698, # Bodies
        0x2436b8, # Tires
        0x2436d8, # Engines
        0x2436f0, # Chassis
        0x243710, # Transmission
        0x243728, # Steering
        0x243750, # Brakes
        0x243770, # Wheels
        0x243788, # Lights
        0x2437a8, # Wing Set
        0x2437c0, # Special Parts
        0x2437e0, # Options
        0x243800, # Sticker
        0x243818, # Horns
        0x243838, # Meters
        # 00243840, # Collectibles, not needed (never sold)
    ]

    for addr in cost_return_hooks:
        pine.write_bytes(addr, mips([
            j(HOOK_ADDR_COST_PERCENTAGE_MODIFIER)
        ]))

    # ASM labels for below hook
    HANDLE_MAX_COST = "Handle Max Cost"
    END = "End"

    # Hook
    pine.write_bytes(HOOK_ADDR_COST_PERCENTAGE_MODIFIER, mips([
        # t0 -- Cost modifier percentage (as int, stored in a halfword (two bytes))
        # t1 -- Temporarily stores the value 100 for a bne, then used as a loop counter (will be division quotient)
        # t2 -- 2nd loop counter

        # Load cost modifier percentage into t0
        lui(t0, get_upper_nibble(Addresses.ADDR_AP_PART_COST_MODIFIER)),
        ori(t0, t0, get_lower_nibble(Addresses.ADDR_AP_PART_COST_MODIFIER)),
        lhu(t0, 0, t0),

        # Set t1 to 100
        addiu(t1, zero, 0x64),

        # If percentage is 100, do nothing - use v0 as-is, move on to the max cost modifier
        bne(t0, t1, 4),
        nop(),
        beq(zero, zero, HANDLE_MAX_COST),
        nop(),

        # If percentage is 0, set cost to 0 and return (no need to handle max cost, cost will always be 0)
        bne(t0, zero, 5),
        nop(),
        addiu(v0, zero, 0),
        beq(zero, zero, END),
        nop(),

        # Initialize quotient
        addiu(t1, zero, 0),

        # Loop 1 (get quotient)
        beq(v0, zero, 5), # If cost is 0, branch to next loop
        nop(),
        addiu(t1, t1, 1), # Increment divisor
        beq(zero, zero, -3), # Return to top of loop
        addiu(v0, v0, -0x64), # ...after subtracting 100 from part cost

        # At this point, v0 will be 0 (all part costs are divisible by 100 in Road Trip)

        # Initialize t2, this will be our addition count
        addiu(t2, zero, 0), 

        # Loop 2 (get modified cost)
        beq(t2, t0, 5), # If the addition count is equal to the cost modifier percentage, we have our new cost, branch to the end
        nop(),
        addiu(t2, t2, 1), # Increment addition count
        beq(zero, zero, -3), # Return to the top of the loop
        addu(v0, v0, t1), # ...after adding division quotient to cost

        label(HANDLE_MAX_COST),
        # Load maximum cost into t0
        lui(t0, get_upper_nibble(Addresses.ADDR_AP_PART_COST_MAXIMUM)),
        ori(t0, t0, get_lower_nibble(Addresses.ADDR_AP_PART_COST_MAXIMUM)),
        lw(t0, 0, t0),
        nop(),

        # If the maximum part cost is less than the cost of the part at this point (i.e. after the multiplier has been applied), set the part cost to the max
        sltu(t3, t0, v0), # Must be sltu, not slt, since 0xFFFFFFFF would be considered negative if signed
        beq(t3, zero, END),
        nop(),
        addu(v0, zero, t0),

        # Return v0
        label(END),
        jr(ra),
        nop()
    ]))

def modify_key_descriptions(pine : Pine, area_unlock_mode : int):
    """
    If in Decorations mode, modify the in-game descriptions of items that are used as area unlock keys
    so that they note which town they unlock.
    """
    if area_unlock_mode != 0: # i.e. not Decorations mode
        return
    
    # "Area unlock key for\n" string
    new_description_part_1 = bytes([0x41, 0x72, 0x65, 0x61, 0x20, 0x75, 0x6E, 0x6C, 0x6F, 0x63, 0x6B, 0x20, 0x6B, 0x65, 0x79, 0x20, 0x66, 0x6F, 0x72, 0x0A])
    key_descriptions = {
        'peach_town': {
            'pointer_addresses': [0x2F0864, 0x2F086C],
            #'addresses': [0x2F0F98, 0x2F0F68], # Local Peach Wine, Peach Doll
            'new_address': 0x2F0F98,
            'new_description': bytes([
                # "Peach Town" + 0x00
                0x50, 0x65, 0x61, 0x63, 0x68, 0x20, 0x54, 0x6F, 0x77, 0x6E, 0x00
            ])
        },
        'fuji_city': {
            'pointer_addresses': [0x2F0874, 0x2F087C],
            #'addresses': [0x2F0F38, 0x2F0EF8], # Gold Ornament, Policeman's Club
            'new_address': 0x2F0F38,
            'new_description': bytes([
                # 'Fuji City" + 0x00
                0x46, 0x75, 0x6A, 0x69, 0x20, 0x43, 0x69, 0x74, 0x79, 0x00
            ])
        },
        'sandpolis': {
            'pointer_addresses': [0x2F0884, 0x2F088C],
            #'addresses': [0x2F0EB8, 0x2F0EA8], # Mini-Tower, Toy Gun
            'new_address': 0x2F0EB8,
            'new_description': bytes([
                # "Sandpolis" + 0x00
                0x53, 0x61, 0x6E, 0x64, 0x70, 0x6F, 0x6C, 0x69, 0x73, 0x00
            ])
        },
        'chestnut_canyon': {
            'pointer_addresses': [0x2F0894, 0x2F089C],
            #'addresses': [0x2F0E68, 0x2F0E30], # M. Carton's Painting, Model Train
            'new_address': 0x2F0E68,
            'new_description': bytes([
                # "Chestnut Canyon" + 0x00
                0x43, 0x68, 0x65, 0x73, 0x74, 0x6E, 0x75, 0x74, 0x20, 0x43, 0x61, 0x6E, 0x79, 0x6F, 0x6E, 0x00
            ])
        },
        'mushroom_road': {
            'pointer_addresses': [0x2F081C, 0x2F0824],
            #'addresses': [0x2F11D0, 0x2F11A0], # Flower Pattern, Sky Pattern
            'new_address': 0x2F11D0,
            'new_description': bytes([
                # "Mushroom Road" + 0x00
                0x4D, 0x75, 0x73, 0x68, 0x72, 0x6F, 0x6F, 0x6D, 0x20, 0x52, 0x6F, 0x61, 0x64, 0x00
            ])
        },
        'white_mountain': {
            'pointer_addresses': [0x2F08A4, 0x2F085C],
            #'addresses': [0x2F0E08, 0x2F0FE0], # Christmas Tree, Arctic Pattern
            'new_address': 0x2F0FE0, # (not enough room at 0x2F0E08)
            'new_description': bytes([
                # "White Mountain" + 0x00
                0x57, 0x68, 0x69, 0x74, 0x65, 0x20, 0x4D, 0x6F, 0x75, 0x6E, 0x74, 0x61, 0x69, 0x6E, 0x00
            ])
        },
        'papaya_island': {
            'pointer_addresses': [0x2F08AC, 0x2F08B4],
            #'addresses': [0x2F0DB8, 0x2F0D88], # UnbaboDoll, Papaya Ukulele
            'new_address': 0x2F0DB8,
            'new_description': bytes([
                # "Papaya Island" + 0x00
                0x50, 0x61, 0x70, 0x61, 0x79, 0x61, 0x20, 0x49, 0x73, 0x6C, 0x61, 0x6E, 0x64, 0x00
            ])
        },
        'cloud_hill': {
            'pointer_addresses': [0x2F08BC, 0x2F08C4],
            #'addresses': [0x2F0D50, 0x2F0D10], # Angel's Wings, God's Rod
            'new_address': 0x2F0D50,
            'new_description': bytes([
                # "Cloud Hill" + 0x00
                0x43, 0x6C, 0x6F, 0x75, 0x64, 0x20, 0x48, 0x69, 0x6C, 0x6C, 0x00
            ])
        }
    }

    for town in key_descriptions.keys():
        for ptr_addr in key_descriptions[town]['pointer_addresses']:
            pine.write_bytes(ptr_addr, int_to_bytes(key_descriptions[town]['new_address'], 4))
        pine.write_bytes(key_descriptions[town]['new_address'], new_description_part_1 + key_descriptions[town]["new_description"])


def fix_vanilla_bugs(pine : Pine):
    """Patch various bugs present in the vanilla game."""
    # In vanilla RTA, if the player clears Tunnel Race on their first attempt, they will only
    #   be rewarded Body Q085, and not the Space Meter.
    # In the vanilla game, the Space Meter could still be purchased in the My City parts shop
    #   afterward, but this makes the check permanently missable in AP.
    # Change the text pointers so that winning on any attempt (first try or not) will provide
    #   both item rewards, and both stamps. (Rewarding both stamps on a later attempt is fine,
    #   since the game seems to properly handle an attempt to reward a stamp that's already been
    #   rewarded).
    pine.write_bytes(0x2A7AC0, bytes([0xd8, 0x39, 0x32]))
    pine.write_bytes(0x2A7AD8, bytes([0x20, 0x3a, 0x32]))

    # TODO: Patch curling bug

def patch_coine_behavior(pine : Pine, randomize_q_coins : bool, q_coins_needed_per_coine_reward : int):
    """
    Modify the number of coins required for each Coine reward. Also, if 'Randomize Q Coins' is
    enabled, patch Coine rewards to check the number of AP Q Coin items received instead of
    the number of Q Coins picked up in-game.
    """
    def convert_int_to_ascii_chars(num : int) -> tuple[int]:
        num_str = str(num)
        int_char_1 = ord(num_str[0])
        if len(num_str) > 1:
            int_char_2 = ord(num_str[1])
        else:
            int_char_2 = 0x20

        return int_char_1, int_char_2

    if q_coins_needed_per_coine_reward < 10:
        # The Q Coin checks use hardcoded values placed within Coine's dialogue strings to determine
        #   how many coins are needed to receive the next reward.
        coin_requirement_addresses = [
            0x322C29, # 1st check (10 coins)
            0x322b61, # 2nd check (20 coins)
            0x322ad1,
            0x322a41,
            0x3229b1,
            0x322921,
            0x322891,
            0x322801,
            0x322771,
            0x3226e1
        ]
        # Addresses for places where Coine mentions a needed coin amount (each is two bytes).
        #   2nd value in the list is for the "You have less than x" strings.
        coin_requirement_text_addresses = [
            [0x322BC8], # 10 coins
            [0x322B38, 0x322B76], # 20 coins
            [0x322AA8, 0x322AE6],
            [0x322A18, 0x322A56],
            [0x322988, 0x3229C6],
            [0x3228F8, 0x322936],
            [0x322868, 0x3228A6],
            [0x3227D8, 0x322816],
            [0x322748, 0x322786],
            [0x3226B9, 0x3226F6],
        ]
        # Address for where Coine mentions how many coins you need per reward (two bytes)
        coin_requirement_interval_text_address = 0x322D9E

        # Set new requirements
        new_amount = q_coins_needed_per_coine_reward
        for addr in coin_requirement_addresses:
            pine.write_int8(addr, new_amount)
            new_amount += q_coins_needed_per_coine_reward

        # Update Coine's text
        new_amount = q_coins_needed_per_coine_reward

        int_as_ascii = convert_int_to_ascii_chars(new_amount)
        pine.write_bytes(coin_requirement_interval_text_address, bytes([int_as_ascii[0], int_as_ascii[1], 0x20]))

        for addr_list in coin_requirement_text_addresses:
            int_as_ascii = convert_int_to_ascii_chars(new_amount)
            for addr in addr_list:
                pine.write_bytes(addr, bytes([int_as_ascii[0], int_as_ascii[1], 0x20]))
            new_amount += q_coins_needed_per_coine_reward

    if randomize_q_coins == True:
        pine.write_bytes(0x23AF38, mips([
            jal(HOOK_ADDR_COINE_PATCH_FOR_Q_COIN_RANDO)
        ]))

        pine.write_bytes(HOOK_ADDR_COINE_PATCH_FOR_Q_COIN_RANDO, mips([
            lui(t0, get_upper_nibble(Addresses.ap_q_coins_received.address)),
            ori(t0, t0, get_lower_nibble(Addresses.ap_q_coins_received.address)),
            lbu(t0, 0, t0),
            addiu(t1, zero, 0x64),
            subu(v0, t1, t0),
            jr(ra),
            nop()
        ]))

        # Patch Coin count display in the pause menu
        pine.write_bytes(0x2165BC, mips([
            jal(HOOK_ADDR_COINE_PATCH_FOR_Q_COIN_RANDO)
        ]))