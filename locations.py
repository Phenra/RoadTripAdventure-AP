from typing import Callable, NamedTuple, Any
from BaseClasses import CollectionState
from worlds.AutoWorld import World

from .names import ItemName, LocationName, RegionName
from .categories import double_up_stamps, challenge_minigames
from .rules import *
from .options import get_RTA_options, LicenseHandling

class LocationData(NamedTuple):
    id: int
    region: RegionName
    access_rule: Callable[[CollectionState, int], bool] = lambda state: True

class BASE_IDS():
    LICENSES = 1
    WORLD_GP = 5
    RACES = 10
    STAMPS = 200
    ITEMS = 1000
    SHOP_PURCHASES = 2000
    COMBINED = 10000

races_c_rank : dict[str, LocationData] = {
    # NOTE: IDs reflect the internal order in race results.
    LocationName.Peach_Raceway_Rank_C: LocationData(
        id = BASE_IDS.RACES + 0,
        region = RegionName.Peach_Town_Qs_Factory,
        # Default access_rule - location always accessible
    ),

    LocationName.Ninja_Temple_Raceway_Rank_C: LocationData(
        id = BASE_IDS.RACES + 3,
        region = RegionName.Fuji_City_Qs_Factory,
        access_rule = lambda state, player:
            has_engine_of_level(1, state, player) or # TODO: Maybe set up ItemName to int conversion function, so this could use 'ItemName.Panther_Engine' instead of 1?
            has_chassis_of_level(1, state, player) or
            has_transmission_of_level(1, state, player) or
            has_tires_of_level(2, state, player)
    ),

    LocationName.Desert_Raceway_Rank_C: LocationData(
        id = BASE_IDS.RACES + 6,
        region = RegionName.Sandpolis_Qs_Factory,
        access_rule = lambda state, player:
            has_engine_of_level(1, state, player) or
            has_tires_of_level(1, state, player) or
            (
                has_chassis_of_level(2, state, player) and 
                has_transmission_of_level(1, state, player) and 
                has_steering_of_level(1, state, player)
            )
    ),

    LocationName.Miner_49er_Raceway_Rank_C: LocationData(
        id = BASE_IDS.RACES + 10,
        region = RegionName.Chestnut_Canyon_Qs_Factory, 
        access_rule = lambda state, player:
        (
            has_tires_of_level(2, state, player) and 
            has_steering_of_level(1, state, player)
        ) or 
        (
            has_engine_of_level(2, state, player) and 
            has_steering_of_level(1, state, player)
        )
    ),

    LocationName.River_Raceway_Rank_C: LocationData(
        id = BASE_IDS.RACES + 14,
        region = RegionName.Mushroom_Road_Qs_Factory,
        access_rule = lambda state, player:
            has_tires_of_level(2, state, player) and 
            has_steering_of_level(1, state, player)
    ),

    LocationName.Slick_Track_Rank_C: LocationData(
        id = BASE_IDS.RACES + 15,
        region = RegionName.Mushroom_Road_Qs_Factory,
        access_rule = lambda state, player:
        (
            has_engine_of_level(2, state, player) and 
            has_steering_of_level(1, state, player)
        ) or
        (
            has_tires_of_level(1, state, player) and 
            has_steering_of_level(1, state, player)
        ) or
        (
            has_tires_of_level(5, state, player)
        )
    )
}

races_b_rank : dict[str, LocationData] = {
    # NOTE: IDs reflect the internal order in race results.
    LocationName.Peach_Raceway_Rank_B: LocationData(
        id = BASE_IDS.RACES + 1,
        region = RegionName.Peach_Town_Qs_Factory,
        access_rule = lambda state, player:
        ((
            has_tires_of_level(9, state, player) and
            has_engine_of_level(3, state, player) and
            has_chassis_of_level(1, state, player) and
            has_transmission_of_level(1, state, player) and
            has_steering_of_level(1, state, player) and
            has_brakes_of_level(1, state, player)
        ) or
        (
            has_tires_of_level(4, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(1, state, player) and
            has_transmission_of_level(1, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        )) and
        has_license_count(1, state, player)
    ),

    LocationName.Temple_Raceway_Rank_B: LocationData(
        id = BASE_IDS.RACES + 4,
        region = RegionName.Fuji_City_Qs_Factory,
        access_rule = lambda state, player:
            has_tires_of_level(1, state, player) and
            has_engine_of_level(3, state, player) and
            has_chassis_of_level(1, state, player) and
            has_transmission_of_level(1, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player) and
            has_license_count(1, state, player)
    ),

    LocationName.Desert_Raceway_Rank_B: LocationData(
        id = BASE_IDS.RACES + 7,
        region = RegionName.Sandpolis_Qs_Factory,
        access_rule = lambda state, player:
        ((
            has_tires_of_level(6, state, player) and
            has_engine_of_level(4, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        ) or
        (
            has_tires_of_level(1, state, player) and
            has_engine_of_level(6, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        )) and
        has_license_count(1, state, player)
    ),

    LocationName.Night_Glow_Raceway_Rank_B: LocationData(
        id = BASE_IDS.RACES + 8,
        region = RegionName.Sandpolis_Qs_Factory,
        access_rule = lambda state, player:
            # The AI pathing in Night Glow Rank B is terrible, this can actually be
            #   cleared with only Normal parts.
            has_license_count(1, state, player)
    ),

    LocationName.Lava_Run_Raceway_Rank_B: LocationData(
        id = BASE_IDS.RACES + 12,
        region = RegionName.Chestnut_Canyon_Qs_Factory,
        access_rule = lambda state, player:
        (
            has_tires_of_level(1, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        ) and
        has_license_count(1, state, player)   
    ),

    LocationName.Oval_Raceway_Rank_B: LocationData(
        id = BASE_IDS.RACES + 16,
        region = RegionName.Mushroom_Road_Qs_Factory,
        access_rule = lambda state, player:
        ((
            has_tires_of_level(4, state, player) and
            has_engine_of_level(6, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        ) or
        (
            has_tires_of_level(9, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        )) and
        has_license_count(1, state, player)
    ),

    LocationName.Snow_Mountain_Raceway_Rank_B: LocationData(
        id = BASE_IDS.RACES + 18,
        region = RegionName.White_Mountain_Qs_Factory,
        access_rule = lambda state, player:
            has_tires_of_level(3, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player) and
            has_license_count(1, state, player)
    ),

    LocationName.Sunny_Beach_Raceway_Rank_B: LocationData(
        id = BASE_IDS.RACES + 20,
        region = RegionName.Papaya_Island_Qs_Factory,
        access_rule = lambda state, player:
            has_tires_of_level(2, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player) and
            has_license_count(1, state, player)
    ),

    LocationName.Lagoon_Raceway_Rank_B: LocationData(
        id = BASE_IDS.RACES + 22,
        region = RegionName.Papaya_Island_Qs_Factory,
        access_rule = lambda state, player:
        ((
            state.count(ItemName.Propeller, player) > 1 and
            has_tires_of_level(1, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        ) or
        (
            has_tires_of_level(6, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        )) and
        has_license_count(1, state, player)
    ),
}

races_a_rank : dict[str, LocationData] = {
    # NOTE: IDs reflect the internal order in race results.
    LocationName.Peach_Raceway_Rank_A: LocationData(
        id = BASE_IDS.RACES + 2,
        region = RegionName.Peach_Town_Qs_Factory,
        access_rule = lambda state, player:
        (
            has_tires_of_level(9, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)
        ) and
        has_license_count(2, state, player) 
    ),

    LocationName.Temple_Raceway_Rank_A: LocationData(
        id = BASE_IDS.RACES + 5,
        region = RegionName.Fuji_City_Qs_Factory,
        access_rule = lambda state, player:
        (
            has_tires_of_level(1, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)
        ) and
        has_license_count(2, state, player)     
    ),

    LocationName.Night_Glow_Raceway_Rank_A: LocationData(
        id = BASE_IDS.RACES + 9,
        region = RegionName.Sandpolis_Qs_Factory,
        access_rule = lambda state, player:
        (
            has_tires_of_level(2, state, player) and
            has_engine_of_level(6, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)
        ) and
        has_license_count(2, state, player)    
    ),

    LocationName.Miner_49er_Raceway_Rank_A: LocationData(
        id = BASE_IDS.RACES + 11,
        region = RegionName.Chestnut_Canyon_Qs_Factory,
        access_rule = lambda state, player:
        (
            has_tires_of_level(6, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)
        ) and
        has_license_count(2, state, player)    
    ),

    LocationName.Lava_Run_Raceway_Rank_A: LocationData(
        id = BASE_IDS.RACES + 13,
        region = RegionName.Chestnut_Canyon_Qs_Factory,
        access_rule = lambda state, player:
        ((
            has_tires_of_level(6, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)
        ) or
        (
            has_tires_of_level(1, state, player) and
            has_engine_of_level(7, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)               
        )) and
        has_license_count(2, state, player)
    ),

    LocationName.Slick_Track_Rank_A: LocationData(
        id = BASE_IDS.RACES + 17,
        region = RegionName.Mushroom_Road_Qs_Factory,
        access_rule = lambda state, player:
        (
            has_tires_of_level(5, state, player) and
            has_engine_of_level(6, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)           
        ) and
        has_license_count(2, state, player)
    ),

    LocationName.Snow_Mountain_Raceway_Rank_A: LocationData(
        id = BASE_IDS.RACES + 19,
        region = RegionName.White_Mountain_Qs_Factory,
        access_rule = lambda state, player:
        (
            has_tires_of_level(3, state, player) and
            has_engine_of_level(6, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)           
        ) and
        has_license_count(2, state, player)
    ),

    LocationName.Sunny_Beach_Raceway_Rank_A: LocationData(
        id = BASE_IDS.RACES + 21,
        region = RegionName.Papaya_Island_Qs_Factory,
        access_rule = lambda state, player:
        (
            has_tires_of_level(2, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)           
        ) and
        has_license_count(2, state, player)    
    ),

    LocationName.Lagoon_Raceway_Rank_A: LocationData(
        id = BASE_IDS.RACES + 23,
        region = RegionName.Papaya_Island_Qs_Factory,
        access_rule = lambda state, player:
        ((
            state.count(ItemName.Propeller, player) > 1 and
            has_tires_of_level(1, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        ) or
        (
            has_tires_of_level(6, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        )) and
        has_license_count(2, state, player)
    ),
}

races_other : dict[str, LocationData] = {
    # NOTE: IDs reflect the internal order in race results.
    LocationName.Endurance_Run: LocationData(
        id = BASE_IDS.RACES + 24, 
        region = RegionName.My_City_Qs_Factory, 
        access_rule = lambda state, player:
            can_clear_endurance_run(state, player)
    ),

    LocationName.Tin_Raceway: LocationData(
        id = BASE_IDS.RACES + 25, 
        region = RegionName.Cloud_Hill_Qs_Factory, 
        access_rule = lambda state, player:
        (
            has_tires_of_level(4, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(1, state, player)
        ) and
        has_license_count(2, state, player)
    ),
}

stamps : dict[str, LocationData] = {
    LocationName.Stamp_1: LocationData(BASE_IDS.STAMPS + 0, RegionName.Base.Peach_Town),
    LocationName.Stamp_2: LocationData(BASE_IDS.STAMPS + 1, RegionName.Peach_Town_Farm_House),
    LocationName.Stamp_3: LocationData(BASE_IDS.STAMPS + 2, RegionName.Peach_Town_Radio_Station,
        access_rule = lambda state, player:
            state.has(ItemName.Voucher, player)
    ),
    LocationName.Stamp_4: LocationData(BASE_IDS.STAMPS + 3, RegionName.Peach_Town_NPC_Kevin),
    LocationName.Stamp_5: LocationData(BASE_IDS.STAMPS + 4, RegionName.Peach_Town_Police_Station, 
        access_rule = lambda state, player:
            state.has(ItemName.Wallet, player)
    ),
    LocationName.Stamp_6: LocationData(BASE_IDS.STAMPS + 5, RegionName.Peach_Town_Barrel_Dodging_Complete),
    LocationName.Stamp_7: LocationData(BASE_IDS.STAMPS + 6, RegionName.Peach_Town_Fight_House, 
        access_rule = lambda state, player:
            state.has(ItemName.Magazine, player)
    ),
    LocationName.Stamp_8: LocationData(BASE_IDS.STAMPS + 7, RegionName.Peach_Town_NPC_James, 
        access_rule = lambda state, player:
            state.has(ItemName.Peach, player)
    ),
    LocationName.Stamp_9: LocationData(BASE_IDS.STAMPS + 8, RegionName.Peach_Town_Gemstone_House, 
        access_rule = lambda state, player:
            has_all_gemstones(state, player)
    ),
    LocationName.Stamp_10: LocationData(BASE_IDS.STAMPS + 9, RegionName.Base.Fuji_City),
    LocationName.Stamp_11: LocationData(BASE_IDS.STAMPS + 10, RegionName.Fuji_City_Castle_Princess_Nanaha),
    LocationName.Stamp_12: LocationData(BASE_IDS.STAMPS + 11, RegionName.Fuji_City_Heizo_House),
    LocationName.Stamp_13: LocationData(BASE_IDS.STAMPS + 12, RegionName.Fuji_City_Treasure_Hunting),
    LocationName.Stamp_14: LocationData(BASE_IDS.STAMPS + 13, RegionName.Fuji_City_Treasure_Hunting),
    LocationName.Stamp_15: LocationData(BASE_IDS.STAMPS + 14, RegionName.Fuji_City_Treasure_Hunting),
    LocationName.Stamp_16: LocationData(BASE_IDS.STAMPS + 15, RegionName.Fuji_City_Castle_Sliding_Door_Race),
    LocationName.Stamp_17: LocationData(BASE_IDS.STAMPS + 16, RegionName.Fuji_City_Guarded_Dungeon),
    LocationName.Stamp_18: LocationData(BASE_IDS.STAMPS + 17, RegionName.Fuji_City_Iwasuke_House),
    LocationName.Stamp_19: LocationData(BASE_IDS.STAMPS + 18, RegionName.Fuji_City_Hakosuke_House),
    LocationName.Stamp_20: LocationData(BASE_IDS.STAMPS + 19, RegionName.Fuji_City_Fortune_Telling_Room),
    LocationName.Stamp_21: LocationData(BASE_IDS.STAMPS + 20, RegionName.Fuji_City_Highway_Race, 
        access_rule = lambda state, player:
            can_clear_highway_race(state, player)
    ),
    LocationName.Stamp_22: LocationData(BASE_IDS.STAMPS + 21, RegionName.Fuji_City_Highway_Race,
        # Identical to Stamp 21. From testing, it seems like if you can clear the race, you can clear it under 50 seconds.
        access_rule = lambda state, player:
            can_clear_highway_race(state, player)
    ),
    LocationName.Stamp_23: LocationData(BASE_IDS.STAMPS + 22, RegionName.Base.Sandpolis),
    LocationName.Stamp_24: LocationData(BASE_IDS.STAMPS + 23, RegionName.Sandpolis_Mini_Tower),
    LocationName.Stamp_25: LocationData(BASE_IDS.STAMPS + 24, RegionName.Sandpolis_Frank_House),
    LocationName.Stamp_26: LocationData(BASE_IDS.STAMPS + 25, RegionName.Sandpolis_NPC_Lisalisa, # TODO: Does Lisalisa only check for Night Glow?
        access_rule = lambda state, player:
            state.can_reach_location(LocationName.Night_Glow_Raceway_Rank_B, player) or
            state.can_reach_location(LocationName.Night_Glow_Raceway_Rank_A, player)
    ),
    LocationName.Stamp_27: LocationData(BASE_IDS.STAMPS + 26, RegionName.Sandpolis_Drag_Race, 
        access_rule = lambda state, player:
            has_tires_of_level(9, state, player) and
            ((
                has_engine_of_level(6, state, player) and
                has_chassis_of_level(3, state, player)
            ) or
            (
                has_engine_of_level(7, state, player) and
                has_chassis_of_level(2, state, player)
            ) or
            (
                has_engine_of_level(8, state, player) and
                has_chassis_of_level(1, state, player) and
                has_transmission_of_level(1, state, player)
            ))
    ),
    LocationName.Stamp_28: LocationData(BASE_IDS.STAMPS + 27, RegionName.Sandpolis_Drag_Race, 
        access_rule = lambda state, player:
            has_engine_of_level(9, state, player) and
            has_tires_of_level(9, state, player) and
            has_chassis_of_level(4, state, player) and
            has_transmission_of_level(5, state, player)
    ),
    LocationName.Stamp_29: LocationData(BASE_IDS.STAMPS + 28, RegionName.Sandpolis_Roulette),
    LocationName.Stamp_30: LocationData(BASE_IDS.STAMPS + 29, RegionName.Sandpolis_Butch_House,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Sheriff_Office, player)
    ),
    LocationName.Stamp_31: LocationData(BASE_IDS.STAMPS + 30, RegionName.Sandpolis_Mr_King_Mansion, 
        access_rule = lambda state, player:
            state.has(ItemName.Soccer_Ball, player)
    ),
    LocationName.Stamp_32: LocationData(BASE_IDS.STAMPS + 31, RegionName.Sandpolis_Figure_8),
    LocationName.Stamp_33: LocationData(BASE_IDS.STAMPS + 32, RegionName.Sandpolis_Figure_8),
    LocationName.Stamp_34: LocationData(BASE_IDS.STAMPS + 33, RegionName.Sandpolis_Figure_8),
    LocationName.Stamp_35: LocationData(BASE_IDS.STAMPS + 34, RegionName.Sandpolis_Figure_8),
    LocationName.Stamp_36: LocationData(BASE_IDS.STAMPS + 35, RegionName.Sandpolis_Figure_8),
    LocationName.Stamp_37: LocationData(BASE_IDS.STAMPS + 36, RegionName.Sandpolis_Soccer),
    LocationName.Stamp_38: LocationData(BASE_IDS.STAMPS + 37, RegionName.Sandpolis_Soccer, 
        access_rule = lambda state, player:
            can_clear_soccer(state, player)
    ),
    LocationName.Stamp_39: LocationData(BASE_IDS.STAMPS + 38, RegionName.NPC_Benji, 
        access_rule = lambda state, player:
            state.has(ItemName.Fountain_Pen, player)
    ),
    LocationName.Stamp_40: LocationData(BASE_IDS.STAMPS + 39, RegionName.My_City_Wonder_Realty),
    LocationName.Stamp_41: LocationData(BASE_IDS.STAMPS + 40, RegionName.My_City_Flower_House, 
        access_rule = lambda state, player:
            state.has(ItemName.Flower_Seed, player)
    ),
    LocationName.Stamp_42: LocationData(BASE_IDS.STAMPS + 41, RegionName.My_City_Fire_Station),
    LocationName.Stamp_43: LocationData(BASE_IDS.STAMPS + 42, RegionName.My_City_Tunnel_Race),
    LocationName.Stamp_44: LocationData(BASE_IDS.STAMPS + 43, RegionName.My_City_Tunnel_Race),
    LocationName.Stamp_45: LocationData(BASE_IDS.STAMPS + 44, RegionName.My_City_Tower),
    LocationName.Stamp_46: LocationData(BASE_IDS.STAMPS + 45, RegionName.My_City_Coine_House,
        access_rule = lambda state, player:
            city_access_count_for_QCoins(state, player) >= 7
    ),
    LocationName.Stamp_47: LocationData(BASE_IDS.STAMPS + 46, RegionName.My_City_Which_Way_Maze),
    LocationName.Stamp_48: LocationData(BASE_IDS.STAMPS + 47, RegionName.My_City_Rally_Center, 
        access_rule = lambda state, player:
            has_engine_of_level(5, state, player) and
            has_tires_of_level(2, state, player) and
            has_chassis_of_level(1, state, player) and 
            has_transmission_of_level(1, state, player) and
            has_steering_of_level(1, state, player)
    ),
    LocationName.Stamp_49: LocationData(BASE_IDS.STAMPS + 48, RegionName.My_City_Qs_Factory,
        # Don't expect the player to attempt Endurance Run until they can realistically clear it.
        access_rule = lambda state, player:
            can_clear_endurance_run(state, player)
    ),
    LocationName.Stamp_50: LocationData(BASE_IDS.STAMPS + 49, RegionName.Base.My_City,
        access_rule = lambda state, player:
            can_access_everything_in_my_city(state, player) and
            can_clear_endurance_run(state, player)
    ),
    LocationName.Stamp_51: LocationData(BASE_IDS.STAMPS + 50, RegionName.Base.My_City,
        access_rule = lambda state, player:
            can_access_everything_in_my_city(state, player)
    ),
    LocationName.Stamp_52: LocationData(BASE_IDS.STAMPS + 51, RegionName.Base.Chestnut_Canyon),
    LocationName.Stamp_53: LocationData(BASE_IDS.STAMPS + 52, RegionName.Chestnut_Canyon_M_Carton_House),
    LocationName.Stamp_54: LocationData(BASE_IDS.STAMPS + 53, RegionName.Chestnut_Canyon_Wallace_House),
    LocationName.Stamp_55: LocationData(BASE_IDS.STAMPS + 54, RegionName.Chestnut_Canyon_Volcano_Run, 
        access_rule = lambda state, player:
            has_steering_of_level(1, state, player)
    ),
    LocationName.Stamp_56: LocationData(BASE_IDS.STAMPS + 55, RegionName.Chestnut_Canyon_Volcano_Run, 
        access_rule = lambda state, player:
            has_tires_of_level(9, state, player) and
            has_engine_of_level(8, state, player) and
            has_chassis_of_level(3, state, player) and 
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)
    ),
    LocationName.Stamp_57: LocationData(BASE_IDS.STAMPS + 56, RegionName.Chestnut_Canyon_Rock_Climbing_Complete),
    LocationName.Stamp_58: LocationData(BASE_IDS.STAMPS + 57, RegionName.Chestnut_Canyon_Rock_Climbing_Complete, 
        access_rule = lambda state, player:
            has_steering_of_level(1, state, player)
    ),
    LocationName.Stamp_59: LocationData(BASE_IDS.STAMPS + 58, RegionName.Chestnut_Canyon_Greeting_House),
    LocationName.Stamp_60: LocationData(BASE_IDS.STAMPS + 59, RegionName.Base.White_Mountain),
    LocationName.Stamp_61: LocationData(BASE_IDS.STAMPS + 60, RegionName.White_Mountain_Grandma_Dizzy_House),
    LocationName.Stamp_62: LocationData(BASE_IDS.STAMPS + 61, RegionName.White_Mountain_Bigfoot_Joe_House),
    LocationName.Stamp_63: LocationData(BASE_IDS.STAMPS + 62, RegionName.White_Mountain_Merrin_House,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.NPC_Orpheus, player)                                        
    ),
    LocationName.Stamp_64: LocationData(BASE_IDS.STAMPS + 63, RegionName.White_Mountain_Emily_House, 
        access_rule = lambda state, player:
            state.has(ItemName.Papu_Flower, player)
    ),
    LocationName.Stamp_65: LocationData(BASE_IDS.STAMPS + 64, RegionName.White_Mountain_Post_Office,
        access_rule = lambda state, player:
            state.has(ItemName.Package, player)
    ),
    LocationName.Stamp_66: LocationData(BASE_IDS.STAMPS + 65, RegionName.White_Mountain_Ski_Jumping, 
        access_rule = lambda state, player:
            state.has(ItemName.Jet_Turbine, player)    
    ),
    LocationName.Stamp_67: LocationData(BASE_IDS.STAMPS + 66, RegionName.White_Mountain_Santa_House),
    LocationName.Stamp_68: LocationData(BASE_IDS.STAMPS + 67, RegionName.White_Mountain_Keitel_House,
        access_rule = lambda state, player:
            can_reach_all_coin_radar_houses(state, player)     
    ),
    LocationName.Stamp_69: LocationData(BASE_IDS.STAMPS + 68, RegionName.White_Mountain_Curling),
    LocationName.Stamp_70: LocationData(BASE_IDS.STAMPS + 69, RegionName.White_Mountain_Curling, 
        access_rule = lambda state, player:
            has_chassis_of_level(1, state, player) 
    ),
    LocationName.Stamp_71: LocationData(BASE_IDS.STAMPS + 70, RegionName.White_Mountain_Policeman_House,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Lightouse, player)                                        
    ),
    LocationName.Stamp_72: LocationData(BASE_IDS.STAMPS + 71, RegionName.Base.Papaya_Island,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Base.Papaya_Island_Upper, player) and 
            state.can_reach_region(RegionName.Base.Papaya_Island_Island, player) 
    ),
    LocationName.Stamp_73: LocationData(BASE_IDS.STAMPS + 72, RegionName.Papaya_Island_Luke_House),
    LocationName.Stamp_74: LocationData(BASE_IDS.STAMPS + 73, RegionName.Papaya_Island_Grandpa_Costello_House),
    LocationName.Stamp_75: LocationData(BASE_IDS.STAMPS + 74, RegionName.Papaya_Island_Obstacle_Course, 
        access_rule = lambda state, player:
            has_tires_of_level(1, state, player) and
            state.has(ItemName.Jet_Turbine, player)
    ),
    LocationName.Stamp_76: LocationData(BASE_IDS.STAMPS + 75, RegionName.Papaya_Island_Obstacle_Course, 
        access_rule = lambda state, player:
            has_tires_of_level(1, state, player) and
            state.has(ItemName.Jet_Turbine, player)    
    ),
    LocationName.Stamp_77: LocationData(BASE_IDS.STAMPS + 76, RegionName.Papaya_Island_Papu_Tree),
    LocationName.Stamp_78: LocationData(BASE_IDS.STAMPS + 77, RegionName.Papaya_Island_Beach_Flag,
        access_rule = lambda state, player:
            can_clear_beach_flag(state, player)
    ),
    LocationName.Stamp_79: LocationData(BASE_IDS.STAMPS + 78, RegionName.Papaya_Island_Mayor_House),
    LocationName.Stamp_80: LocationData(BASE_IDS.STAMPS + 79, RegionName.Papaya_Island_Shirley_House,
        # In order for Shirley to appear in her house, you first need to give the roaming NPC Shirley Uzumasa's Autograph.
        #   Then you can visit her and give her the Fluffy Mushroom.
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.White_Mountain_NPC_Shirley, player) and
            state.has(ItemName.Uzumasas_Autograph, player) and
            state.has(ItemName.Fluffy_Mushroom, player)
    ),
    LocationName.Stamp_81: LocationData(BASE_IDS.STAMPS + 80, RegionName.Papaya_Island_NPC_Kerori),
    LocationName.Stamp_82: LocationData(BASE_IDS.STAMPS + 81, RegionName.Papaya_Island_Fishing),
    LocationName.Stamp_83: LocationData(BASE_IDS.STAMPS + 82, RegionName.Papaya_Island_Casa_House),
    LocationName.Stamp_84: LocationData(BASE_IDS.STAMPS + 83, RegionName.Papaya_Island_NPC_Minerva,
        access_rule = lambda state, player:
            state.has(ItemName.Small_Bottle, player)
    ),
    LocationName.Stamp_85: LocationData(BASE_IDS.STAMPS + 84, RegionName.Base.Cloud_Hill,
        access_rule = lambda state, player:
            # Stamp 85 (Visited all the houses in Cloud Hill) includes the White House
            state.can_reach_location(LocationName.World_GP_Completed, player)
    ),
    LocationName.Stamp_86: LocationData(BASE_IDS.STAMPS + 85, RegionName.Cloud_Hill_NPC_Dust),
    LocationName.Stamp_87: LocationData(BASE_IDS.STAMPS + 86, RegionName.Cloud_Hill_NPC_Yumyum),
    LocationName.Stamp_88: LocationData(BASE_IDS.STAMPS + 87, RegionName.Cloud_Hill_Single_Lap_Race, # TODO: Add Single-Lap Race to challenge category?
        access_rule = lambda state, player:
            can_clear_single_lap_race(state, player)
    ),
    LocationName.Stamp_89: LocationData(BASE_IDS.STAMPS + 88, RegionName.Cloud_Hill_Duck_House),
    LocationName.Stamp_90: LocationData(BASE_IDS.STAMPS + 89, RegionName.Cloud_Hill_Rainbow_Jump, 
        access_rule = lambda state, player:
            can_clear_rainbow_jump(state, player)
    ),
    LocationName.Stamp_91: LocationData(BASE_IDS.STAMPS + 90, RegionName.Base.Mushroom_Road),
    LocationName.Stamp_92: LocationData(BASE_IDS.STAMPS + 91, RegionName.Mushroom_Road_Goddess),
    LocationName.Stamp_93: LocationData(BASE_IDS.STAMPS + 92, RegionName.Mushroom_Road_Golf, 
        # Golf doesn't require anything to play, but leaving this without logic could theoretically result in a
        #   playthrough where the player has to play Golf before they have any chance of getting a score below 36 
        #   (for stamp 94), which would be a very annoying (and time-consuming) experience.
        # Setting this to require the Jet Turbine to match Stamp 94 (see its comment below).
        access_rule = lambda state, player:
            state.has(ItemName.Jet_Turbine, player)
    ),
    LocationName.Stamp_94: LocationData(BASE_IDS.STAMPS + 93, RegionName.Mushroom_Road_Golf, 
        # You can get a score below 36 without the Jet Turbine, but... it takes forever and is annoying.
        # It's maybe not terrible with some of the best late-game gear, but determining what parts are good 
        #   enough would take more testing, which *also* takes a very long time with Golf.
        access_rule = lambda state, player:
            state.has(ItemName.Jet_Turbine, player)
    ),
    LocationName.Stamp_95: LocationData(BASE_IDS.STAMPS + 94, RegionName.My_City_Wonder_Realty
        # NOTE: If randomizing starting city is at some point supported, this will need an access rule that 
        #       checks to see if you can complete at least one race (since, unlike with Peach Town, you may be 
        #       placed in a starting town at the beginning of the game where you can't, making this stamp inaccessible).
    ),
    LocationName.Stamp_96: LocationData(BASE_IDS.STAMPS + 95, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            can_access_all_quick_pic_shops(state, player)
    ),
    LocationName.Stamp_97: LocationData(BASE_IDS.STAMPS + 96, RegionName.Windmill_House),
    LocationName.Stamp_98: LocationData(BASE_IDS.STAMPS + 97, RegionName.NPC_Orpheus),
    LocationName.Stamp_99: LocationData(BASE_IDS.STAMPS + 98, RegionName.UFO),
    LocationName.Stamp_100: LocationData(BASE_IDS.STAMPS + 99, RegionName.Cloud_Hill_President_Room, # Victory condition
        access_rule = lambda state, player:
            state.can_reach_location(LocationName.World_GP_Completed, player) and
            has_license_count(3, state, player) and
            ((
                state.has(ItemName.Jet_Turbine, player) and
                has_tires_of_level(9, state, player) and
                has_engine_of_level(5, state, player) and
                has_chassis_of_level(2, state, player) and
                has_transmission_of_level(2, state, player) and
                has_steering_of_level(2, state, player) and
                has_brakes_of_level(2, state, player)
            ) or
            (
                has_tires_of_level(11, state, player) and
                has_engine_of_level(7, state, player) and
                has_chassis_of_level(4, state, player) and
                has_transmission_of_level(5, state, player) and
                has_steering_of_level(3, state, player) and
                has_brakes_of_level(3, state, player)
            ))
    ),
}

items_received : dict[str, LocationData] = {
    # NOTE: IDs below match the vanilla reward item's offset
    #   e.g. Body Q001 is the 1st item, Billboard Coffee Shop is the 223rd item, etc.
    #   (assuming all item tables are combined in order)
    
    # In RTA AP, instead of the game giving you the vanilla item, it's patched to set the bit of
    #   the item's ID to 1 in our custom bitfield used for tracking NPC item reward locations.
    #   (See 'items_obtained' in the client's Addresses file.)

    LocationName.Billboard_Coffee_Shop: LocationData(BASE_IDS.ITEMS + 222, RegionName.Peach_Town_Coffee_Shop),
    LocationName.Billboard_Noodle_Shop: LocationData(BASE_IDS.ITEMS + 223, RegionName.Fuji_City_Noodle_Shop),
    LocationName.Billboard_Cake_Shop: LocationData(BASE_IDS.ITEMS + 224, RegionName.Sandpolis_Cake_Shop),
    LocationName.Billboard_Wool_Shop: LocationData(BASE_IDS.ITEMS + 225, RegionName.White_Mountain_Wool_Shop),
    LocationName.Billboard_Coconut_Shop: LocationData(BASE_IDS.ITEMS + 226, RegionName.Papaya_Island_Coconut_Shop),
    LocationName.Coine_Reward_1: LocationData(BASE_IDS.ITEMS + 85, RegionName.My_City_Coine_House),
    LocationName.Coine_Reward_2: LocationData(BASE_IDS.ITEMS + 79, RegionName.My_City_Coine_House,
        access_rule = lambda state, player:
            #state.can_reach_region(RegionName.Base.My_City, player) and
            city_access_count_for_QCoins(state, player) >= 2
    ),
    LocationName.Coine_Reward_3: LocationData(BASE_IDS.ITEMS + 80, RegionName.My_City_Coine_House,
        access_rule = lambda state, player:
            #state.can_reach_region(RegionName.Base.My_City, player) and
            city_access_count_for_QCoins(state, player) >= 3
        ),
    LocationName.Coine_Reward_4: LocationData(BASE_IDS.ITEMS + 83, RegionName.My_City_Coine_House,
        access_rule = lambda state, player:
            #state.can_reach_region(RegionName.Base.My_City, player) and
            city_access_count_for_QCoins(state, player) >= 4
        ),
    LocationName.Coine_Reward_5: LocationData(BASE_IDS.ITEMS + 162, RegionName.My_City_Coine_House,
        access_rule = lambda state, player:
            #state.can_reach_region(RegionName.Base.My_City, player) and
            city_access_count_for_QCoins(state, player) >= 5
        ),
    LocationName.Coine_Reward_6: LocationData(BASE_IDS.ITEMS + 190, RegionName.My_City_Coine_House,
        access_rule = lambda state, player:
            #state.can_reach_region(RegionName.Base.My_City, player) and
            city_access_count_for_QCoins(state, player) >= 6
        ),
    LocationName.Coine_Reward_7: LocationData(BASE_IDS.ITEMS + 186, RegionName.My_City_Coine_House,
        access_rule = lambda state, player:
            #state.can_reach_region(RegionName.Base.My_City, player) and
            city_access_count_for_QCoins(state, player) >= 7
        ),
    LocationName.Coine_Reward_8: LocationData(BASE_IDS.ITEMS + 180, RegionName.My_City_Coine_House,
        access_rule = lambda state, player:
            #state.can_reach_region(RegionName.Base.My_City, player) and
            city_access_count_for_QCoins(state, player) >= 7
        ),
    LocationName.Coine_Reward_9: LocationData(BASE_IDS.ITEMS + 194, RegionName.My_City_Coine_House,
        access_rule = lambda state, player:
            #state.can_reach_region(RegionName.Base.My_City, player) and
            city_access_count_for_QCoins(state, player) >= 7
        ),
    LocationName.Coine_Reward_10: LocationData(BASE_IDS.ITEMS + 174, RegionName.My_City_Coine_House,
        access_rule = lambda state, player:
            #state.can_reach_region(RegionName.Base.My_City, player) and
            city_access_count_for_QCoins(state, player) >= 7
        ),
    LocationName.Trade_Quest_1: LocationData(BASE_IDS.ITEMS + 280, RegionName.Peach_Town_Fight_House), # Gives Hero Super Card in vanilla
    LocationName.Trade_Quest_2: LocationData(BASE_IDS.ITEMS + 281, RegionName.Sandpolis_Barton_House, # Gives Pretty Doll in vanilla
        access_rule = lambda state, player:
            state.has(ItemName.Hero_Super_Card, player)
    ),
    LocationName.Trade_Quest_3: LocationData(BASE_IDS.ITEMS + 282, RegionName.Chestnut_Canyon_NPC_Wilde, # Gives Relief in vanilla
        access_rule = lambda state, player:
            state.has(ItemName.Pretty_Doll, player)
    ),
    LocationName.Trade_Quest_4: LocationData(BASE_IDS.ITEMS + 283, RegionName.Fuji_City_Uzumasa_House, # Gives Uzumasa's Autograph in vanilla
        access_rule = lambda state, player:
            state.has(ItemName.Relief, player)
    ),
    LocationName.Trade_Quest_5: LocationData(BASE_IDS.ITEMS + 284, RegionName.Papaya_Island_Shirley_House, # Gives Rice Ball in vanilla
        access_rule = lambda state, player:
            state.has(ItemName.Uzumasas_Autograph, player)
    ),
    LocationName.Trade_Quest_6: LocationData(BASE_IDS.ITEMS + 285, RegionName.Cloud_Hill_NPC_Williams, # Gives Canary Recorder in vanilla
        access_rule = lambda state, player:
            state.has(ItemName.Rice_Ball, player)
    ),
    LocationName.Trade_Quest_7: LocationData(BASE_IDS.ITEMS + 286, RegionName.Papaya_Island_NPC_Moisy, # Gives Magazine in vanilla
        access_rule = lambda state, player:
            state.has(ItemName.Canary_Recorder, player)    
    ),
    LocationName.Angels_Wings: LocationData(BASE_IDS.ITEMS + 276, RegionName.Cloud_Hill_NPC_Dust),
    LocationName.Arctic_Pattern: LocationData(BASE_IDS.ITEMS + 264, RegionName.White_Mountain_Bigfoot_Joe_House),
    LocationName.Baby_Horn: LocationData(BASE_IDS.ITEMS + 242, RegionName.Chestnut_Canyon_Greeting_House),
    LocationName.Body_Q003: LocationData(BASE_IDS.ITEMS + 2, RegionName.NPC_Orpheus),
    LocationName.Body_Q030: LocationData(BASE_IDS.ITEMS + 29, RegionName.My_City_Fire_Station),
    LocationName.Body_Q034: LocationData(BASE_IDS.ITEMS + 33, RegionName.White_Mountain_Post_Office, 
        # Rewarded by going back to the White Mountain post office after delivering the Package to Jousset.
        # In order to do this, the player needs both the Package, and access to Jousset's house (in addition to the White Mountain Post Office region).
        # We could set this access rule to 'state.can_reach_location("LocationName.Stamp_65, player)', but just in case Stamp 65 is ever
        #     changed to a double-up stamp in the future (and therefore sometimes removed from the location pool), I think it's safer to  
        #     write the full requirements out here as well.
        access_rule = lambda state, player:
            state.has(ItemName.Package, player) and
            state.can_reach_region(RegionName.Peach_Town_Jousset_House, player)
    ),
    LocationName.Body_Q037: LocationData(BASE_IDS.ITEMS + 36, RegionName.White_Mountain_Merrin_House,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.NPC_Orpheus, player)
    ),
    LocationName.Body_Q082: LocationData(BASE_IDS.ITEMS + 81, RegionName.White_Mountain_Policeman_House,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Lightouse, player)    
    ),
    LocationName.Body_Q085: LocationData(BASE_IDS.ITEMS + 84, RegionName.My_City_Tunnel_Race),
    LocationName.Body_Q087: LocationData(BASE_IDS.ITEMS + 86, RegionName.Peach_Town_Gemstone_House, # Reward for Stamp 9 (Gemstones)
        access_rule = lambda state, player:
            has_all_gemstones(state, player)
    ),
    LocationName.Body_Q089: LocationData(BASE_IDS.ITEMS + 88, RegionName.My_City_Rally_Center, 
        # Technically, completing Q's Rally doesn't require anything (other than access to all Q's Factories to unlock it).
        # However, logically expecting it early would be annoying, since it could take a pretty long time to complete.
        # The below parts requirement is based on a rough idea of what would be needed to travel semi-quickly through it.

        # Also, adding a time limit to this in AP would be cool in the future - the below could be what is needed to reasonably
        #     finish within the time limit.
        # However, the time limit would have to be lenient enough to be completable with these parts even in a worst-case 
        #     room rando situation...

        # TODO: In room rando, the code in Road Trip that prevents the player from entering non-Q's Factory houses during the rally 
        #     will need an update to allow entry to the houses that *actually* lead to the Q's Factories post-rando (and disallow
        #     access to what used to be Q's Factories, unless they still contain them).
        # TODO: Having any of the 6 Q's Factories stopped at during the Rally placed in Cloud Hill would make the Rally impossible to
        #     complete, as reaching Cloud Hill requires either entering the warp house (not allowed during the rally) or warping there
        #     (also not allowed during the rally). We could potentially modify the rally code to allow one of those specifically for
        #     accessing Cloud Hill, though.
        access_rule = lambda state, player:
            has_engine_of_level(5, state, player) and
            has_tires_of_level(2, state, player) and
            has_chassis_of_level(1, state, player) and
            has_transmission_of_level(1, state, player) and
            has_steering_of_level(1, state, player)
    ),
    LocationName.Body_Q150: LocationData(BASE_IDS.ITEMS + 150, RegionName.Peach_Town_Fight_House, # Reward for giving Magazine to Fight
        access_rule = lambda state, player:
            state.has(ItemName.Magazine, player)
    ),
    LocationName.Cherry_Meter: LocationData(BASE_IDS.ITEMS + 251, RegionName.Fuji_City_Treasure_Hunting),
    LocationName.Chicken_Horn: LocationData(BASE_IDS.ITEMS + 235, RegionName.NPC_Benji, 
        access_rule = lambda state, player:
            state.has(ItemName.Fountain_Pen, player)    
    ),
    LocationName.Christmas_Horn: LocationData(BASE_IDS.ITEMS + 238, RegionName.White_Mountain_Santa_House),
    LocationName.Christmas_Tree: LocationData(BASE_IDS.ITEMS + 273, RegionName.White_Mountain_Grandma_Dizzy_House),
    LocationName.Coin_Radar: LocationData(BASE_IDS.ITEMS + 300, RegionName.White_Mountain_Keitel_House,
        access_rule = lambda state, player:
            can_reach_all_coin_radar_houses(state, player)
        ),
    LocationName.Duck_Quiz_1: LocationData(BASE_IDS.ITEMS + 252, RegionName.Cloud_Hill_Duck_House),
    LocationName.Duck_Quiz_2: LocationData(BASE_IDS.ITEMS + 239, RegionName.Cloud_Hill_Duck_House),
    LocationName.Duck_Quiz_3: LocationData(BASE_IDS.ITEMS + 82, RegionName.Cloud_Hill_Duck_House),
    LocationName.Fantasy_Horn: LocationData(BASE_IDS.ITEMS + 236, RegionName.Windmill_House),
    LocationName.Flower_Pattern: LocationData(BASE_IDS.ITEMS + 256, RegionName.My_City_Flower_House, 
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_NPC_Flower, player) and
            state.has(ItemName.Flower_Seed, player)
    ),
    LocationName.Flower_Seed: LocationData(BASE_IDS.ITEMS + 296, RegionName.White_Mountain_Emily_House, 
        access_rule = lambda state, player:
            state.has(ItemName.Papu_Flower, player)
    ),
    LocationName.Gods_Rod: LocationData(BASE_IDS.ITEMS + 277, RegionName.Cloud_Hill_NPC_Yumyum),
    LocationName.Gold_Ornament: LocationData(BASE_IDS.ITEMS + 267, RegionName.Fuji_City_Castle_Princess_Nanaha),
    LocationName.Hide_Out_Pattern: LocationData(BASE_IDS.ITEMS + 260, RegionName.Sandpolis_Butch_House,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Sheriff_Office, player)
    ),
    LocationName.Jet_Turbine: LocationData(BASE_IDS.ITEMS + 217, RegionName.Papaya_Island_Sandro_House),
    LocationName.Local_Peach_Wine: LocationData(BASE_IDS.ITEMS + 265, RegionName.Peach_Town_Farm_House),
    LocationName.Love_Sick_Meter: LocationData(BASE_IDS.ITEMS + 249, RegionName.Fuji_City_Guarded_Dungeon),
    LocationName.M_Cartons_Painting: LocationData(BASE_IDS.ITEMS + 271, RegionName.Chestnut_Canyon_M_Carton_House),
    LocationName.Mini_Tower: LocationData(BASE_IDS.ITEMS + 269, RegionName.Sandpolis_Mini_Tower),
    LocationName.Model_Train: LocationData(BASE_IDS.ITEMS + 272, RegionName.Chestnut_Canyon_Wallace_House),
    LocationName.Package: LocationData(BASE_IDS.ITEMS + 301, RegionName.White_Mountain_Post_Office),
    LocationName.Papaya_Ukulele: LocationData(BASE_IDS.ITEMS + 275, RegionName.Papaya_Island_Grandpa_Costello_House),
    LocationName.Peach_Doll: LocationData(BASE_IDS.ITEMS + 266, RegionName.Peach_Town_Radio_Station,
        access_rule = lambda state, player:
            state.has(ItemName.Voucher, player)    
    ),
    LocationName.Policemans_Club: LocationData(BASE_IDS.ITEMS + 268, RegionName.Fuji_City_Heizo_House),
    LocationName.Police_Light: LocationData(BASE_IDS.ITEMS + 221, RegionName.My_City_Police_Station),
    LocationName.Propeller: LocationData(BASE_IDS.ITEMS + 216, RegionName.Temple_Under_the_Sea),
    LocationName.RS_Magnum: LocationData(BASE_IDS.ITEMS + 172, RegionName.My_City_Which_Way_Maze),
    LocationName.Rainbow_Meter: LocationData(BASE_IDS.ITEMS + 246, RegionName.Cloud_Hill_Rainbow_Jump, 
        access_rule = lambda state, player:
            can_clear_rainbow_jump(state, player)
    ),
    LocationName.Room_with_a_View: LocationData(BASE_IDS.ITEMS + 261, RegionName.Fuji_City_Fortune_Telling_Room),
    LocationName.Sky_Pattern: LocationData(BASE_IDS.ITEMS + 257, RegionName.Cloud_Hill_Single_Lap_Race, 
        access_rule = lambda state, player:
            can_clear_single_lap_race(state, player)
    ),
    LocationName.Soccer_Ball: LocationData(BASE_IDS.ITEMS + 294, RegionName.Sandpolis_Sand_Sports),
    LocationName.Soccer_Pattern: LocationData(BASE_IDS.ITEMS + 258, RegionName.Sandpolis_Soccer, 
        access_rule = lambda state, player:
            can_clear_soccer(state, player)
    ),
    LocationName.Space_Meter: LocationData(BASE_IDS.ITEMS + 247, RegionName.My_City_Tunnel_Race),
    LocationName.Summer_Pattern: LocationData(BASE_IDS.ITEMS + 263, RegionName.Papaya_Island_Beach_Flag, 
        access_rule = lambda state, player:
            can_clear_beach_flag(state, player)
    ),
    LocationName.Toy_Gun: LocationData(BASE_IDS.ITEMS + 270, RegionName.Sandpolis_Frank_House),
    LocationName.Trumpet_Horn: LocationData(BASE_IDS.ITEMS + 237, RegionName.Fuji_City_Hakosuke_House),
    LocationName.UFO_Pattern: LocationData(BASE_IDS.ITEMS + 259, RegionName.UFO),
    LocationName.UnbaboDoll: LocationData(BASE_IDS.ITEMS + 274, RegionName.Papaya_Island_Luke_House),
    LocationName.Urban_Pattern: LocationData(BASE_IDS.ITEMS + 262, RegionName.Fuji_City_Highway_Race, 
        access_rule = lambda state, player:
            can_clear_highway_race(state, player)
    ),
    LocationName.Venus_Horn: LocationData(BASE_IDS.ITEMS + 234, RegionName.Mushroom_Road_Goddess),
    LocationName.Voucher: LocationData(BASE_IDS.ITEMS + 279, RegionName.Peach_Town_Police_Station, 
        access_rule = lambda state, player:
            state.has(ItemName.Wallet, player)
    ),
    LocationName.Wing_Set: LocationData(BASE_IDS.ITEMS + 214, RegionName.Temple_Under_the_Sea),
    LocationName.Item_from_Butch_After_Stamp_30: LocationData(BASE_IDS.ITEMS + 159, RegionName.Sandpolis_Butch_House,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Sheriff_Office, player)    
    ),
}

overworld_items : dict[str, LocationData] = {
    # NOTE: IDs below match offsets the game uses (assuming all item tables are combined in order)
    # NOTE: Overworld items do not currently have their own regions, as they currently cannot be randomized.
    #    Once randomizing these is supported, these regions will need to be created, and the regions below
    #    will need to be updated.
    LocationName.Wallet: LocationData(BASE_IDS.ITEMS + 278, RegionName.Base.Peach_Town),
    
    LocationName.Blue_Sapphire: LocationData(BASE_IDS.ITEMS + 287, RegionName.Base.Sandpolis),
    LocationName.Emerald: LocationData(BASE_IDS.ITEMS + 288, RegionName.Base.White_Mountain),
    LocationName.Ruby: LocationData(BASE_IDS.ITEMS + 289, RegionName.Base.Sandpolis),
    LocationName.Topaz: LocationData(BASE_IDS.ITEMS + 290, RegionName.Base.Fuji_City),
    LocationName.Black_Opal: LocationData(BASE_IDS.ITEMS + 291, RegionName.Base.Papaya_Island),
    LocationName.Moonstone: LocationData(BASE_IDS.ITEMS + 292, RegionName.Base.Mushroom_Road, 
        access_rule = lambda state, player:
            state.has(ItemName.Water_Ski, player) and
            (
                state.has(ItemName.Propeller, player) or
                state.has(ItemName.Jet_Turbine, player)
            )
    ),
    LocationName.Amethyst: LocationData(BASE_IDS.ITEMS + 293, RegionName.Base.White_Mountain),
    
    LocationName.Fountain_Pen: LocationData(BASE_IDS.ITEMS + 295, RegionName.Base.Sandpolis),

    LocationName.Papu_Flower: LocationData(BASE_IDS.ITEMS + 297, RegionName.Base.Papaya_Island_Upper),
    LocationName.Fluffy_Mushroom: LocationData(BASE_IDS.ITEMS + 298, RegionName.Base.Mushroom_Road),
    LocationName.Small_Bottle: LocationData(BASE_IDS.ITEMS + 299, RegionName.Base.Papaya_Island),
    
    LocationName.Peach: LocationData(BASE_IDS.ITEMS + 302, RegionName.Base.Peach_Town),
}

shop_purchases : dict[str, LocationData] = {
    # NOTE: IDs below match offsets the game uses for the item purchased (assuming all item tables are combined in order).
    # Game is patched to update our new bitfield for tracking shop purchase completions instead of actually
    #     giving you the purchased item. See 'shop_purchases' in the client's Addresses file.

    LocationName.Shop_Purchase_Sports_Tires: LocationData(BASE_IDS.SHOP_PURCHASES + 152, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_Parts_Shop, player) or
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Off_Road_Tires: LocationData(BASE_IDS.SHOP_PURCHASES + 158, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_Parts_Shop, player) or
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Panther_Engine: LocationData(BASE_IDS.SHOP_PURCHASES + 165, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_Parts_Shop, player) or
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Quick_Steering: LocationData(BASE_IDS.SHOP_PURCHASES + 188, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_Parts_Shop, player) or
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Soft_Pad: LocationData(BASE_IDS.SHOP_PURCHASES + 192, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_Parts_Shop, player) or
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Mesh_Wheel: LocationData(BASE_IDS.SHOP_PURCHASES + 196, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_Parts_Shop, player) or
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Spoke_1: LocationData(BASE_IDS.SHOP_PURCHASES + 197, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_Parts_Shop, player) or
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Fog_Lights: LocationData(BASE_IDS.SHOP_PURCHASES + 211, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_Parts_Shop, player) or
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Air_Horn: LocationData(BASE_IDS.SHOP_PURCHASES + 230, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_Parts_Shop, player) or
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Digital_Meter: LocationData(BASE_IDS.SHOP_PURCHASES + 254, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Peach_Town_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Semi_Racing_Tires: LocationData(BASE_IDS.SHOP_PURCHASES + 153, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Blue_MAX_Engine: LocationData(BASE_IDS.SHOP_PURCHASES + 166, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Light_Chassis: LocationData(BASE_IDS.SHOP_PURCHASES + 177, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Sports_Transmission: LocationData(BASE_IDS.SHOP_PURCHASES + 182, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Spoke_2: LocationData(BASE_IDS.SHOP_PURCHASES + 198, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Chronometer: LocationData(BASE_IDS.SHOP_PURCHASES + 245, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Fuji_City_Parts_Shop, player) or
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Racing_Tires: LocationData(BASE_IDS.SHOP_PURCHASES + 154, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_HG_Off_Road_Tires: LocationData(BASE_IDS.SHOP_PURCHASES + 159, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Blue_MAX_V2_Engine: LocationData(BASE_IDS.SHOP_PURCHASES + 167, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_MAD_Engine: LocationData(BASE_IDS.SHOP_PURCHASES + 168, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player)
    ),
    LocationName.Shop_Purchase_Feather_Chassis: LocationData(BASE_IDS.SHOP_PURCHASES + 178, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_X2_Quick_Steering: LocationData(BASE_IDS.SHOP_PURCHASES + 189, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Flush_1: LocationData(BASE_IDS.SHOP_PURCHASES + 199, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Flush_4: LocationData(BASE_IDS.SHOP_PURCHASES + 206, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Sticker: LocationData(BASE_IDS.SHOP_PURCHASES + 228, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Echo_Air_Horn: LocationData(BASE_IDS.SHOP_PURCHASES + 231, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Bus_Horn: LocationData(BASE_IDS.SHOP_PURCHASES + 232, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Triangle_Meter: LocationData(BASE_IDS.SHOP_PURCHASES + 248, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Sandpolis_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Wet_Tires: LocationData(BASE_IDS.SHOP_PURCHASES + 156, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_HG_Wet_Tires: LocationData(BASE_IDS.SHOP_PURCHASES + 157, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_MAD_V2_Engine: LocationData(BASE_IDS.SHOP_PURCHASES + 169, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Power_Transmission: LocationData(BASE_IDS.SHOP_PURCHASES + 183, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player) or
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Flush_3: LocationData(BASE_IDS.SHOP_PURCHASES + 205, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Mushroom_Road_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Studless_Tires: LocationData(BASE_IDS.SHOP_PURCHASES + 160, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_HG_Studless_Tires: LocationData(BASE_IDS.SHOP_PURCHASES + 161, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Long_MAD_Engine: LocationData(BASE_IDS.SHOP_PURCHASES + 170, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Hard_Pad: LocationData(BASE_IDS.SHOP_PURCHASES + 193, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Spoke_3: LocationData(BASE_IDS.SHOP_PURCHASES + 200, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Beam_Lights: LocationData(BASE_IDS.SHOP_PURCHASES + 212, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.White_Mountain_Parts_Shop, player) or
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Black_MAX_Engine: LocationData(BASE_IDS.SHOP_PURCHASES + 171, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_RS_Magnum_Engine: LocationData(BASE_IDS.SHOP_PURCHASES + 172, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Phantom_Chassis: LocationData(BASE_IDS.SHOP_PURCHASES + 179, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Speed_Transmission: LocationData(BASE_IDS.SHOP_PURCHASES + 184, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player) or
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Flush_2: LocationData(BASE_IDS.SHOP_PURCHASES + 201, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Spoke_6: LocationData(BASE_IDS.SHOP_PURCHASES + 204, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Water_Ski: LocationData(BASE_IDS.SHOP_PURCHASES + 219, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Bicycle_Bell: LocationData(BASE_IDS.SHOP_PURCHASES + 233, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Papaya_Island_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Spoke_4: LocationData(BASE_IDS.SHOP_PURCHASES + 202, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Spoke_5: LocationData(BASE_IDS.SHOP_PURCHASES + 203, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Flush_5: LocationData(BASE_IDS.SHOP_PURCHASES + 207, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Flight_Wing: LocationData(BASE_IDS.SHOP_PURCHASES + 220, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    ),

    LocationName.Shop_Purchase_Space_Horn: LocationData(BASE_IDS.SHOP_PURCHASES + 240, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            state.can_reach_region(RegionName.Cloud_Hill_Parts_Shop, player)
    )
}

licenses : dict[str, LocationData] = {
    LocationName.B_License_Obtained: LocationData(BASE_IDS.LICENSES + 1, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            can_access_all_rank_c_races(state, player)
    ),
    LocationName.A_License_Obtained: LocationData(BASE_IDS.LICENSES + 2, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            can_access_all_rank_b_races(state, player)     
    ),
    LocationName.Super_A_License_Obtained: LocationData(BASE_IDS.LICENSES + 3, RegionName.Base.No_Region,
        access_rule = lambda state, player:
            can_access_all_rank_a_races(state, player)
    ),
}

world_gp : dict[str, LocationData] = {
    LocationName.World_GP_Completed: LocationData(BASE_IDS.WORLD_GP, RegionName.Base.No_Region,
        # To complete the world GP, the player needs enough good parts to equip their teammates
        #  and their own car to consistently place high in Grand Prix races.
        #
        #  We shouldn't use the additional progressive part tracks in an access_rule since
        #  they are not progression items (in AP, any item required to complete a location check
        #  is supposed to be progression), and they can also be disabled in the YAML options.
        #
        #  Instead, we test to see if the player has access to the best parts that can be
        #  purchased in the game, and that they have access to the My City parts shop
        #  so they can buy duplicates if needed.
        access_rule = lambda state, player:
            state.can_reach_entrance(RegionName.My_City_Parts_Shop, player) and
            has_license_count(3, state, player) and
            has_engine_of_level(10, state, player) and
            has_tires_of_level(10, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(4, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)
    ),
}

location_table = {
    **races_c_rank,
    **races_b_rank,
    **races_a_rank,
    **races_other,
    **stamps,
    **items_received,
    **overworld_items,
    **shop_purchases,
    **licenses,
    **world_gp,
}

# ------------------------------------------

# Called by __init__.py
def get_double_up_stamp_name(npc_reward_name : str, stamp_name : str):
    return npc_reward_name + " / " + stamp_name

def get_double_up_stamp_id(npc_reward_name : str):
    return BASE_IDS.COMBINED + location_table[npc_reward_name].id

def create_locations_RTA(world : World):
    from . import RoadTripLocation

    def create_location_RTA(name : str, data : LocationData, world : World) -> RoadTripLocation:
        region = world.get_region(data.region)
        assert region, "create_locations_RTA tried to create a Location with a Region that does not exist in this world instance."

        location = RoadTripLocation(world.player, name, data.id, region)
        location.access_rule = apply_player_to_access_rule(data.access_rule, world.player) # See the comment in applyPlayerToAccessRule for why this is needed.
        region.locations.append(location)
        return location

    def handle_double_up_stamps(world : World):
        """ 
        If double-up stamps have been disabled, creates a new 'combined' Location that represents both the Stamp and its NPC reward.
        """
        for npc_reward_name, stamp_name in double_up_stamps.items():
            new_location_name = get_double_up_stamp_name(npc_reward_name, stamp_name)
            new_ID = get_double_up_stamp_id(npc_reward_name)
            
            # We used to add the new location to the world's 'location_name_to_id' and 'location_id_to_name' tables
            #    here (location_id_to_name is generated automatically, but is created prior to this function running,
            #    so we needed to update it here as well). However, apparently this was too late, and was causing the
            #    locations to display as "Unknown location" in the client and on the server (even though they
            #    functioned correctly).
            # These are now added when the world object is created in __init__.py
            # world.location_name_to_id[new_location_name] = new_ID
            # world.location_id_to_name[new_ID] = new_location_name

            if options.remove_double_up_stamps == True:
                # Create new combined Location
                location_data = LocationData(
                    id = new_ID,
                    region = location_table[npc_reward_name].region,
                    access_rule = location_table[npc_reward_name].access_rule
                )
                location = create_location_RTA(new_location_name, location_data, world)

    # -----------------------------------------

    options = get_RTA_options(world.multiworld, world.player)

    for location_name in location_table:
        # If 'Remove Double-Up Stamps' is enabled, don't add any of the Locations that are double-ups.
        #    We'll handle those later.
        if options.remove_double_up_stamps == True and \
            (location_name in double_up_stamps.keys() or location_name in double_up_stamps.values()):
            continue
        # Do not add license locations if they have been set to removed via the YAML.
        if options.license_handling == LicenseHandling.option_remove and \
            (location_name in licenses):
            continue

        location_data = location_table[location_name]
        location = create_location_RTA(location_name, location_data, world)

    handle_double_up_stamps(world)
