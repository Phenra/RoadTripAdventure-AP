from .names import ItemName, LocationName, RegionName

# -------- Regions --------
# Any entrance with one of these destinations should not be included in room rando.
do_not_room_rando_list : list[str] = [
    # These can never be randomized
    RegionName.Fuji_City_Guarded_Dungeon, # Can't return here after visiting
    RegionName.Cloud_Hill_Invalid_Room, # Unused room, never accessible
    RegionName.Papaya_Island_NPC_Kite, # Never available in NTSC due to Recycle Shop being accessible from the start

    # If the garage is always going to be available at the start, this probably shouldn't be randomized?
    RegionName.My_City_Wonder_Realty,

    # Randomizing this could in theory cause some unwinnable seeds due to not being able to get more money?
    RegionName.Peach_Town_Qs_Factory,

    # Keep vanilla for now, should randomize in the future.
    # Need to figure out how to get Kevin's NPC warp to change location.
    RegionName.Peach_Town_Kevin_House,

    # Keep vanilla for now, this should probably have a YAML setting.
    RegionName.Papaya_Island_Cloud_Hill_Warp,

    # TODO: Potentially create a 'chaos mode' that could enable randomizing these
    RegionName.Peach_Town_Barrel_Dodging_Complete,
    RegionName.Chestnut_Canyon_Rock_Climbing_Complete,
    RegionName.My_City_Recycle_Shop,
    RegionName.Cloud_Hill_White_House_Lobby,
    RegionName.Cloud_Hill_President_Room,
]

quick_pic_shops_list : list[str] = {
    # Placing 28 and 29 first in the list so that in playthroughs where rooms are not randomized,
    #  canAccessAllQuickPicShops will fail quickly when False, as these are the hardest two to access.  
    RegionName.Quick_Pic_28, 
    RegionName.Quick_Pic_29,
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
    RegionName.Quick_Pic_11,
    RegionName.Quick_Pic_12,
    RegionName.Quick_Pic_13,
    RegionName.Quick_Pic_14,
    RegionName.Quick_Pic_15,
    RegionName.Quick_Pic_16,
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
    RegionName.Quick_Pic_30,
    RegionName.Quick_Pic_31,
    RegionName.Quick_Pic_32,
    RegionName.Quick_Pic_33,
    RegionName.Quick_Pic_34,
    RegionName.Quick_Pic_35,
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
    RegionName.Quick_Pic_48,
    RegionName.Quick_Pic_49,
    RegionName.Quick_Pic_50,
    RegionName.Quick_Pic_51,
    RegionName.Quick_Pic_52,
    RegionName.Quick_Pic_53,
    RegionName.Quick_Pic_54,
    RegionName.Quick_Pic_55,
    RegionName.Quick_Pic_56,
    RegionName.Quick_Pic_57,
    RegionName.Quick_Pic_58,
    RegionName.Quick_Pic_59,
    RegionName.Quick_Pic_60,
    RegionName.Quick_Pic_61,
    RegionName.Quick_Pic_62,
    RegionName.Quick_Pic_63,
    RegionName.Quick_Pic_64,
    RegionName.Quick_Pic_65,
    RegionName.Quick_Pic_66,
    RegionName.Quick_Pic_67,
    RegionName.Quick_Pic_68,
    RegionName.Quick_Pic_69,
    RegionName.Quick_Pic_70,
    RegionName.Quick_Pic_71,
    RegionName.Quick_Pic_72,
    RegionName.Quick_Pic_73,
    RegionName.Quick_Pic_74,
    RegionName.Quick_Pic_75,
    RegionName.Quick_Pic_76,
    RegionName.Quick_Pic_77,
    RegionName.Quick_Pic_78,
    RegionName.Quick_Pic_79,
    RegionName.Quick_Pic_80,
    RegionName.Quick_Pic_81,
    RegionName.Quick_Pic_82,
    RegionName.Quick_Pic_83,
    RegionName.Quick_Pic_84,
    RegionName.Quick_Pic_85,
    RegionName.Quick_Pic_86,
    RegionName.Quick_Pic_87,
    RegionName.Quick_Pic_88,
    RegionName.Quick_Pic_89,
    RegionName.Quick_Pic_90,
    RegionName.Quick_Pic_91,
    RegionName.Quick_Pic_92,
    RegionName.Quick_Pic_93,
    RegionName.Quick_Pic_94,
    RegionName.Quick_Pic_95,
    RegionName.Quick_Pic_96,
    RegionName.Quick_Pic_97,
    RegionName.Quick_Pic_98,
    RegionName.Quick_Pic_99,
    RegionName.Quick_Pic_100,
}

my_city_invites_list = [
    RegionName.Peach_Town_NPC_Accel, # Police Station
    RegionName.Sandpolis_NPC_Akiban, # Tunnel Race
    RegionName.Fuji_City_NPC_Brian, # Fire Station
    RegionName.Fuji_City_NPC_Coine, # Coine
    RegionName.Sandpolis_NPC_Dayan, # Which-Way Maze
    RegionName.Peach_Town_NPC_Flower, # Flower
    RegionName.Fuji_City_NPC_Gichi, # Gichi
    RegionName.Sandpolis_NPC_George, # Theater
    RegionName.Peach_Town_NPC_Gonzo, # Q's Factory
    # RegionName.Papaya_Island_NPC_Kite, # Recycle Shop. Available by default (in NTSC version).
    RegionName.Chestnut_Canyon_NPC_Kuwano, # Kuwano
    RegionName.White_Mountain_NPC_Manei, # Bank
    RegionName.Papaya_Island_NPC_Mien, # Mien
    RegionName.Papaya_Island_NPC_Nouri, # Paint Shop
    RegionName.Peach_Town_NPC_Ramsey, # Body Shop
    RegionName.Sandpolis_NPC_Roberts, # Tower
    RegionName.Sandpolis_NPC_Ryoji, # School
    RegionName.White_Mountain_NPC_Sally, # Sally
    RegionName.White_Mountain_NPC_Suess, # Parts Shop
    RegionName.Peach_Town_NPC_Cobran, # Roaming NPC Cobran
    RegionName.Chestnut_Canyon_NPC_Saucy, # Roaming NPC Saucy
]


# -------- Locations --------
challenge_minigames : dict[str] = {
    LocationName.Stamp_6,   # Barrel Dodging
    LocationName.Stamp_15,  # Treasure Hunting Maze in 3 min
    LocationName.Stamp_16,  # Sliding Door Race
    LocationName.Stamp_21,  # Highway Race  # Urban Pattern, double-up
    LocationName.Stamp_22,  # Highway Race in less than 50 seconds
    LocationName.Stamp_27,  # Drag Race
    LocationName.Stamp_28,  # Drag Race in less than 8 seconds
    LocationName.Stamp_38,  # Win Soccer  # Soccer Pattern, double-up
    LocationName.Stamp_44,  # Tunnel Race  # Space Meter, double-up
    LocationName.Stamp_47,  # Which-Way Race  # RS Magnum, double-up
    LocationName.Stamp_55,  # Volcano Course
    LocationName.Stamp_56,  # Volcano Course in 1 min 10 seconds
    LocationName.Stamp_57,  # Rock Climbing
    LocationName.Stamp_58,  # Rock Climbing in 2 min
    LocationName.Stamp_66,  # Ski Jump
    LocationName.Stamp_70,  # Curling, over 200 points
    LocationName.Stamp_75,  # Obstacle Course
    LocationName.Stamp_76,  # Obstacle Course within 2 min
    LocationName.Stamp_78,  # Beach Flag  # Summer Pattern, double-up
    LocationName.Stamp_90   # Rainbow Jump  # Rainbow Meter, double-up
}

double_up_stamps : dict[str, str] = {
    # NOTE: The LocationData for the first location (item reward) is used for the new combined location (just with a new unique ID set).
    LocationName.Coine_Reward_10: LocationName.Stamp_46,
    LocationName.Angels_Wings: LocationName.Stamp_86,
    LocationName.Arctic_Pattern: LocationName.Stamp_62,
    LocationName.Baby_Horn: LocationName.Stamp_59,
    LocationName.Body_Q003: LocationName.Stamp_98,
    LocationName.Body_Q030: LocationName.Stamp_42,
    LocationName.Body_Q037: LocationName.Stamp_63,
    LocationName.Body_Q082: LocationName.Stamp_71,
    LocationName.Duck_Quiz_3: LocationName.Stamp_89,
    LocationName.Body_Q087: LocationName.Stamp_9,
    LocationName.Body_Q089: LocationName.Stamp_48,
    LocationName.Body_Q150: LocationName.Stamp_7,
    LocationName.Cherry_Meter: LocationName.Stamp_14,
    LocationName.Chicken_Horn: LocationName.Stamp_39,
    LocationName.Christmas_Horn: LocationName.Stamp_67,
    LocationName.Christmas_Tree: LocationName.Stamp_61,
    LocationName.Coin_Radar: LocationName.Stamp_68,
    LocationName.Fantasy_Horn: LocationName.Stamp_97,
    LocationName.Flower_Pattern: LocationName.Stamp_41,
    LocationName.Flower_Seed: LocationName.Stamp_64,
    LocationName.Gods_Rod: LocationName.Stamp_87,
    LocationName.Gold_Ornament: LocationName.Stamp_11,
    LocationName.Hide_Out_Pattern: LocationName.Stamp_30,
    LocationName.Jet_Turbine: LocationName.Stamp_81,
    LocationName.Local_Peach_Wine: LocationName.Stamp_2,
    LocationName.Love_Sick_Meter: LocationName.Stamp_17,
    LocationName.M_Cartons_Painting: LocationName.Stamp_53,
    LocationName.Mini_Tower: LocationName.Stamp_24,
    LocationName.Model_Train: LocationName.Stamp_54,
    LocationName.Papaya_Ukulele: LocationName.Stamp_74,
    LocationName.Peach_Doll: LocationName.Stamp_3,
    LocationName.Policemans_Club: LocationName.Stamp_12,
    LocationName.RS_Magnum: LocationName.Stamp_47,
    LocationName.Rainbow_Meter: LocationName.Stamp_90,
    LocationName.Room_with_a_View: LocationName.Stamp_20,
    LocationName.Sky_Pattern: LocationName.Stamp_88,
    LocationName.Soccer_Pattern: LocationName.Stamp_38,
    LocationName.Space_Meter: LocationName.Stamp_44,
    LocationName.Summer_Pattern: LocationName.Stamp_78,
    LocationName.Toy_Gun: LocationName.Stamp_25,
    LocationName.Trumpet_Horn: LocationName.Stamp_19,
    LocationName.UFO_Pattern: LocationName.Stamp_99,
    LocationName.UnbaboDoll: LocationName.Stamp_73,
    LocationName.Urban_Pattern: LocationName.Stamp_21,
    LocationName.Venus_Horn: LocationName.Stamp_92,
}

def get_combined_double_up_stamp_name(location_name : str) -> str:
    try:
        stamp = double_up_stamps[location_name]
        return location_name + " / " + stamp
    except KeyError:
        # See if the passed string is maybe a value in the dictionary (i.e. stamp name), instead of a key
        for item_reward, stamp in double_up_stamps.items():
            if location_name == stamp:
                return item_reward + " / " + stamp
        
        # Else, it's not part of a double-up stamp
        raise KeyError("get_combined_double_up_stamp_name: Passed location name is not part of a double-up stamp.")


# -------- Items --------
decoration_progression_only : dict[str] = {
    # Peach Town unlocks (given at the start)
    ItemName.Local_Peach_Wine_Key,
    ItemName.Peach_Doll_Key,

    # Fuji City unlocks
    ItemName.Gold_Ornament_Key,
    ItemName.Policemans_Club_Key,

    # Sandpolis unlocks
    ItemName.Mini_Tower_Key,
    ItemName.Toy_Gun_Key,

    # Chestnut Canyon unlocks
    ItemName.M_Cartons_Painting_Key,
    ItemName.Model_Train_Key,

    # Mushroom Road unlocks
    ItemName.Flower_Pattern_Key,
    ItemName.Sky_Pattern_Key,

    # White Mountain unlocks
    ItemName.Christmas_Tree_Key,
    ItemName.Arctic_Pattern_Key,

    # Papaya Island unlocks
    ItemName.UnbaboDoll_Key,
    ItemName.Papaya_Ukulele_Key,

    # Cloud Hill unlocks
    ItemName.Angels_Wings_Key,
    ItemName.Gods_Rod_Key,
}

stamp_progression_only : dict[str] = {
    ItemName.Stamp,

    # Normal filler versions of the area unlock items
    ItemName.Local_Peach_Wine,
    ItemName.Peach_Doll,
    ItemName.Gold_Ornament,
    ItemName.Policemans_Club,
    ItemName.Mini_Tower,
    ItemName.Toy_Gun,
    ItemName.Model_Train,
    ItemName.M_Cartons_Painting,
    ItemName.Flower_Pattern,
    ItemName.Sky_Pattern,
    ItemName.Christmas_Tree,
    ItemName.Arctic_Pattern,
    ItemName.Papaya_Ukulele,
    ItemName.UnbaboDoll,
    ItemName.Gods_Rod,
    ItemName.Angels_Wings,
}