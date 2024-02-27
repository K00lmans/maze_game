"""The name and logic for all the items available from the shop.

Guide for adding new items:

1: All items take a Player class of the player who used the item, the Room class of the room they used it in, the list
of rooms, the list of players, and a bool for if the item can be used. All inputs except for the players Player class
and the usable bool should be optional defaulting to None for simplified shop logic.

2: All displayed text should only be displayed if the player is a person to prevent confusion.

3: Keep in mind when naming item functions that the name of the function will be displayed to the user. At the start of
the function you should include an inspection description that includes the name and then on a new line indented twice a
short in universe description.

4: Make sure you always include a check_if_used() call after your description and only activate the items effects if
that returns true.

5: If an AI makes a decision in a room that relates to a human player, print a short summary of what happened.

6: If you make a new item that is placed in a room, don't forget to make a function for what it does if it is happened
upon. These functions should take as input the Player class of the player who entered the room it's in, the Room class
of the room its in, the list of rooms, and the list of players and return the same.

7: When your item is placed in a room, make sure to add a list with the first item being the function with the logic for
that item and the second item being the Player class of the player who placed it.

8: If you have an item that is in a room and needs to move, make sure to add it to the movement script in the main file.

9: If you want to remove items, do not remove them from here. Instead, simply remove them from the items list in the
variable file.

10: AI currently can not buy or use items, so you don't HAVE to add code for the AI using it. Doing so will future-proof
your code for when AI using items is added."""

import random as r
import math as m

import global_vars as v


# Helper Functions
def check_if_used(usable, player_human):
    """Asks the player if they want to use the item and returns the response as a bool"""
    if not usable:  # Simplifies in-function logic
        return False
    else:
        if not player_human:
            return True
        else:
            selection_options = ["y", "n"]
            selection = None
            while selection not in selection_options:
                selection = input("Would you like to use this item? (Y/N)\n").lower()
            if selection == "y":
                return True
            else:
                return False


def trapped(player, room, placed_item):
    """Logic for placed trap"""
    player.gold -= 2
    placed_item[1].gold += 2
    if player.human:
        if player is placed_item[1]:
            print("\nYou walk into the room and get stuck in a trap. You realize that this is in fact your trap and"
                  " facepalm. Thankfully when you check your pockets you still have the same amount of gold you have"
                  " before and you breath a sigh of relief.")
        else:
            print("\nYou walk into the room and get stuck in a trap. You hear a loud vacuum sound and see two gold"
                  " coins get sucked from you pocket. After the coins fall deep into the trap you are released. You"
                  " take a moment to inspect the trap to see if you can get your gold back. While you don't see any way"
                  f" to get your gold back, you do notice a plaque that says 'Property of {placed_item[1].name}'.")
    else:
        if placed_item[1].human:
            print(f"\n{player.name} has been trapped in {placed_item[1].name}'s trap and had 2 gold stolen.")


def potion_gold(player, room, placed_item):
    """Logic for placed gold potion"""
    player.gold += 3
    room.placed_items.remove(placed_item)
    if player.human:
        print("\nAs you walk into the room you notice a golden potion sitting in the floor without a cap or cork. Your"
              " instincts take over and you drink it as quickly as possible to prevent violation of the 5 second rule."
              " One you are done drinking you notice your pockets feel heavier and upon further investigation you"
              " realize you have 3 extra gold for some reason. Neat! Upon further examination of the bottle you see a"
              f" small label saying 'Property of {placed_item[1].name}'.")
    else:
        if placed_item[1].human:
            print(f"{player.name} has found and drank {placed_item[1].name}'s potion.")


def encountered_goblin(player, room, placed_item):
    player.gold -= 1
    placed_item[1].gold += 1
    if player.human:
        print("\nYou enter the room and all of a sudden, a small green blur rushes up to you. Before you can even"
              " think, you see the blur reach for your pockets and grab a coin out and run off again before you can"
              " even do anything.")
        if player is placed_item[1]:
            print("After a moment, the goblin walks back up to looking quite ashamed. It takes the gold coin it had"
                  " taken and meekly hands it back to you. You decide to take a moment to comfort your little goblin"
                  " pet and to let it know that you understand that it just made a simple mistake.")
        else:
            print("As the blur speeds away, all you can hear is cackling occasionally interrupted by the cries of 'GOLD"
                  f" COIN FOR MASTER {placed_item[1].upper()}' echoing down the halls. You take a moment to recover"
                  " from the shock of this event before finally inspecting your surroundings.")
    else:
        if placed_item[1].human:
            print(f"\n{placed_item[1].name}'s goblin pet has stolen a gold coin from {player.name}")


def move_goblin(rooms, room):
    """Logic for moving the goblin"""
    room.placed_items.remove(encountered_goblin)
    new_room = r.choice(rooms[:-1])  # Prevents it from being in the goal room
    new_room.placed_items.append(encountered_goblin)


# Items
def match(usable, player, players=None, current_room=None, rooms=None):
    """Identifies the rooms next to the room of the player who activated it"""
    if player.human:
        print("Match\n  A small match. Should create enough light to see into a room down a hallway.")
    if check_if_used(usable, player):
        player.inventory.remove(match)
        if player.human:
            print("\nYou strike the match and quickly look down the hallways of this room before it goes out.")
            for direction in current_room.paths:
                connected_room_x = current_room.x + v.Directions[direction].value[0]
                connected_room_y = current_room.y + v.Directions[direction].value[1]
                for room in rooms:
                    if room.x == connected_room_x and room.y == connected_room_y:
                        connected_room = room
                        break
                if connected_room.style in v.SPECIAL_ROOMS:
                    article = "the "
                else:
                    if connected_room.style.__name__[0] == "a":
                        article = "an "
                    else:
                        article = "a "
                print(f"When you look down the {direction.lower()} hallway, you can just make out the room at the other"
                      f" end. The room appears to be {article + connected_room.style.__name__.replace('_', ' ')} room.")
            print("Almost as soon as your done looking down all the halls, the match fizzles out. It looks like it"
                  " won't light again, so you toss it aside.")


def swapper_remote(usable, player, players=None, room=None, rooms=None):
    """Swaps any two players"""
    if player.human:
        print("Swapper Remote\n  A small box labeled 'swapper remote'. There are two dials each with a name and a big"
              " button in the center.")
    if check_if_used(usable, player):
        player.inventory.remove(swapper_remote)
        if player.human:
            print("\nYou pull out the remote and start fiddling with the dials to try and decide who to swap.\n")
            for player_number, other_player in enumerate(players):
                print(f"{player_number + 1}: {other_player.name}")
            players_selected = False
            swapped_players = []
            while not players_selected:
                try:
                    first_player = int(input("Select the position of the first dial: ")) - 1
                    second_player = int(input("Select the position of the second dial: ")) - 1
                    swapped_players.append(players[first_player])
                    swapped_players.append(players[second_player])
                    players_selected = True
                except ValueError:
                    print("Enter the number next to the player you want to select")
                except IndexError:
                    print("One of your player numbers does not exist")
            print("\nAfter setting the dials to the correct selection you push the big red button and swap"
                  f" {swapped_players[0].name} and {swapped_players[1].name}. The device hums with energy and glows"
                  " bright red. You drop it as it starts to burn your fingers. As soon as it hits the ground, the extra"
                  " burst of kinetic energy causes the whole device to burst. You try and shield yourself from the"
                  " shrapnel, but it never comes. Looking back at where the device hit the ground there is nothing but"
                  " a small scratch mark from where it hit the ground. It must have teleported itself after receiving"
                  " the damage.")
            if player in swapped_players:
                print("For a brief moment you are sad that it did not work. You look up to head on your way once more,"
                      " only to realize that you are now in a different room. You smile to yourself, happy to know it"
                      " worked before you head once more through the maze.")
            else:
                print("You are unsure if the machine was able to do it's job before the rapid dismantalization of the"
                      " device, however you get a strong feeling that it has.")
        else:
            swapped_players = r.choice(players)
            if swapped_players[0].human or swapped_players[1].human:
                print(f"{player.name} has swapped {swapped_players[0].name} and {swapped_players[1].name}.")
        swapped_players_rooms = [None, None]
        for searched_room in rooms:
            if swapped_players[0].name in searched_room.occupants:
                swapped_players_rooms[0] = searched_room
            if swapped_players[1].name in searched_room.occupants:
                swapped_players_rooms[1] = searched_room
        for swapped_player_number, swapped_player in enumerate(swapped_players):
            other_swapped_player_number = 1 if swapped_player_number == 0 else 0
            swapped_players_rooms[swapped_player_number].occupants.remove(swapped_player.name)
            swapped_players_rooms[other_swapped_player_number].occupants.append(swapped_player.name)
            swapped_player.x = swapped_players_rooms[other_swapped_player_number].x
            swapped_player.y = swapped_players_rooms[other_swapped_player_number].y
            swapped_player.state = ["default", None]


def trap(usable, player, players=None, room=None, rooms=None):
    """Sets a trap in the room it's used in, steals two gold from each player who enters that room"""
    if player.human:
        print("Trap\n  A small bear trap that has been modified to house a small teleportation device and a gold"
              " magnet.")
    if check_if_used(usable, player):
        player.inventory.remove(trap)
        room.placed_items.append([trapped, player])
        if player.human:
            print("\nYou set down the trap in the room. Now the only thing for you to do is wait.")


def gold_potion(usable, player, players=None, room=None, rooms=None):
    """Put's three gold in a random nearby room"""
    if player.human:
        print("Gold Potion\n  A small golden potion. There is a label on the cork that warns that opening the potion"
              " will cause it to teleport.")
    if check_if_used(usable, player):
        player.inventory.remove(gold_potion)
        found_new_room = False
        while not found_new_room:  # Reminder to get rid of the need for this while loop later
            direction = r.choice(["NORTH", "EAST", "SOUTH", "WEST"])
            for possible_new_room in rooms:
                if possible_new_room.x == (room.x + v.Directions[direction].value[0]) and possible_new_room.y == (
                        room.y + v.Directions[direction].value[1]):
                    new_room = possible_new_room
                    found_new_room = True
                    break
        new_room.placed_items.append([potion_gold, player])
        if player.human:
            print("\nYou take the potion out of your pack and pop the cork. As soon as the cork leaves the bottle, you"
                  " find your hands empty. The bottle has done what it said it would and teleported somewhere else. You"
                  " do feel that it has stayed nearby.")


def dagger(usable, player, players=None, room=None, rooms=None):
    """Steal 4 gold from any player in the same room"""
    if player.human:
        print("Dagger\n  A sharp dagger. While you don't want to kill anyone, you sure could use this to extort some"
              " people.")
    if check_if_used(usable, player):
        if player.human:
            if len(room.occupants) > 1:  # AI players will make this check before using the item
                other_players_in_room = []
                for person in players:
                    if person.name in room.occupants:
                        other_players_in_room.append(person)
                other_players_in_room.remove(player)
                for player_in_room in other_players_in_room:
                    player_in_room.gold -= 4
                player.gold += 4 * len(other_players_in_room)
                for player_number in range(len(other_players_in_room)):
                    # Changes data from the Player class to the string of their names because when coding this
                    # originally I forgot how my own data types worked and I can't be bothered to re-wright it right now
                    other_players_in_room[player_number] = other_players_in_room[player_number].name
                if len(other_players_in_room) == 1:
                    print(f"You pull out your dagger and point it at {other_players_in_room[0]} and you tell them that"
                          f" if they don't give you 4 gold, you are going to stab them. They quickly scrounge around in"
                          f" their pockets and then hand over 4 gold. You put the gold in your pockets and then put"
                          f" your dagger away.")
                else:
                    print(f"You pull out your dagger and wave it at {', '.join(other_players_in_room[:-1])}, and"
                          f" {other_players_in_room[-1]}. You tell them that anyone who does not hand over 4 gold is"
                          f" going to be stabbed. All of them quickly search through there pockets and toss the 4 gold"
                          f" in your direction. You grab all of the gold off the floor while still holding out your"
                          f" dagger, and only once all of the gold is safely in your pockets do you put away the"
                          f" dagger.")
            else:
                print("\nYou pull out your dagger, but realize that no one else is here.")


def nope_picture(usable, player, players=None, room=None, rooms=None):
    """Lets the player who activated it move to a room without activating that room"""
    if player.human:
        print("Nope Picture\n  It is a small picture of a man with a very long neck and a solid looking yellow hat. You"
              " get the feeling that this picture will guarantee safe travel.")
    if check_if_used(usable, player):
        player.inventory.remove(nope_picture)
        player.state = ["nope", None]
        if player.human:
            print("You take the odd picture from your bag. You know in your heart that it will keep you safe, but your"
                  " not quite sure how to use it. You decide that your best option is to close your eyes and consult"
                  " your spirit animal. As you close your eyes and concentrate, suddenly, a spirit appears before you."
                  " The spirit is not your spirit animal, instead appearing to be a large man from a cold land. He is"
                  " wearing a knit cap and large mittens with a snowflake sewn on them. You ask for his advice on the"
                  " matter, and he simply says one word.\n'Pootis'\nWith that word, you are pulled from you trance and"
                  " it all clicks and you know what you must do. You lick your thumb, smush your thumb on your"
                  " forehead, and stick the image to your head. It sticks just as you knew it would. You don't think it"
                  " will stick past the next room, but you feel confidant in traveling onward.")


def compass(usable, player, players=None, room=None, rooms=None):
    """Says the difference in location between the player and the goal"""
    direction_names = ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"]
    if player.human:
        print("Compass\n  A simple compass. On the back is a label stating that it points to what one desires most.")
    if check_if_used(usable, player):
        # Makes the compass not perfect in line with the lore of it pointing to what you desire most
        target_room = rooms[-1] if r.randint(0, len(rooms)) != 0 else r.choice(rooms)
        x_distance = target_room.x - room.x
        y_distance = target_room.y - room.y
        x_sign = m.copysign(1, x_distance)
        y_sign = m.copysign(1, y_distance)
        supplemental_angle = 0  # Corrects the angle calculation to allow for a full 360 degrees
        if x_distance < 0:
            supplemental_angle += 180
        if x_sign != y_sign:
            supplemental_angle += 90
        current_room_to_goal_angle = m.degrees(m.atan(abs(x_distance) / abs(y_distance))) + supplemental_angle
        current_room_to_goal_angle_compass_name = direction_names[(round(round(current_room_to_goal_angle) / 45)) % 8]
        if player.human:
            # Add art of the compass pointing that direction later
            print("\nYou pull out your compass, making sure that all you desire is to find the room with the object in"
                  " it. After focusing on your 'desire' for what feels long enough you take a look at where it is"
                  f" pointing. The compass points to the {current_room_to_goal_angle_compass_name}. Satisfied, you put"
                  " the compass back in you pack for now.")


def pet_goblin(usable, player, players=None, room=None, rooms=None):
    """Moves around the maze and steals a gold from each player who enters a room he is in"""
    if player.human:
        print("Pet Goblin\n  A small tame goblin. It has told you that it will seek out gold for you.")
    if check_if_used(usable, player):
        player.inventory.remove(pet_goblin)
        room.placed_items.append([encountered_goblin, player])
        if player.human:
            print("\nYou take the small goblin out of your pack and set it softly on the ground. It quickly turns"
                  " around, gives you a salute, and then wildly scampers off into some decrepit corner of the room so"
                  " that you can no longer see it. You hope this was worth it.")
