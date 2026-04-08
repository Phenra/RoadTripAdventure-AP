from dataclasses import dataclass

from BaseClasses import MultiWorld
from Options import Choice, Toggle, Range, PerGameCommonOptions

FILLER_AMOUNT = 500

# TODO: Add president skip logic option
# TODO: Add Q coin and Quick-Pic shop options
# TODO: Add option for 'no logic gating' mode (with big disclaimer to not use it without permission of everyone in the multiworld)
# TODO: Add option for non-progressive parts
# TODO: Add an option to nerf the Jet Turbine (double gas usage, maybe triple?)
# TODO: Add room randomizer and NPC randomizer options once they are stable in-game

class AreaUnlockMode(Choice):
    """In RTA AP, in order to interact with anything in a town (enter houses, talk to cars, etc.), you must unlock the town first.

    In **Decorations** mode, you must obtain one of the garage decorations associated with that town to unlock it.
    Every town has 2. (A couple of towns lacking garage decorations use wallpapers instead.)
    
    In **Stamps** mode, 100 stamp items are added into the pool. Every 5 stamp items you get unlocks the next town.
    """
    display_name = "Area Unlock Mode"
    rich_text_doc = True
    option_decorations = 0
    option_stamps = 1
    default = 0

class RemoveDoubleUpStamps(Toggle):
    """If using Decorations mode, enable this to combine NPC rewards and stamps that are received back-to-back into one location (e.g. Stamp 2, and many many others). 
    Applies to roughly half of the stamps in the game.

    This cannot be enabled in Stamps mode, as it would bring the number of locations well below the number of items.
    """
    display_name = "Remove Double-Up Stamps"
    default: 0

class AdditionalProgressivePartTracks(Range):
    """Add additional progressive part tracks to the item pool. Defaults to 2, one for each of your teammates.

    These parts can also be used by you, or just sold for money at the Recycle Shop.

    Leaving this at 2 is recommended for Decorations mode.
    In Stamps mode, lowering this to 1 is worth considering. When set to 2 in Stamps mode, most cosmetic/filler items (horns, meters, etc.) will have to be removed from the item pool in order to make enough space. (If this is fine, leave at 2.)
    Setting to 0 is not recommended, as it makes finding part upgrades a bit rare.
    """
    display_name = "Additional Progressive Part Tracks"
    range_start = 0
    range_end = 2
    default = 2  

class PrioritizeGoodRewardsForRaces(Range):
    """Set the percent chance that a race will be forced to have a Progression item. (Rolled separately for each race.)

    Before items are placed, a random number between 1 and 100 is rolled for each race.
    If the number is equal to or below the value selected here, the item will be guaranteed to be Progression.
    This provides more incentive to complete races, which require more skill and time than most stamps.

    Since this is rolled for *each* race, it is not a guarantee that a certain percentage of races will have Progression items - just that on average, they will.
    """
    display_name = "Prioritize Good Rewards for Races"
    default = 50
    range_start = 0
    range_end = 100

class PrioritizeGoodRewardsForMinigames(Range):
    """Set the percent chance that a minigame will be forced to have a progression item. (Rolled separately for each minigame.)

    Works the same way as the setting for races.

    Several minigames are not included due to lack of a meaningful challenge (notably Q's Rally, fishing, and the Figure 8 courses, since none of these have time limits).
    """
    display_name = "Prioritize Good Rewards for Minigames"
    default = 25
    range_start = 0
    range_end = 100

class LicenseHandling(Choice):
    """Set how license items/locations should be handled.
    Standard: Licenses are awarded via Progressive License items found in the multiworld. License completions are locations.
    Vanilla: Force the license unlock items to be in their vanilla locations. (e.g. a Progressive License will always be found at Rank C completion, etc.)
    Remove: Start with all licenses. License completions are *not* locations.
    """
    display_name = "License Handling"
    option_standard = 0
    option_vanilla = 1
    option_remove = 2
    default = 0

@dataclass
class RoadTripOptions(PerGameCommonOptions):
    area_unlock_mode:                         AreaUnlockMode
    remove_double_up_stamps:                  RemoveDoubleUpStamps
    additional_progressive_part_tracks:       AdditionalProgressivePartTracks
    prioritize_good_rewards_for_races:        PrioritizeGoodRewardsForRaces
    prioritize_good_rewards_for_minigames:    PrioritizeGoodRewardsForMinigames
    license_handling:                         LicenseHandling

def get_RTA_options(multiworld: MultiWorld, player : int) -> RoadTripOptions:
    options = multiworld.worlds[player].options
    assert options, "getRoadTripOptions returned None"
    
    return options