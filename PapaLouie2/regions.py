from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import PapaLouie2World

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: PapaLouie2World) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: PapaLouie2World) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    Level1 = Region("Level1", world.player, world.multiworld)
    Level2 = Region("Level2", world.player, world.multiworld)
    Level3 = Region("Level3", world.player, world.multiworld)
    Level4 = Region("Level4", world.player, world.multiworld)
    Level5 = Region("Level5", world.player, world.multiworld)
    Level6 = Region("Level6", world.player, world.multiworld)
    Level7 = Region("Level7", world.player, world.multiworld)
    Level8 = Region("Level8", world.player, world.multiworld)
    Level9 = Region("Level9", world.player, world.multiworld)

    # Let's put all these regions in a list.
    regions = [Level1, Level2, Level3, Level4, Level5, Level6, Level7, Level8, Level9]

    # Some regions may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.


    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: PapaLouie2World) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    Level1 = world.get_region("Level1")
    Level2 = world.get_region("Level2")
    Level3 = world.get_region("Level3")
    Level4 = world.get_region("Level4")
    Level5 = world.get_region("Level5")
    Level6 = world.get_region("Level6")
    Level7 = world.get_region("Level7")
    Level8 = world.get_region("Level8")
    Level9 = world.get_region("Level9")
    #CharacterStyles = world.get_region("Character Styles")

    # Okay, now we can get connecting. For this, we need to create Entrances.
    # Entrances are inherently one-way, but crucially, AP assumes you can always return to the origin region.
    # One way to create an Entrance is by calling the Entrance constructor.
    #Level1_to_Level2 = Entrance(world.player, "Level1 to Level2", parent=Level1)
    #Level1.exits.append(Level1_to_Level2)
    #Level2_to_Level3 = Entrance(world.player, "Level2 to Level3", parent=Level2)
    #Level2.exits.append(Level2_to_Level3)
    #Level3_to_Level4 = Entrance(world.player, "Level3 to Level4", parent=Level3)
    #Level3.exits.append(Level3_to_Level4)
    #Level4_to_Level5 = Entrance(world.player, "Level4 to Level5", parent=Level4)
    #Level4.exits.append(Level4_to_Level5)
    #Level5_to_Level6 = Entrance(world.player, "Level5 to Level6", parent=Level5)
    #Level5.exits.append(Level5_to_Level6)
    #Level6_to_Level7 = Entrance(world.player, "Level6 to Level7", parent=Level6)
    #Level6.exits.append(Level6_to_Level7)
    #Level7_to_Level8 = Entrance(world.player, "Level7 to Level8", parent=Level7)
    #Level7.exits.append(Level7_to_Level8)
    #Level8_to_Level9 = Entrance(world.player, "Level8 to Level9", parent=Level8)
    #Level8.exits.append(Level8_to_Level9)

    # You can then connect the Entrance to the target region.
    #Level1_to_Level2.connect(Level2)

    # An even easier way is to use the region.connect helper.
    #Level1.connect(Level2, "Level1 to Level2")
    #Level2.connect(Level3, "Level2 to Level3")
    #Level3.connect(Level4, "Level3 to Level4")
    #Level4.connect(Level5, "Level4 to Level5")
    #Level5.connect(Level6, "Level5 to Level6")
    #Level6.connect(Level7, "Level6 to Level7")
    #Level7.connect(Level8, "Level7 to Level8")
    #Level8.connect(Level9, "Level8 to Level9")

    # The region.connect helper even allows adding a rule immediately.
    # We'll talk more about rule creation in the set_all_rules() function in rules.py.
    Level1.connect(Level2, "Level1 to Level2", lambda state: state.has("Warp Key", world.player, 1))
    Level2.connect(Level3, "Level2 to Level3", lambda state: state.has("Warp Key", world.player, 2))
    Level3.connect(Level4, "Level3 to Level4", lambda state: state.has("Warp Key", world.player, 3))
    Level4.connect(Level5, "Level4 to Level5", lambda state: state.has("Warp Key", world.player, 6))
    Level5.connect(Level6, "Level5 to Level6", lambda state: state.has("Warp Key", world.player, 9))
    Level6.connect(Level7, "Level6 to Level7", lambda state: state.has("Warp Key", world.player, 13))
    Level7.connect(Level8, "Level7 to Level8", lambda state: state.has("Warp Key", world.player, 17))
    Level8.connect(Level9, "Level8 to Level9", lambda state: state.has("Warp Key", world.player, 23))

    # Some Entrances may only exist if the player enables certain options.
    # In our case, the Hammer locks the top middle chest in its own room if the hammer option is enabled.
    # In this case, we previously created an extra "Top Middle Room" region that we now need to connect to Overworld.

