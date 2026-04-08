import entrance_rando
from worlds.AutoWorld import World

from .regions import ConnectionType
from .categories import do_not_room_rando_list

def room_rando_RTA(world : World):
    for entrance in world.get_entrances():
        if entrance.connected_region.name in do_not_room_rando_list:
            continue
        # Do not randomize any entrances that lead to a Region - only randomize rooms and NPCs.
        elif entrance.randomization_group == int(ConnectionType.Regions):
            continue
        # NOTE: The room rando YAML setting should have options for room-only, NPC-only, or both.
        # TODO: Add elifs here once the setting is added
        else:
            entrance_rando.disconnect_entrance_for_randomization(entrance, one_way_target_name="To " + entrance.name)        

    placement = entrance_rando.randomize_entrances(world, coupled=True, target_group_lookup={0: [0], 1: [1], 2: [2]})
