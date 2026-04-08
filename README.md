# Road Trip Adventure Archipelago
This is an Archipelago randomizer implementation for the PlayStation 2 game Road Trip Adventure.

Archipelago is a multi-game randomizer that can shuffle items from one game into another. It can also be played solo like a standard randomizer. For more info, check out their website: https://archipelago.gg/

## Randomizer Details
### Goal
- Win the race against against President Forest (Stamp 100)

### Area Unlock Modes: Decorations, or Stamps
- In Road Trip AP, you must unlock a city before you are allowed to interact with it in any way. This means you cannot enter any buildings, talk to anyone, or collect overworld items in a town until you unlock it. Peach Town and My City are unlocked by default.
- There are two YAML settings for what is required to unlock a town: **Decorations**, or **Stamps**.
- In Decorations mode, the garage decorations serve as area unlock keys. Each town has two decorations that serve as their key - obtaining either unlocks the town.
- In Stamps mode, your stamps become items in the multiworld, and you unlock the next town in linear sequence with every 5 stamps obtained.

| City | Decoration Unlock | Stamp Unlock |
| ---- | ---- | ---- |
| Peach Town | (Free) | (Free) |
| Fuji City | Gold Ornament / Policeman's Club | 5 stamps |
| My City | (Free) | (Free) |
| Sandpolis | Mini-Tower / Toy Gun | 10 stamps |
| Chestnut Canyon | Model Train / M. Carton's Painting | 15 stamps |
| Mushroom Road | Flower Pattern / Sky Pattern | 20 stamps |
| White Mountain | Christmas Tree / Arctic Pattern | 25 stamps |
| Papaya Island | Papaya Ukulele / UnbaboDoll | 30 stamps |
| Cloud Hill | God's Rod / Angel's Wings | 35 stamps |

### Items
- Progressive part upgrades
    - Tire upgrades are awarded in order of their cost (e.g. Off-Road Tires are first, HG Racing Tires are last)
    - Two additional progressive upgrade tracks are also enabled by default (one for each of your teammates, although you can use these parts too, or even sell them)
- All items normally given to you via dialogue
- All overworld items (gemstones, the fountain pen, etc.)
- All license upgrades
- Stamps (only if the Area Unlock Mode is set to Stamps)
- Empty locations are filled with 500 money

### Locations
- Purchasing an item from the parts shop for the first time
    - NOTE: **Only the first purchase of an AP item will send a check. However, the game is not currently patched to prevent you from repurchasing AP items.**
    - To make sure you don't accidentally repurchase a part, check to see whether "You have it" is displaying for that part above its description.
- Receiving an item via dialogue
- Collecting an item via the overworld (except Q Coins)
- Finishing a race in 6th place or higher
- Receiving a license upgrade
- Completing a stamp 

## How to Play
Set the [setup guide](./docs/setup_en.md) for instructions.

## Frequently Asked Questions
- What versions of the game are supported?
    - Currently, only NTSC-U.
- Are there plans to support PAL and/or NTSC-J?
    - Maybe, TBD. If I do, it will likely be a while until they are supported.
    - Uncertain on NTSC-J support in particular, as it likely differs more from NTSC-U internally than PAL.
- Are there plans to add Q coins and Quick-Pic shops as items/locations?
    - Yes! It's one of the higher-priority things on my list.

## Known Issues
- The game is not yet patched to prevent repurchases of AP items from part shops, even though repurchases will not send another check.