"""
Needed for room rando.

Road Trip stores room data (strings, NPC bodies, backgrounds) using separate tables for each piece of data.
  The strings are in one table, the NPC body data is in another table, and so on.
  These tables are all ordered the same way, so that one single index can be used to retrieve all the data
  for a room from each of the tables.

  Each table is an array of pointers. Each pointer points to a table of (strings/npc bodies/etc.) for one
  chunk in the game.
  
  Each of *those* tables is an array of pointers, one for each room in the chunk. Those pointers lead to 
  the actual data for a given room.

Example:
  - NPC Strings:
      -- Peach Town NPC strings:
          --- Q's Factory strings
          --- Parts Shop strings
          ...(and so on)
      -- Fuji City NPC strings
          --- Q's Factory strings
          --- Parts Shop strings
          ... (and so on)
  - NPC body data:
      -- Peach Town NPC body data
          --- Q's Factory NPC body data
          --- Parts Shop NPC body data
          ... (and so on)
      -- Fuji City NPC body data
          --- Q's Factory NPC body data
          --- Parts Shop NPC body data
          ... (and so on)

For room rando to work, we'll need to patch the game's room loading functions to load up a different
  room than the one it would by default based on a lookup table we provide. (i.e. the default ID
  will be the index into our table, and the new ID will be stored there)

This will cause it to load all of the data for that new room.

In NTSC:
- String tables begin at 0x2a7ed4 (e.g. first entry is a pointer to Peach Town's data, points to 0x2a5740)
- Body tables begin at 0x2c22cc (e.g. first entry is a pointer to Peach Town's data, points to 0x2c0718)
- Background tables are not quite understood yet (involve reading from disc), TBD
"""

import typing
from enum import IntEnum
from ..names import RegionName

# This enum is the order the world chunks appear in the top-level room data tables.
# IMPORTANT NOTE: These chunk values are NOT the same as those used by the terrain-loading functions in the game.
#     The current 'dialogue chunk' (or perhaps 'dialogue index'?) is located in RAM at 0x335923 (NTSC).
#     The current 'terrain chunk' is located in RAM at 0x335954 (NTSC).
class Chunk(IntEnum):
    # Chunks that do not contain any rooms do not have entries in the game's room data tables,
    #     and thus will not appear in the below list.
    PEACH_TOWN = 0x1
    FUJI_CITY = 0x2
    SANDPOLIS = 0x3
    CHESTNUT_CANYON = 0x4
    MUSHROOM_ROAD = 0x5
    WHITE_MOUNTAIN = 0x6
    PAPAYA_ISLAND = 0x7
    CLOUD_HILL = 0x8
    MY_CITY = 0x9
    WINDMILLS = 0xA
    FUJI_BRIDGE = 0xB
    NORTH_OF_SANDPOLIS = 0xC
    PYRAMIDS = 0xD
    LIGHTHOUSE = 0XE
    EAST_OF_SANDPOLIS = 0xF
    TUNNEL_TO_CHESTNUT_CANYON = 0x10
    SOUTH_OF_FUJI_CITY = 0x11
    WEST_OF_WHITE_MOUNTAIN = 0x12
    EAST_OF_WHITE_MOUNTAIN = 0x13
    SOUTHWEST_OF_PEACH_TOWN = 0x14
    EAST_OF_PEACH_TOWN = 0x15

class RoomIDs(typing.NamedTuple):
    # i.e. What chunk is this room/NPC in?
    chunkID: Chunk
    # i.e. What index does this room/NPC have in that chunk's tables?
    roomIndex: int

room_IDs = {
    # --- Logically considered part of Peach Town in RTA AP ---
    # Rooms
    RegionName.Peach_Town_Qs_Factory: RoomIDs(Chunk.PEACH_TOWN, 0),
    RegionName.Peach_Town_Parts_Shop: RoomIDs(Chunk.PEACH_TOWN, 1),
    RegionName.Peach_Town_Body_Shop: RoomIDs(Chunk.PEACH_TOWN, 2),
    RegionName.Peach_Town_Paint_Shop: RoomIDs(Chunk.PEACH_TOWN, 3),
    RegionName.Peach_Town_Bar: RoomIDs(Chunk.PEACH_TOWN, 4),
    RegionName.Peach_Town_Police_Station: RoomIDs(Chunk.PEACH_TOWN, 5),
    RegionName.Peach_Town_Radio_Station: RoomIDs(Chunk.PEACH_TOWN, 6),
    RegionName.Peach_Town_Farm_House: RoomIDs(Chunk.PEACH_TOWN, 7),
    RegionName.Peach_Town_Kevin_House: RoomIDs(Chunk.PEACH_TOWN, 8),
    RegionName.Peach_Town_Wolf_House: RoomIDs(Chunk.PEACH_TOWN, 9),
    RegionName.Peach_Town_Best_House: RoomIDs(Chunk.PEACH_TOWN, 10),
    RegionName.Peach_Town_Jousset_House: RoomIDs(Chunk.PEACH_TOWN, 11),
    RegionName.Peach_Town_Coffee_Shop: RoomIDs(Chunk.PEACH_TOWN, 12),
    RegionName.Peach_Town_Barrel_Dodging: RoomIDs(Chunk.PEACH_TOWN, 13),
    RegionName.Peach_Town_Gemstone_House: RoomIDs(Chunk.PEACH_TOWN, 14),
    RegionName.Peach_Town_Fight_House: RoomIDs(Chunk.PEACH_TOWN, 15),
    RegionName.Peach_Town_Milton_House: RoomIDs(Chunk.PEACH_TOWN, 16),
    RegionName.Peach_Town_Barrel_Dodging_Complete: RoomIDs(Chunk.PEACH_TOWN, 17),
    RegionName.Quick_Pic_1: RoomIDs(Chunk.PEACH_TOWN, 18),
    RegionName.Quick_Pic_2: RoomIDs(Chunk.PEACH_TOWN, 19),
    RegionName.Quick_Pic_3: RoomIDs(Chunk.PEACH_TOWN, 20),
    RegionName.Quick_Pic_4: RoomIDs(Chunk.PEACH_TOWN, 21),
    RegionName.Quick_Pic_5: RoomIDs(Chunk.PEACH_TOWN, 22),
    RegionName.Quick_Pic_6: RoomIDs(Chunk.PEACH_TOWN, 23),
    RegionName.Quick_Pic_7: RoomIDs(Chunk.PEACH_TOWN, 24),
    RegionName.Quick_Pic_8: RoomIDs(Chunk.PEACH_TOWN, 25),
    RegionName.Quick_Pic_9: RoomIDs(Chunk.PEACH_TOWN, 26),
    RegionName.Quick_Pic_10: RoomIDs(Chunk.PEACH_TOWN, 27),

    RegionName.Windmill_House: RoomIDs(Chunk.WINDMILLS, 0),
    RegionName.Quick_Pic_85: RoomIDs(Chunk.WINDMILLS, 2),
    RegionName.Quick_Pic_86: RoomIDs(Chunk.WINDMILLS, 3),

    RegionName.Quick_Pic_12: RoomIDs(Chunk.SOUTHWEST_OF_PEACH_TOWN, 0),

    RegionName.Quick_Pic_11: RoomIDs(Chunk.EAST_OF_PEACH_TOWN, 0),

    # Roaming NPCs
    RegionName.Peach_Town_NPC_James: RoomIDs(Chunk.PEACH_TOWN, 28),
    RegionName.Peach_Town_NPC_Gonzo: RoomIDs(Chunk.PEACH_TOWN, 29),
    RegionName.Peach_Town_NPC_Ramsey: RoomIDs(Chunk.PEACH_TOWN, 30),
    RegionName.Peach_Town_NPC_Accel: RoomIDs(Chunk.PEACH_TOWN, 31),
    RegionName.Peach_Town_NPC_Cobran: RoomIDs(Chunk.PEACH_TOWN, 32),
    RegionName.Peach_Town_NPC_Flower: RoomIDs(Chunk.PEACH_TOWN, 33),
    RegionName.Peach_Town_NPC_Klein: RoomIDs(Chunk.PEACH_TOWN, 34),
    RegionName.Peach_Town_NPC_Barthou: RoomIDs(Chunk.PEACH_TOWN, 35),
    RegionName.Peach_Town_NPC_Pillow: RoomIDs(Chunk.PEACH_TOWN, 36),
    RegionName.Peach_Town_NPC_Kevin: RoomIDs(Chunk.PEACH_TOWN, 37),
    RegionName.Peach_Town_NPC_Newman: RoomIDs(Chunk.PEACH_TOWN, 38),

    # --- Logically considered part of Fuji City in RTA AP ---
    # Rooms
    RegionName.Fuji_City_Qs_Factory: RoomIDs(Chunk.FUJI_CITY, 0),
    RegionName.Fuji_City_Parts_Shop: RoomIDs(Chunk.FUJI_CITY, 1),
    RegionName.Fuji_City_Body_Shop: RoomIDs(Chunk.FUJI_CITY, 2),
    RegionName.Fuji_City_Paint_Shop: RoomIDs(Chunk.FUJI_CITY, 3),
    RegionName.Fuji_City_Bar: RoomIDs(Chunk.FUJI_CITY, 4),
    RegionName.Fuji_City_Heizo_House: RoomIDs(Chunk.FUJI_CITY, 5),
    RegionName.Fuji_City_Echigoya_Shop: RoomIDs(Chunk.FUJI_CITY, 6),
    RegionName.Fuji_City_Castle_Princess_Nanaha: RoomIDs(Chunk.FUJI_CITY, 7),
    RegionName.Fuji_City_Castle_Sliding_Door_Race: RoomIDs(Chunk.FUJI_CITY, 8),
    RegionName.Fuji_City_Treasure_Hunting: RoomIDs(Chunk.FUJI_CITY, 9),
    RegionName.Fuji_City_Guarded_Dungeon: RoomIDs(Chunk.FUJI_CITY, 10),
    RegionName.Fuji_City_Fortune_Telling_Room: RoomIDs(Chunk.FUJI_CITY, 11),
    RegionName.Fuji_City_Dumpling_Shop: RoomIDs(Chunk.FUJI_CITY, 12),
    RegionName.Fuji_City_Uzumasa_House: RoomIDs(Chunk.FUJI_CITY, 13),
    RegionName.Fuji_City_Iwasuke_House: RoomIDs(Chunk.FUJI_CITY, 14),
    RegionName.Fuji_City_Hakosuke_House: RoomIDs(Chunk.FUJI_CITY, 15),
    RegionName.Fuji_City_Noodle_Shop: RoomIDs(Chunk.FUJI_CITY, 16),
    RegionName.Fuji_City_Highway_Race: RoomIDs(Chunk.FUJI_CITY, 17),
    RegionName.Fuji_City_Hanako_House: RoomIDs(Chunk.FUJI_CITY, 18),
    RegionName.Quick_Pic_17: RoomIDs(Chunk.FUJI_CITY, 19),
    RegionName.Quick_Pic_18: RoomIDs(Chunk.FUJI_CITY, 20),
    RegionName.Quick_Pic_19: RoomIDs(Chunk.FUJI_CITY, 21),
    RegionName.Quick_Pic_20: RoomIDs(Chunk.FUJI_CITY, 22),
    RegionName.Quick_Pic_21: RoomIDs(Chunk.FUJI_CITY, 23),
    RegionName.Quick_Pic_22: RoomIDs(Chunk.FUJI_CITY, 24),
    RegionName.Quick_Pic_23: RoomIDs(Chunk.FUJI_CITY, 25),
    RegionName.Quick_Pic_24: RoomIDs(Chunk.FUJI_CITY, 26),
    RegionName.Quick_Pic_25: RoomIDs(Chunk.FUJI_CITY, 27),
    RegionName.Quick_Pic_26: RoomIDs(Chunk.FUJI_CITY, 28),

    RegionName.Quick_Pic_13: RoomIDs(Chunk.FUJI_BRIDGE, 0),
    RegionName.Quick_Pic_14: RoomIDs(Chunk.FUJI_BRIDGE, 1),
    RegionName.Quick_Pic_15: RoomIDs(Chunk.FUJI_BRIDGE, 2),
    RegionName.Quick_Pic_16: RoomIDs(Chunk.FUJI_BRIDGE, 3),

    RegionName.Quick_Pic_27: RoomIDs(Chunk.SOUTH_OF_FUJI_CITY, 0),

    # Roaming NPCs
    RegionName.Fuji_City_NPC_Guard: RoomIDs(Chunk.FUJI_CITY, 29),
    RegionName.Fuji_City_NPC_Toki: RoomIDs(Chunk.FUJI_CITY, 30),
    RegionName.Fuji_City_NPC_Matsugoro: RoomIDs(Chunk.FUJI_CITY, 31),
    RegionName.Fuji_City_NPC_Sakuzo: RoomIDs(Chunk.FUJI_CITY, 32),
    RegionName.Fuji_City_NPC_Shinsaku: RoomIDs(Chunk.FUJI_CITY, 33),
    RegionName.Fuji_City_NPC_Shohei: RoomIDs(Chunk.FUJI_CITY, 34),
    RegionName.Fuji_City_NPC_Brian: RoomIDs(Chunk.FUJI_CITY, 35),
    RegionName.Fuji_City_NPC_Coine: RoomIDs(Chunk.FUJI_CITY, 36),
    RegionName.Fuji_City_NPC_Gichi: RoomIDs(Chunk.FUJI_CITY, 37),
    RegionName.Fuji_City_NPC_Goro: RoomIDs(Chunk.FUJI_CITY, 38),
    RegionName.Fuji_City_NPC_Kiyokichi: RoomIDs(Chunk.FUJI_CITY, 39),

    # --- Logically considered part of My City in RTA AP ---
    # Rooms
    RegionName.My_City_Qs_Factory: RoomIDs(Chunk.MY_CITY, 0),
    RegionName.My_City_Parts_Shop: RoomIDs(Chunk.MY_CITY, 1),
    RegionName.My_City_Body_Shop: RoomIDs(Chunk.MY_CITY, 2),
    RegionName.My_City_Paint_Shop: RoomIDs(Chunk.MY_CITY, 3),
    RegionName.My_City_Police_Station: RoomIDs(Chunk.MY_CITY, 4),
    RegionName.My_City_Recycle_Shop: RoomIDs(Chunk.MY_CITY, 5),
    RegionName.My_City_Wonder_Realty: RoomIDs(Chunk.MY_CITY, 6),
    RegionName.My_City_Bank: RoomIDs(Chunk.MY_CITY, 7),
    RegionName.My_City_Theater: RoomIDs(Chunk.MY_CITY, 8),
    RegionName.My_City_Tower: RoomIDs(Chunk.MY_CITY, 9),
    RegionName.My_City_Which_Way_Maze: RoomIDs(Chunk.MY_CITY, 10),
    RegionName.My_City_Fire_Station: RoomIDs(Chunk.MY_CITY, 11),
    RegionName.My_City_School: RoomIDs(Chunk.MY_CITY, 12),
    RegionName.My_City_Coine_House: RoomIDs(Chunk.MY_CITY, 13),
    RegionName.My_City_Kuwano_House: RoomIDs(Chunk.MY_CITY, 14),
    RegionName.My_City_Mien_House: RoomIDs(Chunk.MY_CITY, 15),
    RegionName.My_City_Flower_House: RoomIDs(Chunk.MY_CITY, 16),
    RegionName.My_City_Gichi_House: RoomIDs(Chunk.MY_CITY, 17),
    RegionName.My_City_Tunnel_Race: RoomIDs(Chunk.MY_CITY, 18),
    RegionName.My_City_Sally_House: RoomIDs(Chunk.MY_CITY, 19),
    RegionName.My_City_Rally_Center: RoomIDs(Chunk.MY_CITY, 20),
    RegionName.Quick_Pic_28: RoomIDs(Chunk.MY_CITY, 21),
    RegionName.Quick_Pic_29: RoomIDs(Chunk.MY_CITY, 22),

    # Roaming NPCs
    RegionName.My_City_NPC_Cobran: RoomIDs(Chunk.MY_CITY, 23),
    RegionName.My_City_NPC_Saucy: RoomIDs(Chunk.MY_CITY, 24),
    RegionName.My_City_NPC_Sylvester: RoomIDs(Chunk.MY_CITY, 25),
    RegionName.My_City_NPC_Velvet: RoomIDs(Chunk.MY_CITY, 26),
    RegionName.My_City_NPC_Arnold: RoomIDs(Chunk.MY_CITY, 27),
    RegionName.My_City_NPC_Gump: RoomIDs(Chunk.MY_CITY, 28),

    # --- Logically considered part of Sandpolis in RTA AP ---
    # Rooms
    RegionName.Sandpolis_Qs_Factory: RoomIDs(Chunk.SANDPOLIS, 0),
    RegionName.Sandpolis_Parts_Shop: RoomIDs(Chunk.SANDPOLIS, 1),
    RegionName.Sandpolis_Body_Shop: RoomIDs(Chunk.SANDPOLIS, 2),
    RegionName.Sandpolis_Paint_Shop: RoomIDs(Chunk.SANDPOLIS, 3),
    RegionName.Sandpolis_Bar: RoomIDs(Chunk.SANDPOLIS, 4),
    RegionName.Sandpolis_Sheriff_Office: RoomIDs(Chunk.SANDPOLIS, 5),
    RegionName.Sandpolis_Figure_8: RoomIDs(Chunk.SANDPOLIS, 6),
    RegionName.Sandpolis_Soccer: RoomIDs(Chunk.SANDPOLIS, 7),
    RegionName.Sandpolis_Roulette: RoomIDs(Chunk.SANDPOLIS, 8),
    RegionName.Sandpolis_Mini_Tower: RoomIDs(Chunk.SANDPOLIS, 9),
    RegionName.Sandpolis_Drag_Race: RoomIDs(Chunk.SANDPOLIS, 10),
    RegionName.Sandpolis_Frank_House: RoomIDs(Chunk.SANDPOLIS, 11),
    RegionName.Sandpolis_Sebastian_House: RoomIDs(Chunk.SANDPOLIS, 12),
    RegionName.Sandpolis_Sand_Sports: RoomIDs(Chunk.SANDPOLIS, 13),
    RegionName.Sandpolis_Mr_King_Mansion: RoomIDs(Chunk.SANDPOLIS, 14),
    RegionName.Sandpolis_Butch_House: RoomIDs(Chunk.SANDPOLIS, 15),
    RegionName.Sandpolis_Barton_House: RoomIDs(Chunk.SANDPOLIS, 16),
    RegionName.Sandpolis_Cake_Shop: RoomIDs(Chunk.SANDPOLIS, 17),
    RegionName.Sandpolis_Merci_House: RoomIDs(Chunk.SANDPOLIS, 18),
    RegionName.Sandpolis_Bob_House: RoomIDs(Chunk.SANDPOLIS, 19),
    RegionName.Sandpolis_Richard_House: RoomIDs(Chunk.SANDPOLIS, 20),
    RegionName.Quick_Pic_36: RoomIDs(Chunk.SANDPOLIS, 21),
    RegionName.Quick_Pic_37: RoomIDs(Chunk.SANDPOLIS, 22),
    RegionName.Quick_Pic_38: RoomIDs(Chunk.SANDPOLIS, 23),
    RegionName.Quick_Pic_39: RoomIDs(Chunk.SANDPOLIS, 24),
    RegionName.Quick_Pic_40: RoomIDs(Chunk.SANDPOLIS, 25),
    RegionName.Quick_Pic_41: RoomIDs(Chunk.SANDPOLIS, 26),
    RegionName.Quick_Pic_42: RoomIDs(Chunk.SANDPOLIS, 27),
    RegionName.Quick_Pic_43: RoomIDs(Chunk.SANDPOLIS, 28),
    RegionName.Quick_Pic_44: RoomIDs(Chunk.SANDPOLIS, 29),
    RegionName.Quick_Pic_45: RoomIDs(Chunk.SANDPOLIS, 30),
    RegionName.Quick_Pic_46: RoomIDs(Chunk.SANDPOLIS, 31),
    RegionName.Quick_Pic_47: RoomIDs(Chunk.SANDPOLIS, 32),

    RegionName.UFO: RoomIDs(Chunk.NORTH_OF_SANDPOLIS, 0),
    RegionName.Quick_Pic_52: RoomIDs(Chunk.NORTH_OF_SANDPOLIS, 1),
    RegionName.Quick_Pic_53: RoomIDs(Chunk.NORTH_OF_SANDPOLIS, 2),
    RegionName.Quick_Pic_54: RoomIDs(Chunk.NORTH_OF_SANDPOLIS, 3),

    RegionName.Benji_House: RoomIDs(Chunk.PYRAMIDS, 0),
    RegionName.Quick_Pic_48: RoomIDs(Chunk.PYRAMIDS, 1),
    RegionName.Quick_Pic_49: RoomIDs(Chunk.PYRAMIDS, 2),
    RegionName.Quick_Pic_50: RoomIDs(Chunk.PYRAMIDS, 3),
    RegionName.Quick_Pic_51: RoomIDs(Chunk.PYRAMIDS, 4),

    RegionName.Lightouse: RoomIDs(Chunk.LIGHTHOUSE, 0),
    RegionName.Quick_Pic_55: RoomIDs(Chunk.LIGHTHOUSE, 1),
    RegionName.Quick_Pic_56: RoomIDs(Chunk.LIGHTHOUSE, 2),
    RegionName.Quick_Pic_57: RoomIDs(Chunk.LIGHTHOUSE, 3),

    RegionName.Quick_Pic_30: RoomIDs(Chunk.EAST_OF_SANDPOLIS, 0),
    RegionName.Quick_Pic_31: RoomIDs(Chunk.EAST_OF_SANDPOLIS, 1),
    RegionName.Quick_Pic_32: RoomIDs(Chunk.EAST_OF_SANDPOLIS, 2),
    RegionName.Quick_Pic_33: RoomIDs(Chunk.EAST_OF_SANDPOLIS, 3),
    RegionName.Quick_Pic_34: RoomIDs(Chunk.EAST_OF_SANDPOLIS, 4),
    RegionName.Quick_Pic_35: RoomIDs(Chunk.EAST_OF_SANDPOLIS, 5),

    # Roaming NPCs
    RegionName.Sandpolis_NPC_Michael: RoomIDs(Chunk.SANDPOLIS, 33),
    RegionName.Sandpolis_NPC_Martin: RoomIDs(Chunk.SANDPOLIS, 34),
    RegionName.Sandpolis_NPC_Ryoji: RoomIDs(Chunk.SANDPOLIS, 35),
    RegionName.Sandpolis_NPC_Akiban: RoomIDs(Chunk.SANDPOLIS, 36),
    RegionName.Sandpolis_NPC_Dayan: RoomIDs(Chunk.SANDPOLIS, 37),
    RegionName.Sandpolis_NPC_Roberts: RoomIDs(Chunk.SANDPOLIS, 38),
    RegionName.Sandpolis_NPC_George: RoomIDs(Chunk.SANDPOLIS, 39),
    RegionName.Sandpolis_NPC_Lisalisa: RoomIDs(Chunk.SANDPOLIS, 40),
    RegionName.Sandpolis_NPC_Morrison: RoomIDs(Chunk.SANDPOLIS, 41),

    RegionName.NPC_Benji: RoomIDs(Chunk.PYRAMIDS, 5),

    # --- Logically considered part of Chestnut Canyon in RTA AP ---
    # Rooms
    RegionName.Chestnut_Canyon_Qs_Factory: RoomIDs(Chunk.CHESTNUT_CANYON, 0),
    RegionName.Chestnut_Canyon_Bar: RoomIDs(Chunk.CHESTNUT_CANYON, 1),
    RegionName.Chestnut_Canyon_Wallace_House: RoomIDs(Chunk.CHESTNUT_CANYON, 2),
    RegionName.Chestnut_Canyon_Greeting_House: RoomIDs(Chunk.CHESTNUT_CANYON, 3), # Gene's House
    RegionName.Chestnut_Canyon_M_Carton_House: RoomIDs(Chunk.CHESTNUT_CANYON, 4),
    RegionName.Chestnut_Canyon_Rock_Climbing: RoomIDs(Chunk.CHESTNUT_CANYON, 5),
    RegionName.Chestnut_Canyon_Rock_Climbing_Complete: RoomIDs(Chunk.CHESTNUT_CANYON, 6),
    RegionName.Chestnut_Canyon_Volcano_Run: RoomIDs(Chunk.CHESTNUT_CANYON, 7),
    RegionName.Chestnut_Canyon_Tom_House: RoomIDs(Chunk.CHESTNUT_CANYON, 8),
    RegionName.Chestnut_Canyon_Lowry_House: RoomIDs(Chunk.CHESTNUT_CANYON, 9),
    RegionName.Chestnut_Canyon_Betty_House: RoomIDs(Chunk.CHESTNUT_CANYON, 10),
    RegionName.Chestnut_Canyon_Lucy_House: RoomIDs(Chunk.CHESTNUT_CANYON, 11),
    RegionName.Quick_Pic_60: RoomIDs(Chunk.CHESTNUT_CANYON, 12),
    RegionName.Quick_Pic_61: RoomIDs(Chunk.CHESTNUT_CANYON, 13),
    RegionName.Quick_Pic_62: RoomIDs(Chunk.CHESTNUT_CANYON, 14),
    RegionName.Quick_Pic_63: RoomIDs(Chunk.CHESTNUT_CANYON, 15),
    RegionName.Quick_Pic_64: RoomIDs(Chunk.CHESTNUT_CANYON, 16),

    RegionName.Quick_Pic_58: RoomIDs(Chunk.TUNNEL_TO_CHESTNUT_CANYON, 0),
    RegionName.Quick_Pic_59: RoomIDs(Chunk.TUNNEL_TO_CHESTNUT_CANYON, 1),

    # Roaming NPCs
    RegionName.Chestnut_Canyon_NPC_Leon: RoomIDs(Chunk.CHESTNUT_CANYON, 17),
    RegionName.Chestnut_Canyon_NPC_Stance: RoomIDs(Chunk.CHESTNUT_CANYON, 18),
    RegionName.Chestnut_Canyon_NPC_Matil: RoomIDs(Chunk.CHESTNUT_CANYON, 19),
    RegionName.Chestnut_Canyon_NPC_Rectan: RoomIDs(Chunk.CHESTNUT_CANYON, 20),
    RegionName.Chestnut_Canyon_NPC_Clary: RoomIDs(Chunk.CHESTNUT_CANYON, 21),
    RegionName.Chestnut_Canyon_NPC_Graham: RoomIDs(Chunk.CHESTNUT_CANYON, 22),
    RegionName.Chestnut_Canyon_NPC_Wilde: RoomIDs(Chunk.CHESTNUT_CANYON, 23),
    RegionName.Chestnut_Canyon_NPC_Mojo: RoomIDs(Chunk.CHESTNUT_CANYON, 24),
    RegionName.Chestnut_Canyon_NPC_Saucy: RoomIDs(Chunk.CHESTNUT_CANYON, 25),
    RegionName.Chestnut_Canyon_NPC_Kuwano: RoomIDs(Chunk.CHESTNUT_CANYON, 26),
    RegionName.Chestnut_Canyon_NPC_Steve: RoomIDs(Chunk.CHESTNUT_CANYON, 27),

    # --- Logically considered part of Mushroom Road in RTA AP ---
    # Rooms
    RegionName.Mushroom_Road_Qs_Factory: RoomIDs(Chunk.MUSHROOM_ROAD, 0),
    RegionName.Mushroom_Road_Parts_Shop: RoomIDs(Chunk.MUSHROOM_ROAD, 1),
    RegionName.Mushroom_Road_Bar: RoomIDs(Chunk.MUSHROOM_ROAD, 2),
    RegionName.Mushroom_Road_Golf: RoomIDs(Chunk.MUSHROOM_ROAD, 3),
    RegionName.Mushroom_Road_Goddess: RoomIDs(Chunk.MUSHROOM_ROAD, 4),
    RegionName.Quick_Pic_65: RoomIDs(Chunk.MUSHROOM_ROAD, 5),
    RegionName.Quick_Pic_66: RoomIDs(Chunk.MUSHROOM_ROAD, 6),
    RegionName.Quick_Pic_67: RoomIDs(Chunk.MUSHROOM_ROAD, 7),
    RegionName.Quick_Pic_68: RoomIDs(Chunk.MUSHROOM_ROAD, 8),
    RegionName.Quick_Pic_69: RoomIDs(Chunk.MUSHROOM_ROAD, 9),
    RegionName.Quick_Pic_70: RoomIDs(Chunk.MUSHROOM_ROAD, 10),
    # (No NPCs in Mushroom Road)

    # --- Logically considered part of White Mountain in RTA AP ---
    # Rooms
    RegionName.White_Mountain_Qs_Factory: RoomIDs(Chunk.WHITE_MOUNTAIN, 0),
    RegionName.White_Mountain_Parts_Shop: RoomIDs(Chunk.WHITE_MOUNTAIN, 1),
    RegionName.White_Mountain_Body_Shop: RoomIDs(Chunk.WHITE_MOUNTAIN, 2),
    RegionName.White_Mountain_Paint_Shop: RoomIDs(Chunk.WHITE_MOUNTAIN, 3),
    RegionName.White_Mountain_Bar: RoomIDs(Chunk.WHITE_MOUNTAIN, 4),
    RegionName.White_Mountain_Policeman_House: RoomIDs(Chunk.WHITE_MOUNTAIN, 5),
    RegionName.White_Mountain_Merrin_House: RoomIDs(Chunk.WHITE_MOUNTAIN, 6),
    RegionName.White_Mountain_Ski_Jumping: RoomIDs(Chunk.WHITE_MOUNTAIN, 7),
    RegionName.White_Mountain_Grandma_Dizzy_House: RoomIDs(Chunk.WHITE_MOUNTAIN, 8),
    RegionName.White_Mountain_Post_Office: RoomIDs(Chunk.WHITE_MOUNTAIN, 9),
    RegionName.White_Mountain_Santa_House: RoomIDs(Chunk.WHITE_MOUNTAIN, 10),
    RegionName.White_Mountain_Keitel_House: RoomIDs(Chunk.WHITE_MOUNTAIN, 11),
    RegionName.White_Mountain_Coin_Radar_House_1: RoomIDs(Chunk.WHITE_MOUNTAIN, 12),
    RegionName.White_Mountain_Coin_Radar_House_2: RoomIDs(Chunk.WHITE_MOUNTAIN, 13),
    RegionName.White_Mountain_Coin_Radar_House_3: RoomIDs(Chunk.WHITE_MOUNTAIN, 14),
    RegionName.White_Mountain_Coin_Radar_House_4: RoomIDs(Chunk.WHITE_MOUNTAIN, 15),
    RegionName.White_Mountain_Emily_House: RoomIDs(Chunk.WHITE_MOUNTAIN, 16),
    RegionName.White_Mountain_Bigfoot_Joe_House: RoomIDs(Chunk.WHITE_MOUNTAIN, 17),
    RegionName.White_Mountain_Curling: RoomIDs(Chunk.WHITE_MOUNTAIN, 18),
    RegionName.White_Mountain_Wool_Shop: RoomIDs(Chunk.WHITE_MOUNTAIN, 19),
    RegionName.Quick_Pic_71: RoomIDs(Chunk.WHITE_MOUNTAIN, 20),
    RegionName.Quick_Pic_72: RoomIDs(Chunk.WHITE_MOUNTAIN, 21),
    RegionName.Quick_Pic_73: RoomIDs(Chunk.WHITE_MOUNTAIN, 22),
    RegionName.Quick_Pic_74: RoomIDs(Chunk.WHITE_MOUNTAIN, 23),
    RegionName.Quick_Pic_75: RoomIDs(Chunk.WHITE_MOUNTAIN, 24),
    RegionName.Quick_Pic_76: RoomIDs(Chunk.WHITE_MOUNTAIN, 25),
    RegionName.Quick_Pic_77: RoomIDs(Chunk.WHITE_MOUNTAIN, 26),

    RegionName.Quick_Pic_84: RoomIDs(Chunk.WINDMILLS, 1),

    RegionName.Temple_Under_the_Sea: RoomIDs(Chunk.WEST_OF_WHITE_MOUNTAIN, 0),
    RegionName.Quick_Pic_78: RoomIDs(Chunk.WEST_OF_WHITE_MOUNTAIN, 1),
    RegionName.Quick_Pic_79: RoomIDs(Chunk.WEST_OF_WHITE_MOUNTAIN, 2),

    RegionName.Quick_Pic_80: RoomIDs(Chunk.EAST_OF_WHITE_MOUNTAIN, 0),
    RegionName.Quick_Pic_81: RoomIDs(Chunk.EAST_OF_WHITE_MOUNTAIN, 1),
    RegionName.Quick_Pic_82: RoomIDs(Chunk.EAST_OF_WHITE_MOUNTAIN, 2),
    RegionName.Quick_Pic_83: RoomIDs(Chunk.EAST_OF_WHITE_MOUNTAIN, 3),

    # Roaming NPCs
    RegionName.White_Mountain_NPC_Jack: RoomIDs(Chunk.WHITE_MOUNTAIN, 27),
    RegionName.White_Mountain_NPC_Charles: RoomIDs(Chunk.WHITE_MOUNTAIN, 28),
    RegionName.White_Mountain_NPC_Hitomi: RoomIDs(Chunk.WHITE_MOUNTAIN, 29),
    RegionName.White_Mountain_NPC_Brown: RoomIDs(Chunk.WHITE_MOUNTAIN, 30),
    RegionName.White_Mountain_NPC_Blonty: RoomIDs(Chunk.WHITE_MOUNTAIN, 31),
    RegionName.White_Mountain_NPC_Shirley: RoomIDs(Chunk.WHITE_MOUNTAIN, 32),
    RegionName.White_Mountain_NPC_Nick: RoomIDs(Chunk.WHITE_MOUNTAIN, 33),
    RegionName.White_Mountain_NPC_Suess: RoomIDs(Chunk.WHITE_MOUNTAIN, 34),
    RegionName.White_Mountain_NPC_Manei: RoomIDs(Chunk.WHITE_MOUNTAIN, 35),
    RegionName.White_Mountain_NPC_Sally: RoomIDs(Chunk.WHITE_MOUNTAIN, 36),

    RegionName.NPC_Orpheus: RoomIDs(Chunk.WEST_OF_WHITE_MOUNTAIN, 3),

    # --- Logically considered part of Papaya Island in RTA AP ---
    # Rooms
    RegionName.Papaya_Island_Qs_Factory: RoomIDs(Chunk.PAPAYA_ISLAND, 0),
    RegionName.Papaya_Island_Parts_Shop: RoomIDs(Chunk.PAPAYA_ISLAND, 1),
    RegionName.Papaya_Island_Body_Shop: RoomIDs(Chunk.PAPAYA_ISLAND, 2),
    RegionName.Papaya_Island_Bar: RoomIDs(Chunk.PAPAYA_ISLAND, 3),
    RegionName.Papaya_Island_Policeman_House: RoomIDs(Chunk.PAPAYA_ISLAND, 4),
    RegionName.Papaya_Island_Obstacle_Course: RoomIDs(Chunk.PAPAYA_ISLAND, 5),
    RegionName.Papaya_Island_Mayor_House: RoomIDs(Chunk.PAPAYA_ISLAND, 6),
    RegionName.Papaya_Island_Luke_House: RoomIDs(Chunk.PAPAYA_ISLAND, 7),
    RegionName.Papaya_Island_Grandpa_Costello_House: RoomIDs(Chunk.PAPAYA_ISLAND, 8),
    RegionName.Papaya_Island_Andy_House: RoomIDs(Chunk.PAPAYA_ISLAND, 9),
    RegionName.Papaya_Island_Shirley_House: RoomIDs(Chunk.PAPAYA_ISLAND, 10),
    RegionName.Papaya_Island_Casa_House: RoomIDs(Chunk.PAPAYA_ISLAND, 11),
    RegionName.Papaya_Island_Sandro_House: RoomIDs(Chunk.PAPAYA_ISLAND, 12),
    RegionName.Papaya_Island_Beach_Flag: RoomIDs(Chunk.PAPAYA_ISLAND, 13),
    RegionName.Papaya_Island_Coconut_Shop: RoomIDs(Chunk.PAPAYA_ISLAND, 14),
    RegionName.Papaya_Island_Fishing: RoomIDs(Chunk.PAPAYA_ISLAND, 15),
    RegionName.Papaya_Island_Papu_Tree: RoomIDs(Chunk.PAPAYA_ISLAND, 16),
    RegionName.Papaya_Island_Cloud_Hill_Warp: RoomIDs(Chunk.PAPAYA_ISLAND, 17),
    RegionName.Quick_Pic_87: RoomIDs(Chunk.PAPAYA_ISLAND, 18),
    RegionName.Quick_Pic_88: RoomIDs(Chunk.PAPAYA_ISLAND, 19),
    RegionName.Quick_Pic_89: RoomIDs(Chunk.PAPAYA_ISLAND, 20),
    RegionName.Quick_Pic_90: RoomIDs(Chunk.PAPAYA_ISLAND, 21),
    RegionName.Quick_Pic_91: RoomIDs(Chunk.PAPAYA_ISLAND, 22),
    RegionName.Quick_Pic_92: RoomIDs(Chunk.PAPAYA_ISLAND, 23),
    RegionName.Quick_Pic_93: RoomIDs(Chunk.PAPAYA_ISLAND, 24),
    RegionName.Quick_Pic_94: RoomIDs(Chunk.PAPAYA_ISLAND, 25),
    RegionName.Quick_Pic_95: RoomIDs(Chunk.PAPAYA_ISLAND, 26),
    RegionName.Quick_Pic_96: RoomIDs(Chunk.PAPAYA_ISLAND, 27),

    # Roaming NPCs
    RegionName.Papaya_Island_NPC_Mond: RoomIDs(Chunk.PAPAYA_ISLAND, 28),
    RegionName.Papaya_Island_NPC_John: RoomIDs(Chunk.PAPAYA_ISLAND, 29),
    RegionName.Papaya_Island_NPC_Kerori: RoomIDs(Chunk.PAPAYA_ISLAND, 30),
    RegionName.Papaya_Island_NPC_Nairo: RoomIDs(Chunk.PAPAYA_ISLAND, 31),
    RegionName.Papaya_Island_NPC_Moisy: RoomIDs(Chunk.PAPAYA_ISLAND, 32),
    RegionName.Papaya_Island_NPC_Nouri: RoomIDs(Chunk.PAPAYA_ISLAND, 33),
    RegionName.Papaya_Island_NPC_Minerva: RoomIDs(Chunk.PAPAYA_ISLAND, 34),
    RegionName.Papaya_Island_NPC_Kite: RoomIDs(Chunk.PAPAYA_ISLAND, 35),
    RegionName.Papaya_Island_NPC_Mien: RoomIDs(Chunk.PAPAYA_ISLAND, 36),
    RegionName.Papaya_Island_NPC_Michael: RoomIDs(Chunk.PAPAYA_ISLAND, 37),

    # --- Logically considered part of Cloud Hill in RTA AP ---
    # Rooms
    RegionName.Cloud_Hill_Qs_Factory: RoomIDs(Chunk.CLOUD_HILL, 0),
    RegionName.Cloud_Hill_Parts_Shop: RoomIDs(Chunk.CLOUD_HILL, 1),
    RegionName.Cloud_Hill_Body_Shop: RoomIDs(Chunk.CLOUD_HILL, 2),
    RegionName.Cloud_Hill_Paint_Shop: RoomIDs(Chunk.CLOUD_HILL, 3),
    RegionName.Cloud_Hill_Single_Lap_Race: RoomIDs(Chunk.CLOUD_HILL, 4),
    RegionName.Cloud_Hill_Duck_House: RoomIDs(Chunk.CLOUD_HILL, 5),
    RegionName.Cloud_Hill_Rainbow_Jump: RoomIDs(Chunk.CLOUD_HILL, 6),
    RegionName.Cloud_Hill_Invalid_Room: RoomIDs(Chunk.CLOUD_HILL, 7), # Unused copy of the Cloud Hill warp room with placeholder text.
    RegionName.Cloud_Hill_White_House_Lobby: RoomIDs(Chunk.CLOUD_HILL, 8),
    RegionName.Cloud_Hill_President_Room: RoomIDs(Chunk.CLOUD_HILL, 9),
    RegionName.Quick_Pic_97: RoomIDs(Chunk.CLOUD_HILL, 10),
    RegionName.Quick_Pic_98: RoomIDs(Chunk.CLOUD_HILL, 11),
    RegionName.Quick_Pic_99: RoomIDs(Chunk.CLOUD_HILL, 12),
    RegionName.Quick_Pic_100: RoomIDs(Chunk.CLOUD_HILL, 13),

    # Roaming NPCs
    RegionName.Cloud_Hill_NPC_Yumyum: RoomIDs(Chunk.CLOUD_HILL, 14),
    RegionName.Cloud_Hill_NPC_Dust: RoomIDs(Chunk.CLOUD_HILL, 15),
    RegionName.Cloud_Hill_NPC_Williams: RoomIDs(Chunk.CLOUD_HILL, 16),
    RegionName.Cloud_Hill_NPC_Diez: RoomIDs(Chunk.CLOUD_HILL, 17),
    RegionName.Cloud_Hill_NPC_Peo: RoomIDs(Chunk.CLOUD_HILL, 18),
    RegionName.Cloud_Hill_NPC_Giz: RoomIDs(Chunk.CLOUD_HILL, 19),
    RegionName.Cloud_Hill_NPC_Stuart: RoomIDs(Chunk.CLOUD_HILL, 20),
    RegionName.Cloud_Hill_NPC_Zeron: RoomIDs(Chunk.CLOUD_HILL, 21),
    RegionName.Cloud_Hill_NPC_Bulls: RoomIDs(Chunk.CLOUD_HILL, 22),
    RegionName.Cloud_Hill_NPC_Mug: RoomIDs(Chunk.CLOUD_HILL, 23),
    RegionName.Cloud_Hill_NPC_Gate_Man: RoomIDs(Chunk.CLOUD_HILL, 24),
}