"""
Archipelago randomizer implementation for the PS2 game Road Trip.
(Named "Road Trip Adventure" in PAL, "ChoroQ HG2" in NTSC-J, and sometimes referred to as 
"Everywhere Road Trip" in NTSC-U.)


AP GENERATION PROCESS OVERVIEW (aka "What are all these classes for, and how are they used?")
During the multiworld generation process, AP searches for any files with the .apworld extension in
its "custom_worlds" directory, and attempts to import the contents of each as a Python module.

This file (__init__.py) is the first thing imported. When imported, it will make AP aware of
all of its classes, functions, etc.

Later, after finding all valid .apworld files (and core worlds in the "worlds" directory) that
match the player-provided YAML settings files, AP will create an instance of each of those world's  
World class (for Road Trip, this is RoadTripWorld), and attempt to call a series of methods from all of them.

For example, one of the first methods called is "generate_early". All world instances will have their 
"generate_early" methods called, if they have that method.

Then, AP will attempt to call the next of these methods, "create_regions", from all world instances. 
All of these are run back-to-back. This continues for the remainder of the generation methods.

List of methods available:
https://alwaysintreble.github.io/Archipelago/world%20api.html#generation

This sums up the World side of an AP world (i.e. the portion that runs during generation).
The client is separate, and is the program the user runs from the AP launcher to play the game.
See __init__.py in the client folder for more info.


NOTE: .apworld files are just zip folders with a specific directory structure, see 
https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/apworld%20specification.md#apworld-file-format
"""

# Standard library imports
from typing import ClassVar

# AP imports
import settings
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess # For launching the client. Taken from APRaC2.
from BaseClasses import Region, Location, Item, Tutorial, LocationProgressType, ItemClassification
from Utils import visualize_regions

# Local imports
from .names import ItemName
from .options import RoadTripOptions, get_RTA_options, AreaUnlockMode, FILLER_AMOUNT
from .items import item_table, create_items_RTA, create_item_RTA
from .locations import location_table, create_locations_RTA
from .regions import create_regions_RTA
from .roomRando import room_rando_RTA

# -------- Taken from APRaC2, needed for client ------------
def run_client():
    from .client import launch
    launch_subprocess(launch, name="RTAClient")

components.append(
    Component("Road Trip Client", func=run_client, component_type=Type.CLIENT)
)

# ----------------------------------------

# WebWorlds describe what should appear on the game's settings page on the Archipelago website
class RoadTripWeb(WebWorld):
    theme = "grassFlowers"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago randomizer for Road Trip Adventure.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Phenra"]
    )

    tutorials = [setup_en]

class RoadTripItem(Item):
    game = "Road Trip Adventure"

class RoadTripLocation(Location):
    game = "Road Trip Adventure"

# Reference: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/settings%20api.md
class RoadTripSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of your Road Trip ISO"""

        description = "Road Trip Adventure ISO file"
        copy_to = "RoadTrip.iso"
        md5s = "e1598a1a2b1a296dbeae90927172d52a" # NTSC-only for now

    iso_file: RomFile = RomFile(RomFile.copy_to)


# Reference: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#a-world-class-skeleton
class RoadTripWorld(World):
    """Road Trip Adventure is a racing-RPG hybrid game for the PlayStation 2. Explore a charming open world inhabited
    by talking cars! Travel to new towns full of quirky inhabitants, compete in races, upgrade your car, and earn the 
    chance to become the next President!"""
    
    # -------- Attributes provided by base World class ----------
    game = "Road Trip Adventure"
    options_dataclass = RoadTripOptions
    options: RoadTripOptions
    settings: ClassVar[RoadTripSettings]
    topology_present = False
    web = RoadTripWeb()
    item_name_to_id = {name: data.id for name, data in item_table.items()} # Required by Archipelago
    location_name_to_id = {name: data.id for name, data in location_table.items()} # Required by Archipelago

    # Useful attributes provided by base World class, but not currently utilized by RTA AP:
    # item_name_groups = {}
    # location_name_groups = {}

    # AP no longer needs each world to provide its own unique base ID
    # base_id = 74797278

    # -------- New attributes for our RoadTripWorld class ----------
    # vanillaConnections = list[Entrance] # Will contain all Entrances (objects that connect regions) prior to any entrance randomization.

    # -------- Overriding base class functions NOT called by AP's Main.py ----------
    def get_filler_item_name(self):
        return ItemName.Filler

    # Required override by Archipelago
    def create_item(self, name):
        return create_item_RTA(self, name)

    # -------- Methods called by AP's Main.py ----------
    def generate_early(self):
        check_for_bad_option_combos(self)

    def create_regions(self):
        create_regions_RTA(self) # Also creates most rules, see note under set_rules
        create_locations_RTA(self) # Also creates and connects default entrances

    def create_items(self):
        create_items_RTA(self)
    
    def set_rules(self):
        # Other than setting the victory condition, and setting good item priority for races and
        #    minigames (if those options are set), all other rules are set in createRegionsRTA  
        #    and createLocationsRTA (via access_rule functions on Entrances and Locations).
            
        self.multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.Victory, self.player)

        options = get_RTA_options(self.multiworld, self.player)
        if options.prioritize_good_rewards_for_races != 0: roll_for_good_race_rewards(self)
        if options.prioritize_good_rewards_for_minigames != 0: roll_for_good_minigame_rewards(self)

    def connect_entrances(self):
        # Default entrances are connected in createLocationsRTA
        # For Road Trip, this will only be used for room rando

        # TODO: if room rando setting enabled:
            #room_rando_RTA(self)
        ...

        # DEBUG
        # try:
        #     room_rando_RTA(self)
        # except:
        #     pass
        # finally:
        #     # Copied from Celeste Open World
        #     visualize_regions(self.get_region("Menu"), f"Player{self.player}.puml", show_entrance_names=True, regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[self.player])

    def fill_slot_data(self):
        # slot_data contains the data we pass to the client (that is not already accessible through server API calls)
        slot_data = {
            "filler_amount": FILLER_AMOUNT,
            "save_id": self.random.getrandbits(32),
            "shop_strings": get_shop_strings(self),
            "area_unlock_mode": int(self.options.area_unlock_mode),
            "remove_double_up_stamps": bool(self.options.remove_double_up_stamps)
        }
        return slot_data
    
    def generate_output(self, output_directory: str):
        # Copied from Celeste Open World
        # visualize_regions(self.get_region("Menu"), f"Player{self.player}.puml", show_entrance_names=True, regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[self.player])
        ...

# ------------------------------------------

# Additional functions needed for above functionality that do not belong in items.py, locations.py, etc.
# NOTE: Could move these to a 'helpers.py'? They aren't really 'helpers' though, they're just for RoadTripWorld...
def check_for_bad_option_combos(world : World):
    options = get_RTA_options(world.multiworld, world.player)
    if options.area_unlock_mode == AreaUnlockMode.option_stamps and options.remove_double_up_stamps == True:
        raise Exception("Road Trip: 'Remove Double-Up Stamps' option cannot be used in Stamp progression mode. Please fix your YAML.")

def roll_for_good_race_rewards(world : World):
    from .locations import races_c_rank, races_b_rank, races_a_rank, races_other
    
    races = \
        [name for name in races_c_rank] + \
        [name for name in races_b_rank] + \
        [name for name in races_a_rank] + \
        [name for name in races_other]
     
    percent_chance = get_RTA_options(world.multiworld, world.player).prioritize_good_rewards_for_races
    
    for race in races:
        roll_for_force_good_item(world, percent_chance, world.get_location(race))

def roll_for_good_minigame_rewards(world : World):
    from .categories import challenge_minigames, get_combined_double_up_stamp_name

    # Check if Remove Double-Up Stamps is enabled, and convert the challenge minigames to their new location names if so
    challenges = challenge_minigames
    options = get_RTA_options(world.multiworld, world.player)
    if options.remove_double_up_stamps == True:
        challenges = set()
        for challenge in challenge_minigames:
            try:
                challenges.add(get_combined_double_up_stamp_name(challenge))
            except KeyError:
                challenges.add(challenge)

    minigames = [minigame for minigame in challenges] # Convert set to list
    percent_chance = get_RTA_options(world.multiworld, world.player).prioritize_good_rewards_for_minigames
    
    for minigame in minigames:
        roll_for_force_good_item(world, percent_chance, world.get_location(minigame))

def roll_for_force_good_item(world: World, percent_chance : int, location : Location):
    """Roll for a chance to force a good item to be placed at the passed Location."""
    x = world.random.randint(1, 100)
    if x <= percent_chance:
        location.progress_type = LocationProgressType.PRIORITY
        # print("Forced good item at ", location.name)

class PartDescription(dict):
    vanilla_item_id: int
    item_name: str
    player: str
    item_classification: ItemClassification

def get_shop_strings(world : World) -> list[PartDescription]:
    from .locations import BASE_IDS

    shop_strings = []

    for location in world.get_locations():
        if "Shop Purchase" in location.name:
            part_desc = PartDescription(
                vanilla_item_id = location.address - BASE_IDS.SHOP_PURCHASES, # Address is an AP location's ID
                item_name = location.item.name[:40], # Prevent going over max item name length that our shop strings data structure can hold
                player = world.multiworld.get_player_name(location.item.player),
                item_classification = location.item.classification
            )
            shop_strings.append(part_desc)

    return shop_strings
