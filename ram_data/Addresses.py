"""
Contains the locations in RAM of everything we need to manage the game.

For tables and data structures, we store the starting location of the data, and the size of the data.

We also store the base IDs from the generation process. For all items and locations, the AP IDs match
the in-game IDs, just with a base value added depending on the type of item/location. 
All we need to do to figure out what item/location we're dealing with is to subtract the correct base ID
from the ID we pull from the game.
"""

from typing import NamedTuple
from enum import StrEnum
from math import ceil

from ..locations import BASE_IDS as BASE_LOCATION_IDS
from ..items import BASE_IDS as BASE_ITEM_IDS, item_name_to_base_ID, all_item_table

# Constants
# 1. Basic facts
BITS_IN_BYTE = 8
BYTES_IN_A_WORD = 4

# 2. Counts of things in-game
NUM_COURSES = 26
NUM_BODIES = 151
NUM_STAMPS = 100
NUM_COLLECTIBLES = 48
NUM_LICENSES = 3

# 3. Related to task queue
OFFSET_TASK_FUNC_PTR = 12 # At what byte in a task's data structure is the pointer to the function it runs? (Addr is 4 bytes long)
MAX_TASKS_IN_QUEUE = 48
FUNC_PTR_ADVENTURE_MODE = 0x2105B8
FUNC_PTR_MAIN_MENU = 0x20A2B0
FUNC_PTR_MAIN_MENU_ADVENTURE_MODE_SELECTED = 0x209520
FUNC_PTR_NEW_GAME = 0x26D438
FUNC_PTR_TASK_BETWEEN_NEW_GAME_AND_NAME_INPUT = 0x26D550
FUNC_PTR_NAME_INPUT = 0x26D5E0
FUNC_PTR_CURRENCY_INPUT = 0x26D628

# 4. Related to updating descriptions of parts in shops ("shop strings") to the AP items they've been randomized to
# NOTE: Beginning of email pointers: 0x2da0f0
# NOTE: Beginning of email strings (much more space): 0x329458
ADDR_TEMP_SHORTENED_PART_NAME = 0x2DA630
ADDR_AP_STAMP_STRING = 0x2DA600
ADDR_PART_SHOP_ITEM_CLASSIFICATIONS = 0x2DA650 #0x2DA110
ADDR_SHOP_STRINGS = 0x329460
OFFSET_SHOP_STRING_PLAYER_NAME = 42 # Max item name length is 41 characters + null terminator. Enforced by get_shop_strings, not Archipelago.
OFFSET_SHOP_STRING_ITEM_CLASSIFICATION_PTR = 60 # Max player name in AP is 16 characters + a space at the beginning (for positioning in-game) + the null terminator.
SHOP_STRING_LENGTH = 64
ADDR_SHOP_HOOKS = 0x2DA180 # All functions start on either byte 0x80 or 0x00 (e.g. 2DA180, then 2DA200, so on). Some intervals of 0x80 may be skipped for longer functions.

class StorageType(StrEnum):
    Word = "Word" # Money is stored in a 32-bit signed integer (yes, signed)
    Bytes = "Bytes"
    Bits = "Bits"

class TableData(NamedTuple):
    address: int
    length: int # Typically in bytes (although sometimes not, depends on storage_type). Used for PINE calls.
    storage_type: StorageType
    base_ID: int|None # None for ap_item_index

# Locations
race_results = TableData(
    address = 0x1780750,
    length = NUM_COURSES, # 26 courses in game
    storage_type = StorageType.Bytes,
    base_ID = BASE_LOCATION_IDS.RACES,
)

stamp_completions = TableData(
    address = 0x177FC78,
    length = ceil(NUM_STAMPS / BITS_IN_BYTE), # Should be 13. Technically only 12.5 bytes are used, since final 4 bits are not used (i.e. there are no Stamps 101-104)
    storage_type = StorageType.Bits,
    base_ID = BASE_LOCATION_IDS.STAMPS,
)

shop_purchases = TableData(
    address = 0x17829D0, # Seemingly unused portion of save data toward the end
    length = 32, # 256 bits. There are far fewer than 256 items that can be purchased, but we're keeping the game's part indicies as-is for simplicity, and storing based on that, so we need a lot more space.
    storage_type = StorageType.Bits,
    base_ID = BASE_LOCATION_IDS.SHOP_PURCHASES,
)

items_obtained = TableData(
    address = 0x1782A00, # Seemingly unused portion of save data toward the end
    length = 38, # 304 bits. There are far fewer than 304 items that can be obtained via NPCs (e.g. you can't obtain most parts this way), but we're keeping the game's part indicies as-is for simplicity, and storing based on that, so we need a lot more space.
    storage_type = StorageType.Bits,
    base_ID = BASE_LOCATION_IDS.ITEMS,
)

license_completions = TableData(
    address = 0x1782A30, # Seemingly unused portion of save data toward the end
    length = 1, # Each license level is a different value in one byte, this is not a bitfield.
    storage_type = StorageType.Bytes,
    base_ID = BASE_LOCATION_IDS.LICENSES,
)

# Used for stamp area access mode. Only modified by the server. 
ap_stamps_received = TableData(
    address = 0x1782A31, # Seemingly unused portion of save data toward the end
    length = 1,
    storage_type = StorageType.Bytes,
    base_ID = None,
)

# This *seems* to be a bitfield of event flags, but I haven't confirmed what else gets set here
#   other than World GP completion.
# World GP completion is the most-significant bit of 0x177FCA2 (so, if only that bit is set, the
#   byte's value is 0x80).
event_flags = TableData(
    address = 0x177FCA0,
    length = 8,
    storage_type = StorageType.Bytes,
    base_ID = BASE_LOCATION_IDS.WORLD_GP
)

# Items
inventory_bodies = TableData(
    address = 0x1780390,
    length = ceil(NUM_BODIES / BITS_IN_BYTE),
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.BODIES,
)

inventory_tires = TableData(
    address = 0x17803A4,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.TIRES,
)

inventory_engines = TableData(
    address = 0x17803B8,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.ENGINES,
)

inventory_chassis = TableData(
    address = 0x17803CC,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.CHASSIS,
)

inventory_transmission = TableData(
    address = 0x17803E0,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.TRANSMISSION,
)

inventory_steering = TableData(
    address = 0x17803F4,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.STEERING,
)

inventory_brakes = TableData(
    address = 0x1780408,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.BRAKES,
)

inventory_wheels = TableData(
    address = 0x178041C,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.WHEELS,
)

inventory_lights = TableData(
    address = 0x1780430,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.LIGHTS,
)

inventory_wing_set = TableData(
    address = 0x1780444,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.WING_SET,
)

inventory_special_parts = TableData(
    address = 0x1780458,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.SPECIAL_PARTS,
)

inventory_options = TableData(
    address = 0x178046C,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.OPTIONS,
)

inventory_sticker = TableData(
    address = 0x1780480,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.STICKER,
)

inventory_horns = TableData(
    address = 0x1780494,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.HORNS,
)

inventory_meters = TableData(
    address = 0x17804A8,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.METERS,
)

inventory_collectibles = TableData(
    address = 0x17804BC,
    length = ceil(NUM_COLLECTIBLES / BITS_IN_BYTE),
    storage_type = StorageType.Bits,
    base_ID = BASE_ITEM_IDS.COLLECTIBLES,
)

inventory_licenses = TableData(
    address = 0x177FDB1,
    length = 1, # Each license level is a different value in one byte, this is not a bitfield.
    storage_type = StorageType.Bytes,
    base_ID = BASE_ITEM_IDS.PROGRESSIVE_LICENSE,
)

inventory_money = TableData(
    address = 0x0177FDB4,
    length = BYTES_IN_A_WORD,
    storage_type = StorageType.Word,
    base_ID = BASE_ITEM_IDS.FILLER,
)

inventory_table_data = [
    inventory_bodies,
    inventory_tires,
    inventory_engines,
    inventory_chassis,
    inventory_transmission,
    inventory_steering,
    inventory_brakes,
    inventory_wheels,
    inventory_lights,
    inventory_wing_set,
    inventory_special_parts,
    inventory_options,
    inventory_sticker,
    inventory_horns,
    inventory_meters,
    inventory_collectibles,
    inventory_licenses,
    inventory_money,
]

def get_table_data_for_part(item_name : str) -> TableData:
    # For the decoration key items, remove "key" from the string
    # These are stored in the same location in-game as the non-key versions
    item_name = item_name.replace(" (Key)", "")

    item_base_ID = item_name_to_base_ID(item_name)
    
    for table in inventory_table_data:
        if item_base_ID == table.base_ID:
            return table

    raise Exception("get_table_data_for_part: Invalid item name, item's base ID did not match any inventory table base ID?")

def get_bit_to_update(item_name : str) -> int:
    # For the decoration key items, remove "key" from the string
    # These are stored in the same location in-game as the non-key versions
    item_name = item_name.replace(" (Key)", "")

    item_base_ID = item_name_to_base_ID(item_name)
    item_ID = all_item_table[item_name].id
    bit = item_ID - item_base_ID

    return bit

# Table that defines the default parts available in My City.
# To implement adding parts we've previously acquired to the part shop, we're disabling the game's vanilla functionality
#   (which adds parts depending on which part shops you've visited), and then adding to this default table.
my_city_part_shop_table = TableData(
    address = 0x2DC76C, # Start of the first table, needs to be incremented to get sub-table for particular part type
    length = BYTES_IN_A_WORD, # Length of each table within this table
    storage_type = StorageType.Bits,
    base_ID = None
)

# Stores all currently running functions that run once per frame
task_queue_entry = TableData(
    address = 0x177A0D0, # Address of first entry (max 48 entries before task overflow)
    length = 48, # Length of each entry
    storage_type = StorageType.Bytes,
    base_ID = None
)

# Items received index.
# Needs to be stored in save file so that different players on the same slot can have their own index
#     (ensuring all players will receive all items sent to the slot).
# In both NTSC and PAL, the amount of space allocated for the player's name, currency, and the Chestnut
#     Canyon phrase are all longer than the max character count that the game allows.
#     In NTSC, there are four unused bytes after the latest possible null terminator for the Chestnut
#     Canyon phrase - these unused bytes start at 0x177FDAC. Since we shouldn't ever need more than
#     that for the AP index, this location should work.
ap_item_index = TableData(
    address = 0x177FDAC,
    length = 2,
    storage_type = StorageType.Bytes,
    base_ID = None
)

ap_save_id = TableData(
    address = 0x177FD99, # After end of "UnnamedRacer" default text in save data
    length = 4,
    storage_type = StorageType.Bytes,
    base_ID = None
)

# Bool to indicate to the server that the ap_save_id has not been set, and the server should set it
ready_for_ap_save_id = TableData(
    address = 0x2DA0F0,
    length = 1,
    storage_type = StorageType.Bytes,
    base_ID = None
)

# Bool to indicate to the server that the current My City part shop inventory has not been sent, 
#     and the server should set it
ready_for_my_city_part_shop_inventory = TableData(
    address = 0x2DA0F1,
    length = 1,
    storage_type = StorageType.Bytes,
    base_ID = None
)