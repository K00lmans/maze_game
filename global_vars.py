"""This file stores all global variables for use across files.

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
                sleep(.5)
        self.style(self, entering_player, room_list, player_list)


class Player:
    def __init__(self, is_human, player_name, starting_coins):
        self.human = is_human
        self.name = player_name
        self.gold = starting_coins
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
    import items as i
    import room_styles as rm
    global GOOD_ROOMS
    GOOD_ROOMS = GOOD_ROOMS = [rm.small_treasure, rm.large_treasure, rm.huge_treasure, rm.gold_machine,
                               rm.match_machine, rm.pit_lever, rm.gold_vacuum]
    global BAD_ROOMS
    BAD_ROOMS = [rm.teleport, rm.pit_slide, rm.swapper, rm.magnet, rm.recall, rm.charity, rm.pickpocket]
    global SPECIAL_ROOMS
    SPECIAL_ROOMS = [rm.pit, rm.combat, rm.swapper_control, rm.psycho, rm.wise_old_man]
    global ITEMS
    ITEMS = [i.match, i.swapper_remote, i.trap, i.gold_potion, i.dagger, i.nope_picture, i.compass]
