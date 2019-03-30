#!/usr/bin/env python3

""""
Simple verb-noun text adventure
Relies on items defined in items dictionary and locations
defined in locations dictionary, imported from adventure_data.py.
"""

# Improvements to make?
# More verbs - capability to use items
# Containers - items can hold other items
# More complex interactions
# Possibly have classes for items and/or locations rather than dictionaries


import random
# Import the game data
from adventure_data import intro_text, items, locations


class Adventure(object):
    """Text Adventure
    Relies on data in items and locations dictionaries.
    Args:
        start_location - dictionary key of start location from locations dict
    """
    def __init__(self, start_text, start_location="Start"):
        # Movement directions supported
        self.directions = ["north", "south", "east", "west", "up", "down"]
        # Game start text info
        self.start_text = start_text
        # Player's location
        self.current_location = locations.get(start_location)
        # Holds last input from user as dictionary of words
        self.current_input = []
        # Player inventory
        self.inventory = []
        # Tracks number of moves between locations
        self.move_count = 0
        # Start game
        self.keep_going = True
        self.run_game()

    def run_game(self):
        """Main game loop"""
        self.show_start_text()
        self.display_info()
        while self.keep_going:
            self.get_input()
            self.parse()
            self.extra_stuff()
            self.items_present_check(["cake", "book"])
        # End message
        self.show("Bye!")
            
    def extra_stuff(self):
        """Do some extra stuff - random atmosphere messages"""
        if self.move_count > 10:
            option = random.randint(1, 20)
            if option == 1:
                self.show("The lights flicker ominously but then recover.")
            elif option == 2:
                self.show("Did something move in the shadows?")
            elif option == 3:
                self.show("What was that noise, 'Iä! Iä! Cthulhu fhtagn'?")

    def show(self, text):
        """Display output - currently just uses print"""
        print(text)

    def show_start_text(self):
        """Display introductory message"""
        self.show(self.start_text)

    def display_info(self):
        """Show information about current location"""
        cl = self.current_location
        # Show locations name and description
        self.show("\n[" + cl.get("name") + "]")
        self.show(cl.get("description"))
        # Show items present
        things = cl.get("things", "")
        if things:
            self.show("You can see: " + ", ".join(self.make_item_list(things)))
        # Show exits
        self.show("Obvious exits: " +
                  " - ".join(["{} to {}".format(direction.capitalize(), locations[location]["name"])
                             for direction, location in cl.get("exits", {}).items()]))
        
    def get_input(self, prompt=">"):
        """Get input from user"""
        words = input(prompt)
        words = words.strip().lower()
        self.current_input = words.split()
        #Pad to always have at least two empty strings
        self.current_input.extend([""] * (2 - len(self.current_input)))

    def available_exits(self):
        """Return exits available from current location"""
        return [e for e in self.directions
                if e in self.current_location["exits"]]
    
    def make_item_list(self, item_list):
        """Return formatted list of items in form item name (key)
        from supplied list of item keys
        Args:
            item_list - list of item keys to be included
        """
        return ["{} ({})".format(items[item]["name"], item) for item in item_list]

    def parse(self):
        """Simple verb-noun parser.
        Processes contents of self.current_input.
        """
        # Local "verb" functions
        def v_go(noun):
            """Try to move to a new location.
            Ability to move can be affected by optional "obstacle" location setting.
            Args:
                noun - either one of the standard directions from self.directions or
                       initial letter of a direction (e.g. "n" or "north")
            """
            # Do nothing if no noun
            if not noun:
                self.show("Go where? Direction needed.")
                return
            # Convert single letter noun back into full direction name (eg "n" to "north")
            if len(noun) == 1:
                noun = {d[0]:d for d in self.directions}.get(noun, "")
                
            # Check for blocking condition
            obstacle = self.current_location.get("obstacles", {}).get(noun, {})
            if obstacle:
                if obstacle["need"] in self.inventory:
                    self.show(obstacle["pass_text"])
                else:
                    self.show(obstacle["fail_text"])
                    # Teleport to new location if one set on fail condition
                    if obstacle.get("location_after_fail", ""):
                        self.current_location = locations.get(obstacle["location_after_fail"])
                        self.display_info()
                    return
            
            # See if there is an available destination in chosen direction
            destination = self.current_location["exits"].get(noun, "")
            # If destination available, move to it
            if destination:
                self.current_location = locations.get(destination)
                # Increment move count
                self.move_count += 1
                # Invalid destination - should not happen if data is right
                if not self.current_location:
                    print("GAME ERROR - location not found:", destination)
                self.display_info()
            else:
                self.show("Can't go {}.".format(noun))

        def v_drop(noun):
            """Drop item (or all items) from inventory to present location"""
            # Drop "all"
            if noun == "all":
                if self.inventory:
                    # handy - extend method can be used to combine elements of two lists
                    # (unlike append which puts list inside list)
                    self.show("You drop: " + ", ".join(self.inventory))
                    self.current_location.get("things", []).extend(self.inventory)
                    self.inventory.clear()
                else:
                    self.show("You don't have anything to drop.")
            # Drop individual item
            else:
                if noun in self.inventory:
                    self.current_location.get("things", []).append(noun)
                    self.inventory.remove(noun)
                    self.show("You drop the {}.".format(noun))
                else:
                    self.show("No {} to drop.".format(noun))
                    
        def v_take(noun):
            """Take item (or all items) from location and place in inventory"""
            # Idenfify items present in the current location
            available_things = self.current_location.get("things", [])
            # Set the things we're going to try to pick up
            if noun == "all":
                choices = available_things[:]
            else:
                choices = [noun]
            # Display message if nothing to pick up.
            if not choices:
                self.show("There's nothing to pick up.")
            # Try to pick up each item
            for choice in choices:
                if choice in available_things:
                    self.inventory.append(choice)
                    available_things.remove(choice)
                    self.show("You pick up the {}.".format(choice))
                # Can't pick up because choice not present
                else:
                    self.show("No {} to pick up.".format(choice))

        def v_examine(item):
            """Display item's description, if item available"""
            if item in self.inventory or item in self.current_location.get("things", []):
                self.show(items[item]["description"])
            else:
              self.show("Can't see {} to examine.".format(item))  

        def v_exits(_):
            """Display available exists from current location"""
            self.show("Available exits: " + ", ".join(self.available_exits()))

        def v_help(_):
            """Display some help text"""
            self.show("Game uses simple verb-noun text adventure input.")
            self.show("Some areas can only be accessed if you possess a particular item.")
            self.show("Known verbs: " + ", ".join(verb_to_fn_map.keys()))
            self.show("Known directions: "
                      + ", ".join(self.directions)
                      + ", (or their initial letters)")

        def v_inv(_):
            """Display contents of inventory."""
            if self.inventory:
                things = self.make_item_list(self.inventory)
                self.show("You have: " + ", ".join(things))
            else:
                self.show("You have nothing.")

        def v_look(_):
            """(re) Display description of current location"""
            self.display_info()
        
        def v_quit(_):
            """quit from game"""
            self.get_input(prompt="Are you sure (y/n)? ")
            if self.current_input[0][:1] == "y":
                self.keep_going = False
            
        # Call verb with noun as argument from current input
        ci = self.current_input
        # verb "go" can be ommited for movement, so add "go" back if we have a
        # direction, or initial letter of direction, on its own.
        # If first word is a direction (or initial letter), and second word empty
        # Move first word to second and add "go" as first work
        if not ci[1] and ci[0] in (self.directions + [c[0] for c in self.directions]):
            ci[1] = ci[0]
            ci[0] = "go"

        # Map verbs from user input to their coresponding local functions
        # Can be multi-to-one to handle synonyms (e.g. get, take)
        verb_to_fn_map = {"exits": v_exits,
                  "go": v_go,
                  "get": v_take,
                  "examine": v_examine,
                  "help": v_help,
                  "inv": v_inv,
                  "inventory": v_inv,
                  "take": v_take,
                  "drop": v_drop,
                  "look": v_look,
                  "quit": v_quit,
            }

        # Call "verb" function and send noun as argument
        verb_fn = verb_to_fn_map.get(ci[0], "")
        if verb_fn:
            verb_fn(ci[1])
        # Message when verb not recognised
        else:
            message = random.choice(["Don't undersand what you said.",
                                  "Eh?",
                                  "Do what?",
                                  "Urgle?",
                                  "Kindly rephrase."])
            self.show(message)


    def items_present_check(self, items, in_inventory=False):
        """Check if the listed items are all present in either: (a) the current location
        or (b) player's inventory.
        Args:
            items - items to check (in list or similar container)
            in_inventory (bool) - when True check inventory, otherwise check
                                 current location
        Returns:
                True/False
        """
        status = False

        # 
        # Using sets for convenient comparison
        if in_inventory:
            compare_items = set(self.inventory)
        else:
            compare_items = set(self.current_location.get("things", []))
        
        status = set(items).issubset(compare_items)
        print(items, compare_items, status)
        return status


if __name__ == "__main__":
    go = Adventure(start_text = intro_text)
