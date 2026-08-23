# NOTE: Most rules are defined in-line in locations.py and regions.py.
#   Rules are defined here when they are relatively complex and/or used across several different locations/regions.

from BaseClasses import CollectionState, MultiWorld, Location
from worlds.AutoWorld import World
from typing import Callable
from inspect import signature
from functools import partial

from .names import ItemName, LocationName, RegionName
from .categories import quick_pic_shops_list, my_city_invites_list

# ------------------------------------------------

# Helper functions
def apply_player_to_access_rule(access_rule : Callable[[CollectionState, int], bool] | None, player : int) -> Callable[[CollectionState], bool] | None:
    # If the access_rule lambda has a player parameter, create a new partial function that will always set that argument
    #     to a static value, world.player. The partial function's signature will then only have a state parameter.
    #     Needed since the access_rule property on the Entrance class actually only has a state parameter.
    if access_rule:
        parameters = signature(access_rule).parameters
        str_parameters = [str(parameter) for parameter in parameters.values()]

        if 'player' in str_parameters:
            access_rule = partial(access_rule, player=player)

    return access_rule

# ------------------------------------------------

# Rules
def has_engine_of_level(required_level: int, state: CollectionState, player: int) -> bool:
    return state.count(ItemName.Progressive_Engine, player) >= required_level

    # TODO: if non-progressive parts

def has_tires_of_level(required_level: int, state: CollectionState, player: int) -> bool:
    return state.count(ItemName.Progressive_Tires, player) >= required_level

    # TODO: if non-progressive parts

def has_chassis_of_level(required_level: int, state: CollectionState, player: int) -> bool:
    return state.count(ItemName.Progressive_Chassis, player) >= required_level

    # TODO: if non-progressive parts

def has_transmission_of_level(required_level: int, state: CollectionState, player: int) -> bool:
    return state.count(ItemName.Progressive_Transmission, player) >= required_level

    # TODO: if non-progressive parts

def has_steering_of_level(required_level: int, state: CollectionState, player: int) -> bool:
    return state.count(ItemName.Progressive_Steering, player) >= required_level

    # TODO: if non-progressive parts

def has_brakes_of_level(required_level: int, state: CollectionState, player: int) -> bool:
    return state.count(ItemName.Progressive_Brakes, player) >= required_level

    # TODO: if non-progressive parts

def has_license_count(count: int, state: CollectionState, player: int) -> bool:
    return state.count(ItemName.Progressive_License, player) >= count

def closure__get_q_coins_per_region():
    q_coins_per_region = dict() # Using closure to cache / memoize value. Only needs to be calculated once.

    def get_q_coins_per_region():
        from .locations import q_coins
        nonlocal q_coins_per_region

        if not q_coins_per_region:
            for location_data in q_coins.values():
                if q_coins_per_region.get(location_data.region):
                    q_coins_per_region[location_data.region] += 1
                else:
                    q_coins_per_region[location_data.region] = 1

        return q_coins_per_region

    return get_q_coins_per_region

get_q_coins_per_region = closure__get_q_coins_per_region()

def get_accessible_base_regions(state : CollectionState, player : int) -> list[str]:
    regions = [
        RegionName.Base.Peach_Town,
        RegionName.Base.Fuji_City,
        RegionName.Base.My_City,
        RegionName.Base.Sandpolis,
        RegionName.Base.Chestnut_Canyon,
        RegionName.Base.Mushroom_Road,
        RegionName.Base.White_Mountain,
        RegionName.Base.Papaya_Island,
        RegionName.Base.Papaya_Island_Upper,
        RegionName.Base.Papaya_Island_Island,
        RegionName.Base.Cloud_Hill
    ]
    regions_to_remove = []

    for region in regions:
        if not state.can_reach_region(region, player):
            regions_to_remove.append(region)

    for region in regions_to_remove:
        regions.remove(region)

    return regions

def q_coins_accessible(state: CollectionState, player: int) -> int:
    accessible_regions = get_accessible_base_regions(state, player)
    q_coins_per_region = get_q_coins_per_region()

    coin_count = 0
    for region in accessible_regions:
        coin_count += q_coins_per_region.get(region, 0)

    # Test for coins that have access rules
    if RegionName.Base.Sandpolis in accessible_regions and state.can_reach_location(LocationName.Q_Coin_43, player) == False: # Atop Pyramid
        coin_count -= 1

    return coin_count

def can_clear_coine_reward(state: CollectionState, player: int, reward_level : int) -> bool:
    coins_needed = state.multiworld.worlds[player].options.q_coins_needed_per_coine_reward * reward_level

    if state.multiworld.worlds[player].options.randomize_q_coins == True:
        return state.has(ItemName.Q_Coin, player, coins_needed)

    return q_coins_accessible(state, player) >= coins_needed

def has_all_gemstones(state: CollectionState, player: int) -> bool:
    return (
        state.has(ItemName.Topaz, player) and
        state.has(ItemName.Ruby, player) and
        state.has(ItemName.Blue_Sapphire, player) and
        state.has(ItemName.Moonstone, player) and
        state.has(ItemName.Emerald, player) and
        state.has(ItemName.Amethyst, player) and
        state.has(ItemName.Black_Opal, player)
    )
def can_reach_all_coin_radar_houses(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_region(RegionName.White_Mountain_Coin_Radar_House_1, player) and
        state.can_reach_region(RegionName.White_Mountain_Coin_Radar_House_2, player) and
        state.can_reach_region(RegionName.White_Mountain_Coin_Radar_House_3, player) and
        state.can_reach_region(RegionName.White_Mountain_Coin_Radar_House_4, player)
    )

def can_access_all_rank_c_races(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_region(RegionName.Peach_Town_Qs_Factory, player) and
        state.can_reach_region(RegionName.Fuji_City_Qs_Factory, player) and
        state.can_reach_region(RegionName.Sandpolis_Qs_Factory, player) and
        state.can_reach_region(RegionName.Chestnut_Canyon_Qs_Factory, player) and
        state.can_reach_region(RegionName.Mushroom_Road_Qs_Factory, player)
    )

def can_access_all_rank_b_races(state: CollectionState, player: int) -> bool:
    return can_access_all_rank_a_races(state, player) # Both B-rank and A-rank require access to the same Q's factories

def can_access_all_rank_a_races(state: CollectionState, player: int) -> bool:
    return (
        state.can_reach_region(RegionName.Peach_Town_Qs_Factory, player) and
        state.can_reach_region(RegionName.Fuji_City_Qs_Factory, player) and
        state.can_reach_region(RegionName.Sandpolis_Qs_Factory, player) and
        state.can_reach_region(RegionName.Chestnut_Canyon_Qs_Factory, player) and
        state.can_reach_region(RegionName.Mushroom_Road_Qs_Factory, player) and
        state.can_reach_region(RegionName.White_Mountain_Qs_Factory, player) and
        state.can_reach_region(RegionName.Papaya_Island_Qs_Factory, player)
    )

def can_access_everything_in_my_city(state: CollectionState, player: int) -> bool:
    # NOTE: This needs to check for access to all My City *entrances*, not regions!
    # The My City building/NPC regions might not be in My City in room randomizer!

    for region in my_city_invites_list:
        if not state.can_reach_region(region, player):
            return False
    
    # Quick-Pic 28 and 29 not checked since those both can be accessed if the above conditions are met
    # (and in Quick-Pic 29's case, the Endurance Run is finished)
    
    return True

def can_clear_endurance_run(state: CollectionState, player: int) -> bool:
    return (
        has_tires_of_level(4, state, player) and
        has_engine_of_level(5, state, player) and
        has_chassis_of_level(3, state, player) and
        has_transmission_of_level(3, state, player) and
        has_steering_of_level(2, state, player) and
        has_brakes_of_level(1, state, player) and
        has_license_count(2, state, player)
    ) 

def can_clear_rainbow_jump(state: CollectionState, player: int) -> bool:
    return (
        state.has(ItemName.Jet_Turbine, player) and
        state.has(ItemName.Wing_Set, player) and
        has_tires_of_level(11, state, player) and
        has_engine_of_level(8, state, player) and
        has_chassis_of_level(3, state, player) and
        has_transmission_of_level(3, state, player) and
        has_brakes_of_level(3, state, player)
    )

def can_clear_single_lap_race(state: CollectionState, player: int) -> bool:
    return (
        (
            state.has(ItemName.Jet_Turbine, player) and
            has_tires_of_level(4, state, player) and
            has_engine_of_level(5, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)
        ) or
        (
            has_tires_of_level(9, state, player) and
            has_engine_of_level(7, state, player) and
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player) and
            has_steering_of_level(2, state, player) and
            has_brakes_of_level(2, state, player)
        )
    )

def can_clear_soccer(state: CollectionState, player: int) -> bool:
    return (
        has_tires_of_level(1, state, player) and
        has_steering_of_level(1, state, player)
    )

def can_clear_beach_flag(state: CollectionState, player: int) -> bool:
    return (
        state.has(ItemName.Jet_Turbine, player) or
        (
            # Either of the below tire / engine combinations, as well as good enough chassis, transmission, and steering
            (
                has_tires_of_level(6, state, player) and
                has_engine_of_level(5, state, player)
            ) or
            (
                has_tires_of_level(1, state, player) and
                has_engine_of_level(7, state, player)
                
            ) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(2, state, player)
        )
    )

def can_clear_highway_race(state: CollectionState, player: int) -> bool:
    return (
        (
            has_engine_of_level(5, state, player) and
            has_tires_of_level(4, state, player) and 
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player)
        ) or
        (
            has_engine_of_level(6, state, player) and
            has_tires_of_level(2, state, player) and 
            has_chassis_of_level(3, state, player) and
            has_transmission_of_level(3, state, player)
        ) and
        has_steering_of_level(2, state, player) and
        has_brakes_of_level(1, state, player)
    )

def can_clear_sliding_door_race(state: CollectionState, player: int) -> bool:
    return (
        (
            has_tires_of_level(4, state, player) and
            has_engine_of_level(6, state, player) and
            has_chassis_of_level(2, state, player) and
            has_transmission_of_level(2, state, player) and
            has_steering_of_level(1, state, player) and
            has_brakes_of_level(2, state, player)
        ) or
        (
            state.has(ItemName.Jet_Turbine, player) and
            has_tires_of_level(2, state, player) and
            has_steering_of_level(1, state, player) and
            has_brakes_of_level(2, state, player)
        )
    )

def can_access_all_quick_pic_shops(state: CollectionState, player: int) -> bool:
    for shop in quick_pic_shops_list:
        if not state.can_reach_region(shop, player):
            return False
    
    return True

def can_access_top_of_pyramids(state: CollectionState, player: int) -> bool:
    return has_tires_of_level(10, state, player) # Big Tires, to drive up the pyramid