from .pine import Pine
from ..ram_data import Addresses

NOP_BYTES = bytes([0,0,0,0])
JAL_AP_LOCATION_FUNC_READ = bytes([0x80, 0x68, 0x0B, 0x0C]) # jal 0x2DA200 (0C0B6883)
JAL_AP_LOCATION_FUNC_WRITE = bytes([0x83, 0x68, 0x0B, 0x0C]) # jal 0x2DA20C (0C0B6880)

J_AP_LOCATION_FUNC_READ = bytes([0x80, 0x68, 0x0B, 0x08]) # j 0x2DA200 (080B6883)
J_AP_LOCATION_FUNC_WRITE = bytes([0x83, 0x68, 0x0B, 0x08]) # j 0x2DA20C (080B6880)

# ---------------------------------------------------
_patch_index = 0
def patch_rta_no_slot_data(pine : Pine, verification_run : bool = False):
    patches = [
        # Disable the email system
        # This is where we'll store our patches - but in particular, we need to clear
        #   something of this size to store all of the shop strings.
        disable_email_system,

        # AP save setup
        hook_currency_input_to_init_ap_item_index,

        # Handling AP location checks
        write_ap_location_func,
        hook_shop_purchases,
        hook_npc_rewards,
        hook_overworld_item_funcs,
        hook_license_upgrades,

        # For shop strings (this function does not require slot data)
        change_shop_item_quantity_display_to_ap,

        # Other patches
        patch_npc_equips,
        patch_tin_raceway_requirements,
        disable_func_that_overwrites_ap_save_data,
        # patch_bars_for_ap_hints(pine) # TODO
        # fix_curling_bug(pine) # TODO
    ]

    if verification_run:
        # Run only one patch. Used for patch verification, so we're not verifying every function on every client loop.
        global _patch_index
        patches[_patch_index](pine)
        _patch_index += 1
        if _patch_index >= len(patches):
            _patch_index = 0
    else:
        # Run all patches. Standard use case (i.e. patching the game).
        for patch in patches:
            patch(pine)


def patch_rta_post_connect(pine : Pine, shop_strings : list, area_unlock_mode : int):
    # Handle shop strings
    hook_shops_to_display_ap_item_strings(pine, shop_strings)

    # Handle enforcing area access
    enforce_area_access(pine, area_unlock_mode)

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
    pine.write_bytes(0x210EE8, bytes([0x00, 0x00, 0x05, 0x24])) # addiu a1,zero,0x0 

    # Prevent blinking indicator on the minimap
    # pine.write_bytes(0x249264, NOP_BYTES) # Broken, hides the entire border around the minimap.
    pine.write_bytes(0x2492BC, NOP_BYTES) # NOPing this line instead seems to work?

    # Remove option for email from garage menu.
    pine.write_bytes(0x22CE88, NOP_BYTES)

    # Automatically increment garage menu index by one so that all menu options run the correct tasks.
    # Otherwise, the first option would still open the email inbox, even with its button removed.
    # Also, skip code that handles the email option.
    pine.write_bytes(0x22D118, bytes([0x01, 0x00, 0x63, 0x24])) # addiu v1,v1,0x1
    pine.write_bytes(0x22D11C, bytes([0x08, 0x00, 0x00, 0x10])) # beq zero,zero,0x0022D140
    pine.write_bytes(0x22D120, NOP_BYTES)


def hook_currency_input_to_init_ap_item_index(pine : Pine):
    """ 
    Hook RTA to initialize the AP index variable and get the AP save ID on new game. 
    This hook runs after currency input is complete, but before the President Forest cutscene begins.
    """
    # Overwrite jal to president Forest cutscene so we can add a hook that runs first
    pine.write_bytes(0x26d650, bytes([0x60, 0x68, 0x0B, 0x0C])) # jal 002DA110 (0C0B6844)

    addr = 0x2da180
    # Set AP index to 0x1
    pine.write_bytes(addr+0, bytes([0x01, 0x00, 0x08, 0x24])) # addiu $t0, $zero, 0x1 (24080001)
    pine.write_bytes(addr+4, bytes([0x77, 0x01, 0x09, 0x3C])) # lui $t1, 0x177 (3C090177)
    pine.write_bytes(addr+8, bytes([0xAC, 0xFD, 0x29, 0x35])) # ori $t1, $t1, 0xFDAC (3529FDAC)
    pine.write_bytes(addr+12, bytes([0x00, 0x00, 0x28, 0xA1])) # sb $t0, 0($t1) (A1280000)
    
    # Set boolean to indicate to the server that we are ready to receive the AP save index to 1 (at 0x2DA0F0)
    pine.write_bytes(addr+16, bytes([0x2D, 0x00, 0x09, 0x3C])) # lui $t1, 0x2D (3C09002D)
    pine.write_bytes(addr+20, bytes([0xF0, 0xA0, 0x29, 0x35])) # ori $t1, $t1, 0xA0F0 (3529A0F0)
    pine.write_bytes(addr+24, bytes([0x00, 0x00, 0x28, 0xA1])) # sb $t0, 0($t1) (A1280000)
    
    # Remove the default parts from the My City part shop
    # The My City part shop has several parts that are always sold there, even if you've never received them.
    #   Since My City's part shop is used exclusively for repurchasing parts you already own in AP, 
    #   these are not locations in the multiworld.
    #   Full list: HG Racing Tires, Speed MAX Engine, Wide Transmission, Spoke 7, Horse Horn, Train Horn
    pine.write_bytes(addr+28, bytes([0x00, 0x00, 0x08, 0x24])) # addiu t0,zero,0x0 (24080000)
    pine.write_bytes(addr+32, bytes([0x2d, 0x00, 0x09, 0x3c])) # lui t1,0x002D (3C09002D)
    pine.write_bytes(addr+36, bytes([0x6c, 0xc7, 0x29, 0x35])) # ori t1,t1,0xC76C (3529C76C)
    pine.write_bytes(addr+40, bytes([0x00, 0x00, 0x28, 0xa1])) # sb t0,0x0(t1) (A1280000)
    pine.write_bytes(addr+44, bytes([0x05, 0x00, 0x28, 0xa1])) # sb t0,0x5(t1) (A1280005)
    pine.write_bytes(addr+48, bytes([0x0c, 0x00, 0x28, 0xa1])) # sb t0,0xC(t1) (A128000C)
    pine.write_bytes(addr+52, bytes([0x19, 0x00, 0x28, 0xa1])) # sb t0,0x19(t1) (A1280019)
    pine.write_bytes(addr+56, bytes([0x31, 0x00, 0x28, 0xa1])) # sb t0,0x31(t1) (A1280031)
    
    # Overwrite function that handles vanilla part availability behavior for My City part shop
    #   to a jr ra (i.e. do nothing).
    # By default, all parts from part shops you have previously visited are available in My City.
    pine.write_bytes(addr+60, bytes([0xe0, 0x03, 0x08, 0x3c])) # lui t0,0x03E0 (3C0803E0)
    pine.write_bytes(addr+64, bytes([0x08, 0x00, 0x08, 0x35])) # ori t0,t0,0x8 (35080008)
    pine.write_bytes(addr+68, bytes([0x26, 0x00, 0x09, 0x3c])) # lui t1,0x0026 (3C090026)
    pine.write_bytes(addr+72, bytes([0x30, 0x7c, 0x29, 0x35])) # ori t1,t1,0x7C30 (35297C30)
    pine.write_bytes(addr+76, bytes([0x00, 0x00, 0x28, 0xAD])) # sw t0, 0(t1) (AD280000)
    pine.write_bytes(addr+80, bytes([0x04, 0x00, 0x20, 0xAD])) # sw zero, 4(t1) (AD200004)

    # Now jump to the president Forest cutscene function (don't jal, our jal into this hook already set the ra register)
    pine.write_bytes(addr+84, bytes([0xC2, 0x45, 0x08, 0x08])) # j 00211708 (080845C2)
    pine.write_bytes(addr+88, NOP_BYTES) # nop (00000000)


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
    pine.write_bytes(0x2da100, table_length_table) # Just prior to all ASM patches

    addr = 0x2da200
    # To read a bit, start here. Set t7 to 1 (checked later).
    pine.write_bytes(addr+0, bytes([0x01, 0x00, 0x0F, 0x24])) # addiu $t7, $zero, 1 
    pine.write_bytes(addr+4, bytes([0x02, 0x00, 0x00, 0x10])) # b 0x2DA210
    pine.write_bytes(addr+8, NOP_BYTES)
    # To write a bit, start here. Set t7 to 2 (checked later).
    pine.write_bytes(addr+12, bytes([0x02, 0x00, 0x0F, 0x24])) # addiu $t7, $zero, 2 

    # Main function body
    # First, if a2 is not 0, exit the function.
    # a2 appears to always be 0 when the player is receiving a part.
    pine.write_bytes(addr+16, bytes([0x2C, 0x00, 0xC0, 0x14])) # bne a2,zero,0x002DA2C4
    pine.write_bytes(addr+20, NOP_BYTES)

    # Copy the arguments to temporary registers, instead of mutating directly (they could 
    #   be needed by the vanilla function later)
    pine.write_bytes(addr+24, bytes([0x00, 0x00, 0x88, 0x24])) # addiu t0,a0,0x0
    pine.write_bytes(addr+28, bytes([0x00, 0x00, 0xAA, 0x24])) # addiu t2,a1,0x0

    # Load the address to the table length table
    pine.write_bytes(addr+32, bytes([0x2D, 0x00, 0x09, 0x3C])) # lui t1,0x002D
    pine.write_bytes(addr+36, bytes([0x00, 0xA1, 0x29, 0x35])) # ori t1,t1,0xA100

    # Loop
    # Add the part totals for each part type until we've reached this part's type.
    pine.write_bytes(addr+40, bytes([0x05, 0x00, 0x00, 0x11])) # beq t0,zero,0x002DA240
    pine.write_bytes(addr+44, bytes([0x00, 0x00, 0x2b, 0x91])) # lbu t3,0x0(t1)
    pine.write_bytes(addr+48, bytes([0x21, 0x50, 0x4b, 0x01])) # addu t2,t2,t3
    pine.write_bytes(addr+52, bytes([0x01, 0x00, 0x29, 0x25])) # addiu t1,t1,0x1
    pine.write_bytes(addr+56, bytes([0xff, 0xff, 0x08, 0x25])) # addiu t0,t0,-0x1
    pine.write_bytes(addr+60, bytes([0xfa, 0xff, 0x00, 0x10])) # beq zero,zero,0x002DA228

    # Determine whether we are currently in a shop by testing for either shop task
    #   address in ra.
    # One will be in ra during a buy, the other will be in ra while browsing.
    # If we are in the shop, set the address to check to the the AP shop purchases 
    #   bitfield. Otherwise, set it to the AP NPC items received bitfield.
    pine.write_bytes(addr+64, bytes([0x26, 0x00, 0x0B, 0x3C])) # lui t3,0x0026
    pine.write_bytes(addr+68, bytes([0xE0, 0x97, 0x6B, 0x35])) # ori t3,t3,0x97E0
    pine.write_bytes(addr+72, bytes([0x09, 0x00, 0xeb, 0x13])) # beq ra,t3,0x002DA270
    pine.write_bytes(addr+76, NOP_BYTES)
    pine.write_bytes(addr+80, bytes([0x24, 0x00, 0x0b, 0x3c])) # lui t3,0x0024
    pine.write_bytes(addr+84, bytes([0x44, 0x72, 0x6b, 0x35])) # ori t3,t3,0x7244
    pine.write_bytes(addr+88, bytes([0x05, 0x00, 0xeb, 0x13])) # beq ra,t3,0x002DA270
    pine.write_bytes(addr+92, NOP_BYTES)

    # Set table to NPC reward table
    pine.write_bytes(addr+96, bytes([0x78, 0x01, 0x09, 0x3C])) # lui t1,0x0178
    pine.write_bytes(addr+100, bytes([0x00, 0x2A, 0x29, 0x25])) # addiu t1,t1,0x2A00
    pine.write_bytes(addr+104, bytes([0x03, 0x00, 0x00, 0x10])) # beq zero,zero,0x002DA278
    pine.write_bytes(addr+108, NOP_BYTES)

    # Set table to shop purchases table
    pine.write_bytes(addr+112, bytes([0x78, 0x01, 0x09, 0x3C])) # lui t1,0x0178
    pine.write_bytes(addr+116, bytes([0xD0, 0x29, 0x29, 0x25])) # addiu t1,t1,0x29D0

    # Loop
    # Continue subtracting 8 from the total item count until it would go negative.
    # This is to determine which *byte* contains our bit (since 8 bits are in a byte).
    pine.write_bytes(addr+120, bytes([0xF8, 0xFF, 0x4B, 0x25])) # addiu t3,t2,-0x8
    pine.write_bytes(addr+124, bytes([0x05, 0x00, 0x60, 0x05])) # bltz t3,0x0031F094
    pine.write_bytes(addr+128, NOP_BYTES)
    pine.write_bytes(addr+132, bytes([0xF8, 0xFF, 0x4A, 0x25])) # addiu t2,t2,-0x8
    pine.write_bytes(addr+136, bytes([0x01, 0x00, 0x29, 0x25])) # addiu t1,t1,0x1
    pine.write_bytes(addr+140, bytes([0xFA, 0xFF, 0x00, 0x10])) # beq zero,zero,0x0031F088
    pine.write_bytes(addr+144, NOP_BYTES)

    # Load the byte, and prepare t2 to contain a 1 in the bit we want to read/write, and
    #   0 in all other bits (i.e. create a bit mask)
    pine.write_bytes(addr+148, bytes([0x00, 0x00, 0x28, 0x91])) # lbu t0,0x0(t1)
    pine.write_bytes(addr+152, bytes([0x01, 0x00, 0x0B, 0x24])) # addiu t3,zero,0x1
    pine.write_bytes(addr+156, bytes([0x04, 0x50, 0x4B, 0x01])) # sllv t2,t3,t2

    # If t7 (read/write enum) is 1, branch to TABLE READ
    pine.write_bytes(addr+160, bytes([0x02, 0x00, 0xEF, 0x29])) # slti t7, t7, 0x2
    pine.write_bytes(addr+164, bytes([0x04, 0x00, 0xE0, 0x15])) # bne t7, zero, 0x0031F0C8
    pine.write_bytes(addr+168, NOP_BYTES)

    # TABLE WRITE
    pine.write_bytes(addr+172, bytes([0x25, 0x40, 0x0A, 0x01])) # or t0,t0,t2
    pine.write_bytes(addr+176, bytes([0x00, 0x00, 0x28, 0xA1])) # sb t0,0x0(t1)
    pine.write_bytes(addr+180, bytes([0x08, 0x00, 0xE0, 0x03])) # jr ra

    # TABLE READ
    pine.write_bytes(addr+184, bytes([0x24, 0x40, 0x0A, 0x01])) # and t0, t0, t2
    pine.write_bytes(addr+188, bytes([0x01, 0x00, 0x02, 0x29])) # slti v0, t0, 1
    pine.write_bytes(addr+192, bytes([0x01, 0x00, 0x42, 0x38])) # xori v0, v0, 0x1
    pine.write_bytes(addr+196, bytes([0x08, 0x00, 0xE0, 0x03])) # jr ra
    pine.write_bytes(addr+200, NOP_BYTES)


def hook_shop_purchases(pine : Pine):
    """
    Convert shop purchases to AP locations, instead of giving the player the item purchased - *except* in My City.
    My City's part shop does not contain any locations, and is used exclusively for repurchasing parts you've
    already obtained.
    """
    # At 0x2697d8, change the ASM instruction (which is currently a jump-and-link to the function that handles
    #   updating your inventory) to a jal to our new hook.
    pine.write_bytes(0x2697D8, bytes([0xE0, 0x68, 0x0B, 0x0C])) # jal 002DA380
    
    # In our hook, test if the current region index is 9 (My City).
    #   If it's not, run our AP location check function (defined above).
    #   If it is, jump (not jal) to the normal shop function that updates your inventory.
    addr = 0x2DA380
    pine.write_bytes(addr+0, bytes([0x33, 0x00, 0x08, 0x3C])) # lui t0, 0x0033
    pine.write_bytes(addr+4, bytes([0x23, 0x59, 0x08, 0x25])) # addiu t0, t0, 0x5923
    pine.write_bytes(addr+8, bytes([0x00, 0x00, 0x08, 0x81])) # lb t0, 0x0(t0)
    pine.write_bytes(addr+12, bytes([0x09, 0x00, 0x09, 0x24])) # addiu t1, zero, 0x9
    pine.write_bytes(addr+16, bytes([0x03, 0x00, 0x09, 0x15])) # bne t0, t1, 0x2DA3A0
    pine.write_bytes(addr+20, NOP_BYTES)
    pine.write_bytes(addr+24, bytes([0xB0, 0xF4, 0x08, 0x08])) # j 0x23D2C0
    pine.write_bytes(addr+28, NOP_BYTES)
    pine.write_bytes(addr+32, J_AP_LOCATION_FUNC_WRITE) # j 0x2DA20C
    pine.write_bytes(addr+36, NOP_BYTES)


def hook_npc_rewards(pine : Pine):
    """
    Convert NPC rewards to AP locations, instead of the vanilla behavior of giving the player an item. 
    Also sets the name of the received item to 'AP Item', instead of the vanilla name.
    """
    # Overwrite the call to the normal 'set inventory' function with our AP location function.
    pine.write_bytes(0x23A0B4, JAL_AP_LOCATION_FUNC_WRITE)

    # Set all NPC reward item names to 'AP Item'
    # 1. Hook the JAL that would normally get the pointer to the reward's name.
    pine.write_bytes(0x239fe4, bytes([0x00, 0x69, 0x0b, 0x0c])) # jal 0x002DA400

    # 2. In our hook, instead return the address to our new "AP Item" string.
    addr = 0x2DA400
    pine.write_bytes(addr+0, bytes([0x2d, 0x00, 0x02, 0x3c])) # lui v0,0x002D
    pine.write_bytes(addr+4, bytes([0x10, 0xa6, 0x42, 0x34])) # ori v0,v0,0xA610
    pine.write_bytes(addr+8, bytes([0x08, 0x00, 0xe0, 0x03])) # jr ra
    pine.write_bytes(addr+12, NOP_BYTES)

    # 3. Write the 'AP Item' string.
    pine.write_bytes(0x2DA610, bytes([0x41, 0x50, 0x20, 0x49]))
    pine.write_bytes(0x2DA614, bytes([0x74, 0x65, 0x6d, 0x00]))

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
        pine.write_bytes(address, JAL_AP_LOCATION_FUNC_WRITE)

    # Also modify these functions to prevent overworld items from disappearing when we add that item to our
    #    inventory. (Road Trip uses the status of the item in your inventory to determine whether it should
    #    appear in the overworld.)
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
        pine.write_bytes(address, JAL_AP_LOCATION_FUNC_READ)


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
    #    2. When saving a license update, update the AP license location bitfield instead of incrementing
    #       the actual license count owned by the player.

    # --------------------------------------

    # PART 1 - Modifying the license upgrade check
    
    # The function starting at 0x237508 (NTSC) handles determining whether all of the races that match
    #   the rank of the race just completed are now complete.
    #
    # Here we call our hook to get license upgrades to check against the AP license location bitfield,
    #   instead of the licenses in your inventory.
    pine.write_bytes(0x23757C, bytes([0x20, 0x69, 0x0B, 0x0C])) # jal 0x002DA480

    # Hook 1
    addr = 0x2DA480
    # Road Trip has a table containing (among other things) the corresponding rank for each race. 
    # a2 contains a pointer to the entry in that table for this race. Byte 3 contains the race rank.
    # This instruction loads that byte.
    pine.write_bytes(addr+0, bytes([0x03, 0x00, 0xc7, 0x80])) # lb a3, 0x3(a2)

    # Convert rank int to a bitfield index.
    pine.write_bytes(addr+4, bytes([0x01, 0x00, 0x0f, 0x24])) # addiu $t7, $zero, 1
    pine.write_bytes(addr+8, bytes([0x04, 0x78, 0xef, 0x00])) # sllv $t7, $t7, $a3     

    # Load AP license location bitfield
    pine.write_bytes(addr+12, bytes([0x78, 0x01, 0x0e, 0x3c])) # lui $t6, 0x178
    pine.write_bytes(addr+16, bytes([0x30, 0x2a, 0xce, 0x25])) # addiu $t6, $t6, 0x2A30
    pine.write_bytes(addr+20, bytes([0x00, 0x00, 0xce, 0x81])) # lb $t6, 0($t6)

    # Bitwise and. Result is 0 if we haven't completed this license location yet, not 0 if we have.
    pine.write_bytes(addr+24, bytes([0x24, 0x70, 0xcf, 0x01])) # and $t6, $t6, $t7  

    # If 0, return. Setting a3 to the current race rank on line 1 has already tricked the game 
    #   into thinking our current license matches this race, so the remaining check logic should work
    #   (i.e. for the 'you earned a license' text).
    pine.write_bytes(addr+28, bytes([0x02, 0x00, 0xc0, 0x11])) # beq $t6, $zero, 0x2ea210 
    pine.write_bytes(addr+32, NOP_BYTES)
    # Otherwise, if 1, set a3 to 3 instead. This will cause the function to assume we have all licenses 
    #    already, and it will not check for any license rank completions.
    pine.write_bytes(addr+36, bytes([0x03, 0x00, 0x07, 0x24])) # addiu $a3, $zero, 3      
    pine.write_bytes(addr+40, bytes([0x08, 0x00, 0xe0, 0x03])) # jr ra
    pine.write_bytes(addr+44, NOP_BYTES)

    # ---------------------------------

    # PART 2 - Modifying the function that updates your license count to update the AP license bitfield instead.
    
    # Overwrite existing lines that handle updating license byte in the 'handleRaceResults' function.
    pine.write_bytes(0x2366FC, bytes([0x40, 0x69, 0x0B, 0x0C])) # jal 0x002DA500
    pine.write_bytes(0x236700, NOP_BYTES)
    pine.write_bytes(0x236704, NOP_BYTES)

    # Hook 2 - Updates our AP location byte for license checks
    addr = 0x2DA500
    pine.write_bytes(addr+0, bytes([0x08, 0x00, 0x60, 0x10])) # beq v1,zero,0x002EA1AC   # Skip if no license bit to update
    pine.write_bytes(addr+4, bytes([0x01, 0x00, 0x02, 0x24])) # addiu v0,zero,0x1        # Init license bit slot to 1
    pine.write_bytes(addr+8, bytes([0xFF, 0xFF, 0x63, 0x24])) # addiu v1,v1,-0x1         # Number of left shifts to apply to 1 
    pine.write_bytes(addr+12, bytes([0x04, 0x18, 0x62, 0x00])) # sllv v1,v0,v1           # Apply shift. Result is the bit that corresponds to this license.
    pine.write_bytes(addr+16, bytes([0x78, 0x01, 0x02, 0x3C])) # lui v0, 0x0178
    pine.write_bytes(addr+20, bytes([0x30, 0x2A, 0x42, 0x24])) # addiu v0, v0, 0x2A30
    pine.write_bytes(addr+24, bytes([0x00, 0x00, 0x4F, 0x80])) # lb t7, 0(v0)            # Load current AP license bitfield
    pine.write_bytes(addr+28, bytes([0x25, 0x18, 0x6F, 0x00])) # or v1, v1, t7 
    pine.write_bytes(addr+32, bytes([0x00, 0x00, 0x43, 0xA0])) # sb v1, 0(v0)            # Store updated AP license bitfield
    pine.write_bytes(addr+36, bytes([0x08, 0x00, 0xE0, 0x03])) # jr ra
    pine.write_bytes(addr+40, NOP_BYTES)

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
    pine.write_bytes(0x24723c, bytes([0x00, 0x6b, 0x0b, 0x0c])) # jal 0x2DAC00

    # Change the check at this location to jump to our hook, which will prevent the game from displaying 
    #     "You have #" in part shops (except My City), and always display "You [don't] have it" instead.
    #     ("You have #" would not make sense for AP location checks.)
    pine.write_bytes(0x247284, NOP_BYTES)
    pine.write_bytes(0x247288, bytes([0x20, 0x6b, 0x0b, 0x08])) # jal 0x2DAC80

    # Is this the My City part shop? If so, jump to the normal function. 
    # Otherwise, call the AP location check function
    addr = 0x2DAC00
    pine.write_bytes(addr+0, bytes([0x33, 0x00, 0x08, 0x3c])) # lui t0,0x0033
    pine.write_bytes(addr+4, bytes([0x21, 0x59, 0x08, 0x35])) # ori t0,t0,0x5921
    pine.write_bytes(addr+8, bytes([0x00, 0x00, 0x09, 0x91])) # lbu t1,0x0(t0)
    pine.write_bytes(addr+12, bytes([0x01, 0x00, 0x0a, 0x24])) # addiu t2,zero,0x1
    pine.write_bytes(addr+16, bytes([0x06, 0x00, 0x2a, 0x15])) # bne t1,t2,0x2DABAC
    pine.write_bytes(addr+20, bytes([0x02, 0x00, 0x09, 0x91])) # lbu t1,0x2(t0)
    pine.write_bytes(addr+24, bytes([0x09, 0x00, 0x0a, 0x24])) # addiu t2,zero,0x9
    pine.write_bytes(addr+28, bytes([0x03, 0x00, 0x2a, 0x15])) # bne t1,t2,0x2DABAC
    pine.write_bytes(addr+32, NOP_BYTES)
    pine.write_bytes(addr+36, bytes([0x22, 0xf5, 0x08, 0x08])) # j 0x23d488  
    pine.write_bytes(addr+40, NOP_BYTES)
    pine.write_bytes(addr+44, J_AP_LOCATION_FUNC_READ) # j 0x2DA200
    pine.write_bytes(addr+48, NOP_BYTES)

    addr = 0x2DAC80
    # If this is not the My City part shop, jump to the part of the calling function that makes the
    #     displayed text "You have it" or "You don't have it".
    #     Otherwise, jump to the part that could make it "You have #".
    pine.write_bytes(addr+0, bytes([0x33, 0x00, 0x08, 0x3c])) # lui t0,0x0033
    pine.write_bytes(addr+4, bytes([0x21, 0x59, 0x08, 0x35])) # ori t0,t0,0x5921
    pine.write_bytes(addr+8, bytes([0x00, 0x00, 0x09, 0x91])) # lbu t1,0x0(t0)
    pine.write_bytes(addr+12, bytes([0x01, 0x00, 0x0a, 0x24])) # addiu t2,zero,0x1
    pine.write_bytes(addr+16, bytes([0x08, 0x00, 0x2a, 0x15])) # bne t1,t2,0x2DACB4
    pine.write_bytes(addr+20, bytes([0x02, 0x00, 0x09, 0x91])) # lbu t1,0x2(t0)
    pine.write_bytes(addr+24, bytes([0x09, 0x00, 0x0a, 0x24])) # addiu t2,zero,0x9
    pine.write_bytes(addr+28, bytes([0x05, 0x00, 0x2a, 0x15])) # bne t1,t2,0x2DACB4
    pine.write_bytes(addr+32, bytes([0x75, 0x01, 0x08, 0x3c])) # lui t0, 0175
    pine.write_bytes(addr+36, bytes([0x88, 0x7b, 0x08, 0x35])) # ori, t0, t0, 7b88
    pine.write_bytes(addr+40, bytes([0x00, 0x00, 0x03, 0x8d])) # lw v1, 0(t0)
    pine.write_bytes(addr+44, bytes([0xac, 0x1c, 0x09, 0x08])) # j 0x2472b0 # If My City part shop
    pine.write_bytes(addr+48, NOP_BYTES)
    pine.write_bytes(addr+52, bytes([0xa3, 0x1c, 0x09, 0x08])) # j 0x24728c # If not My City part shop
    pine.write_bytes(addr+56, NOP_BYTES)


def patch_npc_equips(pine : Pine):
    """
    Prevent NPCs from equipping parts to the player (which could allow them to, at least temporarily, have parts
    when they shouldn't in AP).
    """
    # Write hook in dialogue handler function that only allows your equipped items to be modified
    #   if you are in the Ski Jump lobby (since it should still remove the Flight Wing).
    # All other NPC equips should be disabled. (e.g. Billboards, Wing Set + Propeller)
    pine.write_bytes(0x23B984, bytes([0xe0, 0x6a, 0x0b, 0x0c]))

    addr = 0x2DAB80
    pine.write_bytes(addr+0, bytes([0x33, 0x00, 0x08, 0x3c])) # lui t0,0x0033
    pine.write_bytes(addr+4, bytes([0x21, 0x59, 0x08, 0x35])) # ori t0,t0,0x5921
    pine.write_bytes(addr+8, bytes([0x00, 0x00, 0x09, 0x91])) # lbu t1,0x0(t0)
    pine.write_bytes(addr+12, bytes([0x07, 0x00, 0x0a, 0x24])) # addiu t2,zero,0x7
    pine.write_bytes(addr+16, bytes([0x06, 0x00, 0x2a, 0x15])) # bne t1,t2,0x002DABAC
    pine.write_bytes(addr+20, bytes([0x02, 0x00, 0x09, 0x91])) # lbu t1,0x2(t0)
    pine.write_bytes(addr+24, bytes([0x06, 0x00, 0x0a, 0x24])) # addiu t2,zero,0x6
    pine.write_bytes(addr+28, bytes([0x03, 0x00, 0x2a, 0x15])) # bne t1,t2,0x002DABAC
    pine.write_bytes(addr+32, NOP_BYTES)
    pine.write_bytes(addr+36, bytes([0x06, 0xf1, 0x08, 0x08])) # j z_un_0023c418
    pine.write_bytes(addr+40, NOP_BYTES)
    pine.write_bytes(addr+44, bytes([0x08, 0x00, 0xe0, 0x03])) # jr ra
    pine.write_bytes(addr+48, NOP_BYTES)


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
    pine.write_bytes(0x23daf4, bytes([0x08, 0x00, 0xe0, 0x03])) # jr ra (instead of a j to the offending function)

def encode_as_ascii_code_list(string : str) -> list[int]:
    codes = []
    for char in string:
        try:
            codes.append(list(char.encode('ascii'))[0])
        # If a character is not a valid ASCII character, fall back to a space.
        except Exception:
            codes.append(20) # 20 is a space in ASCII
    
    return codes

def hook_shops_to_display_ap_item_strings(pine : Pine, shop_strings : list):
    """
    Write the AP part shop descriptions (item name, player, classification) into the now-unused email text data.
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
                temp = Addresses.ADDR_PART_SHOP_ITEM_CLASSIFICATIONS
            case ItemClassification.useful:
                temp = Addresses.ADDR_PART_SHOP_ITEM_CLASSIFICATIONS + 0x10
            case ItemClassification.filler:
                temp = Addresses.ADDR_PART_SHOP_ITEM_CLASSIFICATIONS + 0x18
            case ItemClassification.trap:
                temp = Addresses.ADDR_PART_SHOP_ITEM_CLASSIFICATIONS + 0x20
            case _:
                temp = Addresses.ADDR_PART_SHOP_ITEM_CLASSIFICATIONS + 0x28
        
        item_classification_addr = list(temp.to_bytes(4))
        item_classification_addr.reverse()
        item_classification_addr = bytes(item_classification_addr)

        pine.write_bytes(addr, item_name_bytes)
        pine.write_bytes(addr+Addresses.OFFSET_SHOP_STRING_PLAYER_NAME, player_bytes)
        pine.write_bytes(addr+Addresses.OFFSET_SHOP_STRING_ITEM_CLASSIFICATION_PTR, item_classification_addr)
        
    # 'Progression' string
    pine.write_bytes(0x2DA650, bytes([0x20, 0x50, 0x72, 0x6f]))
    pine.write_bytes(0x2DA654, bytes([0x67, 0x72, 0x65, 0x73]))
    pine.write_bytes(0x2DA658, bytes([0x73, 0x69, 0x6f, 0x6e]))
    pine.write_bytes(0x2DA65C, bytes([0x00, 0x00, 0x00, 0x00]))

    # 'Useful' string
    pine.write_bytes(0x2DA660, bytes([0x20, 0x55, 0x73, 0x65]))
    pine.write_bytes(0x2DA664, bytes([0x66, 0x75, 0x6c, 0x00]))

    # 'Filler' string
    pine.write_bytes(0x2DA668, bytes([0x20, 0x46, 0x69, 0x6c]))
    pine.write_bytes(0x2DA66C, bytes([0x6c, 0x65, 0x72, 0x00]))

    # 'Trap' string
    pine.write_bytes(0x2DA670, bytes([0x20, 0x54, 0x72, 0x61]))
    pine.write_bytes(0x2DA674, bytes([0x70, 0x00, 0x00, 0x00]))

    # 'Other' string
    pine.write_bytes(0x2DA678, bytes([0x20, 0x4f, 0x74, 0x68]))
    pine.write_bytes(0x2DA67C, bytes([0x65, 0x72, 0x00, 0x00]))

    # ------------------------------------------

    # Change JAL in func that handles the final buy confirmation to our hook.
    # This will change it to display the full AP item name.
    pine.write_bytes(0x268910, bytes([0x60, 0x6a, 0x0b, 0x0c])) # jal 0x002DA980

    # Change JAL that would get the address of the vanilla parts description to our hook
    pine.write_bytes(0x22e9c4, bytes([0x63, 0x6a, 0x0b, 0x0c])) # jal 0x002DA98C

    # Write the hook to replace the part descriptions in stores with AP item data
    addr = 0x2DA980
    # Start here if we want the full part name (set t0 to 1, checked later)
    # This would likely give us too many characters to fit in the part description box,
    #   but is important for the final buy confirmation so the player can see the full
    #   item name somewhere.
    pine.write_bytes(addr+0, bytes([0x01, 0x00, 0x08, 0x24])) # addiu t0,zero,0x1
    pine.write_bytes(addr+4, bytes([0x02, 0x00, 0x00, 0x10])) # beq zero,zero,0x002DA990
    pine.write_bytes(addr+8, NOP_BYTES)

    # Otherwise, start here for a truncated version of the item name (set t0 to 0, checked later)
    pine.write_bytes(addr+12, bytes([0x00, 0x00, 0x08, 0x24])) # addiu t0,zero,0x0

    # Check if we are in a part shop. If not, return.
    # (We don't want to modify part descriptions when in other places - for example,
    #   while changing our parts in a Q's Factory.)
    #
    # Load shop type value
    pine.write_bytes(addr+16, bytes([0x75, 0x01, 0x0f, 0x3c])) # lui t7,0x0175
    pine.write_bytes(addr+20, bytes([0x88, 0x7b, 0xef, 0x35])) # ori t7,t7,0x7B88
    pine.write_bytes(addr+24, bytes([0x00, 0x00, 0xef, 0x81])) # lb t7,0x0(t7)
    pine.write_bytes(addr+28, bytes([0x01, 0x00, 0x0e, 0x24])) # addiu t6,zero,0x1

    # Check if shop type value is one, else return
    pine.write_bytes(addr+32, bytes([0x03, 0x00, 0xee, 0x11])) # beq t7,t6,0x002DA9B0
    pine.write_bytes(addr+36, NOP_BYTES)
    pine.write_bytes(addr+40, bytes([0xa7, 0x6a, 0x0b, 0x08])) # j 002DAA9C # JUMP TO 'PASSTHROUGH' BELOW
    pine.write_bytes(addr+44, NOP_BYTES)

    # Check if this is the My City part shop. If so, return
    pine.write_bytes(addr+48, bytes([0x09, 0x00, 0x0f, 0x24])) # addiu t7,zero,0x9
    pine.write_bytes(addr+52, bytes([0x33, 0x00, 0x0e, 0x3c])) # lui t6,0x0033
    pine.write_bytes(addr+56, bytes([0x23, 0x59, 0xce, 0x35])) # ori t6,t6,0x5923
    pine.write_bytes(addr+60, bytes([0x00, 0x00, 0xce, 0x91])) # lbu t6,0x0(t6)
    pine.write_bytes(addr+64, bytes([0x03, 0x00, 0xee, 0x15])) # bne t7,t6,0x002DA9D0
    pine.write_bytes(addr+68, NOP_BYTES)
    pine.write_bytes(addr+72, bytes([0xa7, 0x6a, 0x0b, 0x08])) # j 002DAA9C # JUMP TO 'PASSTHROUGH' BELOW
    pine.write_bytes(addr+76, NOP_BYTES)

    # Init t5 and t6
    pine.write_bytes(addr+80, bytes([0x00, 0x00, 0x0d, 0x24])) # addiu t5,zero,0x0
    pine.write_bytes(addr+84, bytes([0x00, 0x00, 0x0e, 0x24])) # addiu t6,zero,0x0

    # Load address to table_length_table
    pine.write_bytes(addr+88, bytes([0x2D, 0x00, 0x0f, 0x3c])) # lui t7,0x002D
    pine.write_bytes(addr+92, bytes([0x00, 0xa1, 0xef, 0x35])) # ori t7,t7,0xA100

    # Iterate through table_length_table and add part counts of all prior part types
    pine.write_bytes(addr+96, bytes([0x05, 0x00, 0x80, 0x10])) # beq a0,zero,0x002DA9D8
    pine.write_bytes(addr+100, bytes([0xff, 0xff, 0x84, 0x24])) # addiu a0,a0,-0x1
    pine.write_bytes(addr+104, bytes([0x00, 0x00, 0xed, 0x91])) # lbu t5,0x0(t7)
    pine.write_bytes(addr+108, bytes([0x21, 0x70, 0xae, 0x01])) # addu t6,t5,t6
    pine.write_bytes(addr+112, bytes([0x01, 0x00, 0xef, 0x25])) # addiu t7,t7,0x1
    pine.write_bytes(addr+116, bytes([0xfa, 0xff, 0x00, 0x10])) # beq zero,zero,0x002DA9C0
    pine.write_bytes(addr+120, NOP_BYTES)

    # Add ID of this part to the total
    pine.write_bytes(addr+124, bytes([0x21, 0x70, 0xc5, 0x01]))

    # Multiply the total by 64 (each part description is 64 bytes)
    pine.write_bytes(addr+128, bytes([0x80, 0x71, 0x0e, 0x00])) # sll t6,t6,0x06

    # Get address of part descriptions
    pine.write_bytes(addr+132, bytes([0x32, 0x00, 0x0f, 0x3c])) # lui t7,0x0032
    pine.write_bytes(addr+136, bytes([0x60, 0x94, 0xef, 0x35])) # ori t7,t7,0x9460

    # Add ID * 64 to that address to get the address of this part description
    pine.write_bytes(addr+140, bytes([0x21, 0x78, 0xee, 0x01])) # addu t7,t7,t6

    # Test if t0 is not 0. 
    #   t0 == 0 -> Get truncated name
    #   t0 == 1 -> Get full name
    # If 1, jump to 'RETURN FULL NAME' at the end (we don't need the next part).
    pine.write_bytes(addr+144, bytes([0x1F, 0x00, 0x00, 0x15])) # bne t0,zero,0x002DAA70
    pine.write_bytes(addr+148, NOP_BYTES)

    # If t0 is 0, we're trying to fill the part description box.
    # a2 stores the current line we're trying to print in the part description
    # If it's line 0, get the name of the item.
    # If it's line 1, get the name of the player that item is for.
    # If it's line 2, get the AP item classification for that item (e.g. Progression, Useful, etc.)
    
    # Test if line 0. Decrement a2 and branch if not.
    pine.write_bytes(addr+152, bytes([0x0F, 0x00, 0xc0, 0x14])) # bne a2,zero,0x002DAA38

    # Line 0 - Get truncated version of item name
    # Copy characters to the temp address location, return the address to it
    pine.write_bytes(addr+156, bytes([0xff, 0xff, 0xc6, 0x24])) # addiu a2,a2,-0x1
    pine.write_bytes(addr+160, bytes([0x2d, 0x00, 0x0e, 0x3c])) # lui t6,0x002D
    pine.write_bytes(addr+164, bytes([0x30, 0xa6, 0xce, 0x35])) # ori t6,t6,0xA630
    pine.write_bytes(addr+168, bytes([0x21, 0x10, 0x0e, 0x00])) # addu v0,zero,t6
    pine.write_bytes(addr+172, bytes([0x12, 0x00, 0x0c, 0x24])) # addiu t4,zero,0x12 # Max character count is 18 (19 total when null terminator added)

    # Loop. Break if char in t5 is null terminator, or if we hit the max character count
    # (i.e. t4 == 0). Otherwise, copy char and increment.
    pine.write_bytes(addr+176, bytes([0x00, 0x00, 0xed, 0x91])) # lbu t5,0x0(t7)
    pine.write_bytes(addr+180, bytes([0x00, 0x00, 0xcd, 0xa1])) # sb t5,0x0(t6)
    pine.write_bytes(addr+184, bytes([0x16, 0x00, 0xa0, 0x11])) # beq t5,zero,0x002DAA74
    pine.write_bytes(addr+188, bytes([0x01, 0x00, 0xc0, 0xa1])) # sb zero,0x1(t6) # Write null terminator in following char - will get overwritten if we aren't done looping, otherwise sets null terminator
    pine.write_bytes(addr+192, bytes([0x01, 0x00, 0xef, 0x25])) # addiu t7,t7,0x1
    pine.write_bytes(addr+196, bytes([0x01, 0x00, 0xce, 0x25])) # addiu t6,t6,0x1
    pine.write_bytes(addr+200, bytes([0x12, 0x00, 0x80, 0x11])) # beq t4,zero,0x002DAA74
    pine.write_bytes(addr+204, NOP_BYTES)
    pine.write_bytes(addr+208, bytes([0xf7, 0xff, 0x00, 0x10])) # beq zero,zero,0x002DAA10
    pine.write_bytes(addr+212, bytes([0xFF, 0xFF, 0x8C, 0x25])) # addiu t4,t4,-0x1

    # Test if line 1. Decrement a2 and branch if not.
    pine.write_bytes(addr+216, bytes([0x04, 0x00, 0xc0, 0x14])) # bne a2,zero,0x002DAA4C
    pine.write_bytes(addr+220, bytes([0xff, 0xff, 0xc6, 0x24])) # addiu a2,a2,-0x1

    # Line 1 - Get name of player this item is for
    pine.write_bytes(addr+224, bytes([0x2a, 0x00, 0xe2, 0x25])) # addiu v0,t7,0x2A (add offset to part description address)
    pine.write_bytes(addr+228, bytes([0x0b, 0x00, 0x00, 0x10])) # beq zero,zero,0x002DAA74
    pine.write_bytes(addr+232, NOP_BYTES)

    # Test if line 2. Decrement a2 and branch if not.
    pine.write_bytes(addr+236, bytes([0x05, 0x00, 0xc0, 0x14])) # bne a2,zero,0x002DAA64
    pine.write_bytes(addr+240, bytes([0xff, 0xff, 0xc6, 0x24])) # addiu a2,a2,-0x1

    # Line 2 - Get the AP item classification
    pine.write_bytes(addr+244, bytes([0x3c, 0x00, 0xef, 0x25])) # addiu t7,t7,0x3C (add offset to part description address)
    pine.write_bytes(addr+248, bytes([0x00, 0x00, 0xe2, 0x8d])) # lw v0,0x0(t7)
    pine.write_bytes(addr+252, bytes([0x05, 0x00, 0x00, 0x10])) # beq zero,zero,0x002DAA74
    pine.write_bytes(addr+256, NOP_BYTES)

    # Line 3 - Return null terminator
    pine.write_bytes(addr+260, bytes([0x3f, 0x00, 0xE2, 0x25])) # addiu v0,t7,0x3F (offset of null terminator)

    # Return
    pine.write_bytes(addr+264, bytes([0x08, 0x00, 0xe0, 0x03])) # jr ra
    pine.write_bytes(addr+268, NOP_BYTES)

    # RETURN FULL NAME
    pine.write_bytes(addr+272, bytes([0x00, 0x00, 0xe2, 0x25])) # addiu v0,t7,0x0 (no offset)
    pine.write_bytes(addr+276, bytes([0x08, 0x00, 0xe0, 0x03])) # jr ra
    pine.write_bytes(addr+280, NOP_BYTES)

    # PASSTHROUGH
    # If we've jumped here, it's because we're either not in a part shop, or in the My City part shop.
    # Depending on whether this function was called for a part shop description or for the full part title displayed
    #   just before purchase, we need to now jump to different functions.
    pine.write_bytes(addr+284, bytes([0x03, 0x00, 0x00, 0x11])) # beq t0,zero,0x002DAAAC
    pine.write_bytes(addr+288, NOP_BYTES)
    pine.write_bytes(addr+292, bytes([0x1a, 0x0d, 0x09, 0x08])) # j 0x243468
    pine.write_bytes(addr+296, NOP_BYTES)
    pine.write_bytes(addr+300, bytes([0x12, 0x0e, 0x09, 0x08])) # j 0x243848
    pine.write_bytes(addr+304, NOP_BYTES)

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
    FUJI_CITY = "Fuji City"
    MUSHROOM_ROAD = "Mushroom Road"
    PEACH_TOWN = "Peach Town"
    WHITE_MOUNTAIN = "White Mountain"
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
        CHESTNUT_CANYON,NO_REGION,SANDPOLIS,FUJI_CITY,
        FUJI_CITY,NO_REGION,MY_CITY,NO_REGION,
        NO_REGION,NO_REGION,NO_REGION,NO_REGION,

        # 0x20 through 0x2F
        NO_REGION,WHITE_MOUNTAIN,NO_REGION,WHITE_MOUNTAIN,
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
                data += [0xFF, 0xFF]
            elif chunk == FUJI_CITY:
                data += [0xC, 0xD]
            elif chunk == MY_CITY:
                data += [0,0]
            elif chunk == SANDPOLIS:
                data += [0xe, 0xf]
            elif chunk == CHESTNUT_CANYON:
                data += [0x10, 0x11]
            elif chunk == MUSHROOM_ROAD:
                data += [0x1, 0x2]
            elif chunk == WHITE_MOUNTAIN:
                data += [0x9, 0x12]
            elif chunk == PAPAYA_ISLAND:
                data += [0x13, 0x14]
            elif chunk == CLOUD_HILL:
                data += [0x15, 0x16]
            else:
                raise Exception("enforce_area_access, decorations table: Invalid region?")
            
        # DECORATIONS MODE PATCH
        addr = 0x2DA680
        pine.write_bytes(addr+0, bytes([0xfc, 0xff, 0xbd, 0x27]))
        pine.write_bytes(addr+4, bytes([0x00, 0x00, 0xbf, 0xaf]))
        pine.write_bytes(addr+8, bytes([0x33, 0x00, 0x08, 0x3c]))
        pine.write_bytes(addr+12, bytes([0x54, 0x59, 0x08, 0x25]))
        pine.write_bytes(addr+16, bytes([0x00, 0x00, 0x08, 0x91]))
        pine.write_bytes(addr+20, bytes([0x2d, 0x00, 0x09, 0x3c]))
        pine.write_bytes(addr+24, bytes([0x80, 0xa5, 0x29, 0x35]))
        pine.write_bytes(addr+28, bytes([0x21, 0x48, 0x28, 0x01]))
        pine.write_bytes(addr+32, bytes([0x21, 0x48, 0x28, 0x01]))
        pine.write_bytes(addr+36, bytes([0x01, 0x00, 0x2a, 0x91]))
        pine.write_bytes(addr+40, bytes([0x00, 0x00, 0x29, 0x91]))
        pine.write_bytes(addr+44, bytes([0x25, 0x00, 0x20, 0x11]))
        pine.write_bytes(addr+48, bytes([0xff, 0x00, 0x0b, 0x34]))
        pine.write_bytes(addr+52, bytes([0x0d, 0x00, 0x2b, 0x15]))
        pine.write_bytes(addr+56, NOP_BYTES)
        pine.write_bytes(addr+60, bytes([0x77, 0x01, 0x0b, 0x3c]))
        pine.write_bytes(addr+64, bytes([0xe0, 0xac, 0x6b, 0x35]))
        pine.write_bytes(addr+68, bytes([0x02, 0x00, 0x6b, 0x95]))
        pine.write_bytes(addr+72, bytes([0xb0, 0x43, 0x6b, 0x29]))
        pine.write_bytes(addr+76, bytes([0x04, 0x00, 0x60, 0x15]))
        pine.write_bytes(addr+80, NOP_BYTES)
        pine.write_bytes(addr+84, bytes([0x2b, 0x00, 0x08, 0x24]))
        pine.write_bytes(addr+88, bytes([0xee, 0xff, 0x00, 0x10]))
        pine.write_bytes(addr+92, NOP_BYTES)
        pine.write_bytes(addr+96, bytes([0x23, 0x00, 0x08, 0x24]))
        pine.write_bytes(addr+100, bytes([0xeb, 0xff, 0x00, 0x10]))
        pine.write_bytes(addr+104, NOP_BYTES)
        pine.write_bytes(addr+108, bytes([0x2d, 0x00, 0x0b, 0x3c]))
        pine.write_bytes(addr+112, bytes([0x7f, 0xa5, 0x6b, 0x35]))
        pine.write_bytes(addr+116, bytes([0x0f, 0x00, 0x04, 0x24]))
        pine.write_bytes(addr+120, bytes([0x00, 0x00, 0x25, 0x25]))
        pine.write_bytes(addr+124, bytes([0x22, 0xf5, 0x08, 0x0c]))
        pine.write_bytes(addr+128, bytes([0x00, 0x00, 0x06, 0x24]))
        pine.write_bytes(addr+132, bytes([0x0f, 0x00, 0x40, 0x14]))
        pine.write_bytes(addr+136, bytes([0x0f, 0x00, 0x04, 0x24]))
        pine.write_bytes(addr+140, bytes([0x00, 0x00, 0x45, 0x25]))
        pine.write_bytes(addr+144, bytes([0x22, 0xf5, 0x08, 0x0c]))
        pine.write_bytes(addr+148, bytes([0x00, 0x00, 0x06, 0x24]))
        pine.write_bytes(addr+152, bytes([0x0a, 0x00, 0x40, 0x14]))
        pine.write_bytes(addr+156, NOP_BYTES)
        pine.write_bytes(addr+160, bytes([0x11, 0x00, 0x04, 0x24]))
        pine.write_bytes(addr+164, bytes([0x07, 0x00, 0x05, 0x24]))
        pine.write_bytes(addr+168, bytes([0x2d, 0x00, 0x06, 0x3c]))
        pine.write_bytes(addr+172, bytes([0x20, 0xa6, 0xc6, 0x34]))
        pine.write_bytes(addr+176, bytes([0x06, 0x00, 0x07, 0x24]))
        pine.write_bytes(addr+180, bytes([0x00, 0x00, 0xbf, 0x8f]))
        pine.write_bytes(addr+184, bytes([0x04, 0x00, 0xbd, 0x27]))
        pine.write_bytes(addr+188, bytes([0xf2, 0x0f, 0x08, 0x08]))
        pine.write_bytes(addr+192, bytes([0x00, 0x00, 0x62, 0xa1]))
        pine.write_bytes(addr+196, bytes([0x00, 0x00, 0xbf, 0x8f]))
        pine.write_bytes(addr+200, bytes([0x01, 0x00, 0x02, 0x24]))
        pine.write_bytes(addr+204, bytes([0x2d, 0x00, 0x0b, 0x3c]))
        pine.write_bytes(addr+208, bytes([0x7f, 0xa5, 0x6b, 0x35]))
        pine.write_bytes(addr+212, bytes([0x04, 0x00, 0xbd, 0x27]))
        pine.write_bytes(addr+216, bytes([0x08, 0x00, 0xe0, 0x03]))
        pine.write_bytes(addr+220, bytes([0x00, 0x00, 0x62, 0xa1]))
        pine.write_bytes(addr+224, NOP_BYTES)

    elif area_unlock_mode == 1: # Stamps       
        # For stamp mode, the table values should contain the number of AP stamp items
        #   needed to unlock access to the chunk.
        for chunk in chunks:
            if chunk == NO_REGION:
                data += [0,0]
            elif chunk == PEACH_TOWN:
                data += [0, 0]
            elif chunk == WINDMILLS:
                data += [0xFF, 0]
            elif chunk == FUJI_CITY:
                data += [5, 0]
            elif chunk == MY_CITY:
                data += [0,0]
            elif chunk == SANDPOLIS:
                data += [10, 0]
            elif chunk == CHESTNUT_CANYON:
                data += [15, 0]
            elif chunk == MUSHROOM_ROAD:
                data += [20, 0]
            elif chunk == WHITE_MOUNTAIN:
                data += [25, 0]
            elif chunk == PAPAYA_ISLAND:
                data += [30, 0]
            elif chunk == CLOUD_HILL:
                data += [35, 0]
            else:
                raise Exception("enforce_area_access, stamp table: Invalid region?")
        
        # STAMP MODE PATCH
        addr = 0x2DA680
        # Save file location for AP stamp count: 0x1782A31 (next to license checks)
        pine.write_bytes(addr+0, bytes([0xfc, 0xff, 0xbd, 0x27]))
        pine.write_bytes(addr+4, bytes([0x00, 0x00, 0xbf, 0xaf]))
        pine.write_bytes(addr+8, bytes([0x33, 0x00, 0x08, 0x3c]))
        pine.write_bytes(addr+12, bytes([0x54, 0x59, 0x08, 0x25]))
        pine.write_bytes(addr+16, bytes([0x00, 0x00, 0x08, 0x91]))
        pine.write_bytes(addr+20, bytes([0x2d, 0x00, 0x09, 0x3c]))
        pine.write_bytes(addr+24, bytes([0x80, 0xa5, 0x29, 0x35]))
        pine.write_bytes(addr+28, bytes([0x21, 0x48, 0x28, 0x01]))
        pine.write_bytes(addr+32, bytes([0x21, 0x48, 0x28, 0x01]))
        pine.write_bytes(addr+36, NOP_BYTES)
        pine.write_bytes(addr+40, bytes([0x00, 0x00, 0x29, 0x91]))
        pine.write_bytes(addr+44, bytes([0x22, 0x00, 0x20, 0x11]))
        pine.write_bytes(addr+48, NOP_BYTES)
        pine.write_bytes(addr+52, bytes([0xff, 0x00, 0x0b, 0x34]))
        pine.write_bytes(addr+56, bytes([0x0d, 0x00, 0x2b, 0x15]))
        pine.write_bytes(addr+60, NOP_BYTES)
        pine.write_bytes(addr+64, bytes([0x77, 0x01, 0x0b, 0x3c]))
        pine.write_bytes(addr+68, bytes([0xe0, 0xac, 0x6b, 0x35]))
        pine.write_bytes(addr+72, bytes([0x02, 0x00, 0x6b, 0x95]))
        pine.write_bytes(addr+76, bytes([0xb0, 0x43, 0x6b, 0x29]))
        pine.write_bytes(addr+80, bytes([0x04, 0x00, 0x60, 0x15]))
        pine.write_bytes(addr+84, NOP_BYTES)
        pine.write_bytes(addr+88, bytes([0x2b, 0x00, 0x08, 0x24]))
        pine.write_bytes(addr+92, bytes([0xed, 0xff, 0x00, 0x10]))
        pine.write_bytes(addr+96, NOP_BYTES)
        pine.write_bytes(addr+100, bytes([0x23, 0x00, 0x08, 0x24]))
        pine.write_bytes(addr+104, bytes([0xea, 0xff, 0x00, 0x10]))
        pine.write_bytes(addr+108, NOP_BYTES)
        pine.write_bytes(addr+112, bytes([0x78, 0x01, 0x0b, 0x3c]))
        pine.write_bytes(addr+116, bytes([0x31, 0x2a, 0x6b, 0x35]))
        pine.write_bytes(addr+120, bytes([0x00, 0x00, 0x6b, 0x91]))
        pine.write_bytes(addr+124, bytes([0x01, 0x00, 0x6b, 0x25]))
        pine.write_bytes(addr+128, bytes([0x2a, 0x10, 0x2b, 0x01]))
        pine.write_bytes(addr+132, bytes([0x2d, 0x00, 0x0b, 0x3c]))
        pine.write_bytes(addr+136, bytes([0x7f, 0xa5, 0x6b, 0x35]))
        pine.write_bytes(addr+140, bytes([0x0a, 0x00, 0x40, 0x14]))
        pine.write_bytes(addr+144, NOP_BYTES)
        pine.write_bytes(addr+148, bytes([0x11, 0x00, 0x04, 0x24]))
        pine.write_bytes(addr+152, bytes([0x07, 0x00, 0x05, 0x24]))
        pine.write_bytes(addr+156, bytes([0x2d, 0x00, 0x06, 0x3c]))
        pine.write_bytes(addr+160, bytes([0x20, 0xa6, 0xc6, 0x34]))
        pine.write_bytes(addr+164, bytes([0x06, 0x00, 0x07, 0x24]))
        pine.write_bytes(addr+168, bytes([0x00, 0x00, 0xbf, 0x8f]))
        pine.write_bytes(addr+172, bytes([0x04, 0x00, 0xbd, 0x27]))
        pine.write_bytes(addr+176, bytes([0xf2, 0x0f, 0x08, 0x08]))
        pine.write_bytes(addr+180, bytes([0x00, 0x00, 0x62, 0xa1]))
        pine.write_bytes(addr+184, bytes([0x00, 0x00, 0xbf, 0x8f]))
        pine.write_bytes(addr+188, bytes([0x01, 0x00, 0x02, 0x24]))
        pine.write_bytes(addr+192, bytes([0x2d, 0x00, 0x0b, 0x3c]))
        pine.write_bytes(addr+196, bytes([0x7f, 0xa5, 0x6b, 0x35]))
        pine.write_bytes(addr+200, bytes([0x04, 0x00, 0xbd, 0x27]))
        pine.write_bytes(addr+204, bytes([0x08, 0x00, 0xe0, 0x03]))
        pine.write_bytes(addr+208, bytes([0x00, 0x00, 0x62, 0xa1]))
        pine.write_bytes(addr+212, NOP_BYTES)

        # In stamp mode, display the number of AP stamp items received in the Stamps page in the Notebook
        # Part 1 - Write "AP stamps: " string
        addr = 0x2DA600
        pine.write_bytes(addr+0, bytes([0x41, 0x50, 0x20, 0x53]))
        pine.write_bytes(addr+4, bytes([0x74, 0x61, 0x6d, 0x70]))
        pine.write_bytes(addr+8, bytes([0x73, 0x3a, 0x20]))

        # Part 2 - Jump to our hook instead of returning from notebook stamps page task
        pine.write_bytes(0x265FDC, bytes([0x40, 0x6B, 0x0B, 0x08])) # j 0x2DAD00

        # Part 3 - Hook
        # Takes the AP stamp count, converts the number to a string, concatenates it to the end of
        #    our "AP stamps: " string, and then passes that string's address (+ positioning values
        #    and text color value) to RTA's print text function.
        addr = 0x2DAD00
        pine.write_bytes(addr+0, bytes([0xfc, 0xff, 0xbd, 0x27]))
        pine.write_bytes(addr+4, bytes([0x00, 0x00, 0xbf, 0xaf]))
        pine.write_bytes(addr+8, bytes([0x78, 0x01, 0x04, 0x3c]))
        pine.write_bytes(addr+12, bytes([0x31, 0x2a, 0x84, 0x34]))
        pine.write_bytes(addr+16, bytes([0x00, 0x00, 0x84, 0x90]))
        pine.write_bytes(addr+20, bytes([0x2d, 0x00, 0x06, 0x3c]))
        pine.write_bytes(addr+24, bytes([0x00, 0xa6, 0xc6, 0x34]))
        pine.write_bytes(addr+28, bytes([0x0b, 0x00, 0xc0, 0xa0]))
        pine.write_bytes(addr+32, bytes([0x60, 0x6b, 0x0b, 0x0c]))
        pine.write_bytes(addr+36, bytes([0x64, 0x00, 0x05, 0x24]))
        pine.write_bytes(addr+40, bytes([0x21, 0x20, 0x02, 0x00]))
        pine.write_bytes(addr+44, bytes([0x60, 0x6b, 0x0b, 0x0c]))
        pine.write_bytes(addr+48, bytes([0x0a, 0x00, 0x05, 0x24]))
        pine.write_bytes(addr+52, bytes([0x21, 0x20, 0x02, 0x00]))
        pine.write_bytes(addr+56, bytes([0x60, 0x6b, 0x0b, 0x0c]))
        pine.write_bytes(addr+60, bytes([0x01, 0x00, 0x05, 0x24]))
        pine.write_bytes(addr+64, bytes([0x14, 0x00, 0x04, 0x24]))
        pine.write_bytes(addr+68, bytes([0x04, 0x00, 0x05, 0x24]))
        pine.write_bytes(addr+72, bytes([0x00, 0x00, 0x07, 0x24]))
        pine.write_bytes(addr+76, bytes([0x00, 0x00, 0xbf, 0x8f]))
        pine.write_bytes(addr+80, bytes([0xf2, 0x0f, 0x08, 0x08]))
        pine.write_bytes(addr+84, bytes([0x04, 0x00, 0xbd, 0x27])) # j 00203fc8
        pine.write_bytes(addr+88, NOP_BYTES)

        # Function extracting a character from a number (sets only one char, for one digit)
        # Called by above
        # a0 - Number to print
        # a1 - Lowest possible value that contains the digit to test against (i.e to get hundreds digit, pass 100, or 0x64)
        # a2 - Address to string, we'll save the char to the end of the string and then add a null terminator after it
        addr = 0x2DAD80
        pine.write_bytes(addr+0, bytes([0x00, 0x00, 0x08, 0x24]))
        pine.write_bytes(addr+4, bytes([0x21, 0x48, 0x06, 0x00]))
        pine.write_bytes(addr+8, bytes([0x00, 0x00, 0x2a, 0x91]))
        pine.write_bytes(addr+12, bytes([0xfe, 0xff, 0x40, 0x15]))
        pine.write_bytes(addr+16, bytes([0x01, 0x00, 0x29, 0x25]))
        pine.write_bytes(addr+20, bytes([0x21, 0x50, 0x04, 0x00]))
        pine.write_bytes(addr+24, bytes([0x2b, 0x58, 0x45, 0x01]))
        pine.write_bytes(addr+28, bytes([0x04, 0x00, 0x60, 0x15]))
        pine.write_bytes(addr+32, NOP_BYTES)
        pine.write_bytes(addr+36, bytes([0x01, 0x00, 0x08, 0x25]))
        pine.write_bytes(addr+40, bytes([0xfb, 0xff, 0x00, 0x10]))
        pine.write_bytes(addr+44, bytes([0x23, 0x50, 0x45, 0x01]))
        pine.write_bytes(addr+48, bytes([0xff, 0xff, 0x29, 0x25]))
        pine.write_bytes(addr+52, bytes([0x03, 0x00, 0x00, 0x11]))
        pine.write_bytes(addr+56, NOP_BYTES)
        pine.write_bytes(addr+60, bytes([0x30, 0x00, 0x08, 0x25]))
        pine.write_bytes(addr+64, bytes([0x00, 0x00, 0x28, 0xa1]))
        pine.write_bytes(addr+68, bytes([0x01, 0x00, 0x20, 0xa1]))
        pine.write_bytes(addr+72, bytes([0x01, 0x00, 0x0c, 0x24]))
        pine.write_bytes(addr+76, bytes([0x03, 0x00, 0x85, 0x15]))
        pine.write_bytes(addr+80, NOP_BYTES)
        pine.write_bytes(addr+84, bytes([0xf9, 0xff, 0x00, 0x11]))
        pine.write_bytes(addr+88, NOP_BYTES)
        pine.write_bytes(addr+92, bytes([0x08, 0x00, 0xe0, 0x03]))
        pine.write_bytes(addr+96, bytes([0x21, 0x10, 0x0a, 0x00]))
        pine.write_bytes(addr+100, NOP_BYTES)
   

    # Write the reference table into the game's memory
    pine.write_bytes(0x2DA580, bytes(data))

    # Write 'No access!' string
    pine.write_bytes(0x2DA620, bytes([0x4e, 0x6f, 0x20, 0x61]))
    pine.write_bytes(0x2DA624, bytes([0x63, 0x63, 0x65, 0x73]))
    pine.write_bytes(0x2DA628, bytes([0x73, 0x21, 0x00, 0x00]))

    # While in the overworld, if the player doesn't have access to the chunk they're currently in,
    #   display "No access!" in the top-left of the screen.
    # This calls the big patch above every frame, which sets a boolean value that the hooks below
    #   reference to see if they should allow an action or not.
    pine.write_bytes(0x24332c, bytes([0xa0, 0x69, 0x0b, 0x08]))

    # NPCs and entrances
    pine.write_bytes(0x210EEC, bytes([0x00, 0x6a, 0x0b, 0x0c]))

    addr = 0x2DA800 # Hook
    pine.write_bytes(addr+0, bytes([0x07, 0x00, 0x40, 0x10]))
    pine.write_bytes(addr+4, bytes([0x2d, 0x00, 0x08, 0x3c]))
    pine.write_bytes(addr+8, bytes([0x7f, 0xa5, 0x08, 0x35]))
    pine.write_bytes(addr+12, bytes([0x00, 0x00, 0x08, 0x81]))
    pine.write_bytes(addr+16, bytes([0x03, 0x00, 0x00, 0x11]))
    pine.write_bytes(addr+20, NOP_BYTES)
    pine.write_bytes(addr+24, bytes([0x08, 0x00, 0xe0, 0x03]))
    pine.write_bytes(addr+28, NOP_BYTES)
    pine.write_bytes(addr+32, bytes([0x40, 0x44, 0x08, 0x08]))
    pine.write_bytes(addr+36, NOP_BYTES)

    # Q Coins
    pine.write_bytes(0x241c98, bytes([0x20, 0x6a, 0x0b, 0x0c]))
    pine.write_bytes(0x241c9c, NOP_BYTES)

    addr = 0x2DA880 # Hook
    pine.write_bytes(addr+0, bytes([0x08, 0x00, 0x02, 0x45]))
    pine.write_bytes(addr+4, NOP_BYTES)
    pine.write_bytes(addr+8, bytes([0x2d, 0x00, 0x08, 0x3c]))
    pine.write_bytes(addr+12, bytes([0x7f, 0xa5, 0x08, 0x35]))
    pine.write_bytes(addr+16, bytes([0x00, 0x00, 0x08, 0x81]))
    pine.write_bytes(addr+20, bytes([0x03, 0x00, 0x00, 0x11]))
    pine.write_bytes(addr+24, NOP_BYTES)
    pine.write_bytes(addr+28, bytes([0x08, 0x00, 0xe0, 0x03]))
    pine.write_bytes(addr+32, NOP_BYTES)
    pine.write_bytes(addr+36, bytes([0x40, 0x07, 0x09, 0x08]))
    pine.write_bytes(addr+40, NOP_BYTES)

    # Overworld items
    addr = 0x2DA900 # Hook
    pine.write_bytes(addr+0, bytes([0x00, 0x00, 0xe9, 0x27]))
    pine.write_bytes(addr+4, bytes([0x2d, 0x00, 0x08, 0x3c]))
    pine.write_bytes(addr+8, bytes([0x7f, 0xa5, 0x08, 0x35]))
    pine.write_bytes(addr+12, bytes([0x00, 0x00, 0x08, 0x81]))
    pine.write_bytes(addr+16, bytes([0x04, 0x00, 0x00, 0x15]))
    pine.write_bytes(addr+20, NOP_BYTES)
    pine.write_bytes(addr+24, bytes([0x10, 0x00, 0xff, 0x27]))
    pine.write_bytes(addr+28, bytes([0x08, 0x00, 0xe0, 0x03]))
    pine.write_bytes(addr+32, NOP_BYTES)
    pine.write_bytes(addr+36, bytes([0x94, 0x63, 0x09, 0x0c]))
    pine.write_bytes(addr+40, bytes([0x00, 0x00, 0x3f, 0x25]))
    pine.write_bytes(addr+44, NOP_BYTES)

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
        pine.write_bytes(address+8, bytes([0x40, 0x6a, 0x0b, 0x0c])) # jal 0x002DA900
