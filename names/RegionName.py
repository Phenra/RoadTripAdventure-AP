from enum import StrEnum

# Overworld regions
#
# Most locations in Road Trip have their own dedicated region for the sake of supporting room rando.
#   Therefore, most locations should NOT have their region attribute set to a base region.
#   To help enforce this, the base regions have been placed inside of a class to make them harder to use by mistake.
class Base(StrEnum):
    # Menu is the default first region created by AP, which will connect to all of the base regions (except Cloud Hill).
    # Should also be used for several locations handled entirely by access rules (e.g. license upgrades).
    No_Region = "None"
    Menu = "Menu"
    Peach_Town = "Peach Town",
    Fuji_City = "Fuji City",
    My_City = "My City",
    Sandpolis = "Sandpolis",
    Chestnut_Canyon = "Chestnut Canyon",
    Mushroom_Road = "Mushroom Road",
    White_Mountain = "White Mountain",
    Papaya_Island = "Papaya Island",
    Papaya_Island_Upper = "Papaya Island - Upper Region",
    Papaya_Island_Island = "Papaya Island - Warp Island",
    Cloud_Hill = "Cloud Hill"

# Peach Town rooms
Peach_Town_Qs_Factory = "Peach Town - Q's Factory"
Peach_Town_Parts_Shop = "Peach Town - Parts Shop"
Peach_Town_Body_Shop = "Peach Town - Body Shop"
Peach_Town_Paint_Shop = "Peach Town - Paint Shop"
Peach_Town_Bar = "Peach Town - Bar"
Peach_Town_Police_Station = "Peach Town - Police Station"
Peach_Town_Radio_Station = "Peach Town - Radio Station"
Peach_Town_Farm_House = "Peach Town - Farm House"
Peach_Town_Kevin_House = "Peach Town - Kevin's House"
Peach_Town_Wolf_House = "Peach Town - Wolf's House"
Peach_Town_Best_House = "Peach Town - Best's House"
Peach_Town_Jousset_House = "Peach Town - Jousset's House"
Peach_Town_Coffee_Shop = "Peach Town - Coffee Shop"
Peach_Town_Barrel_Dodging = "Peach Town - Barrel Dodging"
Peach_Town_Gemstone_House = "Peach Town - Gemstone House"
Peach_Town_Fight_House = "Peach Town - Fight's House (Trade Quests 1 & 8)"
Peach_Town_Milton_House = "Peach Town - Milton's House"
Peach_Town_Barrel_Dodging_Complete = "Peach Town - Barrel Dodging Complete"
Quick_Pic_1 = "Quick-Pic Shop No. 1"
Quick_Pic_2 = "Quick-Pic Shop No. 2"
Quick_Pic_3 = "Quick-Pic Shop No. 3"
Quick_Pic_4 = "Quick-Pic Shop No. 4"
Quick_Pic_5 = "Quick-Pic Shop No. 5"
Quick_Pic_6 = "Quick-Pic Shop No. 6"
Quick_Pic_7 = "Quick-Pic Shop No. 7"
Quick_Pic_8 = "Quick-Pic Shop No. 8"
Quick_Pic_9 = "Quick-Pic Shop No. 9"
Quick_Pic_10 = "Quick-Pic Shop No. 10"

# Peach Town NPCs
Peach_Town_NPC_James = "Peach Town Roaming NPC - James"
Peach_Town_NPC_Gonzo = "Peach Town Roaming NPC - Gonzo"
Peach_Town_NPC_Ramsey = "Peach Town Roaming NPC - Ramsey"
Peach_Town_NPC_Accel = "Peach Town Roaming NPC - Accel"
Peach_Town_NPC_Cobran = "Peach Town Roaming NPC - Cobran"
Peach_Town_NPC_Flower = "Peach Town Roaming NPC - Flower"
Peach_Town_NPC_Klein = "Peach Town Roaming NPC - Klein"
Peach_Town_NPC_Barthou = "Peach Town Roaming NPC - Barthou"
Peach_Town_NPC_Pillow = "Peach Town Roaming NPC - Pillow"
Peach_Town_NPC_Kevin = "Peach Town Roaming NPC - Kevin"
Peach_Town_NPC_Newman = "Peach Town Roaming NPC - Newman"

# Fuji City rooms
Fuji_City_Qs_Factory = "Fuji City - Q's Factory"
Fuji_City_Parts_Shop = "Fuji City - Parts Shop"
Fuji_City_Body_Shop = "Fuji City - Body Shop"
Fuji_City_Paint_Shop = "Fuji City - Paint Shop"
Fuji_City_Bar = "Fuji City - Bar"
Fuji_City_Heizo_House = "Fuji City - Heizo's House"
Fuji_City_Echigoya_Shop = "Fuji City - Echigoya Shop"
Fuji_City_Castle_Princess_Nanaha = "Fuji City - Castle, Princess Nanaha"
Fuji_City_Castle_Sliding_Door_Race = "Fuji City - Castle, Sliding Door Race"
Fuji_City_Treasure_Hunting = "Fuji City - Treasure Hunting"
Fuji_City_Guarded_Dungeon = "Fuji City - Guarded Dungeon"
Fuji_City_Fortune_Telling_Room = "Fuji City - Fortune Telling Room"
Fuji_City_Dumpling_Shop = "Fuji City - Dumpling Shop"
Fuji_City_Uzumasa_House = "Fuji City - Uzumasa's House (Trade Quest 4)"
Fuji_City_Iwasuke_House = "Fuji City - Iwasuke's House"
Fuji_City_Hakosuke_House = "Fuji City - Hakosuke's House"
Fuji_City_Noodle_Shop = "Fuji City - Noodle Shop"
Fuji_City_Highway_Race = "Fuji City - Highway Race"
Fuji_City_Hanako_House = "Fuji City - Hanako House"
Quick_Pic_17 = "Quick-Pic Shop No. 17"
Quick_Pic_18 = "Quick-Pic Shop No. 18"
Quick_Pic_19 = "Quick-Pic Shop No. 19"
Quick_Pic_20 = "Quick-Pic Shop No. 20"
Quick_Pic_21 = "Quick-Pic Shop No. 21"
Quick_Pic_22 = "Quick-Pic Shop No. 22"
Quick_Pic_23 = "Quick-Pic Shop No. 23"
Quick_Pic_24 = "Quick-Pic Shop No. 24"
Quick_Pic_25 = "Quick-Pic Shop No. 25"
Quick_Pic_26 = "Quick-Pic Shop No. 26"

# Fuji City NPCs
Fuji_City_NPC_Guard = "Fuji City Roaming NPC - Guard"
Fuji_City_NPC_Toki = "Fuji City Roaming NPC - Toki"
Fuji_City_NPC_Matsugoro = "Fuji City Roaming NPC - Matsugoro"
Fuji_City_NPC_Sakuzo = "Fuji City Roaming NPC - Sakuzo"
Fuji_City_NPC_Shinsaku = "Fuji City Roaming NPC - Shinsaku"
Fuji_City_NPC_Shohei = "Fuji City Roaming NPC - Shohei"
Fuji_City_NPC_Brian = "Fuji City Roaming NPC - Brian"
Fuji_City_NPC_Coine = "Fuji City Roaming NPC - Coine"
Fuji_City_NPC_Gichi = "Fuji City Roaming NPC - Gichi"
Fuji_City_NPC_Goro = "Fuji City Roaming NPC - Goro"
Fuji_City_NPC_Kiyokichi = "Fuji City Roaming NPC - Kiyokichi"

# Sandpolis rooms
Sandpolis_Qs_Factory = "Sandpolis - Q's Factory"
Sandpolis_Parts_Shop = "Sandpolis - Parts Shop"
Sandpolis_Body_Shop = "Sandpolis - Body Shop"
Sandpolis_Paint_Shop = "Sandpolis - Paint Shop"
Sandpolis_Bar = "Sandpolis - Bar"
Sandpolis_Sheriff_Office = "Sandpolis - Sheriff's Office"
Sandpolis_Figure_8 = "Sandpolis - Figure 8"
Sandpolis_Soccer = "Sandpolis - Soccer"
Sandpolis_Roulette = "Sandpolis - Roulette"
Sandpolis_Mini_Tower = "Sandpolis - Mini-Tower"
Sandpolis_Drag_Race = "Sandpolis - Drag Race"
Sandpolis_Frank_House = "Sandpolis - Frank's House"
Sandpolis_Sebastian_House = "Sandpolis - Sebastian's House"
Sandpolis_Sand_Sports = "Sandpolis - Sand Sports"
Sandpolis_Mr_King_Mansion = "Sandpolis - Mr. King's Mansion"
Sandpolis_Butch_House = "Sandpolis - Butch's House"
Sandpolis_Barton_House = "Sandpolis - Barton's House (Trade Quest 2)"
Sandpolis_Cake_Shop = "Sandpolis - Cake Shop"
Sandpolis_Merci_House = "Sandpolis - Merci's House"
Sandpolis_Bob_House = "Sandpolis - Bob's House"
Sandpolis_Richard_House = "Sandpolis - Richard's House"
Quick_Pic_36 = "Quick-Pic Shop No. 36"
Quick_Pic_37 = "Quick-Pic Shop No. 37"
Quick_Pic_38 = "Quick-Pic Shop No. 38"
Quick_Pic_39 = "Quick-Pic Shop No. 39"
Quick_Pic_40 = "Quick-Pic Shop No. 40"
Quick_Pic_41 = "Quick-Pic Shop No. 41"
Quick_Pic_42 = "Quick-Pic Shop No. 42"
Quick_Pic_43 = "Quick-Pic Shop No. 43"
Quick_Pic_44 = "Quick-Pic Shop No. 44"
Quick_Pic_45 = "Quick-Pic Shop No. 45"
Quick_Pic_46 = "Quick-Pic Shop No. 46"
Quick_Pic_47 = "Quick-Pic Shop No. 47"

# Sandpolis NPCs
Sandpolis_NPC_Michael = "Sandpolis Roaming NPC - Michael"
Sandpolis_NPC_Martin = "Sandpolis Roaming NPC - Martin"
Sandpolis_NPC_Ryoji = "Sandpolis Roaming NPC - Ryoji"
Sandpolis_NPC_Akiban = "Sandpolis Roaming NPC - Akiban"
Sandpolis_NPC_Dayan = "Sandpolis Roaming NPC - Dayan"
Sandpolis_NPC_Roberts = "Sandpolis Roaming NPC - Roberts"
Sandpolis_NPC_George = "Sandpolis Roaming NPC - George"
Sandpolis_NPC_Lisalisa = "Sandpolis Roaming NPC - Lisalisa"
Sandpolis_NPC_Morrison = "Sandpolis Roaming NPC - Morrison"

# Chestnut Canyon rooms
Chestnut_Canyon_Qs_Factory = "Chestnut Canyon - Q's Factory"
Chestnut_Canyon_Bar = "Chestnut Canyon - Bar"
Chestnut_Canyon_Wallace_House = "Chestnut Canyon - Wallace"
Chestnut_Canyon_Greeting_House = "Chestnut Canyon - Greeting House" # Gene's House
Chestnut_Canyon_M_Carton_House = "Chestnut Canyon - M. Carton's House"
Chestnut_Canyon_Rock_Climbing = "Chestnut Canyon - Rock Climbing"
Chestnut_Canyon_Rock_Climbing_Complete = "Chestnut Canyon - Rock Climbing Complete"
Chestnut_Canyon_Volcano_Run = "Chestnut Canyon - Volcano Run"
Chestnut_Canyon_Tom_House = "Chestnut Canyon - Tom's House"
Chestnut_Canyon_Lowry_House = "Chestnut Canyon - Lowry's House"
Chestnut_Canyon_Betty_House = "Chestnut Canyon - Betty's House"
Chestnut_Canyon_Lucy_House = "Chestnut Canyon - Lucy's House"

Quick_Pic_60 = "Quick-Pic Shop No. 60"
Quick_Pic_61 = "Quick-Pic Shop No. 61"
Quick_Pic_62 = "Quick-Pic Shop No. 62"
Quick_Pic_63 = "Quick-Pic Shop No. 63"
Quick_Pic_64 = "Quick-Pic Shop No. 64"

# Chestnut Canyon NPCs
Chestnut_Canyon_NPC_Leon = "Chestnut Canyon Roaming NPC - Leon"
Chestnut_Canyon_NPC_Stance = "Chestnut Canyon Roaming NPC - Stance"
Chestnut_Canyon_NPC_Matil = "Chestnut Canyon Roaming NPC - Matil"
Chestnut_Canyon_NPC_Rectan = "Chestnut Canyon Roaming NPC - Rectan"
Chestnut_Canyon_NPC_Clary = "Chestnut Canyon Roaming NPC - Clary"
Chestnut_Canyon_NPC_Graham = "Chestnut Canyon Roaming NPC - Graham"
Chestnut_Canyon_NPC_Wilde = "Chestnut Canyon Roaming NPC - Wilde (Trade Quest 3)"
Chestnut_Canyon_NPC_Mojo = "Chestnut Canyon Roaming NPC - Mojo"
Chestnut_Canyon_NPC_Saucy = "Chestnut Canyon Roaming NPC - Saucy"
Chestnut_Canyon_NPC_Kuwano = "Chestnut Canyon Roaming NPC - Kuwano"
Chestnut_Canyon_NPC_Steve = "Chestnut Canyon Roaming NPC - Steve"

# Mushroom Road rooms
Mushroom_Road_Qs_Factory = "Mushroom Road - Q's Factory"
Mushroom_Road_Parts_Shop = "Mushroom Road - Parts Shop"
Mushroom_Road_Bar = "Mushroom Road - Bar"
Mushroom_Road_Golf = "Mushroom Road - Golf"
Mushroom_Road_Goddess = "Mushroom Road - Goddess of the Pond"

Quick_Pic_65 = "Quick-Pic Shop No. 65"
Quick_Pic_66 = "Quick-Pic Shop No. 66"
Quick_Pic_67 = "Quick-Pic Shop No. 67"
Quick_Pic_68 = "Quick-Pic Shop No. 68"
Quick_Pic_69 = "Quick-Pic Shop No. 69"
Quick_Pic_70 = "Quick-Pic Shop No. 70"

# Mushroom Road NPCs
# (none)

# White Mountain rooms
White_Mountain_Qs_Factory = "White Mountain - Q's Factory"
White_Mountain_Parts_Shop = "White Mountain - Parts Shop"
White_Mountain_Body_Shop = "White Mountain - Body Shop"
White_Mountain_Paint_Shop = "White Mountain - Paint Shop"
White_Mountain_Bar = "White Mountain - Bar"
White_Mountain_Policeman_House = "White Mountain - Policeman's House"
White_Mountain_Merrin_House = "White Mountain - Merrin's House"
White_Mountain_Ski_Jumping = "White Mountain - Ski Jumping"
White_Mountain_Grandma_Dizzy_House = "White Mountain - Grandma Dizzy's House"
White_Mountain_Post_Office = "White Mountain - Post Office"
White_Mountain_Santa_House = "White Mountain - Santa's House"
White_Mountain_Keitel_House = "White Mountain - Keitel's House"
White_Mountain_Coin_Radar_House_1 = "White Mountain - Coin Radar House 1"
White_Mountain_Coin_Radar_House_2 = "White Mountain - Coin Radar House 2"
White_Mountain_Coin_Radar_House_3 = "White Mountain - Coin Radar House 3"
White_Mountain_Coin_Radar_House_4 = "White Mountain - Coin Radar House 4"
White_Mountain_Emily_House = "White Mountain - Emily's House"
White_Mountain_Bigfoot_Joe_House = "White Mountain - Bigfoot Joe House"
White_Mountain_Curling = "White Mountain - Curling"
White_Mountain_Wool_Shop = "White Mountain - Wool Shop"

Quick_Pic_71 = "Quick-Pic Shop No. 71"
Quick_Pic_72 = "Quick-Pic Shop No. 72"
Quick_Pic_73 = "Quick-Pic Shop No. 73"
Quick_Pic_74 = "Quick-Pic Shop No. 74"
Quick_Pic_75 = "Quick-Pic Shop No. 75"
Quick_Pic_76 = "Quick-Pic Shop No. 76"
Quick_Pic_77 = "Quick-Pic Shop No. 77"

# White Mountain NPCs
White_Mountain_NPC_Jack = "White Mountain Roaming NPC - Jack"
White_Mountain_NPC_Charles = "White Mountain Roaming NPC - Charles"
White_Mountain_NPC_Hitomi = "White Mountain Roaming NPC - Hitomi"
White_Mountain_NPC_Brown = "White Mountain Roaming NPC - Brown"
White_Mountain_NPC_Blonty = "White Mountain Roaming NPC - Blonty"
White_Mountain_NPC_Shirley = "White Mountain Roaming NPC - Shirley (Trade Quest 5)"
White_Mountain_NPC_Nick = "White Mountain Roaming NPC - Nick"
White_Mountain_NPC_Suess = "White Mountain Roaming NPC - Suess"
White_Mountain_NPC_Manei = "White Mountain Roaming NPC - Manei"
White_Mountain_NPC_Sally = "White Mountain Roaming NPC - Sally"

# Papaya Island rooms
Papaya_Island_Qs_Factory = "Papaya Island - Q's Factory"
Papaya_Island_Parts_Shop = "Papaya Island - Parts Shop"
Papaya_Island_Body_Shop = "Papaya Island - Body Shop"
Papaya_Island_Bar = "Papaya Island - Bar"
Papaya_Island_Policeman_House = "Papaya Island - Policeman's House"
Papaya_Island_Obstacle_Course = "Papaya Island - Obstacle Course"
Papaya_Island_Mayor_House = "Papaya Island - Mayor's House"
Papaya_Island_Luke_House = "Papaya Island - Luke's House"
Papaya_Island_Grandpa_Costello_House = "Papaya Island - Grandpa Costello's House"
Papaya_Island_Andy_House = "Papaya Island - Andy's House"
Papaya_Island_Shirley_House = "Papaya Island - Shirley's House"
Papaya_Island_Casa_House = "Papaya Island - Casa's House"
Papaya_Island_Sandro_House = "Papaya Island - Sandro's House"
Papaya_Island_Beach_Flag = "Papaya Island - Beach Flag"
Papaya_Island_Coconut_Shop = "Papaya Island - Coconut Shop"
Papaya_Island_Fishing = "Papaya Island - Fishing"
Papaya_Island_Papu_Tree = "Papaya Island - Papu Tree"
Papaya_Island_Cloud_Hill_Warp = "Papaya Island - Cloud Hill Warp"

Quick_Pic_87 = "Quick-Pic Shop No. 87"
Quick_Pic_88 = "Quick-Pic Shop No. 88"
Quick_Pic_89 = "Quick-Pic Shop No. 89"
Quick_Pic_90 = "Quick-Pic Shop No. 90"
Quick_Pic_91 = "Quick-Pic Shop No. 91"
Quick_Pic_92 = "Quick-Pic Shop No. 92"
Quick_Pic_93 = "Quick-Pic Shop No. 93"
Quick_Pic_94 = "Quick-Pic Shop No. 94"
Quick_Pic_95 = "Quick-Pic Shop No. 95"
Quick_Pic_96 = "Quick-Pic Shop No. 96"

# Papaya Island NPCs
Papaya_Island_NPC_Mond = "Papaya Island Roaming NPC - Mond"
Papaya_Island_NPC_John = "Papaya Island Roaming NPC - John"
Papaya_Island_NPC_Kerori = "Papaya Island Roaming NPC - Kerori"
Papaya_Island_NPC_Nairo = "Papaya Island Roaming NPC - Nairo"
Papaya_Island_NPC_Moisy = "Papaya Island Roaming NPC - Moisy (Trade Quest 7)"
Papaya_Island_NPC_Nouri = "Papaya Island Roaming NPC - Nouri"
Papaya_Island_NPC_Minerva = "Papaya Island Roaming NPC - Minerva"
Papaya_Island_NPC_Kite = "Papaya Island Roaming NPC - Kite"
Papaya_Island_NPC_Mien = "Papaya Island Roaming NPC - Mien"
Papaya_Island_NPC_Michael = "Papaya Island Roaming NPC - Michael"

# Cloud Hill rooms
Cloud_Hill_Qs_Factory = "Cloud Hill - Q's Factory"
Cloud_Hill_Parts_Shop = "Cloud Hill - Parts Shop"
Cloud_Hill_Body_Shop = "Cloud Hill - Body Shop"
Cloud_Hill_Paint_Shop = "Cloud Hill - Paint Shop"
Cloud_Hill_Single_Lap_Race = "Cloud Hill - Single Lap Race"
Cloud_Hill_Duck_House = "Cloud Hill - Duck's House"
Cloud_Hill_Rainbow_Jump = "Cloud Hill - Rainbow Jump"
Cloud_Hill_Invalid_Room = "Cloud Hill - Invalid Room"
Cloud_Hill_White_House_Lobby = "Cloud Hill - White House Lobby"
Cloud_Hill_President_Room = "Cloud Hill - President's Room"

Quick_Pic_97 = "Quick-Pic Shop No. 97"
Quick_Pic_98 = "Quick-Pic Shop No. 98"
Quick_Pic_99 = "Quick-Pic Shop No. 99"
Quick_Pic_100 = "Quick-Pic Shop No. 100"

# Cloud Hill NPCs
Cloud_Hill_NPC_Yumyum = "Cloud Hill Roaming NPC - Yumyum"
Cloud_Hill_NPC_Dust = "Cloud Hill Roaming NPC - Dust"
Cloud_Hill_NPC_Williams = "Cloud Hill Roaming NPC - Williams (Trade Quest 6)"
Cloud_Hill_NPC_Diez = "Cloud Hill Roaming NPC - Diez"
Cloud_Hill_NPC_Peo = "Cloud Hill Roaming NPC - Peo"
Cloud_Hill_NPC_Giz = "Cloud Hill Roaming NPC - Giz"
Cloud_Hill_NPC_Stuart = "Cloud Hill Roaming NPC - Stuart"
Cloud_Hill_NPC_Zeron = "Cloud Hill Roaming NPC - Zeron"
Cloud_Hill_NPC_Bulls = "Cloud Hill Roaming NPC - Bulls"
Cloud_Hill_NPC_Mug = "Cloud Hill Roaming NPC - Mug"
Cloud_Hill_NPC_Gate_Man = "Cloud Hill Roaming NPC - Gate Man"

# My City rooms
My_City_Qs_Factory = "My City - Q's Factory"
My_City_Parts_Shop = "My City - Parts Shop"
My_City_Body_Shop = "My City - Body Shop"
My_City_Paint_Shop = "My City - Paint Shop"
My_City_Police_Station = "My City - Police Station"
My_City_Recycle_Shop = "My City - Recycle Shop"
My_City_Wonder_Realty = "My City - Wonder Realty"
My_City_Bank = "My City - Bank"
My_City_Theater = "My City - Theater"
My_City_Tower = "My City - Tower"
My_City_Which_Way_Maze = "My City - Which-Way Maze"
My_City_Fire_Station = "My City - Fire Station"
My_City_School = "My City - School"
My_City_Coine_House = "My City - Coine House"
My_City_Kuwano_House = "My City - Kuwano House"
My_City_Mien_House = "My City - Mien House"
My_City_Flower_House = "My City - Flower House"
My_City_Gichi_House = "My City - Gichi House"
My_City_Tunnel_Race = "My City - Tunnel Race"
My_City_Sally_House = "My City - Sally House"
My_City_Rally_Center = "My City - Rally Center"

Quick_Pic_28 = "Quick-Pic Shop No. 28"
Quick_Pic_29 = "Quick-Pic Shop No. 29"

# My City NPCs
My_City_NPC_Cobran = "My City Roaming NPC - Cobran"
My_City_NPC_Saucy = "My City Roaming NPC - Saucy"
My_City_NPC_Sylvester = "My City Roaming NPC - Sylvester"
My_City_NPC_Velvet = "My City Roaming NPC - Velvet"
My_City_NPC_Arnold = "My City Roaming NPC - Arnold"
My_City_NPC_Gump = "My City Roaming NPC - Gump"

# Windmills near Peach Town rooms (0xA)
Windmill_House = "Peach Town - Windmill House"

Quick_Pic_84 = "Quick-Pic Shop No. 84"
Quick_Pic_85 = "Quick-Pic Shop No. 85"
Quick_Pic_86 = "Quick-Pic Shop No. 86"

# Fuji Bridge (0xB)
Quick_Pic_13 = "Quick-Pic Shop No. 13"
Quick_Pic_14 = "Quick-Pic Shop No. 14"
Quick_Pic_15 = "Quick-Pic Shop No. 15"
Quick_Pic_16 = "Quick-Pic Shop No. 16"

# North of Sandpolis (0xC)
UFO = "Sandpolis - UFO"

Quick_Pic_52 = "Quick-Pic Shop No. 52"
Quick_Pic_53 = "Quick-Pic Shop No. 53"
Quick_Pic_54 = "Quick-Pic Shop No. 54"

# Pyramids (0xD)
Benji_House = "Sandpolis - Benji's House"

Quick_Pic_48 = "Quick-Pic Shop No. 48"
Quick_Pic_49 = "Quick-Pic Shop No. 49"
Quick_Pic_50 = "Quick-Pic Shop No. 50"
Quick_Pic_51 = "Quick-Pic Shop No. 51"

NPC_Benji = "Sandpolis Roaming NPC - Benji"

# Lighthouse (0xE)
Lightouse = "Sandpolis - Lighthouse"

Quick_Pic_55 = "Quick-Pic Shop No. 55"
Quick_Pic_56 = "Quick-Pic Shop No. 56"
Quick_Pic_57 = "Quick-Pic Shop No. 57"

# East of Sandpolis, near interchange (0xF)
Quick_Pic_30 = "Quick-Pic Shop No. 30"
Quick_Pic_31 = "Quick-Pic Shop No. 31"
Quick_Pic_32 = "Quick-Pic Shop No. 32"
Quick_Pic_33 = "Quick-Pic Shop No. 33"
Quick_Pic_34 = "Quick-Pic Shop No. 34"
Quick_Pic_35 = "Quick-Pic Shop No. 35"

# Tunnel to Chestnut Canyon (0x10)
Quick_Pic_58 = "Quick-Pic Shop No. 58"
Quick_Pic_59 = "Quick-Pic Shop No. 59"

# South of Fuji City (0x11)
Quick_Pic_27 = "Quick-Pic Shop No. 27" # This is just barely outside of Fuji City's chunk boundary

# West of White Mountain, near Temple Under the Sea (0x12)
Temple_Under_the_Sea = "White Mountain - Temple Under the Sea"

Quick_Pic_78 = "Quick-Pic Shop No. 78"
Quick_Pic_79 = "Quick-Pic Shop No. 79"

NPC_Orpheus = "White Mountain - Orpheus"

# East of White Mountain, path to Peach Town (0x13)
Quick_Pic_80 = "Quick-Pic Shop No. 80"
Quick_Pic_81 = "Quick-Pic Shop No. 81"
Quick_Pic_82 = "Quick-Pic Shop No. 82"
Quick_Pic_83 = "Quick-Pic Shop No. 83"

# Southwest of Peach Town, highway to Fuji Bridge (0x14)
Quick_Pic_12 = "Quick-Pic Shop No. 12"

# East of Peach Town, near water (0x15)
Quick_Pic_11 = "Quick-Pic Shop No. 11"
