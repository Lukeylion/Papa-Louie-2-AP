from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import PapaLouie2World

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {
    "Level1 Complete": 1,
    "Level2 Complete": 2,
    "Level3 Complete": 3,
    "Level4 Complete": 4,
    "Level5 Complete": 5,
    "Level6 Complete": 6,
    "Level7 Complete": 7,
    "Level8 Complete": 8,
    "Level9 Complete": 9,
    "Prudence Rescued": 10,
    "Taylor Rescued": 11,
    "Clover Rescued": 12,
    "Mindy Rescued": 13,
    "Akari Rescued": 14,
    "Big Pauly Rescued": 15,
    "Kahuna Rescued": 16,
    "Kingsley Rescued": 17,
    "Ninjoy Rescued": 18,
    "James Rescued": 19,
    "Scooter Rescued": 20,
    "Connor Rescued": 21,
    "Georito Rescued": 22,
    "Yippy Rescued": 23,
    "Boomer Rescued": 24,
    "Prof. Fitz Rescued": 25,
    "Foodini Rescued": 26,
    "Level1 Find 5 Red Coins": 27,
    "Level1 Defeat 3 Burgerzillas": 28,
    "Level1 Find 100 Coins": 29,
    "Level2 Find 5 Flowers": 30,
    "Level2 Defeat 11 Burgerzillas": 31,
    "Level2 Find 100 Coins": 32,
    "Level3 Find 5 Gold Helmets": 33,
    "Level3 Defeat 11 Burgerzillas": 34,
    "Level3 Find 100 Coins": 35,
    "Level4 Find 5 Purple Coins": 36,
    "Level4 Defeat 6 Burgerzillas": 37,
    "Level4 Find 100 Coins": 38,
    "Level5 Find 5 Gummie Worms": 39,
    "Level5 Defeat 8 Burgerzillas": 40,
    "Level5 Find 100 Coins": 41,
    "Level6 Find 5 Gold Ballons": 42,
    "Level6 Defeat 10 Burgerzillas": 43,
    "Level6 Find 100 Coins": 44,
    "Level7 Find 5 Sodas": 45,
    "Level7 Defeat 13 Burgerzillas": 46,
    "Level7 Find 100 Coins": 47,
    #"Marty Style B": 48,
    #"Marty Style C": 49,
    "Peggy Rescued": 51,
    "Sarge Fan Rescued": 52,
    "Greg Rescued": 53,
    "Xandra Rescued": 54,
    "Zoe Rescued": 55,
    "Penny Rescued": 57,
    "Captain Cori Rescued": 58,
    "Level8 Find 100 Coins": 59,
    "Level8 Find 5 Raddish Coins": 60,
    "Level8 Defeat 12 Burgerzillas": 61,
    #"Prudence Style B": 62,
    #"Prudence Style C": 63,
    #"Taylor Style B": 64,
    #"Taylor Style C": 65,
    #"Dover Style B": 66,
    #"Dover Style C": 67,
    #"Mindy Style B": 68,
    #"Mindy Style C": 69,
    #"Akari Style B": 70,
    #"Akari Style C": 71,
    #"Big Pauly Style B": 72,
    #"Big Pauly Style C": 73,
    #"Boomer Style B": 74,
    #"Boomer Style C": 75,
    #"Kahuna Style B": 76,
    #"Kahuna Style C": 77,
   #"Georgito Style B": 78,
    #"Georgito Style C": 79,
    #"Foodini Style B": 80,
    #"Foodini Style C": 81,
    #"Yippy Style B": 82,
    #"Yippy Style C": 83,
    #"Scooter Style B": 84,
    #"Scooter Style C": 85,
    #"Connor Style B": 86,
    #"Connor Style C": 87,
    #"Kingsley Style B": 88,
    #"Kingsley Style C": 89,
    #"James Style B": 90,
    #"James Style C": 91,
    #"Greg Style B": 92,
    #"Greg Style C": 93,
    #"Captain Cori Style B": 94,
    #"Captain Cori Style C": 95,
    #"Peggy Style B": 96,
    #"Peggy Style C": 97,
    #"Sarge Fan Style B": 98,
    #"Sarge Fan Style C": 99,
    #"Rita Style B": 100,
    #"Rita Style C": 101,
    #"Zoe Style B": 102,
    #"Zoe Style C": 103,
    #"Penny Style B": 104,
    #"Penny Style C": 105,
    "Rico Rescued": 106,
    "Georgito Rescued": 107,
    "Papa Louie Rescued": 108,





}

GROUND_POUND_LOCATIONS = [
    "Clover Rescued",
    "Mindy Rescued",
    "Level2 Defeat 11 Burgerzillas",
    "Level3 Find 5 Gold Helmets",
    "Level4 Find 5 Purple Coins",
    "Level5 Find 5 Gummie Worms",
    "Level6 Find 100 Coins",
    "Penny Rescued",
    "Level8 Find 5 Raddish Coins",
]

GLIDING_LOCATIONS = [
    "Level1 Find 100 Coins",
    "Akari Rescued",
    "Kahuna Rescued",
    "Level3 Defeat 11 Burgerzillas",
    "Level5 Defeat 8 Burgerzillas",
    "Level6 Find 5 Gold Ballons",
    "Level7 Find 5 Sodas",
    "Level8 Find 100 Coins",
]

WALL_JUMPING_LOCATIONS = [
    "Level5 Find 100 Coins",
    "Captain Cori Rescued",
    "Peggy Rescued",
    "Rico Rescued",
]

CRAWLING_LOCATIONS = [
    "Level2 Find 100 Coins",
    "Prof. Fitz Rescued",
    "Foodini Rescued",
    "Level4 Defeat 6 Burgerzillas",
    "Level6 Defeat 10 Burgerzillas",
    "Zoe Rescued",
]

DOUBLE_JUMPING_LOCATIONS = [
    "Level3 Find 100 Coins",
    "Yippy Rescued",
    "Kingsley Rescued",
    "Level7 Find 100 Coins",
    "Level8 Defeat 12 Burgerzillas",
]

PUSHING_LOCATIONS = [
    
]

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class PapaLouie2Location(Location):
    game = "PapaLouie2"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: PapaLouie2World) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: PapaLouie2World) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    Level1 = world.get_region("Level1")
    Level2 = world.get_region("Level2")
    Level3 = world.get_region("Level3")
    Level4 = world.get_region("Level4")
    Level5 = world.get_region("Level5")
    Level6 = world.get_region("Level6")
    Level7 = world.get_region("Level7")
    Level8 = world.get_region("Level8")
    Level9 = world.get_region("Level9")

    # One way to create locations is by just creating them directly via their constructor.
    #Level1_Complete = PapaLouie2Location(
#        world.player, "Level1 Complete", world.location_name_to_id["Level1 Complete"], Level1
#    )
 #   Level2_Complete = PapaLouie2Location(
  #      world.player, "Level2 Complete", world.location_name_to_id["Level2 Complete"], Level2
   # )
    #Level3_Complete = PapaLouie2Location(
     #   world.player, "Level3 Complete", world.location_name_to_id["Level3 Complete"], Level3
    #)
 #   Level4_Complete = PapaLouie2Location(
 #       world.player, "Level4 Complete", world.location_name_to_id["Level4 Complete"], Level4
  #  )
   # Level5_Complete = PapaLouie2Location(
    #    world.player, "Level5 Complete", world.location_name_to_id["Level5 Complete"], Level5
#    )
#    Level6_Complete = PapaLouie2Location(
#        world.player, "Level6 Complete", world.location_name_to_id["Level6 Complete"], Level6
#    )
#    Level7_Complete = PapaLouie2Location(
#        world.player, "Level7 Complete", world.location_name_to_id["Level7 Complete"], Level7
#    )
#    Level8_Complete = PapaLouie2Location(
#        world.player, "Level8 Complete", world.location_name_to_id["Level8 Complete"], Level8
#    )
#    Level9_Complete = PapaLouie2Location(
#        world.player, "Level9 Complete", world.location_name_to_id["Level9 Complete"], Level9
#    )

    # You can then add them to the region.
    #Level1.locations.append(Level1_Complete)
    #Level2.locations.append(Level2_Complete)
    #Level3.locations.append(Level3_Complete)
    #Level4.locations.append(Level4_Complete)
    #Level5.locations.append(Level5_Complete)
    #Level6.locations.append(Level6_Complete)
    #Level7.locations.append(Level7_Complete)
    #Level8.locations.append(Level8_Complete)
    #Level9.locations.append(Level9_Complete)

    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also need to pass your overridden Location class.
    Level1_Locations = get_location_names_with_ids(
        ["Level1 Complete", "Level1 Find 5 Red Coins", "Level1 Defeat 3 Burgerzillas", "Level1 Find 100 Coins", "Prudence Rescued", "Taylor Rescued", "Clover Rescued"]
    )
    Level1.add_locations(Level1_Locations, PapaLouie2Location)

    Level2_Locations = get_location_names_with_ids([
        "Level2 Complete", "Level2 Find 5 Flowers", "Level2 Defeat 11 Burgerzillas", "Level2 Find 100 Coins", "Big Pauly Rescued", "Mindy Rescued", "Akari Rescued"
    ])
    Level2.add_locations(Level2_Locations, PapaLouie2Location)

    Level3_Locations = get_location_names_with_ids([
       "Level3 Complete", "Level3 Find 5 Gold Helmets", "Level3 Defeat 11 Burgerzillas", "Level3 Find 100 Coins", "Boomer Rescued", "Kahuna Rescued", "Prof. Fitz Rescued"
    ])
    Level3.add_locations(Level3_Locations, PapaLouie2Location)

    Level4_Locations = get_location_names_with_ids([
        "Level4 Complete", "Level4 Find 5 Purple Coins", "Level4 Defeat 6 Burgerzillas", "Level4 Find 100 Coins", "Georgito Rescued", "Foodini Rescued", "Yippy Rescued"
    ])
    Level4.add_locations(Level4_Locations, PapaLouie2Location)

    Level5_Locations = get_location_names_with_ids([
        "Level5 Complete", "Level5 Find 5 Gummie Worms", "Level5 Defeat 8 Burgerzillas", "Level5 Find 100 Coins", "Scooter Rescued", "Connor Rescued", "Kingsley Rescued"
    ])
    Level5.add_locations(Level5_Locations, PapaLouie2Location)

    Level6_Locations = get_location_names_with_ids([
        "Level6 Complete", "Level6 Find 5 Gold Ballons", "Level6 Defeat 10 Burgerzillas", "Level6 Find 100 Coins", "James Rescued", "Greg Rescued", "Captain Cori Rescued"
    ])
    Level6.add_locations(Level6_Locations, PapaLouie2Location)

    Level7_Locations = get_location_names_with_ids([
        "Level7 Complete", "Level7 Find 5 Sodas", "Level7 Defeat 13 Burgerzillas", "Level7 Find 100 Coins", "Ninjoy Rescued", "Peggy Rescued", "Penny Rescued"
   ])
    Level7.add_locations(Level7_Locations, PapaLouie2Location)

    Level8_Locations = get_location_names_with_ids([
       "Level8 Complete", "Level8 Find 100 Coins", "Level8 Find 5 Raddish Coins", "Level8 Defeat 12 Burgerzillas", "Sarge Fan Rescued", "Rico Rescued", "Zoe Rescued"
    ])
    Level8.add_locations(Level8_Locations, PapaLouie2Location)

    Level9_Locations = get_location_names_with_ids([
        "Level9 Complete", 
        #"Papa Louie Rescued"
    ])
    Level9.add_locations(Level9_Locations, PapaLouie2Location)


    # Now we can create the locations for the individual rooms.
    
    #Level1.add_locations(Level1_Locations, PapaLouie2Location)
    #Level2.add_locations(Level2_Locations, PapaLouie2Location)
    #Level3.add_locations(Level3_Locations, PapaLouie2Location)
    #Level4.add_locations(Level4_Locations, PapaLouie2Location)
    #Level5.add_locations(Level5_Locations, PapaLouie2Location)
    #Level6.add_locations(Level6_Locations, PapaLouie2Location)
    #Level7.add_locations(Level7_Locations, PapaLouie2Location)
    #Level8.add_locations(Level8_Locations, PapaLouie2Location)
    #Level9.add_locations(Level9_Locations, PapaLouie2Location)

    # Locations may be in different regions depending on the player's options.
    # In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    #COME BACK LATER CharacterStyle_locations = get_location_names_with_ids([
        #"Marty Style B", "Marty Style C", "Scooter Style B", "Scooter Style C", "Connor Style B", "Connor Style C", "Kingsley Style B", "Kingsley Style C", "James Style B", "James Style C", 
        #"Greg Style B", "Greg Style C", "Captain Cori Style B", "Captain Cori Style C", "Peggy Style B", "Peggy Style C", "Sarge Fan Style B", "Sarge Fan Style C", "Rita Style B", "Rita Style C", 
        #"Zoe Style B", "Zoe Style C", "Penny Style B", "Penny Style C"])
    #if world.options.RandomCharacterStyle:
        #CharacterStyles = world.get_region("Character Styles")
        #CharacterStyles.add_locations(CharacterStyle_locations, PapaLouie2Location)

    # Locations may exist only if the player enables certain options.
    # In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.

        # Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
        # exist, it must still always be present in the world's location_name_to_id.
        # Whether the location actually exists in the seed is purely determined by whether we create and add it here.


def create_events(world: PapaLouie2World) -> None:
    # Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    # In our case, the player must press a button in the top left room to open the final boss door.
    # AP has something for this purpose: "Event locations" and "Event items".
    # An event location is no different than a regular location, except it has the address "None".
    # It is treated during generation like any other location, but then it is discarded.
    # This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
    # Since we are creating more locations and adding them to regions, we need to grab those regions again first.
    level9 = world.get_region("Level9")

    # One way to create an event is simply to use one of the normal methods of creating a location.


    # We then need to put an event item onto the location.
    # An event item is an item whose code is "None" (same as the event location's address),
    # and whose classification is "progression". Item creation will be discussed more in items.py.
    # Note: Usually, items are created in world.create_items(), which for us happens in items.py.
    # However, when the location of an item is known ahead of time (as is the case with an event location/item pair),
    # it is common practice to create the item when creating the location.
    # Since locations also have to be finalized after world.create_regions(), which runs before world.create_items(),
    # we'll create both the event location and the event item in our locations.py code.


    # A way simpler way to do create an event location/item pair is by using the region.create_event helper.
    # Luckily, we have another event we want to create: The Victory event.
    # We will use this event to track whether the player can win the game.
    # The Victory event is a completely optional abstraction - This will be discussed more in set_rules().
    level9.add_event(
        "Papa Louie Rescued", "Victory", location_type=PapaLouie2Location, item_type=items.PapaLouie2Item
    )

    # If you create all your regions and locations line-by-line like this,
    # the length of your create_regions might get out of hand.
    # Many worlds use more data-driven approaches using dataclasses or NamedTuples.
    # However, it is worth understanding how the actual creation of regions and locations works,
    # That way, we're not just mindlessly copy-pasting! :)