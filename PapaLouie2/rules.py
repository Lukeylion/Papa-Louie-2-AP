from __future__ import annotations

from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

from .locations import GROUND_POUND_LOCATIONS, WALL_JUMPING_LOCATIONS, GLIDING_LOCATIONS, DOUBLE_JUMPING_LOCATIONS, CRAWLING_LOCATIONS, LOCATION_NAME_TO_ID

if TYPE_CHECKING:
    from .world import PapaLouie2World

HAS_KEY = Has("Key")  # Hmm, what could this be? A little foreshadowing perhaps? :) You'll find out if you keep reading!


def set_all_rules(world: PapaLouie2World) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: PapaLouie2World) -> None:
    # First, we need to actually grab our entrances. Luckily, there is a helper method for this.
    level1_to_level2 = world.get_entrance("Level1 to Level2")
    level2_to_level3 = world.get_entrance("Level2 to Level3")
    level3_to_level4 = world.get_entrance("Level3 to Level4")
    level4_to_level5 = world.get_entrance("Level4 to Level5")
    level5_to_level6 = world.get_entrance("Level5 to Level6")
    level6_to_level7 = world.get_entrance("Level6 to Level7")
    level7_to_level8 = world.get_entrance("Level7 to Level8")
    level8_to_level9 = world.get_entrance("Level8 to Level9")

    # Now, let's make some rules!
    # First, let's handle the transition from the overworld to the bottom right room,
    # which requires slashing a bush with the Sword.
    # For this, we need a rule that says "player has a Sword".
    # We can use a "Has"-type rule from the rule_builder module for this.
    can_access_level_2 = Has("Warp Key", count =1)
    can_access_level_3 = Has("Warp Key", count =2)
    can_access_level_4 = Has("Warp Key", count=4)
    can_access_level_5 = Has("Warp Key", count=6)
    can_access_level_6 = Has("Warp Key", count=9)
    can_access_level_7 = Has("Warp Key", count=13)
    can_access_level_8 = Has("Warp Key", count=17)
    can_access_level_9 = Has("Warp Key", count=23)

    # Now we can set our "can_destroy_bush" rule to the entrance which requires slashing a bush to clear the path.
    # The easiest way to do this is by calling world.set_rule, which works for both Locations and Entrances.
    world.set_rule(level1_to_level2, can_access_level_2)
    world.set_rule(level2_to_level3, can_access_level_3)
    world.set_rule(level3_to_level4, can_access_level_4)
    world.set_rule(level4_to_level5, can_access_level_5)
    world.set_rule(level5_to_level6, can_access_level_6)
    world.set_rule(level6_to_level7, can_access_level_7)
    world.set_rule(level7_to_level8, can_access_level_8)
    world.set_rule(level8_to_level9, can_access_level_9)

    # Conditions can also depend on event items.

    # Some entrance rules may only apply if the player enabled certain options.
    # In our case, if the hammer option is enabled, we need to add the Hammer requirement to the Entrance from
    # Overworld to the Top Middle Room.

    # So far, we've been using "Has" from the Rule Builder to make our rules.
    # There is another way to make rules that you will see in a lot of older worlds.
    # A rule can just be a function that takes a "state" argument and returns a bool.
    # As a demonstration of what that looks like, let's do it with our final Entrance rule:

    # This style is not really recommended anymore, though.
    # Notice how you have to explicitly capture world.player here so that the rule applies to the correct player?
    # Well, Rule Builder does this part for you, inside of world.set_rule.
    # This doesn't just result in shorter code, it also means you can define rules statically (at the module level).
    # PapaLouie2 opts to create its Rule objects locally, but just to show what this would look like,
    # we'll re-set the "Overworld to Top Left Room" rule to a constant defined at the top of this file:


    # Beyond these structural advantages,
    # Rule Builder also allows the core AP code to do a lot of under-the-hood optimizations.
    # Rule Builder is quite comprehensive, and even if you have really esoteric rules,
    # you can make custom rules by subclassing CustomRule.

def set_all_location_rules(self: PapaLouie2World) -> None:
    # Location rules work no differently from Entrance rules.
    # Most of our locations are chests that can simply be opened by walking up to them.
    # Thus, their logical requirements are covered by the Entrance rules of the Entrances that were required to
    # reach the region that the chest sits in.
    # However, our two enemies work differently.
    # Entering the room with the enemy is not enough, you also need to have enough combat items to be able to defeat it.
    # So, we need to set requirements on the Locations themselves.
    # Since combat is a bit more complicated, we'll use this chance to cover some advanced access rule concepts.

    # In "set_all_entrance_rules", we had a rule for a location that doesn't always exist.
    # In this case, we had to check for its existence (by checking the player's chosen options) before setting the rule.
    # Other times, you may have a situation where a location can have two different rules depending on the options.
    # In our case, the enemy in the right room has more health if hard mode is selected,
    # so ontop of the Sword, the player will either need one more health or a Shield in hard mode.
    # First, let's make our sword condition.
    can_do_ground_pound_objectives: Rule = Has("Big Pauly Unlocked") | Has("Kingsley Unlocked") | Has("Kahuna Unlocked")
    can_do_double_jump_objectives: Rule = Has("Connor Unlocked") | Has("Peggy Unlocked") | Has("Scooter Unlocked")
    can_do_wall_jump_objectives: Rule = Has("Ninjoy Unlocked") | Has("Penny Unlocked") | Has("Sarge Fan Unlocked")
    can_do_gliding_objectives: Rule = Has("Boomer Unlocked") | Has("Foodini Unlocked") | Has("Papa Louie Unlocked") | Has("Prof. Fitz Unlocked") | Has("Xandra Unlocked")
    can_do_crawl_objectives: Rule = Has("Georgito Unlocked") | Has("Greg Unlocked") | Has("Yippy Unlocked")

    # Next, we'll check whether hard mode has been chosen in the player options.
    #if world.options.hard_mode:
        # We'll make the condition for "Has a Shield or a Health Upgrade".
        # We can chain two "Has" conditions together with the | operator to make "Has Shield or has Health Upgrade".
        #can_withstand_a_hit = Has("Shield") | Has("Health Upgrade")

        # Now, we chain this rule to our Sword rule.
        # Since we want both conditions to be true, in this case, we have to chain them in an "and" way.
        # For this, we can use the & operator.
        #can_defeat_basic_enemy = can_defeat_basic_enemy & can_withstand_a_hit

    # Finally, we set our rule onto the Right Room Eney Drop location.
    
    
    #Ground Pound Rules
    set_rule(self.multiworld.get_location("Mindy Rescued", self.player), lambda state: (state.has("Big Pauly Unlocked", self.player)) or state.has("Kahuna Unlocked", self.player) or state.has("Kingsley Unlocked", self.player))
    set_rule(self.multiworld.get_location("Clover Rescued", self.player), lambda state: (state.has("Big Pauly Unlocked", self.player)) or state.has("Kahuna Unlocked", self.player) or state.has("Kingsley Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level3 Find 5 Gold Helmets", self.player), lambda state: (state.has("Big Pauly Unlocked", self.player)) or state.has("Kahuna Unlocked", self.player) or state.has("Kingsley Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level2 Defeat 11 Burgerzillas", self.player), lambda state: (state.has("Big Pauly Unlocked", self.player)) or state.has("Kahuna Unlocked", self.player) or state.has("Kingsley Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level4 Find 5 Purple Coins", self.player), lambda state: (state.has("Big Pauly Unlocked", self.player)) or state.has("Kahuna Unlocked", self.player) or state.has("Kingsley Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level5 Find 5 Gummie Worms", self.player), lambda state: (state.has("Big Pauly Unlocked", self.player)) or state.has("Kahuna Unlocked", self.player) or state.has("Kingsley Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level6 Find 100 Coins", self.player), lambda state: (state.has("Big Pauly Unlocked", self.player)) or state.has("Kahuna Unlocked", self.player) or state.has("Kingsley Unlocked", self.player))
    set_rule(self.multiworld.get_location("Penny Rescued", self.player), lambda state: (state.has("Big Pauly Unlocked", self.player)) or state.has("Kahuna Unlocked", self.player) or state.has("Kingsley Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level8 Find 5 Raddish Coins", self.player), lambda state: (state.has("Big Pauly Unlocked", self.player)) or state.has("Kahuna Unlocked", self.player) or state.has("Kingsley Unlocked", self.player))

    #Glide Rules
    set_rule(self.multiworld.get_location("Level1 Find 100 Coins", self.player), lambda state: (state.has("Boomer Unlocked", self.player)) or state.has("Foodini Unlocked", self.player) or state.has("Xandra Unlocked", self.player) or state.has("Prof. Fitz Unlocked", self.player) or state.has("Papa Louie Unlocked", self.player))
    set_rule(self.multiworld.get_location("Akari Rescued", self.player), lambda state: (state.has("Boomer Unlocked", self.player)) or state.has("Foodini Unlocked", self.player) or state.has("Xandra Unlocked", self.player) or state.has("Prof. Fitz Unlocked", self.player) or state.has("Papa Louie Unlocked", self.player))
    set_rule(self.multiworld.get_location("Kahuna Rescued", self.player), lambda state: (state.has("Boomer Unlocked", self.player)) or state.has("Foodini Unlocked", self.player) or state.has("Xandra Unlocked", self.player) or state.has("Prof. Fitz Unlocked", self.player) or state.has("Papa Louie Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level3 Defeat 11 Burgerzillas", self.player), lambda state: (state.has("Boomer Unlocked", self.player)) or state.has("Foodini Unlocked", self.player) or state.has("Xandra Unlocked", self.player) or state.has("Prof. Fitz Unlocked", self.player) or state.has("Papa Louie Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level5 Defeat 8 Burgerzillas", self.player), lambda state: (state.has("Boomer Unlocked", self.player)) or state.has("Foodini Unlocked", self.player) or state.has("Xandra Unlocked", self.player) or state.has("Prof. Fitz Unlocked", self.player) or state.has("Papa Louie Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level6 Find 5 Gold Ballons", self.player), lambda state: (state.has("Boomer Unlocked", self.player)) or state.has("Foodini Unlocked", self.player) or state.has("Xandra Unlocked", self.player) or state.has("Prof. Fitz Unlocked", self.player) or state.has("Papa Louie Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level7 Find 5 Sodas", self.player), lambda state: (state.has("Boomer Unlocked", self.player)) or state.has("Foodini Unlocked", self.player) or state.has("Xandra Unlocked", self.player) or state.has("Prof. Fitz Unlocked", self.player) or state.has("Papa Louie Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level8 Find 100 Coins", self.player), lambda state: (state.has("Boomer Unlocked", self.player)) or state.has("Foodini Unlocked", self.player) or state.has("Xandra Unlocked", self.player) or state.has("Prof. Fitz Unlocked", self.player) or state.has("Papa Louie Unlocked", self.player))

    #Wall Jump Rules
    set_rule(self.multiworld.get_location("Level5 Find 100 Coins", self.player), lambda state: (state.has("Sarge Fan Unlocked", self.player)) or state.has("Penny Unlocked", self.player) or state.has("Ninjoy Unlocked", self.player))
    set_rule(self.multiworld.get_location("Captain Cori Rescued", self.player), lambda state: (state.has("Sarge Fan Unlocked", self.player)) or state.has("Penny Unlocked", self.player) or state.has("Ninjoy Unlocked", self.player))
    set_rule(self.multiworld.get_location("Peggy Rescued", self.player), lambda state: (state.has("Sarge Fan Unlocked", self.player)) or state.has("Penny Unlocked", self.player) or state.has("Ninjoy Unlocked", self.player))
    set_rule(self.multiworld.get_location("Rico Rescued", self.player), lambda state: (state.has("Sarge Fan Unlocked", self.player)) or state.has("Penny Unlocked", self.player) or state.has("Ninjoy Unlocked", self.player))

    #Crawling Rules
    set_rule(self.multiworld.get_location("Level2 Find 100 Coins", self.player), lambda state: (state.has("Georgito Unlocked", self.player)) or state.has("Greg Unlocked", self.player) or state.has("Yippy Unlocked", self.player))
    set_rule(self.multiworld.get_location("Prof. Fitz Rescued", self.player), lambda state: (state.has("Georgito Unlocked", self.player)) or state.has("Greg Unlocked", self.player) or state.has("Yippy Unlocked", self.player))
    set_rule(self.multiworld.get_location("Foodini Rescued", self.player), lambda state: (state.has("Georgito Unlocked", self.player)) or state.has("Greg Unlocked", self.player) or state.has("Yippy Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level4 Defeat 6 Burgerzillas", self.player), lambda state: (state.has("Georgito Unlocked", self.player)) or state.has("Greg Unlocked", self.player) or state.has("Yippy Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level6 Defeat 10 Burgerzillas", self.player), lambda state: (state.has("Georgito Unlocked", self.player)) or state.has("Greg Unlocked", self.player) or state.has("Yippy Unlocked", self.player))
    set_rule(self.multiworld.get_location("Zoe Rescued", self.player), lambda state: (state.has("Georgito Unlocked", self.player)) or state.has("Greg Unlocked", self.player) or state.has("Yippy Unlocked", self.player))

    #Double Jump Rules
    set_rule(self.multiworld.get_location("Yippy Rescued", self.player), lambda state: (state.has("Connor Unlocked", self.player)) or state.has("Peggy Unlocked", self.player) or state.has("Scooter Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level3 Find 100 Coins", self.player), lambda state: (state.has("Connor Unlocked", self.player)) or state.has("Peggy Unlocked", self.player) or state.has("Scooter Unlocked", self.player))
    set_rule(self.multiworld.get_location("Kingsley Rescued", self.player), lambda state: (state.has("Connor Unlocked", self.player)) or state.has("Peggy Unlocked", self.player) or state.has("Scooter Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level7 Find 100 Coins", self.player), lambda state: (state.has("Connor Unlocked", self.player)) or state.has("Peggy Unlocked", self.player) or state.has("Scooter Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level8 Defeat 12 Burgerzillas", self.player), lambda state: (state.has("Connor Unlocked", self.player)) or state.has("Peggy Unlocked", self.player) or state.has("Scooter Unlocked", self.player))

    #Push Rules
    set_rule(self.multiworld.get_location("Level4 Find 100 Coins", self.player), lambda state: (state.has("Captain Cory Unlocked", self.player)) or state.has("James Unlocked", self.player) or state.has("Rico Unlocked", self.player))
    set_rule(self.multiworld.get_location("Greg Rescued", self.player), lambda state: (state.has("Captain Cory Unlocked", self.player)) or state.has("James Unlocked", self.player) or state.has("Rico Unlocked", self.player))
    set_rule(self.multiworld.get_location("Level7 Defeat 13 Burgerzillas", self.player), lambda state: (state.has("Captain Cory Unlocked", self.player)) or state.has("James Unlocked", self.player) or state.has("Rico Unlocked", self.player))
    set_rule(self.multiworld.get_location("Connor Rescued", self.player), lambda state: (state.has("Captain Cory Unlocked", self.player)) or state.has("James Unlocked", self.player) or state.has("Rico Unlocked", self.player))




    # For the final boss, we also need to chain multiple conditions.
    # First of all, you always need a Sword and a Shield.
    # So far, we used the | and & operators to chain "Has" rules.
    # Instead, we can also use HasAny for an or-chain of items, or HasAll for an and-chain of items.


    # In hard mode, the player also needs both Health Upgrades to survive long enough to defeat the boss.
    # For this, we can use the optional "count" parameter for "Has".


    # Previously, we used an "if world.options.hard_mode" condition to check if we should apply the extra requirement.
    # However, if you're comfortable with boolean logic, there is another way.
    # OptionFilter is a rule component which isn't a "Rule" on its own, but when used in a boolean expression with
    # rules, it acts like True if the option has the specified value, and acts like False otherwise.


    # So with this option-checking rule component in hand, we can write our boss condition like this:

    # If you're not as comfortable with boolean logic, it might be somewhat confusing why this is correct.
    # There is nothing wrong with using "if" conditions to check for options, if you find that easier to understand.

    # Finally, we apply the rule to our "Final Boss Defeated" event location.



def set_completion_condition(world: PapaLouie2World) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # For this, we can use world.set_completion_rule.
    # You can just set a completion condition directly like any other condition, referencing items the player receives:
    world.set_completion_rule(Has("Warp Key", count=23))

    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.set_completion_rule(Has("Victory"))


# One final comment about rules:
# If your world exclusively uses Rule Builder rules (like PapaLouie2), it's worth trying CachedRuleBuilderWorld.
# CachedRuleBuilderWorld is a subclass of World that has a bunch of caching magic to make rules faster.
# Just have your world class subclass CachedRuleBuilderWorld instead of World:
#   class PapaLouie2World(CachedRuleBuilderWorld): ...
# This may speed up your world, or it may make it slower.
# The exact factors are complex and not well understood, but there is no harm in trying it.
# Generate a few seeds and see if there is a noticeable difference!
# If you're wondering, author has checked: PapaLouie2 is too simple to see any benefits, so we'll stick with "World".
