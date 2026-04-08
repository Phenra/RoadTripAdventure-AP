from typing import Callable, Optional
from enum import IntEnum, StrEnum

from BaseClasses import Region, CollectionState, Entrance, EntranceType
from worlds.AutoWorld import World
from .names import RegionName
from .rules import *
from .options import get_RTA_options, AreaUnlockMode

class ConnectionType(StrEnum):
    Rooms = "Rooms"
    NPCs = "NPCs" # TODO: When an NPC is invited to My City, they disappear from the overworld. This will likely get messed up by randomizer, and will need a patch...
    Regions = "Regions"

    # For converting ConnectionType to randomization group
    def __int__(arg):
        match arg:
            case ConnectionType.Regions: return 0
            case ConnectionType.Rooms: return 1
            case ConnectionType.NPCs: return 2
            case _: raise TypeError("Could not convert passed ConnectionType to int")

# TODO: At run time, create a dictionary of all entrance names, and what the entrance points to now.
# Using that, we can make a lookup table in RTA (RoomData of key -> RoomData of value)
regions = {
    RegionName.Base.Menu: {
        ConnectionType.Regions: {
            RegionName.Base.No_Region,
            RegionName.Base.Peach_Town,
            RegionName.Base.Fuji_City,
            RegionName.Base.My_City,
            RegionName.Base.Sandpolis,
            RegionName.Base.Chestnut_Canyon,
            RegionName.Base.Mushroom_Road,
            RegionName.Base.White_Mountain,
            RegionName.Base.Papaya_Island,
            #RegionName.Base.Papaya_Island_Upper, # Must be accessed through Papaya Island
            #RegionName.Base.Papaya_Island_Island, # Must be accessed through Papaya Island
            #RegionName.Base.Cloud_Hill, # Must be accessed through the warp room
        }
    },
    RegionName.Base.Peach_Town: { # All connections that are logically considered part of Peach Town in AP. This includes some chunks that are technically not Peach Town in-game.
        ConnectionType.Rooms: {
            RegionName.Peach_Town_Qs_Factory,
            RegionName.Peach_Town_Parts_Shop,
            RegionName.Peach_Town_Body_Shop,
            RegionName.Peach_Town_Paint_Shop,
            RegionName.Peach_Town_Bar,
            RegionName.Peach_Town_Police_Station,
            RegionName.Peach_Town_Radio_Station,
            RegionName.Peach_Town_Farm_House,
            RegionName.Peach_Town_Kevin_House,
            RegionName.Peach_Town_Wolf_House,
            RegionName.Peach_Town_Best_House,
            RegionName.Peach_Town_Jousset_House,
            RegionName.Peach_Town_Coffee_Shop,
            RegionName.Peach_Town_Barrel_Dodging,
            RegionName.Peach_Town_Gemstone_House,
            RegionName.Peach_Town_Fight_House,
            RegionName.Peach_Town_Milton_House,
            # RegionName.Peach_Town_Barrel_Dodging_Complete, # Not connected directly to Peach Town
            RegionName.Quick_Pic_1,
            RegionName.Quick_Pic_2,
            RegionName.Quick_Pic_3,
            RegionName.Quick_Pic_4,
            RegionName.Quick_Pic_5,
            RegionName.Quick_Pic_6,
            RegionName.Quick_Pic_7,
            RegionName.Quick_Pic_8,
            RegionName.Quick_Pic_9,
            RegionName.Quick_Pic_10,

            RegionName.Windmill_House,
            RegionName.Quick_Pic_85,
            RegionName.Quick_Pic_86,

            RegionName.Quick_Pic_13,
            RegionName.Quick_Pic_14,
            RegionName.Quick_Pic_15,
            RegionName.Quick_Pic_16,

            RegionName.Quick_Pic_12,

            RegionName.Quick_Pic_11,
        },
        ConnectionType.NPCs: {
            RegionName.Peach_Town_NPC_James,
            RegionName.Peach_Town_NPC_Gonzo,
            RegionName.Peach_Town_NPC_Ramsey,
            RegionName.Peach_Town_NPC_Accel,
            RegionName.Peach_Town_NPC_Cobran,
            RegionName.Peach_Town_NPC_Flower,
            RegionName.Peach_Town_NPC_Klein,
            RegionName.Peach_Town_NPC_Barthou,
            RegionName.Peach_Town_NPC_Pillow,
            RegionName.Peach_Town_NPC_Kevin,
            RegionName.Peach_Town_NPC_Newman,
        },
    },

    RegionName.Base.Fuji_City: {
        ConnectionType.Rooms: {
            RegionName.Fuji_City_Qs_Factory,
            RegionName.Fuji_City_Parts_Shop,
            RegionName.Fuji_City_Body_Shop,
            RegionName.Fuji_City_Paint_Shop,
            RegionName.Fuji_City_Bar,
            RegionName.Fuji_City_Heizo_House,
            RegionName.Fuji_City_Echigoya_Shop,
            RegionName.Fuji_City_Castle_Princess_Nanaha,
            RegionName.Fuji_City_Castle_Sliding_Door_Race,
            RegionName.Fuji_City_Treasure_Hunting,
            RegionName.Fuji_City_Guarded_Dungeon,
            RegionName.Fuji_City_Fortune_Telling_Room,
            RegionName.Fuji_City_Dumpling_Shop,
            RegionName.Fuji_City_Uzumasa_House,
            RegionName.Fuji_City_Iwasuke_House,
            RegionName.Fuji_City_Hakosuke_House,
            RegionName.Fuji_City_Noodle_Shop,
            RegionName.Fuji_City_Highway_Race,
            RegionName.Fuji_City_Hanako_House,
            RegionName.Quick_Pic_17,
            RegionName.Quick_Pic_18,
            RegionName.Quick_Pic_19,
            RegionName.Quick_Pic_20,
            RegionName.Quick_Pic_21,
            RegionName.Quick_Pic_22,
            RegionName.Quick_Pic_23,
            RegionName.Quick_Pic_24,
            RegionName.Quick_Pic_25,
            RegionName.Quick_Pic_26,

            RegionName.Quick_Pic_27,
        },
        ConnectionType.NPCs: {
            RegionName.Fuji_City_NPC_Guard,
            RegionName.Fuji_City_NPC_Toki,
            RegionName.Fuji_City_NPC_Matsugoro,
            RegionName.Fuji_City_NPC_Sakuzo,
            RegionName.Fuji_City_NPC_Shinsaku,
            RegionName.Fuji_City_NPC_Shohei,
            RegionName.Fuji_City_NPC_Brian,
            RegionName.Fuji_City_NPC_Coine,
            RegionName.Fuji_City_NPC_Gichi,
            RegionName.Fuji_City_NPC_Goro,
            RegionName.Fuji_City_NPC_Kiyokichi,
        },
    },

    RegionName.Base.My_City: {
        ConnectionType.Rooms: {
            RegionName.My_City_Qs_Factory,
            RegionName.My_City_Parts_Shop,
            RegionName.My_City_Body_Shop,
            RegionName.My_City_Paint_Shop,
            RegionName.My_City_Police_Station,
            RegionName.My_City_Recycle_Shop,
            RegionName.My_City_Wonder_Realty,
            RegionName.My_City_Bank,
            RegionName.My_City_Theater,
            RegionName.My_City_Tower,
            RegionName.My_City_Which_Way_Maze,
            RegionName.My_City_Fire_Station,
            RegionName.My_City_School,
            RegionName.My_City_Coine_House,
            RegionName.My_City_Kuwano_House,
            RegionName.My_City_Mien_House,
            RegionName.My_City_Flower_House,
            RegionName.My_City_Gichi_House,
            RegionName.My_City_Tunnel_Race,
            RegionName.My_City_Sally_House,
            RegionName.My_City_Rally_Center,
            RegionName.Quick_Pic_28,
            RegionName.Quick_Pic_29,
        },
        ConnectionType.NPCs: {
            RegionName.My_City_NPC_Cobran,
            RegionName.My_City_NPC_Saucy,
            RegionName.My_City_NPC_Sylvester,
            RegionName.My_City_NPC_Velvet,
            RegionName.My_City_NPC_Arnold,
            RegionName.My_City_NPC_Gump,
        },
    },

    RegionName.Base.Sandpolis: {
        ConnectionType.Rooms: {
            RegionName.Sandpolis_Qs_Factory,
            RegionName.Sandpolis_Parts_Shop,
            RegionName.Sandpolis_Body_Shop,
            RegionName.Sandpolis_Paint_Shop,
            RegionName.Sandpolis_Bar,
            RegionName.Sandpolis_Sheriff_Office,
            RegionName.Sandpolis_Figure_8,
            RegionName.Sandpolis_Soccer,
            RegionName.Sandpolis_Roulette,
            RegionName.Sandpolis_Mini_Tower,
            RegionName.Sandpolis_Drag_Race,
            RegionName.Sandpolis_Frank_House,
            RegionName.Sandpolis_Sebastian_House,
            RegionName.Sandpolis_Sand_Sports,
            RegionName.Sandpolis_Mr_King_Mansion,
            RegionName.Sandpolis_Butch_House,
            RegionName.Sandpolis_Barton_House,
            RegionName.Sandpolis_Cake_Shop,
            RegionName.Sandpolis_Merci_House,
            RegionName.Sandpolis_Bob_House,
            RegionName.Sandpolis_Richard_House,
            RegionName.Quick_Pic_36,
            RegionName.Quick_Pic_37,
            RegionName.Quick_Pic_38,
            RegionName.Quick_Pic_39,
            RegionName.Quick_Pic_40,
            RegionName.Quick_Pic_41,
            RegionName.Quick_Pic_42,
            RegionName.Quick_Pic_43,
            RegionName.Quick_Pic_44,
            RegionName.Quick_Pic_45,
            RegionName.Quick_Pic_46,
            RegionName.Quick_Pic_47,

            RegionName.UFO,
            RegionName.Quick_Pic_52,
            RegionName.Quick_Pic_53,
            RegionName.Quick_Pic_54,

            RegionName.Benji_House,
            RegionName.Quick_Pic_48,
            RegionName.Quick_Pic_49,
            RegionName.Quick_Pic_50,
            RegionName.Quick_Pic_51,

            RegionName.Lightouse,
            RegionName.Quick_Pic_55,
            RegionName.Quick_Pic_56,
            RegionName.Quick_Pic_57,

            RegionName.Quick_Pic_30,
            RegionName.Quick_Pic_31,
            RegionName.Quick_Pic_32,
            RegionName.Quick_Pic_33,
            RegionName.Quick_Pic_34,
            RegionName.Quick_Pic_35,
        },
        ConnectionType.NPCs: {
            RegionName.Sandpolis_NPC_Michael,
            RegionName.Sandpolis_NPC_Martin,
            RegionName.Sandpolis_NPC_Ryoji,
            RegionName.Sandpolis_NPC_Akiban,
            RegionName.Sandpolis_NPC_Dayan,
            RegionName.Sandpolis_NPC_Roberts,
            RegionName.Sandpolis_NPC_George,
            RegionName.Sandpolis_NPC_Lisalisa,
            RegionName.Sandpolis_NPC_Morrison,

            RegionName.NPC_Benji,
        },
    },
    
    RegionName.Base.Chestnut_Canyon: {
        ConnectionType.Rooms: {
            RegionName.Chestnut_Canyon_Qs_Factory,
            RegionName.Chestnut_Canyon_Bar,
            RegionName.Chestnut_Canyon_Wallace_House,
            RegionName.Chestnut_Canyon_Greeting_House,
            RegionName.Chestnut_Canyon_M_Carton_House,
            RegionName.Chestnut_Canyon_Rock_Climbing,
            #RegionName.Chestnut_Canyon_Rock_Climbing_Complete, # Not connected directly to Chestnut Canyon
            RegionName.Chestnut_Canyon_Volcano_Run,
            RegionName.Chestnut_Canyon_Tom_House,
            RegionName.Chestnut_Canyon_Lowry_House,
            RegionName.Chestnut_Canyon_Betty_House,
            RegionName.Chestnut_Canyon_Lucy_House,
            RegionName.Quick_Pic_60,
            RegionName.Quick_Pic_61,
            RegionName.Quick_Pic_62,
            RegionName.Quick_Pic_63,
            RegionName.Quick_Pic_64,

            RegionName.Quick_Pic_58,
            RegionName.Quick_Pic_59,
        },
        ConnectionType.NPCs: {
            RegionName.Chestnut_Canyon_NPC_Leon,
            RegionName.Chestnut_Canyon_NPC_Stance,
            RegionName.Chestnut_Canyon_NPC_Matil,
            RegionName.Chestnut_Canyon_NPC_Rectan,
            RegionName.Chestnut_Canyon_NPC_Clary,
            RegionName.Chestnut_Canyon_NPC_Graham,
            RegionName.Chestnut_Canyon_NPC_Wilde,
            RegionName.Chestnut_Canyon_NPC_Mojo,
            RegionName.Chestnut_Canyon_NPC_Saucy,
            RegionName.Chestnut_Canyon_NPC_Kuwano,
            RegionName.Chestnut_Canyon_NPC_Steve,
        },
    },

    RegionName.Base.Mushroom_Road: {
        ConnectionType.Rooms: {
            RegionName.Mushroom_Road_Qs_Factory,
            RegionName.Mushroom_Road_Parts_Shop,
            RegionName.Mushroom_Road_Bar,
            RegionName.Mushroom_Road_Golf,
            RegionName.Mushroom_Road_Goddess,
            RegionName.Quick_Pic_65,
            RegionName.Quick_Pic_66,
            RegionName.Quick_Pic_67,
            RegionName.Quick_Pic_68,
            RegionName.Quick_Pic_69,
            RegionName.Quick_Pic_70,
        },
        # No roaming NPCs in Mushroom Road
    },

    RegionName.Base.White_Mountain: {
        ConnectionType.Rooms: {
            RegionName.White_Mountain_Qs_Factory,
            RegionName.White_Mountain_Parts_Shop,
            RegionName.White_Mountain_Body_Shop,
            RegionName.White_Mountain_Paint_Shop,
            RegionName.White_Mountain_Bar,
            RegionName.White_Mountain_Policeman_House,
            RegionName.White_Mountain_Merrin_House,
            RegionName.White_Mountain_Ski_Jumping,
            RegionName.White_Mountain_Grandma_Dizzy_House,
            RegionName.White_Mountain_Post_Office,
            RegionName.White_Mountain_Santa_House,
            RegionName.White_Mountain_Keitel_House,
            RegionName.White_Mountain_Coin_Radar_House_1,
            RegionName.White_Mountain_Coin_Radar_House_2,
            RegionName.White_Mountain_Coin_Radar_House_3,
            RegionName.White_Mountain_Coin_Radar_House_4,
            RegionName.White_Mountain_Emily_House,
            RegionName.White_Mountain_Bigfoot_Joe_House,
            RegionName.White_Mountain_Curling,
            RegionName.White_Mountain_Wool_Shop,
            RegionName.Quick_Pic_71,
            RegionName.Quick_Pic_72,
            RegionName.Quick_Pic_73,
            RegionName.Quick_Pic_74,
            RegionName.Quick_Pic_75,
            RegionName.Quick_Pic_76,
            RegionName.Quick_Pic_77,

            # Intentionally placed here, and not in Peach Town. This is the Quick-Pic on top of the cliff
            #   by the waterfall, which you can only access via White Mountain (w/o physics exploits, at least).
            RegionName.Quick_Pic_84,

            RegionName.Temple_Under_the_Sea,
            RegionName.Quick_Pic_78,
            RegionName.Quick_Pic_79,

            RegionName.Quick_Pic_80,
            RegionName.Quick_Pic_81,
            RegionName.Quick_Pic_82,
            RegionName.Quick_Pic_83,
        },
        ConnectionType.NPCs: {
            RegionName.White_Mountain_NPC_Jack,
            RegionName.White_Mountain_NPC_Charles,
            RegionName.White_Mountain_NPC_Hitomi,
            RegionName.White_Mountain_NPC_Brown,
            RegionName.White_Mountain_NPC_Blonty,
            RegionName.White_Mountain_NPC_Shirley,
            RegionName.White_Mountain_NPC_Nick,
            RegionName.White_Mountain_NPC_Suess,
            RegionName.White_Mountain_NPC_Manei,
            RegionName.White_Mountain_NPC_Sally,

            RegionName.NPC_Orpheus,
        },
    },

    RegionName.Base.Papaya_Island: {
        ConnectionType.Rooms: {
            RegionName.Papaya_Island_Qs_Factory,
            RegionName.Papaya_Island_Parts_Shop,
            RegionName.Papaya_Island_Body_Shop,
            RegionName.Papaya_Island_Bar,
            RegionName.Papaya_Island_Policeman_House,
            RegionName.Papaya_Island_Mayor_House,
            RegionName.Papaya_Island_Luke_House,
            RegionName.Papaya_Island_Andy_House,
            RegionName.Papaya_Island_Shirley_House,
            RegionName.Papaya_Island_Casa_House,
            RegionName.Papaya_Island_Beach_Flag,
            RegionName.Papaya_Island_Fishing,
            RegionName.Quick_Pic_87,
            RegionName.Quick_Pic_88,
            RegionName.Quick_Pic_89,
            RegionName.Quick_Pic_93,
            RegionName.Quick_Pic_95,
            RegionName.Quick_Pic_96,
        },
        ConnectionType.NPCs: {
            RegionName.Papaya_Island_NPC_Mond,
            RegionName.Papaya_Island_NPC_John,
            RegionName.Papaya_Island_NPC_Kerori,
            RegionName.Papaya_Island_NPC_Nairo,
            RegionName.Papaya_Island_NPC_Moisy,
            RegionName.Papaya_Island_NPC_Nouri,
            RegionName.Papaya_Island_NPC_Kite,
            RegionName.Papaya_Island_NPC_Mien,
            RegionName.Papaya_Island_NPC_Michael,
        },
        ConnectionType.Regions: {
            RegionName.Base.Papaya_Island_Upper,
            RegionName.Base.Papaya_Island_Island,
        },
    },

    RegionName.Base.Papaya_Island_Upper: {
        ConnectionType.Rooms: {
            RegionName.Papaya_Island_Obstacle_Course,
            RegionName.Papaya_Island_Grandpa_Costello_House,
            RegionName.Papaya_Island_Sandro_House,
            RegionName.Papaya_Island_Coconut_Shop,
            RegionName.Papaya_Island_Papu_Tree,
            RegionName.Quick_Pic_90,
            RegionName.Quick_Pic_91,
            RegionName.Quick_Pic_94,
        },
        ConnectionType.NPCs: {
            RegionName.Papaya_Island_NPC_Minerva,
        },
    },

    RegionName.Base.Papaya_Island_Island: {
        ConnectionType.Rooms: {
            RegionName.Quick_Pic_92,
            RegionName.Papaya_Island_Cloud_Hill_Warp,
        },  
    },
    RegionName.Base.Cloud_Hill: {
        ConnectionType.Rooms: {
            RegionName.Cloud_Hill_Qs_Factory,
            RegionName.Cloud_Hill_Parts_Shop,
            RegionName.Cloud_Hill_Body_Shop,
            RegionName.Cloud_Hill_Paint_Shop,
            RegionName.Cloud_Hill_Single_Lap_Race,
            RegionName.Cloud_Hill_Duck_House,
            RegionName.Cloud_Hill_Rainbow_Jump,
            RegionName.Cloud_Hill_Invalid_Room,
            RegionName.Cloud_Hill_White_House_Lobby,
            #RegionName.Cloud_Hill_President_Room, # Not connected directly to Cloud Hill
            RegionName.Quick_Pic_97,
            RegionName.Quick_Pic_98,
            RegionName.Quick_Pic_99,
            RegionName.Quick_Pic_100,
        },
        ConnectionType.NPCs: {
            RegionName.Cloud_Hill_NPC_Yumyum,
            RegionName.Cloud_Hill_NPC_Dust,
            RegionName.Cloud_Hill_NPC_Williams,
            RegionName.Cloud_Hill_NPC_Diez,
            RegionName.Cloud_Hill_NPC_Peo,
            RegionName.Cloud_Hill_NPC_Giz,
            RegionName.Cloud_Hill_NPC_Stuart,
            RegionName.Cloud_Hill_NPC_Zeron,
            RegionName.Cloud_Hill_NPC_Bulls,
            RegionName.Cloud_Hill_NPC_Mug,
            RegionName.Cloud_Hill_NPC_Gate_Man,
        },
    },

    # Rooms that link to other rooms/regions
    RegionName.Peach_Town_Barrel_Dodging: {
        ConnectionType.Rooms: {
            RegionName.Peach_Town_Barrel_Dodging_Complete
        }
    },

    RegionName.Chestnut_Canyon_Rock_Climbing: {
        ConnectionType.Rooms: {
            RegionName.Chestnut_Canyon_Rock_Climbing_Complete
        }
    },

    RegionName.Papaya_Island_Cloud_Hill_Warp: {
        ConnectionType.Regions: {
            RegionName.Base.Cloud_Hill
        }
    },

    RegionName.Cloud_Hill_White_House_Lobby: {
        ConnectionType.Rooms: {
            RegionName.Cloud_Hill_President_Room
        }
    }
}

# ------------------------------------------

# Defining a few access rule functions for the base regions
# These can't be defined in-line just from lambdas because they require an if statement (to check options),
#   which can't be used in lambdas
def can_access_fuji_city(state: CollectionState, player: int) -> bool:
    options = get_RTA_options(state.multiworld, player)

    # TODO: Should we also require Quick Steering and Soft Brakes to entire Fuji, like with the other base regions?
    #if not hasSteeringOfLevel(1, state, player) or not hasBrakesOfLevel(1, state, player):
    #    return False
    
    if options.area_unlock_mode == AreaUnlockMode.option_decorations:
        return state.has(ItemName.Gold_Ornament_Key, player) or state.has(ItemName.Policemans_Club_Key, player)
    
    elif options.area_unlock_mode == AreaUnlockMode.option_stamps:
        requiredStamps = 5
        return state.count(ItemName.Stamp, player) >= requiredStamps

    else:
        raise Exception("Road Trip: Area Unlock Mode is not Decorations or Stamps, please fix your YAML.")

def can_access_sandpolis(state: CollectionState, player: int) -> bool:
    options = get_RTA_options(state.multiworld, player)

    # Require Quick Steering and Soft Brakes to encourage the randomization to place a steering upgrade
    #   and brakes upgrade earlier in the multiworld.
    if not has_steering_of_level(1, state, player) or not has_brakes_of_level(1, state, player):
        return False

    if options.area_unlock_mode == AreaUnlockMode.option_decorations:
        return state.has(ItemName.Mini_Tower_Key, player) or state.has(ItemName.Toy_Gun_Key, player)
    
    elif options.area_unlock_mode == AreaUnlockMode.option_stamps:
        requiredStamps = 10
        return state.count(ItemName.Stamp, player) >= requiredStamps

    else:
        raise Exception("Road Trip: Area Unlock Mode is not Decorations or Stamps, please fix your YAML.")

def can_access_chestnut_canyon(state: CollectionState, player: int) -> bool:
    options = get_RTA_options(state.multiworld, player)

    # Require Quick Steering and Soft Brakes to encourage the randomization to place a steering upgrade
    #   and brakes upgrade earlier in the multiworld.
    if not has_steering_of_level(1, state, player) or not has_brakes_of_level(1, state, player):
        return False

    if options.area_unlock_mode == AreaUnlockMode.option_decorations:
        return state.has(ItemName.Model_Train_Key, player) or state.has(ItemName.M_Cartons_Painting_Key, player)
    
    elif options.area_unlock_mode == AreaUnlockMode.option_stamps:
        requiredStamps = 15
        return state.count(ItemName.Stamp, player) >= requiredStamps

    else:
        raise Exception("Road Trip: Area Unlock Mode is not Decorations or Stamps, please fix your YAML.")

def can_access_mushroom_road(state: CollectionState, player: int) -> bool:
    options = get_RTA_options(state.multiworld, player)

    # Require Quick Steering and Soft Brakes to encourage the randomization to place a steering upgrade
    #   and brakes upgrade earlier in the multiworld.
    if not has_steering_of_level(1, state, player) or not has_brakes_of_level(1, state, player):
        return False

    if options.area_unlock_mode == AreaUnlockMode.option_decorations:
        return state.has(ItemName.Flower_Pattern_Key, player) or state.has(ItemName.Sky_Pattern_Key, player)
    
    elif options.area_unlock_mode == AreaUnlockMode.option_stamps:
        requiredStamps = 20
        return state.count(ItemName.Stamp, player) >= requiredStamps

def can_access_white_mountain(state: CollectionState, player: int) -> bool:
    options = get_RTA_options(state.multiworld, player)

    # Require Quick Steering and Soft Brakes to encourage the randomization to place a steering upgrade
    #   and brakes upgrade earlier in the multiworld.
    if not has_steering_of_level(1, state, player) or not has_brakes_of_level(1, state, player):
        return False

    if options.area_unlock_mode == AreaUnlockMode.option_decorations:
        return state.has(ItemName.Christmas_Tree_Key, player) or state.has(ItemName.Arctic_Pattern_Key, player)
    
    elif options.area_unlock_mode == AreaUnlockMode.option_stamps:
        requiredStamps = 25
        return state.count(ItemName.Stamp, player) >= requiredStamps

def can_access_papaya_island(state: CollectionState, player: int) -> bool:
    options = get_RTA_options(state.multiworld, player)

    # Require Quick Steering and Soft Brakes to encourage the randomization to place a steering upgrade
    #   and brakes upgrade earlier in the multiworld.
    if not has_steering_of_level(1, state, player) or not has_brakes_of_level(1, state, player):
        return False

    if options.area_unlock_mode == AreaUnlockMode.option_decorations:
        return state.has(ItemName.UnbaboDoll_Key, player) or state.has(ItemName.Papaya_Ukulele_Key, player)
    
    elif options.area_unlock_mode == AreaUnlockMode.option_stamps:
        requiredStamps = 30
        return state.count(ItemName.Stamp, player) >= requiredStamps

def can_access_cloud_hill(state: CollectionState, player: int) -> bool:
    options = get_RTA_options(state.multiworld, player)

    # Require Quick Steering and Soft Brakes to encourage the randomization to place a steering upgrade
    #   and brakes upgrade earlier in the multiworld.
    if not has_steering_of_level(1, state, player) or not has_brakes_of_level(1, state, player):
        return False

    if options.area_unlock_mode == AreaUnlockMode.option_decorations:
        return state.has(ItemName.Gods_Rod_Key, player) or state.has(ItemName.Angels_Wings_Key, player)
    
    elif options.area_unlock_mode == AreaUnlockMode.option_stamps:
        requiredStamps = 35
        return state.count(ItemName.Stamp, player) >= requiredStamps

# ------------------------------------------

access_rules : dict[str, Callable[[CollectionState, int], bool]] = {
    RegionName.Base.Fuji_City:
        lambda state, player:
            can_access_fuji_city(state, player),
    
    RegionName.Base.Sandpolis:
        lambda state, player:
            can_access_sandpolis(state, player),
    
    RegionName.Base.Chestnut_Canyon:
        lambda state, player:
            can_access_chestnut_canyon(state, player),

    RegionName.Base.Mushroom_Road:
        lambda state, player:
            can_access_mushroom_road(state, player),

    RegionName.Base.White_Mountain:
        lambda state, player:
            can_access_white_mountain(state, player),

    RegionName.Base.Papaya_Island:
        lambda state, player:
            can_access_papaya_island(state, player),

    RegionName.Base.Cloud_Hill:
        lambda state, player:
            can_access_cloud_hill(state, player),

    RegionName.Base.Papaya_Island_Upper: 
        lambda state, player:
            has_tires_of_level(1, state, player) and
            has_steering_of_level(1, state, player) and
            has_brakes_of_level(1, state, player) and
            state.has(ItemName.Jet_Turbine, player) or
            (
                has_engine_of_level(1, state, player) and
                has_chassis_of_level(1, state, player) and
                has_transmission_of_level(1, state, player)
            ) or
            (
                has_engine_of_level(3, state, player) # This is possible with 2 (Blue MAX), but setting this to 3 (Blue MAX v2) to be safe
            ),

    RegionName.Base.Papaya_Island_Island:
        lambda state, player:
            has_engine_of_level(6, state, player) and
            has_steering_of_level(1, state, player) and    # Not required to reach the island, but including here to encourage earlier placement of a steering upgrade
            has_brakes_of_level(1, state, player) and      # Not required to reach the island, but including here to encourage earlier placement of a brake upgrade
            (
                state.has(ItemName.Jet_Turbine, player) or
                (
                    state.has(ItemName.Propeller, player) and
                    state.has(ItemName.Wing_Set, player)
                )
            ),
    
    #RegionName.Peach_Town_Barrel_Dodging_Complete: lambda state, player: True # Barrel Dodging can be completed with no part upgrades

    RegionName.Chestnut_Canyon_Rock_Climbing_Complete: 
        lambda state, player: 
            has_steering_of_level(1, state, player),

    # My City
    RegionName.My_City_Qs_Factory: 
        lambda state, player: 
            state.can_reach_region(RegionName.Peach_Town_NPC_Gonzo, player),
    
    RegionName.My_City_Parts_Shop: 
        lambda state, player: 
            state.can_reach_region(RegionName.White_Mountain_NPC_Suess, player),
    
    RegionName.My_City_Body_Shop: 
        lambda state, player: 
            state.can_reach_region(RegionName.Peach_Town_NPC_Ramsey, player),

    RegionName.My_City_Paint_Shop: 
        lambda state, player: 
            state.can_reach_region(RegionName.Papaya_Island_NPC_Nouri, player),

    RegionName.My_City_Police_Station: 
        lambda state, player: 
            state.can_reach_region(RegionName.Peach_Town_NPC_Accel, player),
    
    RegionName.My_City_Bank: 
        lambda state, player: 
            state.can_reach_region(RegionName.White_Mountain_NPC_Manei, player),
    
    RegionName.My_City_Theater: 
        lambda state, player: 
            state.can_reach_region(RegionName.Sandpolis_NPC_George, player),
    
    RegionName.My_City_Tower: 
        lambda state, player: 
            state.can_reach_region(RegionName.Sandpolis_NPC_Roberts, player),
    
    RegionName.My_City_Which_Way_Maze: 
        lambda state, player: 
            state.can_reach_region(RegionName.Sandpolis_NPC_Dayan, player),
    
    RegionName.My_City_Fire_Station: 
        lambda state, player: 
            state.can_reach_region(RegionName.Fuji_City_NPC_Brian, player),
    
    RegionName.My_City_School: 
        lambda state, player: 
            state.can_reach_region(RegionName.Sandpolis_NPC_Ryoji, player),
    
    RegionName.My_City_Coine_House: 
        lambda state, player: 
            state.can_reach_region(RegionName.Fuji_City_NPC_Coine, player),
    
    RegionName.My_City_Kuwano_House: 
        lambda state, player: 
            state.can_reach_region(RegionName.Chestnut_Canyon_NPC_Kuwano, player),
    
    RegionName.My_City_Mien_House: 
        lambda state, player: 
            state.can_reach_region(RegionName.Papaya_Island_NPC_Mien, player),

    RegionName.My_City_Flower_House: 
        lambda state, player: 
            state.can_reach_region(RegionName.Peach_Town_NPC_Flower, player),
    
    RegionName.My_City_Gichi_House: 
        lambda state, player: 
            state.can_reach_region(RegionName.Fuji_City_NPC_Gichi, player),
    
    RegionName.My_City_Tunnel_Race: 
        lambda state, player: 
            state.can_reach_region(RegionName.Sandpolis_NPC_Akiban, player),
    
    RegionName.My_City_Sally_House: 
        lambda state, player: 
            state.can_reach_region(RegionName.White_Mountain_NPC_Sally, player),

    RegionName.My_City_Rally_Center:
        lambda state, player:
            # Rally Center does not unlock until the player has visited all Qs Factories (including those not actually visited during the rally).
            state.can_reach_region(RegionName.Sandpolis_Qs_Factory, player) and # 1st checkpoint
            state.can_reach_region(RegionName.Chestnut_Canyon_Qs_Factory, player) and # 2nd checkpoint
            state.can_reach_region(RegionName.White_Mountain_Qs_Factory, player) and # 3rd checkpoint
            state.can_reach_region(RegionName.Peach_Town_Qs_Factory, player) and # 4th checkpoint
            state.can_reach_region(RegionName.Fuji_City_Qs_Factory, player) and # 5th checkpoint
            state.can_reach_region(RegionName.My_City_Qs_Factory, player) and # Final checkpoint

            state.can_reach_region(RegionName.Mushroom_Road_Qs_Factory, player) and
            state.can_reach_region(RegionName.Papaya_Island_Qs_Factory, player) and
            state.can_reach_region(RegionName.Cloud_Hill_Qs_Factory, player),

    RegionName.Quick_Pic_28: 
        lambda state, player: 
            can_access_everything_in_my_city(state, player),

    # Quick-Pic 29 appears in My City once the Endurance Run has been completed - not necessarily won.
    # However, we currently don't expect the player to attempt Endurance Run until they can realistically
    #     clear it. Quick-Pic 29 should match this, so we use the same access rule as Stamp 49 
    #     ("Participated in the Endurance Race").
    RegionName.Quick_Pic_29: 
        lambda state, player: 
            state.can_reach_region(RegionName.My_City_Qs_Factory, player) and
            can_clear_endurance_run(state, player),

    RegionName.My_City_NPC_Cobran: 
        lambda state, player: 
            state.can_reach_region(RegionName.Peach_Town_NPC_Cobran, player),
    
    RegionName.My_City_NPC_Saucy: 
        lambda state, player: 
            state.can_reach_region(RegionName.Chestnut_Canyon_NPC_Saucy, player),
    
    RegionName.My_City_NPC_Sylvester: 
        lambda state, player: 
            state.can_reach_region(RegionName.Sandpolis_NPC_Dayan, player),
    
    RegionName.My_City_NPC_Velvet: 
        lambda state, player: 
            state.can_reach_region(RegionName.Fuji_City_NPC_Brian, player),
    
    RegionName.My_City_NPC_Arnold: 
        lambda state, player: 
            state.can_reach_region(RegionName.Sandpolis_NPC_Roberts, player),
    
    RegionName.My_City_NPC_Gump: 
        lambda state, player: 
            state.can_reach_region(RegionName.Sandpolis_NPC_Ryoji, player),
}

# ----------------------------------------------

# Called by __init__.py
def create_regions_RTA(world: World):
    # First, let's define some private helper functions.
    def get_region_names_in_world(world: World):
        return world.multiworld.regions.region_cache[world.player].keys()

    def create_region_if_unique(region: str, world: World):
        if region not in get_region_names_in_world(world):
            world.multiworld.regions += [Region(region, world.player, world.multiworld)]
        else:
            pass # this is fine, not an error

    def connect_regions(src: str, dest: str, world: World, connection_type : ConnectionType, access_rule : Callable[[CollectionState, int], bool]) -> Entrance:
        # Get the actual Region objects of the region names provided.
        src_region = world.multiworld.get_region(src, world.player)
        dest_region = world.multiworld.get_region(dest, world.player)

        # Create the Entrance.
        # NOTE: All entrances use their destination as the name. All *should* be unique, there shouldn't
        #     be multiple ways into a region in Road Trip (given that base regions are connected to Menu, 
        #     not to each other). A new progression mode could cause this to change in the future, though.
        connection = Entrance(world.player, dest, src_region, int(connection_type), EntranceType.ONE_WAY)

        # If the access_rule lambda has a player parameter, create a new partial function that will always set that argument
        #     to a static value, world.player. The partial function's signature will then only have a state parameter.
        #     Needed since the access_rule property on the Entrance class actually only has a state parameter.
        access_rule = apply_player_to_access_rule(access_rule, world.player)

        # Apply provided access rule to the Entrance.
        # If none, set the access_rule to always return True.
        connection.access_rule = access_rule if access_rule else lambda state: True

        # Connect the entrance to the destination.
        connection.connect(dest_region)

        # Connect the source to the entrance (since apparently the connect method does not do this?)
        src_region.exits.append(connection)

        return connection

    def register_indirect_conditions(world: World):
        # If an access rule for an Entrance (i.e. a region-to-region connection) calls any of the below methods on the state
        #     object, then it must be registered as an indirect connection:
        #   - state.can_reach_region
        #   - state.can_reach_location (because it calls state.can_reach_region)
        #   - state.can_reach_entrance (because it calls state.can_reach_region)
        #
        # According to the AP documentation, this is because:
        #     "For efficiency reasons, every time reachable regions are searched, every entrance is only checked once in a 
        #     somewhat non-deterministic order."
        # So (if I understand this correctly), if AP were to check the accessibility of regions in the wrong order by chance, 
        #     it might miss that (for example) being able to access an NPC you can invite to My City means that their house 
        #     in My City is now also logically reachable. This is because the region sweep might have already checked that 
        #     house's entrance rule, and now won't check it again.
        # Registering this link as an indirect condition will cause AP to redo that check if it runs into this situation.
        #
        # https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#an-important-note-on-entrance-access-rules

        region_to_region_it_unlocks = {
            RegionName.Peach_Town_NPC_Gonzo: RegionName.My_City_Qs_Factory,
            RegionName.White_Mountain_NPC_Suess: RegionName.My_City_Parts_Shop,
            RegionName.Peach_Town_NPC_Ramsey: RegionName.My_City_Body_Shop,
            RegionName.Papaya_Island_NPC_Nouri: RegionName.My_City_Paint_Shop,
            RegionName.Peach_Town_NPC_Accel: RegionName.My_City_Police_Station,
            RegionName.White_Mountain_NPC_Manei: RegionName.My_City_Bank,
            RegionName.Sandpolis_NPC_George: RegionName.My_City_Theater,
            RegionName.Sandpolis_NPC_Roberts: {
                RegionName.My_City_Tower,
                RegionName.My_City_NPC_Arnold,
            },
            RegionName.Sandpolis_NPC_Dayan: {
                RegionName.My_City_Which_Way_Maze,
                RegionName.My_City_NPC_Sylvester,
            },
            RegionName.Fuji_City_NPC_Brian: {
                RegionName.My_City_Fire_Station,
                RegionName.My_City_NPC_Velvet,
            },
            RegionName.Sandpolis_NPC_Ryoji: {
                RegionName.My_City_School,
                RegionName.My_City_NPC_Gump,
            },
            RegionName.Fuji_City_NPC_Coine: RegionName.My_City_Coine_House,
            RegionName.Chestnut_Canyon_NPC_Kuwano: RegionName.My_City_Kuwano_House,
            RegionName.Papaya_Island_NPC_Mien: RegionName.My_City_Mien_House,
            RegionName.Peach_Town_NPC_Flower: RegionName.My_City_Flower_House,
            RegionName.Fuji_City_NPC_Gichi: RegionName.My_City_Gichi_House,
            RegionName.Sandpolis_NPC_Akiban: RegionName.My_City_Tunnel_Race,
            RegionName.White_Mountain_NPC_Sally: RegionName.My_City_Sally_House,
            RegionName.My_City_Qs_Factory: {
                RegionName.Quick_Pic_29,
                RegionName.My_City_Rally_Center # See note below
            },
            RegionName.Peach_Town_NPC_Cobran: RegionName.My_City_NPC_Cobran,
            RegionName.Chestnut_Canyon_NPC_Saucy: RegionName.My_City_NPC_Saucy,
            
            # For Rally Center - any Q's Factory could be the final one visited that unlocks it
            RegionName.Peach_Town_Qs_Factory: RegionName.My_City_Rally_Center,
            RegionName.Fuji_City_Qs_Factory: RegionName.My_City_Rally_Center,
            # RegionName.My_City_Qs_Factory: RegionName.My_City_Rally_Center, # Already handled above
            RegionName.Sandpolis_Qs_Factory: RegionName.My_City_Rally_Center,
            RegionName.Chestnut_Canyon_Qs_Factory: RegionName.My_City_Rally_Center,
            RegionName.Mushroom_Road_Qs_Factory: RegionName.My_City_Rally_Center,
            RegionName.White_Mountain_Qs_Factory: RegionName.My_City_Rally_Center,
            RegionName.Papaya_Island_Qs_Factory: RegionName.My_City_Rally_Center,
            RegionName.Cloud_Hill_Qs_Factory: RegionName.My_City_Rally_Center,
        }

        for src_name, destinations in region_to_region_it_unlocks.items():
            if isinstance(destinations, str):
                destinations = {destinations}

            for dest_name in destinations:
                src = world.get_region(src_name)
                dest = world.get_entrance(dest_name)
                world.multiworld.register_indirect_condition(src, dest)
        
        # For Quick-Pic 28, add indirect conditions noting that any NPC invite to My City could be
        #   the last one that unlocks its entrance. Needed for stamps 50, 51, and 96.
        # TODO: Do we need to add all base regions, as well?
        dest = world.get_entrance(RegionName.Quick_Pic_28)
        for npc_region in my_city_invites_list:
            src = world.get_region(npc_region)
            world.multiworld.register_indirect_condition(src, dest)

    # -----------------------------------------------------

    # For each top level region:
    #    Create if does not exist
    #    For each region in each connectionType:
    #         Create it if it does not exist
    #         Now that it for sure exists, connect base region to this region, with correct randomization group, AND pull access_rule if it has one
    # Finally, register all indirect conditions

    for region in regions:
        # First, get the actual dictionary object that contains all of this region's connections.
        # The 'region' variable is a String.
        region_dict = regions[region]

        # Create the region if it does not already exist.
        create_region_if_unique(region, world)

        connection = None

        # Next, for every *base* region this one connects to (if any), create it, and then create 
        #     the entrance between the two (with the correct access_rule applied).
        if ConnectionType.Regions in region_dict:
            for subRegion in region_dict[ConnectionType.Regions]:
                create_region_if_unique(subRegion, world)
                access_rule = access_rules.get(subRegion) # get() returns None if key not found in dictionary
                connection = connect_regions(region, subRegion, world, ConnectionType.Regions, access_rule)

        # Next, do the same for all rooms this region connects to (if any).
        if ConnectionType.Rooms in region_dict:
            for room in region_dict[ConnectionType.Rooms]:
                create_region_if_unique(room, world)
                access_rule = access_rules.get(room)
                connection = connect_regions(region, room, world, ConnectionType.Rooms, access_rule)

        # Finally, do the same for all NPCs this region connects to (if any).
        if ConnectionType.NPCs in region_dict:
            for npc in region_dict[ConnectionType.NPCs]:
                create_region_if_unique(npc, world)
                access_rule = access_rules.get(npc) 
                connection = connect_regions(region, npc, world, ConnectionType.NPCs, access_rule)

        #if connection:
        #    world.vanillaConnections += [connection]

    register_indirect_conditions(world)
