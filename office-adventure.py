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
import textwrap
# Import the game data
from adventure_data import intro_text, items, locations, item_events


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
            self.extra_stuff()
            self.get_input()
            self.parse()
            self.item_events_check()
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

    def show(self, text, line_length=80, add_line=False):
        """Display output - currently just uses print and textwrap
        Args:
            text - text to be displayed
            line_length (int) - line-length used for text wrapiing
            add_line (bool) - when True, add blank line between paragraphs
        """
        # Using textwrap.fill to set line length. However, it also
        # removes any new lines (even when drop_whitespace=False)
        # causing existing paragraphs to be lost. Have added
        # paragraph splitting here first, so textwrap only
        # applied to one paragraph at a time.
        for paragraph in text.splitlines():
            print(textwrap.fill(paragraph, line_length))
        if add_line:
            print("")

    def show_start_text(self):
        """Display introductory message"""
        self.show(self.start_text, add_line=True)

    def display_info(self):
        """Show information about current location"""
        cl = self.current_location
        # Show locations name and description
        self.show("[" + cl.get("name") + "]", add_line=False)
        self.show(cl.get("description"), add_line=True)
        # Show items present
        things = cl.get("things", "")
        if things:
            self.show("You can see: " + ", ".join(self.make_item_list(things)))
        # Show exits
        self.show("Obvious exits: " +
                  " ".join(["[{} to {}]".format(direction.capitalize(), locations[location]["name"])
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
                
            # Check for event associated with the particular move
            event = self.current_location.get("events", {}).get(noun, {})
            # If there's an event, see if event passes/fails
            if event:
                result = self.event_check(**event["needs"])
                # Process outcomes of pass/fail
                if result == False:
                    self.event_outcomes(**event["fail_outcomes"])
                    # don't move to new location if event didn't pass
                    return
                else:
                    self.event_outcomes(**event["pass_outcomes"])
                    
            
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
                    for item in self.inventory:
                        self.show("You drop the " + item)
                    # handy - extend method can be used to combine elements of two lists
                    # (unlike append which puts list inside list)
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
                    # Can't pick up item with "fixed" status
                    if "fixed" in  items[choice].get("statuses", []):
                        self.show("You are unable to lift the {}.".format(choice))
                    else:
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



    # Methods dealing with events that depend on presence/absence of items
    # in current location or player inventory.
    def item_events_check(self):
        """Check each item event
        Events based on items present in current location
        """
        for event in item_events:
            result = self.event_check(**event.get("needs", {}))
            if result:
                self.event_outcomes(**event.get("pass_outcome", {}))
            else:
                self.event_outcomes(**event.get("fail_outcome", {}))
                

    def event_check(self, player_needs=(), location_needs=(), location_not_needs=(), **kwargs):
        """Check prerequisites for an action
        Can be any combination of player needs, location needs or location not needs.
        Args:
            player_needs - list of item(s) the player needs in inventory for "pass" result
            location_needs - list of items needed in location for "pass" result
            location_not_needs - list of items absent from location for "pass" result
        Returns:
            Pass/Fail - fails if any condition fails

        """
        outcomes = []
        
        if player_needs:
            temp = self.items_present_check(items=player_needs, in_inventory=True)
            outcomes.append(temp)
        if location_needs:
            temp = self.items_present_check(items=location_needs, in_inventory=False)
            outcomes.append(temp)
        if location_not_needs:
            temp = self.items_present_check(items=location_not_needs,
                                            in_inventory=False,
                                            invert=True)
            outcomes.append(temp)
        
        return False not in outcomes 
        

    def event_outcomes(self, message="", new_location="", remove_location_items=(), **kwargs):
        """Process event outcome
        Will likely expand to cover add/remove item(s) from location/player
        """
        if message:
            self.show(message)
        if new_location:
            self.current_location = locations.get(new_location)
        #Remove items from current location
        for item in remove_location_items:
            location_items = self.current_location.get("things", [])
            if item in location_items:
                location_items.remove(item)
            

    def items_present_check(self, items, in_inventory=False, invert=False):
        """Check if the listed items are all present in either: (a) the current location
        or (b) player's inventory. Alternatively, do the reverse, i.e. check not present
        when invert flag set.
        Args:
            items - items to check (in list or similar container)
            in_inventory (bool) - when True check inventory, otherwise check
                                 current location
            invert - reverse the response (effecitively reverse the check to "not present")
        Returns:
                True/False
        """
        status = False

        # Using sets for convenient comparison
        if in_inventory:
            compare_items = set(self.inventory)
        else:
            compare_items = set(self.current_location.get("things", []))
        
        status = set(items).issubset(compare_items)
        
        #Invert the result if flag set
        if invert:
            satus = not status
        return status




if __name__ == "__main__":
    go = Adventure(start_text = intro_text)
