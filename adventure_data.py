""""
Game data for Office Adventure text adventure.
Holds details of locations and items 
One fragment of text taken from Annihilation by Jeff Vandermeer.
"""


# Introductory text
intro_text = """Tickety-Boo

Following an enjoyable evening carousing in a local pub you
have returned to the office to retrieve you laptop which you
prudently left in your locker.

The building seems eerily unfamiliar at this hour but
surely this is a simple task even though you are somewhat
befuddled.

Goal: get your laptop and go home.

Type 'help' for some info."""



# Items
# Each item must have a name and description. Other values, e.g. "statuses" not currently used.
items = {
    "pass": {"name": "Security Pass",
             "description": "Security pass bearing name name 'Rowley Birkin'.",
             "statuses": ["movable"]
             },
    
    "book": {"name": "The Necronomicon Guide To Interior Design",
             "description": "The text is in an unrecognisable language. There are several illustractions, all of which are incomprehensible and disturbing."},
    
    "cake": {"name": "Green Cake",
             "description": "Round cake with green icing",
             "statuses": ["movable"],
             "things": ["locker key"]
             },
    
    "fish": {"name": "Herring", "description": "Somewhat crimson in hue"}

    }


# Location definitions
# Each location must have a name and description
# "things" holds items present in the location
# "exits" defines areas accessed in particular directions
# "obstacles" contains optional inventory-based conditional behaviour triggered by upon moving to another location.
      
locations = {
    "Start": {"name": "Entryway", "description": "A dull office foyer with a seemingly deserted reception desk. Automatic barriers prevent ne'er-do-wells from wandering further.",
              "things": ["pass"],
              "exits": {"north": "Atrium", "south": "Outside"},
              "obstacles": {"north": {"need": "pass",
                                      "pass_text": "The pass enables you to cross the security gates.",
                                      "fail_text": "The security gates bar your way."},
                            "south": {"need": "laptop",
                                      "pass_text": "Well done - mission accomplished!. You've retrieved your laptop and left the building. You now just have to make your way home (in a yet-to-be-written sequel).",
                                      "fail_text": "You're not leaving without your laptop - that's the whole point!",
                                      }
                            },
              },
    
    "Outside": {"name": "Outside", "description": "The street outside. If you've made it here, you've completed the game!",
                "things": [],
                "exits": {"north": "Start"}
                },
    
    "Atrium": {"name": "Atrium", "description": "Spacious area. At the centre there is a sculpture made from giant wooden coat-hangers. Several posters advertise Bring Your Pet To Work Day, which was today.",
              "things": [],
              "exits": {"north": "Coffee Shop", "south": "Start", "east": "Stairwell (G)", "west": "West Side"}
              },
    
    "West Side": {"name": "West Side", "description": "A maze of twisty offices, all alike. Well off your route, so not worth exploring.",
                  "exits": {"east": "Atrium"}
                  },
    
    "Coffee Shop": {"name": "Coffee Shop", "description": "Crumbs litter the floor but the shelves are depleted.",
                   "things": ["cake"],
                   "exits": {"north": "Library", "south": "Atrium"}
                   },
    
    "Library": {"name": "Library", "description": "Ranks of metal shelves hold a multitude of documents.",
                "things": ["book"],
                "exits": {"south": "Coffee Shop"}
                },
    
    "Doom": {"name": "Enter the Doom Vortex" , "description": "SHOULD NOT BE ABLE TO REACH 'DOOM'!"},
    
    "Stairwell (G)": {"name": "Stairwell (G)", "description": "Dismal stairwell. A sign extols the virtues of using the stairs rather than the lifts.",
                      "things": [],
                      "exits": {"west": "Atrium", "up": "Stairwell (1)", "down": "Stairwell (B)", "east": "Lifts (G)"}
                      },
    
    "Stairwell (1)": {"name": "Stairwell (1)",
                      "description": "The wall is adorned with a mesmerising pattern of triangles.",
                      "things": [],
                      "exits": {"down": "Stairwell (G)", "up": "Stairwell (2)"},
                      },

    "Stairwell (2)": {"name": "Stairwell (2)",
                      "description": "The wall is adorned with a mesmerising pattern of triangles, slightly different from those on the first floor.",
                      "things": [],
                      "exits": {"down": "Stairwell (1)", "up": "Stairwell (3)"},
                      },
    
    "Stairwell (3)": {"name": "Stairwell (3)",
                      "description": "The wall is adorned with a mesmerising pattern of triangles, slightly different from those on the second floor, and might also owe more to Escher than Euclid.",
                      "things": [],
                      "exits": {"down": "Stairwell (2)", "up": "Stairwell (4)", "north": "Vortex"},
                      "obstacles": {"up":
                                    {"need": "oxygen",
                                     "pass_text": "YOU'RE NOT SUPPOSED TO GET THIS FAR!",
                                     "fail_text": "Gasping for breath you are unable to ascend further possibly because the air is too thin, or perhaps your feeble legs are too knackered."}
                                    }
                      },
    
    "Stairwell (4)": {"name": "Stairwell (4)", "description": "SHOULD NOT BE ABLE TO REACH 4TH FLOOR!"},

    "Stairwell (B)": {"name": "Stairwell (B)", "description": "Bottom of stairwell. Rather dingy with bare concrete walls.",
                      "things": [],
                      "exits": {"up": "Stairwell (G)", "north": "Carpark"}
                      },

    "Carpark": {"name": "Carpark", "description": "Underground carpark. No cars are present.",
                      "things": ["fish"],
                      "exits": {"south": "Stairwell (B)"}
                      },


    "Lifts (G)": {"name": "Lifts (G)", "description": "Six gleaming sets of lift doors promise speedy and convenient access to all floors, but unfortunately a sign indicates they are all out of order. This is also rather convenient from the point of view of someone wishing to place you in a simulated office environment without having to go to the bother of creating working lifts.",
                      "things": [],
                      "exits": {"west": "Stairwell (G)"}
                      },


    "Vortex": {"name": "Vortex", "description": """A swirling inter-dimensional vortex beyond the capacity of human perception.
Would make a cool screen saver, although the hypnotic compulsion to dive in might be a bit distracting.""",
                      "things": [],
                      "exits": {"south": "Stairwell (3)", "north": "Doom"},
                        "obstacles": {"north":
                                    {"need": "",
                                     "pass_text": "YOU'RE NOT SUPPOSED TO GET THIS FAR!",
                                     "fail_text": """That was a bit rash!
You shatter into countless fragments with the following words echoing
in the fading remnants of your conciousness: 
'That which dies shall still know life in death for all that decays is not forgotten
and reanimated it shall walk the world in the bliss of not-knowing.
And then there shall be a fire that knows the naming of you, and in the presence of the
strangling fruit, its dark flame shall acquire every part of you that remains.'\n """,
                                     "location_after_fail": "Start"}
                                    }               
                      },
}

