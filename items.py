import typing

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World

from .names import ItemName
from .categories import decoration_progression_only, stamp_progression_only
from .options import get_RTA_options, AreaUnlockMode, LicenseHandling

class ItemData(typing.NamedTuple):
    id: int
    quantity: int
    classification: ItemClassification

class BASE_IDS(): # Cannot inherit from IntEnum, causes pickle error in AP for some reason
    #DEFAULT = 1
    TIRES = 10
    ENGINES = 30
    CHASSIS = 50
    TRANSMISSION = 60
    STEERING = 70
    BRAKES = 80
    WHEELS = 90
    LIGHTS = 110
    WING_SET = 120
    SPECIAL_PARTS = 130
    OPTIONS = 140
    STICKER = 150
    HORNS = 160
    METERS = 180

    COLLECTIBLES = 200
    BODIES = 400
    STAMP = 1000
    PROGRESSIVE_LICENSE = 1001
    PROGRESSIVE_PARTS_SET1 = 1100
    PROGRESSIVE_PARTS_SET2 = 1200
    PROGRESSIVE_PARTS_SET3 = 1300
    AREA_UNLOCKS = 2001
    FILLER = 9998
    VICTORY = 9999

    @classmethod
    def get_all_as_list(self) -> list[int]: # TODO: This kinda sucks? Maybe move Base_IDs into a folder like with names?
        return [
            self.TIRES,
            self.ENGINES,
            self.CHASSIS,
            self.TRANSMISSION,
            self.STEERING,
            self.BRAKES,
            self.WHEELS,
            self.LIGHTS,
            self.WING_SET,
            self.SPECIAL_PARTS,
            self.OPTIONS,
            self.STICKER,
            self.HORNS,
            self.METERS,

            self.COLLECTIBLES,
            self.BODIES,
            self.BODIES,
            self.STAMP,
            self.PROGRESSIVE_LICENSE,
            self.PROGRESSIVE_PARTS_SET1,
            self.PROGRESSIVE_PARTS_SET2,
            self.PROGRESSIVE_PARTS_SET3,
            self.AREA_UNLOCKS,
            self.FILLER,
            self.VICTORY,
        ]

# NOTE: Reserving IDs for all items currently handled only by progressive upgrades, or not currently randomized for another reason (e.g body shop purchases)
bodies = {
    # ItemName.Body_Q001: ItemData(BASE_IDS.BODIES + 0, 1, ItemClassification.filler),
    # ItemName.Body_Q002: ItemData(BASE_IDS.BODIES + 1, 1, ItemClassification.filler),
    ItemName.Body_Q003: ItemData(BASE_IDS.BODIES + 2, 1, ItemClassification.filler),
    # ItemName.Body_Q004: ItemData(BASE_IDS.BODIES + 3, 1, ItemClassification.filler),
    # ItemName.Body_Q005: ItemData(BASE_IDS.BODIES + 4, 1, ItemClassification.filler),
    # ItemName.Body_Q006: ItemData(BASE_IDS.BODIES + 5, 1, ItemClassification.filler),
    # ItemName.Body_Q007: ItemData(BASE_IDS.BODIES + 6, 1, ItemClassification.filler),
    # ItemName.Body_Q008: ItemData(BASE_IDS.BODIES + 7, 1, ItemClassification.filler),
    # ItemName.Body_Q009: ItemData(BASE_IDS.BODIES + 8, 1, ItemClassification.filler),
    # ItemName.Body_Q010: ItemData(BASE_IDS.BODIES + 9, 1, ItemClassification.filler),
    # ItemName.Body_Q011: ItemData(BASE_IDS.BODIES + 10, 1, ItemClassification.filler),
    # ItemName.Body_Q012: ItemData(BASE_IDS.BODIES + 11, 1, ItemClassification.filler),
    # ItemName.Body_Q013: ItemData(BASE_IDS.BODIES + 12, 1, ItemClassification.filler),
    # ItemName.Body_Q014: ItemData(BASE_IDS.BODIES + 13, 1, ItemClassification.filler),
    # ItemName.Body_Q015: ItemData(BASE_IDS.BODIES + 14, 1, ItemClassification.filler),
    # ItemName.Body_Q016: ItemData(BASE_IDS.BODIES + 15, 1, ItemClassification.filler),
    # ItemName.Body_Q017: ItemData(BASE_IDS.BODIES + 16, 1, ItemClassification.filler),
    # ItemName.Body_Q018: ItemData(BASE_IDS.BODIES + 17, 1, ItemClassification.filler),
    # ItemName.Body_Q019: ItemData(BASE_IDS.BODIES + 18, 1, ItemClassification.filler),
    # ItemName.Body_Q020: ItemData(BASE_IDS.BODIES + 19, 1, ItemClassification.filler),
    # ItemName.Body_Q021: ItemData(BASE_IDS.BODIES + 20, 1, ItemClassification.filler),
    # ItemName.Body_Q022: ItemData(BASE_IDS.BODIES + 21, 1, ItemClassification.filler),
    # ItemName.Body_Q023: ItemData(BASE_IDS.BODIES + 22, 1, ItemClassification.filler),
    # ItemName.Body_Q024: ItemData(BASE_IDS.BODIES + 23, 1, ItemClassification.filler),
    # ItemName.Body_Q025: ItemData(BASE_IDS.BODIES + 24, 1, ItemClassification.filler),
    # ItemName.Body_Q026: ItemData(BASE_IDS.BODIES + 25, 1, ItemClassification.filler),
    # ItemName.Body_Q027: ItemData(BASE_IDS.BODIES + 26, 1, ItemClassification.filler),
    # ItemName.Body_Q028: ItemData(BASE_IDS.BODIES + 27, 1, ItemClassification.filler),
    # ItemName.Body_Q029: ItemData(BASE_IDS.BODIES + 28, 1, ItemClassification.filler),
    ItemName.Body_Q030: ItemData(BASE_IDS.BODIES + 29, 1, ItemClassification.filler),
    # ItemName.Body_Q031: ItemData(BASE_IDS.BODIES + 30, 1, ItemClassification.filler),
    # ItemName.Body_Q032: ItemData(BASE_IDS.BODIES + 31, 1, ItemClassification.filler),
    # ItemName.Body_Q033: ItemData(BASE_IDS.BODIES + 32, 1, ItemClassification.filler),
    ItemName.Body_Q034: ItemData(BASE_IDS.BODIES + 33, 1, ItemClassification.filler),
    # ItemName.Body_Q035: ItemData(BASE_IDS.BODIES + 34, 1, ItemClassification.filler),
    # ItemName.Body_Q036: ItemData(BASE_IDS.BODIES + 35, 1, ItemClassification.filler),
    ItemName.Body_Q037: ItemData(BASE_IDS.BODIES + 36, 1, ItemClassification.filler),
    # ItemName.Body_Q038: ItemData(BASE_IDS.BODIES + 37, 1, ItemClassification.filler),
    # ItemName.Body_Q039: ItemData(BASE_IDS.BODIES + 38, 1, ItemClassification.filler),
    # ItemName.Body_Q040: ItemData(BASE_IDS.BODIES + 39, 1, ItemClassification.filler),
    # ItemName.Body_Q041: ItemData(BASE_IDS.BODIES + 40, 1, ItemClassification.filler),
    # ItemName.Body_Q042: ItemData(BASE_IDS.BODIES + 41, 1, ItemClassification.filler),
    # ItemName.Body_Q043: ItemData(BASE_IDS.BODIES + 42, 1, ItemClassification.filler),
    # ItemName.Body_Q044: ItemData(BASE_IDS.BODIES + 43, 1, ItemClassification.filler),
    # ItemName.Body_Q045: ItemData(BASE_IDS.BODIES + 44, 1, ItemClassification.filler),
    # ItemName.Body_Q046: ItemData(BASE_IDS.BODIES + 45, 1, ItemClassification.filler),
    # ItemName.Body_Q047: ItemData(BASE_IDS.BODIES + 46, 1, ItemClassification.filler),
    # ItemName.Body_Q048: ItemData(BASE_IDS.BODIES + 47, 1, ItemClassification.filler),
    # ItemName.Body_Q049: ItemData(BASE_IDS.BODIES + 48, 1, ItemClassification.filler),
    # ItemName.Body_Q050: ItemData(BASE_IDS.BODIES + 49, 1, ItemClassification.filler),
    # ItemName.Body_Q051: ItemData(BASE_IDS.BODIES + 50, 1, ItemClassification.filler),
    # ItemName.Body_Q052: ItemData(BASE_IDS.BODIES + 51, 1, ItemClassification.filler),
    # ItemName.Body_Q053: ItemData(BASE_IDS.BODIES + 52, 1, ItemClassification.filler),
    # ItemName.Body_Q054: ItemData(BASE_IDS.BODIES + 53, 1, ItemClassification.filler),
    # ItemName.Body_Q055: ItemData(BASE_IDS.BODIES + 54, 1, ItemClassification.filler),
    # ItemName.Body_Q056: ItemData(BASE_IDS.BODIES + 55, 1, ItemClassification.filler),
    # ItemName.Body_Q057: ItemData(BASE_IDS.BODIES + 56, 1, ItemClassification.filler),
    # ItemName.Body_Q058: ItemData(BASE_IDS.BODIES + 57, 1, ItemClassification.filler),
    # ItemName.Body_Q059: ItemData(BASE_IDS.BODIES + 58, 1, ItemClassification.filler),
    # ItemName.Body_Q060: ItemData(BASE_IDS.BODIES + 59, 1, ItemClassification.filler),
    # ItemName.Body_Q061: ItemData(BASE_IDS.BODIES + 60, 1, ItemClassification.filler),
    # ItemName.Body_Q062: ItemData(BASE_IDS.BODIES + 61, 1, ItemClassification.filler),
    # ItemName.Body_Q063: ItemData(BASE_IDS.BODIES + 62, 1, ItemClassification.filler),
    # ItemName.Body_Q064: ItemData(BASE_IDS.BODIES + 63, 1, ItemClassification.filler),
    # ItemName.Body_Q065: ItemData(BASE_IDS.BODIES + 64, 1, ItemClassification.filler),
    # ItemName.Body_Q066: ItemData(BASE_IDS.BODIES + 65, 1, ItemClassification.filler),
    # ItemName.Body_Q067: ItemData(BASE_IDS.BODIES + 66, 1, ItemClassification.filler),
    # ItemName.Body_Q068: ItemData(BASE_IDS.BODIES + 67, 1, ItemClassification.filler),
    # ItemName.Body_Q069: ItemData(BASE_IDS.BODIES + 68, 1, ItemClassification.filler),
    # ItemName.Body_Q070: ItemData(BASE_IDS.BODIES + 69, 1, ItemClassification.filler),
    # ItemName.Body_Q071: ItemData(BASE_IDS.BODIES + 70, 1, ItemClassification.filler),
    # ItemName.Body_Q072: ItemData(BASE_IDS.BODIES + 71, 1, ItemClassification.filler),
    # ItemName.Body_Q073: ItemData(BASE_IDS.BODIES + 72, 1, ItemClassification.filler),
    # ItemName.Body_Q074: ItemData(BASE_IDS.BODIES + 73, 1, ItemClassification.filler),
    # ItemName.Body_Q075: ItemData(BASE_IDS.BODIES + 74, 1, ItemClassification.filler),
    # ItemName.Body_Q076: ItemData(BASE_IDS.BODIES + 75, 1, ItemClassification.filler),
    # ItemName.Body_Q077: ItemData(BASE_IDS.BODIES + 76, 1, ItemClassification.filler),
    # ItemName.Body_Q078: ItemData(BASE_IDS.BODIES + 77, 1, ItemClassification.filler),
    # ItemName.Body_Q079: ItemData(BASE_IDS.BODIES + 78, 1, ItemClassification.filler),
    ItemName.Body_Q080: ItemData(BASE_IDS.BODIES + 79, 1, ItemClassification.filler),
    ItemName.Body_Q081: ItemData(BASE_IDS.BODIES + 80, 1, ItemClassification.filler),
    ItemName.Body_Q082: ItemData(BASE_IDS.BODIES + 81, 1, ItemClassification.filler),
    ItemName.Body_Q083: ItemData(BASE_IDS.BODIES + 82, 1, ItemClassification.filler),
    ItemName.Body_Q084: ItemData(BASE_IDS.BODIES + 83, 1, ItemClassification.filler),
    ItemName.Body_Q085: ItemData(BASE_IDS.BODIES + 84, 1, ItemClassification.filler),
    ItemName.Body_Q086: ItemData(BASE_IDS.BODIES + 85, 1, ItemClassification.filler),
    ItemName.Body_Q087: ItemData(BASE_IDS.BODIES + 86, 1, ItemClassification.filler),
    # ItemName.Body_Q088: ItemData(BASE_IDS.BODIES + 87, 1, ItemClassification.filler),
    ItemName.Body_Q089: ItemData(BASE_IDS.BODIES + 88, 1, ItemClassification.filler),
    # ItemName.Body_Q090: ItemData(BASE_IDS.BODIES + 89, 1, ItemClassification.filler),
    # ItemName.Body_Q091: ItemData(BASE_IDS.BODIES + 90, 1, ItemClassification.filler),
    # ItemName.Body_Q092: ItemData(BASE_IDS.BODIES + 91, 1, ItemClassification.filler),
    # ItemName.Body_Q093: ItemData(BASE_IDS.BODIES + 92, 1, ItemClassification.filler),
    # ItemName.Body_Q094: ItemData(BASE_IDS.BODIES + 93, 1, ItemClassification.filler),
    # ItemName.Body_Q095: ItemData(BASE_IDS.BODIES + 94, 1, ItemClassification.filler),
    # ItemName.Body_Q096: ItemData(BASE_IDS.BODIES + 95, 1, ItemClassification.filler),
    # ItemName.Body_Q097: ItemData(BASE_IDS.BODIES + 96, 1, ItemClassification.filler),
    # ItemName.Body_Q098: ItemData(BASE_IDS.BODIES + 97, 1, ItemClassification.filler),
    # ItemName.Body_Q099: ItemData(BASE_IDS.BODIES + 98, 1, ItemClassification.filler),
    # ItemName.Body_Q0100: ItemData(BASE_IDS.BODIES + 99, 1, ItemClassification.filler),
    # ItemName.Body_Q0101: ItemData(BASE_IDS.BODIES + 100, 1, ItemClassification.filler),
    # ItemName.Body_Q0102: ItemData(BASE_IDS.BODIES + 101, 1, ItemClassification.filler),
    # ItemName.Body_Q0103: ItemData(BASE_IDS.BODIES + 102, 1, ItemClassification.filler),
    # ItemName.Body_Q0104: ItemData(BASE_IDS.BODIES + 103, 1, ItemClassification.filler),
    # ItemName.Body_Q0105: ItemData(BASE_IDS.BODIES + 104, 1, ItemClassification.filler),
    # ItemName.Body_Q0106: ItemData(BASE_IDS.BODIES + 105, 1, ItemClassification.filler),
    # ItemName.Body_Q0107: ItemData(BASE_IDS.BODIES + 106, 1, ItemClassification.filler),
    # ItemName.Body_Q0108: ItemData(BASE_IDS.BODIES + 107, 1, ItemClassification.filler),
    # ItemName.Body_Q0109: ItemData(BASE_IDS.BODIES + 108, 1, ItemClassification.filler),
    # ItemName.Body_Q0110: ItemData(BASE_IDS.BODIES + 109, 1, ItemClassification.filler),
    # ItemName.Body_Q0111: ItemData(BASE_IDS.BODIES + 110, 1, ItemClassification.filler),
    # ItemName.Body_Q0112: ItemData(BASE_IDS.BODIES + 111, 1, ItemClassification.filler),
    # ItemName.Body_Q0113: ItemData(BASE_IDS.BODIES + 112, 1, ItemClassification.filler),
    # ItemName.Body_Q0114: ItemData(BASE_IDS.BODIES + 113, 1, ItemClassification.filler),
    # ItemName.Body_Q0115: ItemData(BASE_IDS.BODIES + 114, 1, ItemClassification.filler),
    # ItemName.Body_Q0116: ItemData(BASE_IDS.BODIES + 115, 1, ItemClassification.filler),
    # ItemName.Body_Q0117: ItemData(BASE_IDS.BODIES + 116, 1, ItemClassification.filler),
    # ItemName.Body_Q0118: ItemData(BASE_IDS.BODIES + 117, 1, ItemClassification.filler),
    # ItemName.Body_Q0119: ItemData(BASE_IDS.BODIES + 118, 1, ItemClassification.filler),
    # ItemName.Body_Q0120: ItemData(BASE_IDS.BODIES + 119, 1, ItemClassification.filler),
    # ItemName.Body_Q0121: ItemData(BASE_IDS.BODIES + 120, 1, ItemClassification.filler),
    # ItemName.Body_Q0122: ItemData(BASE_IDS.BODIES + 121, 1, ItemClassification.filler),
    # ItemName.Body_Q0123: ItemData(BASE_IDS.BODIES + 122, 1, ItemClassification.filler),
    # ItemName.Body_Q0124: ItemData(BASE_IDS.BODIES + 123, 1, ItemClassification.filler),
    # ItemName.Body_Q0125: ItemData(BASE_IDS.BODIES + 124, 1, ItemClassification.filler),
    # ItemName.Body_Q0126: ItemData(BASE_IDS.BODIES + 125, 1, ItemClassification.filler),
    # ItemName.Body_Q0127: ItemData(BASE_IDS.BODIES + 126, 1, ItemClassification.filler),
    # ItemName.Body_Q0128: ItemData(BASE_IDS.BODIES + 127, 1, ItemClassification.filler),
    # ItemName.Body_Q0129: ItemData(BASE_IDS.BODIES + 128, 1, ItemClassification.filler),
    # ItemName.Body_Q0130: ItemData(BASE_IDS.BODIES + 129, 1, ItemClassification.filler),
    # ItemName.Body_Q0131: ItemData(BASE_IDS.BODIES + 130, 1, ItemClassification.filler),
    # ItemName.Body_Q0132: ItemData(BASE_IDS.BODIES + 131, 1, ItemClassification.filler),
    # ItemName.Body_Q0133: ItemData(BASE_IDS.BODIES + 132, 1, ItemClassification.filler),
    # ItemName.Body_Q0134: ItemData(BASE_IDS.BODIES + 133, 1, ItemClassification.filler),
    # ItemName.Body_Q0135: ItemData(BASE_IDS.BODIES + 134, 1, ItemClassification.filler),
    # ItemName.Body_Q0136: ItemData(BASE_IDS.BODIES + 135, 1, ItemClassification.filler),
    # ItemName.Body_Q0137: ItemData(BASE_IDS.BODIES + 136, 1, ItemClassification.filler),
    # ItemName.Body_Q0138: ItemData(BASE_IDS.BODIES + 137, 1, ItemClassification.filler),
    # ItemName.Body_Q0139: ItemData(BASE_IDS.BODIES + 138, 1, ItemClassification.filler),
    # ItemName.Body_Q0140: ItemData(BASE_IDS.BODIES + 139, 1, ItemClassification.filler),
    # ItemName.Body_Q0141: ItemData(BASE_IDS.BODIES + 140, 1, ItemClassification.filler),
    # ItemName.Body_Q0142: ItemData(BASE_IDS.BODIES + 141, 1, ItemClassification.filler),
    # ItemName.Body_Q0143: ItemData(BASE_IDS.BODIES + 142, 1, ItemClassification.filler),
    # ItemName.Body_Q0144: ItemData(BASE_IDS.BODIES + 143, 1, ItemClassification.filler),
    # ItemName.Body_Q0145: ItemData(BASE_IDS.BODIES + 144, 1, ItemClassification.filler),
    # ItemName.Body_Q0146: ItemData(BASE_IDS.BODIES + 145, 1, ItemClassification.filler),
    # ItemName.Body_Q0147: ItemData(BASE_IDS.BODIES + 146, 1, ItemClassification.filler),
    # ItemName.Body_Q0148: ItemData(BASE_IDS.BODIES + 147, 1, ItemClassification.filler),
    # ItemName.Body_Q0149: ItemData(BASE_IDS.BODIES + 148, 1, ItemClassification.filler),
    # ItemName.Life Body: ItemData(BASE_IDS.BODIES + 149, 1, ItemClassification.filler), # Unused in vanilla game
    ItemName.Body_Q0150: ItemData(BASE_IDS.BODIES + 150, 1, ItemClassification.filler),
}

tires = {
    ItemName.Sports_Tires: ItemData(BASE_IDS.TIRES + 1, 1, ItemClassification.progression),
    ItemName.Semi_Racing_Tires: ItemData(BASE_IDS.TIRES + 2, 1, ItemClassification.progression),
    ItemName.Racing_Tires: ItemData(BASE_IDS.TIRES + 3, 1, ItemClassification.progression),
    ItemName.HG_Racing_Tires: ItemData(BASE_IDS.TIRES + 4, 1, ItemClassification.progression),
    ItemName.Wet_Tires: ItemData(BASE_IDS.TIRES + 5, 1, ItemClassification.progression),
    ItemName.HG_Wet_Tires: ItemData(BASE_IDS.TIRES + 6, 1, ItemClassification.progression),
    ItemName.Off_Road_Tires: ItemData(BASE_IDS.TIRES + 7, 1, ItemClassification.progression),
    ItemName.HG_Off_Road_Tires: ItemData(BASE_IDS.TIRES + 8, 1, ItemClassification.progression), # Copy is given via Butch quest, not currently added to item pool since handled via progressive upgrades
    ItemName.Studless_Tires: ItemData(BASE_IDS.TIRES + 9, 1, ItemClassification.progression),
    ItemName.HG_Studless_Tires: ItemData(BASE_IDS.TIRES + 10, 1, ItemClassification.progression),
    ItemName.Big_Tires: ItemData(BASE_IDS.TIRES + 11, 1, ItemClassification.progression), # Copy is given via Coine reward, not currently added to item pool since handled via progressive upgrades
    # ItemName.Devil_Tires: ItemData(BASE_IDS.TIRES + 12, 1, ItemClassification.progression),
}

engines = {
    ItemName.Panther_Engine: ItemData(BASE_IDS.ENGINES + 1, 1, ItemClassification.progression),
    ItemName.Blue_MAX_Engine: ItemData(BASE_IDS.ENGINES + 2, 1, ItemClassification.progression),
    ItemName.Blue_MAX_v2_Engine: ItemData(BASE_IDS.ENGINES + 3, 1, ItemClassification.progression),
    ItemName.MAD_Engine: ItemData(BASE_IDS.ENGINES + 4, 1, ItemClassification.progression),
    ItemName.MAD_v2_Engine: ItemData(BASE_IDS.ENGINES + 5, 1, ItemClassification.progression),
    ItemName.Long_MAD_Engine: ItemData(BASE_IDS.ENGINES + 6, 1, ItemClassification.progression),
    ItemName.Black_MAX_Engine: ItemData(BASE_IDS.ENGINES + 7, 1, ItemClassification.progression),
    ItemName.RS_Magnum_Engine: ItemData(BASE_IDS.ENGINES + 8, 1, ItemClassification.progression), # Copy is given via Which-Way Maze, not currently added to item pool since handled via progressive upgrades
    ItemName.Speed_MAX_Engine: ItemData(BASE_IDS.ENGINES + 9, 1, ItemClassification.progression),
    ItemName.Hyper_MAX_Engine: ItemData(BASE_IDS.ENGINES + 10, 1, ItemClassification.progression), # Copy is given via Coine reward, not currently added to item pool since handled via progressive upgrades
    # ItemName.Devil_Engine: ItemData(BASE_IDS.ENGINES + 11, 1, ItemClassification.progression),
}

chassis = {
    ItemName.Light_Chassis: ItemData(BASE_IDS.CHASSIS + 1, 1, ItemClassification.progression),
    ItemName.Feather_Chassis: ItemData(BASE_IDS.CHASSIS + 2, 1, ItemClassification.progression),
    ItemName.Phantom_Chassis: ItemData(BASE_IDS.CHASSIS + 3, 1, ItemClassification.progression),
    ItemName.Hyper_Chassis: ItemData(BASE_IDS.CHASSIS + 4, 1, ItemClassification.progression), # Copy is given via Coine reward, not currently added to item pool since handled via progressive upgrades
}

transmission = {
    ItemName.Sports_Transmission: ItemData(BASE_IDS.TRANSMISSION + 1, 1, ItemClassification.progression),
    ItemName.Power_Transmission: ItemData(BASE_IDS.TRANSMISSION + 2, 1, ItemClassification.progression),
    ItemName.Speed_Transmission: ItemData(BASE_IDS.TRANSMISSION + 3, 1, ItemClassification.progression),
    ItemName.Wide_Transmission: ItemData(BASE_IDS.TRANSMISSION + 4, 1, ItemClassification.progression),
    ItemName.Hyper_Transmission: ItemData(BASE_IDS.TRANSMISSION + 5, 1, ItemClassification.progression), # Copy is given via Coine reward, not currently added to item pool since handled via progressive upgrades
}

steering = {
    ItemName.Quick_Steering: ItemData(BASE_IDS.STEERING + 1, 1, ItemClassification.progression),
    ItemName.X2_Quick_Steering: ItemData(BASE_IDS.STEERING + 2, 1, ItemClassification.progression),
    ItemName.X3_Quick_Steering: ItemData(BASE_IDS.STEERING + 3, 1, ItemClassification.progression), # Copy is given via Coine reward, not currently added to item pool since handled via progressive upgrades
}

brakes = {
    ItemName.Soft_Pad: ItemData(BASE_IDS.BRAKES + 1, 1, ItemClassification.progression),
    ItemName.Hard_Pad: ItemData(BASE_IDS.BRAKES + 2, 1, ItemClassification.progression),
    ItemName.Metal_Pad: ItemData(BASE_IDS.BRAKES + 3, 1, ItemClassification.progression), # Copy is given via Coine reward, not currently added to item pool since handled via progressive upgrades
}

wheels = {
    ItemName.Mesh_Wheel: ItemData(BASE_IDS.WHEELS + 1, 1, ItemClassification.filler),
    ItemName.Spoke_1: ItemData(BASE_IDS.WHEELS + 2, 1, ItemClassification.filler),
    ItemName.Spoke_2: ItemData(BASE_IDS.WHEELS + 3, 1, ItemClassification.filler),
    ItemName.Flush_1: ItemData(BASE_IDS.WHEELS + 4, 1, ItemClassification.filler),
    ItemName.Spoke_3: ItemData(BASE_IDS.WHEELS + 5, 1, ItemClassification.filler),
    ItemName.Flush_2: ItemData(BASE_IDS.WHEELS + 6, 1, ItemClassification.filler),
    ItemName.Spoke_4: ItemData(BASE_IDS.WHEELS + 7, 1, ItemClassification.filler),
    ItemName.Spoke_5: ItemData(BASE_IDS.WHEELS + 8, 1, ItemClassification.filler),
    ItemName.Spoke_6: ItemData(BASE_IDS.WHEELS + 9, 1, ItemClassification.filler),
    ItemName.Flush_3: ItemData(BASE_IDS.WHEELS + 10, 1, ItemClassification.filler),
    ItemName.Flush_4: ItemData(BASE_IDS.WHEELS + 11, 1, ItemClassification.filler),
    ItemName.Flush_5: ItemData(BASE_IDS.WHEELS + 12, 1, ItemClassification.filler),
    ItemName.Spoke_7: ItemData(BASE_IDS.WHEELS + 13, 1, ItemClassification.filler),
    # ItemName.Spoke_666: ItemData(BASE_IDS.WHEELS + 14, 1, ItemClassification.filler), # Devil Parts not currently in item pool
}

lights = {
    ItemName.Fog_Lights: ItemData(BASE_IDS.LIGHTS + 1, 1, ItemClassification.filler),
    ItemName.Beam_Lights: ItemData(BASE_IDS.LIGHTS + 2, 1, ItemClassification.filler),
}

wing_set = {
    ItemName.Wing_Set: ItemData(BASE_IDS.WING_SET + 1, 1, ItemClassification.progression),
}

special_parts = {
    ItemName.Propeller: ItemData(BASE_IDS.SPECIAL_PARTS + 1, 1, ItemClassification.progression),
    ItemName.Jet_Turbine: ItemData(BASE_IDS.SPECIAL_PARTS + 2, 1, ItemClassification.progression),
}

options = {
    ItemName.Water_Ski: ItemData(BASE_IDS.OPTIONS + 1, 1, ItemClassification.progression),
    ItemName.Flight_Wing: ItemData(BASE_IDS.OPTIONS + 2, 1, ItemClassification.useful),
    ItemName.Police_Light: ItemData(BASE_IDS.OPTIONS + 3, 1, ItemClassification.filler),
    ItemName.Billboard_Coffee_Shop: ItemData(BASE_IDS.OPTIONS + 4, 1, ItemClassification.filler),
    ItemName.Billboard_Noodle_Shop: ItemData(BASE_IDS.OPTIONS + 5, 1, ItemClassification.filler),
    ItemName.Billboard_Cake_Shop: ItemData(BASE_IDS.OPTIONS + 6, 1, ItemClassification.filler),
    ItemName.Billboard_Wool_Shop: ItemData(BASE_IDS.OPTIONS + 7, 1, ItemClassification.filler),
    ItemName.Billboard_Coconut_Shop: ItemData(BASE_IDS.OPTIONS + 8, 1, ItemClassification.filler),
}

sticker = {
    ItemName.Sticker: ItemData(BASE_IDS.STICKER + 1, 1, ItemClassification.filler),
}

horns = {
    ItemName.Air_Horn: ItemData(BASE_IDS.HORNS + 1, 1, ItemClassification.filler),
    ItemName.Echo_Air_Horn: ItemData(BASE_IDS.HORNS + 2, 1, ItemClassification.filler),
    ItemName.Bus_Horn: ItemData(BASE_IDS.HORNS + 3, 1, ItemClassification.filler),
    ItemName.Bicycle_Bell: ItemData(BASE_IDS.HORNS + 4, 1, ItemClassification.filler),
    ItemName.Venus_Horn: ItemData(BASE_IDS.HORNS + 5, 1, ItemClassification.filler),
    ItemName.Chicken_Horn: ItemData(BASE_IDS.HORNS + 6, 1, ItemClassification.filler),
    ItemName.Fantasy_Horn: ItemData(BASE_IDS.HORNS + 7, 1, ItemClassification.filler),
    ItemName.Trumpet_Horn: ItemData(BASE_IDS.HORNS + 8, 1, ItemClassification.filler),
    ItemName.Christmas_Horn: ItemData(BASE_IDS.HORNS + 9, 1, ItemClassification.filler),
    ItemName.Duck_Horn: ItemData(BASE_IDS.HORNS + 10, 1, ItemClassification.filler),
    ItemName.Space_Horn: ItemData(BASE_IDS.HORNS + 11, 1, ItemClassification.filler),
    ItemName.Horse_Horn: ItemData(BASE_IDS.HORNS + 12, 1, ItemClassification.filler),
    ItemName.Baby_Horn: ItemData(BASE_IDS.HORNS + 13, 1, ItemClassification.filler),
    ItemName.Train_Horn: ItemData(BASE_IDS.HORNS + 14, 1, ItemClassification.filler),
}

meters = {
    ItemName.Chronometer: ItemData(BASE_IDS.METERS + 1, 1, ItemClassification.filler),
    ItemName.Rainbow_Meter: ItemData(BASE_IDS.METERS + 2, 1, ItemClassification.filler),
    ItemName.Space_Meter: ItemData(BASE_IDS.METERS + 3, 1, ItemClassification.filler),
    ItemName.Triangle_Meter: ItemData(BASE_IDS.METERS + 4, 1, ItemClassification.filler),
    ItemName.Love_Sick_Meter: ItemData(BASE_IDS.METERS + 5, 1, ItemClassification.filler),
    ItemName.Life_Meter: ItemData(BASE_IDS.METERS + 6, 1, ItemClassification.filler), # Unused in vanilla game
    ItemName.Cherry_Meter: ItemData(BASE_IDS.METERS + 7, 1, ItemClassification.filler),
    ItemName.Duck_Meter: ItemData(BASE_IDS.METERS + 8, 1, ItemClassification.filler),
    # ItemName.Devil_Meter: ItemData(BASE_IDS.METERS + 9, 1, ItemClassification.filler), # Devil Parts not currently in item pool
    ItemName.Digital_Meter: ItemData(BASE_IDS.METERS + 10, 1, ItemClassification.filler),
}

garage_wallpapers = {
    # ItemName.Stylish Pattern: ItemData(BASE_IDS.COLLECTIBLES + 0, 1, ItemClassification.filler), # Automatically given after entering garage for first time
    ItemName.Flower_Pattern: ItemData(BASE_IDS.COLLECTIBLES + 1, 1, ItemClassification.filler),
    ItemName.Sky_Pattern: ItemData(BASE_IDS.COLLECTIBLES + 2, 1, ItemClassification.filler),
    ItemName.Soccer_Pattern: ItemData(BASE_IDS.COLLECTIBLES + 3, 1, ItemClassification.filler),
    ItemName.UFO_Pattern: ItemData(BASE_IDS.COLLECTIBLES + 4, 1, ItemClassification.filler),
    ItemName.Hide_Out_Pattern: ItemData(BASE_IDS.COLLECTIBLES + 5, 1, ItemClassification.filler),
    ItemName.Room_With_A_View: ItemData(BASE_IDS.COLLECTIBLES + 6, 1, ItemClassification.filler),
    ItemName.Urban_Pattern: ItemData(BASE_IDS.COLLECTIBLES + 7, 1, ItemClassification.filler),
    ItemName.Summer_Pattern: ItemData(BASE_IDS.COLLECTIBLES + 8, 1, ItemClassification.filler),
    ItemName.Arctic_Pattern: ItemData(BASE_IDS.COLLECTIBLES + 9, 1, ItemClassification.filler),
}

garage_decorations = {
    ItemName.Local_Peach_Wine: ItemData(BASE_IDS.COLLECTIBLES + 10, 1, ItemClassification.filler),
    ItemName.Peach_Doll: ItemData(BASE_IDS.COLLECTIBLES + 11, 1, ItemClassification.filler),
    ItemName.Gold_Ornament: ItemData(BASE_IDS.COLLECTIBLES + 12, 1, ItemClassification.filler),
    ItemName.Policemans_Club: ItemData(BASE_IDS.COLLECTIBLES + 13, 1, ItemClassification.filler),
    ItemName.Mini_Tower: ItemData(BASE_IDS.COLLECTIBLES + 14, 1, ItemClassification.filler),
    ItemName.Toy_Gun: ItemData(BASE_IDS.COLLECTIBLES + 15, 1, ItemClassification.filler),
    ItemName.M_Cartons_Painting: ItemData(BASE_IDS.COLLECTIBLES + 16, 1, ItemClassification.filler),
    ItemName.Model_Train: ItemData(BASE_IDS.COLLECTIBLES + 17, 1, ItemClassification.filler),
    ItemName.Christmas_Tree: ItemData(BASE_IDS.COLLECTIBLES + 18, 1, ItemClassification.filler),
    ItemName.UnbaboDoll: ItemData(BASE_IDS.COLLECTIBLES + 19, 1, ItemClassification.filler),
    ItemName.Papaya_Ukulele: ItemData(BASE_IDS.COLLECTIBLES + 20, 1, ItemClassification.filler),
    ItemName.Angels_Wings: ItemData(BASE_IDS.COLLECTIBLES + 21, 1, ItemClassification.filler),
    ItemName.Gods_Rod: ItemData(BASE_IDS.COLLECTIBLES + 22, 1, ItemClassification.filler),
}

area_unlocks = {
    ItemName.Local_Peach_Wine_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 10, 1, ItemClassification.progression), # Peach Town unlock (given at start)
    ItemName.Peach_Doll_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 11, 1, ItemClassification.progression), # Peach Town unlock (given at start)    
    ItemName.Gold_Ornament_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 12, 1, ItemClassification.progression), # Fuji City unlock
    ItemName.Policemans_Club_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 13, 1, ItemClassification.progression), # Fuji City unlock
    ItemName.Mini_Tower_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 14, 1, ItemClassification.progression), # Sandpolis unlock
    ItemName.Toy_Gun_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 15, 1, ItemClassification.progression), # Sandpolis unlock
    ItemName.M_Cartons_Painting_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 16, 1, ItemClassification.progression), # Chestnut Canyon unlock
    ItemName.Model_Train_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 17, 1, ItemClassification.progression), # Chestnut Canyon unlock
    ItemName.Flower_Pattern_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 1, 1, ItemClassification.progression), # Mushroom Road unlock
    ItemName.Sky_Pattern_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 2, 1, ItemClassification.progression), # Mushroom Road unlock
    ItemName.Christmas_Tree_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 18, 1, ItemClassification.progression), # White Mountain unlock
    ItemName.Arctic_Pattern_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 9, 1, ItemClassification.progression), # White Mountain unlock
    ItemName.UnbaboDoll_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 19, 1, ItemClassification.progression), # Papaya Island unlock
    ItemName.Papaya_Ukulele_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 20, 1, ItemClassification.progression), # Papaya Island unlock
    ItemName.Angels_Wings_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 21, 1, ItemClassification.progression), # Cloud Hill unlock
    ItemName.Gods_Rod_Key: ItemData(BASE_IDS.AREA_UNLOCKS + 22, 1, ItemClassification.progression), # Cloud Hill unlock
}

collectibles = {
    ItemName.Wallet: ItemData(BASE_IDS.COLLECTIBLES + 23, 1, ItemClassification.progression),
    ItemName.Voucher: ItemData(BASE_IDS.COLLECTIBLES + 24, 1, ItemClassification.progression),
    ItemName.Hero_Super_Card: ItemData(BASE_IDS.COLLECTIBLES + 25, 1, ItemClassification.progression),
    ItemName.Pretty_Doll: ItemData(BASE_IDS.COLLECTIBLES + 26, 1, ItemClassification.progression),
    ItemName.Relief: ItemData(BASE_IDS.COLLECTIBLES + 27, 1, ItemClassification.progression),
    ItemName.Uzumasas_Autograph: ItemData(BASE_IDS.COLLECTIBLES + 28, 1, ItemClassification.progression),
    ItemName.Rice_Ball: ItemData(BASE_IDS.COLLECTIBLES + 29, 1, ItemClassification.progression),
    ItemName.Canary_Recorder: ItemData(BASE_IDS.COLLECTIBLES + 30, 1, ItemClassification.progression),
    ItemName.Magazine: ItemData(BASE_IDS.COLLECTIBLES + 31, 1, ItemClassification.progression),
    ItemName.Blue_Sapphire: ItemData(BASE_IDS.COLLECTIBLES + 32, 1, ItemClassification.progression),
    ItemName.Emerald: ItemData(BASE_IDS.COLLECTIBLES + 33, 1, ItemClassification.progression),
    ItemName.Ruby: ItemData(BASE_IDS.COLLECTIBLES + 34, 1, ItemClassification.progression),
    ItemName.Topaz: ItemData(BASE_IDS.COLLECTIBLES + 35, 1, ItemClassification.progression),
    ItemName.Black_Opal: ItemData(BASE_IDS.COLLECTIBLES + 36, 1, ItemClassification.progression),
    ItemName.Moonstone: ItemData(BASE_IDS.COLLECTIBLES + 37, 1, ItemClassification.progression),
    ItemName.Amethyst: ItemData(BASE_IDS.COLLECTIBLES + 38, 1, ItemClassification.progression),
    ItemName.Soccer_Ball: ItemData(BASE_IDS.COLLECTIBLES + 39, 1, ItemClassification.progression),
    ItemName.Fountain_Pen: ItemData(BASE_IDS.COLLECTIBLES + 40, 1, ItemClassification.progression),
    ItemName.Flower_Seed: ItemData(BASE_IDS.COLLECTIBLES + 41, 1, ItemClassification.progression),
    ItemName.Papu_Flower: ItemData(BASE_IDS.COLLECTIBLES + 42, 1, ItemClassification.progression),
    ItemName.Fluffy_Mushroom: ItemData(BASE_IDS.COLLECTIBLES + 43, 1, ItemClassification.progression),
    ItemName.Small_Bottle: ItemData(BASE_IDS.COLLECTIBLES + 44, 1, ItemClassification.progression),
    ItemName.Coin_Radar: ItemData(BASE_IDS.COLLECTIBLES + 45, 1, ItemClassification.useful),
    ItemName.Package: ItemData(BASE_IDS.COLLECTIBLES + 46, 1, ItemClassification.progression),
    ItemName.Peach: ItemData(BASE_IDS.COLLECTIBLES + 47, 1, ItemClassification.progression),
}

licenses = {
    ItemName.Progressive_License: ItemData(BASE_IDS.PROGRESSIVE_LICENSE, 3, ItemClassification.progression),
}

stamps = {
    ItemName.Stamp: ItemData(BASE_IDS.STAMP, 99, ItemClassification.progression),
}

progressive_parts = {
    ItemName.Progressive_Tires: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET1, 11, ItemClassification.progression), # Devil Tires not included
    ItemName.Progressive_Engine: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET1 + 1, 10, ItemClassification.progression), # Devil Engine not included
    ItemName.Progressive_Chassis: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET1 + 2, 4, ItemClassification.progression),
    ItemName.Progressive_Transmission: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET1 + 3, 5, ItemClassification.progression),
    ItemName.Progressive_Steering: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET1 + 4, 3, ItemClassification.progression),
    ItemName.Progressive_Brakes: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET1 + 5, 3, ItemClassification.progression),
}

progressive_parts_set_2 = {
    ItemName.Progressive_Tires_Set_2: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET2, 11, ItemClassification.useful), # Devil Tires not included
    ItemName.Progressive_Engine_Set_2: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET2 + 1, 10, ItemClassification.useful), # Devil Engine not included
    ItemName.Progressive_Chassis_Set_2: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET2 + 2, 4, ItemClassification.useful),
    ItemName.Progressive_Transmission_Set_2: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET2 + 3, 5, ItemClassification.useful),
    ItemName.Progressive_Steering_Set_2: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET2 + 4, 3, ItemClassification.useful),
    ItemName.Progressive_Brakes_Set_2: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET2 + 5, 3, ItemClassification.useful),
}

progressive_parts_set_3 = {
    ItemName.Progressive_Tires_Set_3: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET3 + 1, 11, ItemClassification.useful), # Devil Tires not included
    ItemName.Progressive_Engine_Set_3: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET3 + 2, 10, ItemClassification.useful), # Devil Engine not included
    ItemName.Progressive_Chassis_Set_3: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET3 + 3, 4, ItemClassification.useful),
    ItemName.Progressive_Transmission_Set_3: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET3 + 4, 5, ItemClassification.useful),
    ItemName.Progressive_Steering_Set_3: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET3 + 5, 3, ItemClassification.useful),
    ItemName.Progressive_Brakes_Set_3: ItemData(BASE_IDS.PROGRESSIVE_PARTS_SET3 + 6, 3, ItemClassification.useful),
}

filler = {
    ItemName.Filler: ItemData(BASE_IDS.FILLER, 0, ItemClassification.filler)
}

victory = {
    ItemName.Victory: ItemData(BASE_IDS.VICTORY, 1, ItemClassification.progression)
}

item_table : dict[str, ItemData] = {
    **filler,
    **bodies,

    # TODO: Include if non-progressive parts, remove if progressive parts
    #**tires, 
    #**engines
    #**chassis
    #**transmission
    #**steering
    #**brakes

    **wheels,
    **lights,
    **wing_set,
    **special_parts,
    **options,
    **sticker,
    **horns,
    **meters,
    **garage_wallpapers,
    **garage_decorations,
    **area_unlocks,
    **collectibles,
    **licenses,
    **stamps,

    # TODO: Include if progressive parts, remove if non-progressive parts
    **progressive_parts,
    **progressive_parts_set_2,
    **progressive_parts_set_3,

    **victory
}

# Used for item_name_to_base_ID in Addresses.py
# TODO: Change logic so that item_table can have all items?
all_item_table : dict[str, ItemData] = {
    **filler,
    **bodies,
    **tires,
    **engines,
    **chassis,
    **transmission,
    **steering,
    **brakes,
    **wheels,
    **lights,
    **wing_set,
    **special_parts,
    **options,
    **sticker,
    **horns,
    **meters,
    **garage_wallpapers,
    **garage_decorations,
    **area_unlocks,
    **collectibles,
    **licenses,
    **stamps,
    **progressive_parts,
    **progressive_parts_set_2,
    **progressive_parts_set_3,
    **victory 
}

def item_name_to_base_ID(item_name : str) -> int:
    item_ID = all_item_table[item_name].id

    prev_base_ID = 0
    for base_ID in BASE_IDS.get_all_as_list():
        if item_ID >= base_ID:
            prev_base_ID = base_ID
            continue
        else:
            assert prev_base_ID != 0, "item_name_to_base_ID: Item has a lower index than the lowest Road Trip item"
            return prev_base_ID

# ------------------------------------------

# Called by __init__.py
def create_item_RTA(world : World, name : str):
    from . import RoadTripItem

    data = item_table[name]
    return RoadTripItem(name, data.classification, data.id, world.player)
    
# Called by __init__.py
def create_items_RTA(world : World):
    from .names import LocationName

    # Confirm that locations have been created
    assert list(world.get_locations()).count, "create_items_RTA tried to run before any Locations were added to the passed in world instance."

    options = get_RTA_options(world.multiworld, world.player)
    
    item_count = 0
    license_items = [] # Store the license items in case needed later for the 'force vanilla location' option
    for item_name in item_table:
        # If our area unlock mode is Decorations, skip any Stamp-mode-only items.
        if item_name in stamp_progression_only and options.area_unlock_mode == AreaUnlockMode.option_decorations:
            continue

        # If our area unlock mode is Stamps, skip any Decorations-mode-only items.
        if item_name in decoration_progression_only and options.area_unlock_mode == AreaUnlockMode.option_stamps:
            continue

        # If we're not adding two additional progressive item tracks, do not add any of the 3rd
        #     set of progression items.
        if item_name in progressive_parts_set_3 and options.additional_progressive_part_tracks < 2:
            continue

        # If we're not adding *any* additional progressive item tracks, don't add any of the 2nd
        #     set of progression items, either.
        if item_name in progressive_parts_set_2 and options.additional_progressive_part_tracks < 1:
            continue

        item_data = item_table[item_name]
        for _ in range(item_data.quantity):
            item = create_item_RTA(world, item_name)
            
            # If this is the victory item, force it to be placed at Stamp 100, and *don't* place it in the item pool.
            #    (Items placed prior to AP's fill algorithm running can't be in the item pool.)
            if item.name == ItemName.Victory:
                world.multiworld.get_location(LocationName.Stamp_100, world.player).place_locked_item(item)
                item_count += 1
            # If we're using decorations progression mode, and this item is either of the Peach Town keys, precollect them,
            #     and don't add them to the item pool.
            elif options.area_unlock_mode == AreaUnlockMode.option_decorations and \
               item.name == ItemName.Local_Peach_Wine_Key or item.name == ItemName.Peach_Doll_Key:
               world.multiworld.push_precollected(item)
            # Store reference to license items prior to adding them to the item pool.
            elif item.name == ItemName.Progressive_License:
                license_items.append(item)
                # Do not add licenses to the item pool if they are going to be forced to their vanilla locations
                #     (AP expects all force-placed items to not be in the item pool), or if they will be precollected.
                if options.license_handling == LicenseHandling.option_standard:
                    world.multiworld.itempool += [item]
                    item_count += 1
                if options.license_handling == LicenseHandling.option_vanilla:
                    # Still increase the item count for vanilla placement, since they will get added later.
                    item_count += 1
                if options.license_handling == LicenseHandling.option_remove:
                    world.multiworld.push_precollected(item)
            else:
                world.multiworld.itempool += [item]
                item_count += 1
    
    # If the licenses have been forced to their vanilla locations, handle this now.
    if options.license_handling == LicenseHandling.option_vanilla:
        if len(license_items) == 3:
            world.multiworld.get_location(LocationName.B_License_Obtained, world.player).place_locked_item(license_items[0])
            world.multiworld.get_location(LocationName.A_License_Obtained, world.player).place_locked_item(license_items[1])
            world.multiworld.get_location(LocationName.Super_A_License_Obtained, world.player).place_locked_item(license_items[2])
        else:
            raise Exception(f"create_items_RTA: License item count not equal to 3? License count: {len(license_items)}")
    
    # Check to see if the location and item counts do not match (they likely will not)
    iterator = world.get_locations() # world.get_locations() returns an Iterator
    location_count = sum(1 for _ in iterator) # len() can't handle Iterators, we have to exhaust the iterator instead to get the count

    # If there are more items than there are locations, remove filler items in a particular order until
    #     the counts are equal.
    if item_count > location_count:
        # First remove (non-key) wallpapers, then (non-key) decorations, and so on in the below order.
        # Wallpapers and decorations are removed first since they have the least use in game.
        wallpaper_names = [name for name in garage_wallpapers.keys()]
        decoration_names = [name for name in garage_decorations.keys()]
        body_names = [name for name in bodies.keys()]
        sticker_names = [name for name in sticker.keys()]
        wheel_names = [name for name in wheels.keys()]
        meter_names = [name for name in meters.keys()]

        categories = [wallpaper_names, decoration_names, body_names, sticker_names, wheel_names, meter_names]

        for category in categories:
            world.random.shuffle(category)

        # Remove items until the item count matches the location count.
        while item_count > location_count:
            # Check to make sure we haven't run out of items to try to remove.
            if not len(categories):
                raise Exception("Road Trip: Could not remove enough items to make item count equal to location count.")
            
            # Get the next category to remove an item from.
            category = categories[0]

            # If there are still items to remove in this category...
            if len(category):
                # Get the next item from that category to remove.
                item_name = category[0]
                item_pool = world.multiworld.itempool

                # See if we can find an item with this name in the item pool
                item = next((item for item in item_pool if item.name == item_name), None) # https://stackoverflow.com/a/2364277

                # If an item with this name was found, remove it, and decrement the item count.
                # An item with the given name might *not* be found if we skipped creating the item with that name
                #     earlier. For example, we're only trying to remove non-key versions of the garage items - if
                #     we made the key version of a garage item instead of the non-key version, we won't find it now.
                if item != None:
                    item_pool.remove(item)
                    item_count -= 1

                # Either way, pop the item name from the category list.
                category.remove(item_name)
            # If we're out of items to remove from the category, remove the category so we can move on to the next one.
            else:
                categories.remove(category)
    # If there are fewer items than there are locations, create filler items and add them to the pool.
    else:
        while item_count < location_count:
            item = create_item_RTA(world, ItemName.Filler)
            world.multiworld.itempool += [item]
            item_count += 1

    # assert item_count - 1 == len(world.multiworld.itempool), "End of create_items_RTA: item_count does not match actual count in itempool, something went wrong while processing items."
    # Subtract one because the victory item is not in the item pool