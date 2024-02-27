"""This file stores all global variables for use across files.

Note: I have no idea why this works, I just stole it from StackOverflow"""

from enum import Enum


class Directions(Enum):
    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)


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
