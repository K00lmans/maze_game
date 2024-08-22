"""This file stores all global variables and functions for use across files.

Note: I have no idea why this works, I just stole it from StackOverflow.

Do not type hint this file as it gets funky."""

from enum import Enum
from time import sleep


class Directions(Enum):
    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)


class Room:
    def __init__(self, room_style, x, y):
        self.style = room_style
        self.x = x
        self.y = y
        self.paths = []
        self.occupants = []
        self.placed_items = []  # All the items placed in a room

    def entered(self, entering_player, room_list, player_list):
        if len(self.placed_items) > 0:
            for item in self.placed_items:
                item[0](entering_player, self, item)
                sleep(2)
        self.style(self, entering_player, room_list, player_list)


class Player:
    def __init__(self, is_human, player_name, starting_coins, difficulty):
        self.human = is_human
        self.name = player_name
        self.gold = starting_coins
        self.difficulty = difficulty
        self.x = 0
        self.y = 0
        self.state = ["default", None]  # First is the name of the state, second is a place for data about the state
        self.inventory = []
        self.visited_rooms = []

    def check_inventory(self, room, rooms, players):
        if self.gold >= 0:
            print(f"\nYou check your pockets and find you have {self.gold} gold coins.")
        else:
            print(f"\nYou check your pockets and find a paper saying you are {-self.gold} gold"
                  f" coins in debt.")
        if len(self.inventory) == 0:
            print("You currently have nothing in your pack.")
            sleep(2.5)
        else:
            done_using_items = False
            while not done_using_items:
                print("\nYou have the following items in your pack:")
                for item_number, item in enumerate(self.inventory):
                    print(f"  {item_number + 1}: {item.__name__.replace('_', ' ').capitalize()}")
                item_selected = False
                while not item_selected:
                    try:
                        selection = int(input(f"Enter the number next to the item to view/use it and"
                                              f" {len(self.inventory) + 1} to move on.\n"))
                        item_selected = True
                    except ValueError:
                        print("Enter only the number of the item")
                if 1 <= selection <= len(self.inventory):
                    self.inventory[selection - 1](True, self, players, room, rooms)
                    sleep(2.5)
                else:
                    done_using_items = True


def init():
    import room_styles as rm
    import items as i
    good_rooms = {
        "small_treasure": rm.small_treasure,
        "large_treasure": rm.large_treasure,
        "gold_machine": rm.gold_machine,
        "match_machine": rm.match_machine,
        "pit_lever": rm.pit_lever,
        "gold_vacuum": rm.gold_vacuum
    }
    bad_rooms = {
        "teleport": rm.teleport,
        "pit_slide": rm.pit_slide,
        "swapper": rm.swapper,
        "magnet": rm.magnet,
        "recall": rm.recall,
        "charity": rm.charity,
        "pickpocket": rm.pickpocket
    }
    special_rooms = {
        "pit": rm.pit,
        "combat": rm.combat,
        "swapper_control": rm.swapper_control,
        "psycho": rm.psycho,
        "wise_old_man": rm.wise_old_man
    }
    other_rooms = {
        "start": rm.start,
        "empty": rm.empty,
        "goal": rm.goal,
        "shop": rm.shop
    }
    global ROOMS
    ROOMS = {
        "good_rooms": good_rooms,
        "bad_rooms": bad_rooms,
        "special_rooms": special_rooms,
        "other_rooms": other_rooms
    }
    global ROOM_HELPER_FUNCTIONS
    ROOM_HELPER_FUNCTIONS = {
        "display_players_in_room": rm.display_players_in_room,
        "generate_room_based_rng_number": rm.generate_room_based_rng_number,
        "generate_room_rng_number": rm.generate_room_rng_number,
        "put_player_in_room": rm.put_player_in_room,
        "in_pit": rm.in_pit,
        "in_combat": rm.in_combat
    }

    global ITEMS
    ITEMS = {
        "match": i.match,
        "swapper_remote": i.swapper_remote,
        "trap": i.trap,
        "gold_potion": i.gold_potion,
        "dagger": i.dagger,
        "nope_picture": i.nope_picture,
        "compass": i.compass,
        "magic_map": i.magic_map
    }
    global ITEM_HELPER_FUNCTIONS
    ITEM_HELPER_FUNCTIONS = {
        "check_if_used": i.check_if_used,
        "trapped": i.trapped,
        "potion_gold": i.potion_gold,
        "encountered_goblin": i.encountered_goblin,
        "move_goblin": i.move_goblin
    }
    global HUMAN_ONLY_ITEMS
    HUMAN_ONLY_ITEMS = [i.match, i.compass, i.magic_map]  # Items the AI can't use


def generate_maze_image(rooms_to_display, player=None):
    """Generates an ascii representation of the maze"""
    # Make sure the min and max values correspond to a room
    max_x = rooms_to_display[0].x
    min_x = rooms_to_display[0].x
    max_y = rooms_to_display[0].y
    min_y = rooms_to_display[0].y
    for room in rooms_to_display:
        if room.x > max_x:
            max_x = room.x
        if room.x < min_x:
            min_x = room.x
        if room.y > max_y:
            max_y = room.y
        if room.y < min_y:
            min_y = room.y
    empty_row = []
    for _ in range((max_x - min_x) + 1):
        empty_row.append(None)
    location_relative_room_grid = []
    for _ in range((max_y - min_y) + 1):
        location_relative_room_grid.append(empty_row.copy())

    # I don't really know how this translation code works
    # It was also made assuming a room at (0, 0) and I don't know if it breaks if that's not true
    for room in rooms_to_display:
        translated_x = room.x + abs(min_x)
        translated_y = max_y - room.y
        location_relative_room_grid[translated_y][translated_x] = room

    map_image = ""
    for row in location_relative_room_grid:
        printed_room_row = ["", "", "", "", ""]
        for room in row:
            if room is None:
                for text_row_number in range(len(printed_room_row)):
                    printed_room_row[text_row_number] += "     "
            else:
                if room.style in list(ROOMS["good_rooms"].values()):
                    room_category = "G"
                elif room.style in list(ROOMS["bad_rooms"].values()):
                    room_category = "B"
                elif room.style in list(ROOMS["special_rooms"].values()):
                    room_category = "S"
                elif room.style == ROOMS["other_rooms"]["start"]:
                    room_category = "⌂"
                elif room.style == ROOMS["other_rooms"]["empty"]:
                    room_category = "E"
                elif room.style == ROOMS["other_rooms"]["goal"]:
                    room_category = "G"
                elif room.style == ROOMS["other_rooms"]["shop"]:
                    room_category = "$"
                else:
                    room_category = "U"
                if player is not None:
                    if player.name in room.occupants:
                        room_category = "C"

                printed_room_row[1] += " ┌─┐ "
                printed_room_row[3] += " └─┘ "
                if "NORTH" in room.paths:
                    printed_room_row[0] += "  ▲  "
                else:
                    printed_room_row[0] += "     "
                if "SOUTH" in room.paths:
                    printed_room_row[4] += "  ▼  "
                else:
                    printed_room_row[4] += "     "
                if "WEST" in room.paths:
                    printed_room_row[2] += f"◄│{room_category}│"
                else:
                    printed_room_row[2] += f" │{room_category}│"
                if "EAST" in room.paths:
                    printed_room_row[2] += "►"
                else:
                    printed_room_row[2] += " "
        for text_row in printed_room_row:
            map_image += text_row + "\n"
    return map_image
