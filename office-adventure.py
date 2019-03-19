#!/usr/bin/env python3

""""
Text Adventure
"""

import random


# (1) Need to add some conditional stuff. For example exit through the
# security barriers only becomes possible if pass used
# Defined "obstacles" which depend on - location / item present in location (and sate of item)
# and can be overcome by - item in player inventory or action by player


# (2) Need to improve items
# - want to be able to specify which verbs work with an item
# - want to be able to use an item as container from item(s)
# - want to have option of more detailed description
#  Something like
items = {
    "pass": {"description": "security pass bearing name name 'Rowley Birkin'.",
             "statuses": ["movable"]
             },
    
    "cake": {"description": "round cake with green icing",
             "statuses": ["movable"],
             "things": ["locker key"]
             }
    
    }


# Location definitions
locations = {
    "Start": {"name": "Entryway", "description": "A dull office foyer with a seemingly deserted reception desk. Automatic barriers prevent ne'er-do-wells from wandering further.",
              "things": ["pass"],
              "exits": {"north": "Atrium", "south": "Outside"},
              "obstacles": {"north": {"need": "pass",
                                      "pass_text": "The pass enables you to cross the security gates.",
                                      "fail_text": "The security gates bar your way."}},
              },
    
    "Outside": {"name": "Outside", "description": "The street outside.",
                "things": [],
                "exits": {"north": "Start"}
                },
    
    "Atrium": {"name": "Atrium", "description": "Spacious area. At the centre there is a sculpture made from giant wooden coat-hangers.",
              "things": [],
              "exits": {"north": "Coffee Shop", "south": "Start", "east": "Stairwell (G)"}
              },
    
    "Coffee Shop": {"name": "Coffee Shop", "description": "Crumbs litter the floor but there is no sign of food nor drink.",
                   "things": ["cake"],
                   "exits": {"south": "Atrium"}
                   },
    
    "Stairwell (G)": {"name": "Stairwell (G)", "description": "Dismal stairwell. A sign extols the virtues of using the stairs rather than the lifts.",
                      "things": [],
                      "exits": {"west": "Start", "up": "Stairwell (1)", "down": "Stairwell (B)"}
                      },
    
    "Stairwell (1)": {"name": "Stairwell (1)",
                      "description": "The wall is adorned with a mesmerising pattern of triangles.",
                      "things": [],
                      "exits": {"down": "Stairwell (G)"},
                      },
    
    "Stairwell (B)": {"name": "Stairwell (B)", "description": "Bottom of stairwell. Rather dingy with bare concrete walls.",
                      "things": [],
                      "exits": {"up": "Stairwell (G)"}
                      }

}




        

class Adventure(object):
    """Text Adventure"""
    def __init__(self, start_location="Start"):
        self.directions = ["north", "south", "east", "west", "up", "down"]
        self.current_location = locations.get(start_location)
        self.current_input = []
        self.inventory = []
        # Start game
        self.keep_going = True
        self.run_game()
        self.show("Bye!")

    def run_game(self):
        """Main game loop"""
        self.show_start_text()
        self.display_info()
        while self.keep_going:
            self.get_input()
            self.parse()

    def show(self, text):
        """Display output - currently just uses print"""
        print(text)

    def show_start_text(self):
        """Display introductory message"""
        text = """Tickety-Boo

Following an enjoyable evening carousing in a local pub you
have returned to the office to retrieve you laptop which you
prudently left in your locker.

The building seems eerily unfamiliar at this hour but
surely this is a simple task even though you are somewhat
befuddled.

Goal: get your laptop and go home.

Type 'help' for some info."""
        self.show(text)
        self.show("")

    def display_info(self):
        """Show information about current location"""
        cl = self.current_location
        self.show(cl.get("name"))
        self.show(cl.get("description"))
        # Show items
        things = cl.get("things", "")
        if things:
            self.show("You can see: " + ", ".join(things))
        # Show exits (needs improving - currently shows location key rather than associated name)
        self.show(". ".join(["{} to {}".format(k.capitalize(), v)
                             for k,v in cl.get("exits", {}).items()]))

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

    def parse(self):
        """Simple verb-noun parser"""
        # Local "verb" functions
        def v_go(noun):
            """Try to move to a new location.
            Args:
                noun - either one of the standard directions from self.directions or
                       initial letter of a direction (e.g. "n" or "north")
            """
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
                    return
            
            # See if there is an available destination in chosen direction
            destination = self.current_location["exits"].get(noun, "")
            # If destination available, move to it
            if destination:
                self.current_location = locations.get(destination)
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
                    # extend method can be used to combine elements of two lists
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
            available_things = self.current_location.get("things", [])
            # Take all available items
            if noun == "all":
                if available_things:
                    self.show("You pick up: " + ", ".join(available_things))
                    self.inventory.extend(available_things)
                    available_things.clear()
                else:
                    self.show("There's nothing to pick up.")
            # Take individual item
            else:
                if noun in available_things:
                    self.inventory.append(noun)
                    available_things.remove(noun)
                    self.show("You pick up the {}.".format(noun))
                else:
                    self.show("No {} to pick up.".format(noun))


        def v_examine(item):
            """Display item's description, if item available"""
            if item in self.inventory or item in self.current_location.get("things", []):
                self.show("A " + items[item]["description"])
            else:
              self.show("Can't see {} to examine.".format(item))  

        def v_exits(_):
            """Display available exists from current location"""
            self.show("Available exits: " + ", ".join(self.available_exits()))

        def v_help(_):
            """Display some help text"""
            self.show("Game uses simple verb-noun text adventure input.")
            self.show("Known verbs: " + ", ".join(verb_to_fn_map.keys()))
            self.show("Known directions: "
                      + ", ".join(self.directions)
                      + ", (or their initial letters)")

        def v_inv(_):
            """Display contents of inventory."""
            if self.inventory:
                self.show("You have: " + ", ".join(self.inventory))
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

        # Map verbs to their coresponding functions
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
        fn = verb_to_fn_map.get(ci[0], "")
        if fn:
            fn(ci[1])
        # Message when verb not recognised
        else:
            message = random.choice(["Don't undersand what you said.",
                                  "Eh?",
                                  "Do what?",
                                  "Urgle?",
                                  "Kindly rephrase."])
            self.show(message)


if __name__ == "__main__":
    go = Adventure()
