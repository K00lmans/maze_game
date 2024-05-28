"""The names and logic for each room style.

Guide for adding new room styles:

1: All styles take a Player class of the player who entered the room, the Room class of the room they entered, the list
of rooms, and the list of players.

2: You must add the new room style to the corresponding style category list in the variable file.

3: All displayed text should only be displayed if the player is a person to prevent confusion.

4: All rooms must include a call to put_player_in_room() to prevent issues.

5: If you make a room that does not transport the player somewhere else, make sure to call display_players_in_room() for
human players

6: If an AI makes a decision in a room that relates to a human player, print a short summary of what happened.

7: Keep in mind that special rooms appear only once.

8: Keep in mind when naming the room style that it will be shown to the user in the style of 'the [room style name]
room' for special rooms or 'a(n) [room style name] room' for other room category's.

9: If you add a room style that relates to a special room style, make sure that it's removed if that special room style
is disabled.

10: If you add a 'stuck spot' make sure to include the code for getting out of that spot in a separate function named
the same as the name for its state in the helper function section. Those functions must take in a Player class of the
player.

11: If you want to remove room styles, do not remove them from here, simply remove them from the category list in the
variable file."""

import random as r

import global_vars as v
import items as i


# Helper Functions
def display_players_in_room(room_info, player_name=None):
    room_occupants = room_info.occupants.copy()
    if player_name is None:  # If no name is inputted, it is assumed the newest player in the room is the players name
        room_occupants = room_occupants[:-1]
    else:
        room_occupants.remove(player_name)
    if len(room_occupants) == 0:
        print("\nNobody else is here.")
    elif len(room_occupants) == 1:
        print(f"\nYou see that {room_occupants[0]} is also here.")
    else:
        print(f"\nYou see that {', '.join(room_occupants[:-1])}, and {room_occupants[-1]} are also here.")


def generate_room_based_rng_number(rooms: list) -> int:
    """Generates a large number based on the number of rooms for use in rng. On average, each room increases the number
    by 55. Use this number only in combination with generate_room_rng_number and for Easter egg levels of rarity.

    This function works by finding the height and width of the whole maze, then finding the number of digits for each
    value. The digit count of the height and width is then added together to get the digit count of the final rng
    number. Finally, it creates the max number possible for that many digits and returns it as the rng number."""
    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0
    for room in rooms:
        if room.x > max_x:
            max_x = room.x
        elif room.x < min_x:
            min_x = room.x
        elif room.y > max_y:
            max_y = room.y
        elif room.y < min_y:
            min_y = room.y
    x_width = max_x - min_x
    y_height = max_y - min_y
    # This numbers length is the length of if you added the x and y numbers length together
    rng_number_length = len(str(x_width)) + len(str(y_height))
    rng_number = 0
    for _ in range(rng_number_length):
        rng_number *= 10  # Adds a zero at the end
        rng_number += 9
    return rng_number


def generate_room_rng_number(room_data: v.Room) -> int:
    """Generates a number for use with the generate_room_based_rng_number function. The number is the absolute value of
    the x and y coordinates of the room stuck together, i.e. (12, -33) would become 1233."""
    str_x_y = [str(abs(room_data.x)), str(abs(room_data.y))]
    rng_number = int("".join(str_x_y))
    return rng_number


def put_player_in_room(player: v.Player, entered_room: v.Room, rooms: list):
    for room in rooms:
        if player.name in room.occupants:
            room.occupants.remove(player.name)
            break
    entered_room.occupants.append(player.name)


def in_pit(player_profile: v.Player):
    if r.randint(1, 4 + player_profile.difficulty) == 1:
        player_profile.state[1] = True
    if player_profile.human:
        if player_profile.state[1]:
            print("\nYou attempt to climb the walls of the pit. You gain a little bit of height with each movement"
                  " until, suddenly, your at the top.\nYou have escaped from the pit!")
        else:
            print("\nYou attempt to climb the walls of the pit. Despite your best efforts, no matter what you do you"
                  " just fall back down.")
    if player_profile.state[1]:
        player_profile.state = ["default", None]


def in_combat(player_profile: v.Player):
    player_profile.state[1][0] -= r.randint(1, player_profile.state[1][1])
    if player_profile.human:
        if player_profile.state[1][0] <= 0:
            print("\nAfter a long battle, you finally have defeated the monster. The gates around you fall and you can"
                  " now continue your journey.")
        else:
            print("\nYou strike the monster with all your might but it does not fall.")
    if player_profile.state[1][0] <= 0:
        player_profile.state = ["default", None]


# Required room styles
def start(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Where players start, gives you a coin when you return"""
    put_player_in_room(player_profile, room_info, rooms)
    player_profile.gold += 1
    if player_profile.human:
        print("\nYou enter the room and see a large open hole where the ceiling should be. The room seems familiar to"
              " you.\nAs your looking up you suddenly see a coin fall from the opening.\n+1 gold!")
        display_players_in_room(room_info)


def empty(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """A filler room for generation and to reduce landmarks"""
    put_player_in_room(player_profile, room_info, rooms)
    if player_profile.human:
        # An example of the room based rng number being used. All usage should reflect this example
        if generate_room_rng_number(room_info) == r.randint(0, generate_room_based_rng_number(rooms)):
            print("\nYou enter a large empty room. Your gaze is pulled upward and instead of seeing the ceiling that"
                  " you would have expected, you see right through the roof. Behind the wall is a giant being shrouded"
                  " in mist. Though shrouded, you can still make out four long, thin appendages, one coming from each"
                  " corner of the room. While you can't see where those appendages connect to, you can see what appears"
                  " to be a face through the fog, and its staring directly at you. Despite being understanding very"
                  " clearly that it is some kind of face, it is entirely unrecognizable as a face. The entirety of what"
                  " could be called its face is covered in number pairs, all of them constantly shifting and changing"
                  " in a seemingly random pattern. You find yourself unable to tear your gaze away from the beast. You"
                  " start to feel fuzzy and your vision slowly narrows. You collapse.\n\nWhen you wake, the room just"
                  " seems like normal. You feel misplaced.")
        else:
            print("\nYou enter a large empty room. You feel lost.")
        display_players_in_room(room_info)


def goal(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Getting here first wins for that player"""
    player_profile.state = ["winner", None]
    if player_profile.human:
        print("\nAt long last you have found it! *INSERT FOUND ITEM LATER*\nA WINNER IS YOU")  # Still need joke object


def shop(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """A place to buy items"""
    put_player_in_room(player_profile, room_info, rooms)
    shop_selection = r.sample(v.ITEMS, r.randint(3, len(v.ITEMS) - (1 + player_profile.difficulty)))
    if player_profile.human:  # Still needs way for AI to buy stuff
        print("\nYou enter the room and see that a small storefront has been set up.")
        display_players_in_room(room_info)
        print("\nAs you walk up to the shopkeeper, he hands you a small piece of paper that lists all of the items he"
              f" has in stock and tells you that all items cost {len(players)//(2 - player_profile.difficulty)} gold."
              f" The shopkeep tells you he will is more than willing to show you any items you are interested in.")
        if player_profile.gold >= (len(players)//(2 - player_profile.difficulty)):
            print("You decide to take a look at what he has.\n")
            in_shop = True
            while in_shop:
                for item_number, item in enumerate(shop_selection):
                    print(f"{item_number + 1}: {item.__name__.replace('_', ' ').capitalize()}")
                print(f"{len(shop_selection) + 1}: Done browsing")
                try:
                    selection = int(input())
                    if 1 <= selection <= len(shop_selection):
                        shop_selection[selection - 1](False, player_profile)
                        selection_options = ["y", "n"]
                        purchase = None
                        while purchase not in selection_options:
                            purchase = input("Would you like to buy this item? (Y/N)\n").lower()
                        if purchase == "y":
                            player_profile.inventory.append(shop_selection[selection - 1])
                            player_profile.gold -= len(players)//(2 - player_profile.difficulty)
                            print(f"\nYou hand over the gold and the shopkeep hands you the"
                                  f" {shop_selection[selection - 1].__name__}. You put it in your pack for safe"
                                  " keeping.")
                            if player_profile.gold < (len(players)//(2 - player_profile.difficulty)):
                                in_shop = False
                                print("As you put your new purchase in your pack, you realize that you no longer have"
                                      " enough gold to make another purchase. You thank the shopkeep, hand back the"
                                      " stock paper, and prepare to head out once more.")
                    else:
                        in_shop = False
                        print("\nYou thank the shopkeep for his time and hand back the stock paper and prepare to head"
                              " on your way once more.")
                except ValueError:
                    print("Enter only the number of the item\n")
        else:
            print("You thank the shopkeep for the offer but you don't have enough gold to buy anything. You then"
                  " prepare to head on your way.")


# Special room styles
def pit(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """A 'stuck spot' that needs a high roll to leave"""
    put_player_in_room(player_profile, room_info, rooms)
    if player_profile.human:
        if player_profile.state[0] != in_pit:
            print("\nYou enter a large empty room. Before you can start feeling lost, the floor falls out from"
                  " underneath you and you fall into a large pit.")
        print("\nYou are in a large empty pit with steep walls. Scattered around you seems to be parts for what appears"
              " to be a communication device of some kinda as well as several orange, yellow, and black candies.")
        display_players_in_room(room_info)
    if player_profile.state[0] != in_pit:
        player_profile.state = [in_pit, False]  # The state data indicates if the player can leave the pit


def combat(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """A 'stuck spot' that needs multiple rolls to leave"""
    put_player_in_room(player_profile, room_info, rooms)
    if player_profile.human:
        if player_profile.state[0] != in_combat:
            print("\nBefore you can take in anything about the room, a cage pops up around you and a monster is lifted"
                  " into the now arena. You get the feeling your going to have to fight this thing to escape.\nWhile"
                  " the monster was being lifted into the cage you got a chance to look around.")
        else:
            print("\nYou are in combat with a terrible beast!\nDuring a brief lull in the combat you manage to get a"
                  " look outside your cage.")
        display_players_in_room(room_info)
    if player_profile.state[0] != in_combat:
        # Min health is min hits plus one to prevent insta-kills
        enemy_health = r.randint(3 + player_profile.difficulty, 10*(2 + player_profile.difficulty))
        # The state data indicates the enemy's health and the max damage the player can do per turn
        player_profile.state = [in_combat, [enemy_health, (enemy_health//(2 + player_profile.difficulty)) + 1]]


def swapper_control(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Lets them swap any two players"""
    put_player_in_room(player_profile, room_info, rooms)
    selected_players = []
    if player_profile.human:
        print("\nYou enter the room and see a large table filled with levers, buttons, dials, switches, and other input"
              " devices. A sign above the table says 'Swapper Control Panel'. You realize you can use this machine to"
              " swap any two other players. However before you do that you decide to take a look around the room.")
        display_players_in_room(room_info)
        print("\nNow that you have observed the room you decide to take your pick of who to swap.\n")
        for player_number, player in enumerate(players):
            print(f"{player_number + 1}: {player.name}")
        players_selected = False
        while not players_selected:
            try:
                first_player = int(input("Select the first player to swap: ")) - 1
                second_player = int(input("Select the second player to swap: ")) - 1
                selected_players.append(players[first_player])
                selected_players.append(players[second_player])
                players_selected = True
            except ValueError:
                print("Enter the number next to the player you want to select")
            except IndexError:
                print("One of your player numbers does not exist")
        print(f"\nAfter everything is set up, you push the big red button and swap {selected_players[0].name} and"
              f" {selected_players[1].name}.")
    else:
        selected_players = r.sample(players, 2)
        if selected_players[0].human or selected_players[1].human:
            print(f"\n{player_profile.name} has swapped the locations of {selected_players[0].name} and"
                  f" {selected_players[1].name}.")

    swapped_players_rooms = [None, None]
    for searched_room in rooms:
        if selected_players[0].name in searched_room.occupants:
            swapped_players_rooms[0] = searched_room
        if selected_players[1].name in searched_room.occupants:
            swapped_players_rooms[1] = searched_room
    for swapped_player_number, swapped_player in enumerate(selected_players):
        other_swapped_player_number = 1 if swapped_player_number == 0 else 0
        swapped_players_rooms[swapped_player_number].occupants.remove(swapped_player.name)
        swapped_players_rooms[other_swapped_player_number].occupants.append(swapped_player.name)
        if swapped_players_rooms[other_swapped_player_number] not in swapped_player.visited_rooms:
            swapped_player.visited_rooms.append(swapped_players_rooms[other_swapped_player_number])
        swapped_player.x = swapped_players_rooms[other_swapped_player_number].x
        swapped_player.y = swapped_players_rooms[other_swapped_player_number].y
        swapped_player.state = ["default", None]


def psycho(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Houses a random crazy person to listen too"""
    put_player_in_room(player_profile, room_info, rooms)
    # I love inside jokes
    crazy_people = ["'...then the random walk...'\n'...then the loop through...'\n'...then the random walk...'\nYou"
                    " notice that they are scrawling 1's and 0's on the wall.",
                    "'no... you are the awake me...'\n'...and then the python was a mounty!'\n'of course the world is"
                    " flat, how else would it fit on the elephants and the turtle?'\nYou notice they have scrawled some"
                    " form of art using only the characters from a printing press on the wall.",
                    "'oh no, you rolled a 3, you don't get to leave the pit'\n'and that's heads for the 50th time in a"
                    " row'\n'oh no, this d20 needs to go to dice jail...'\nYou notice they are surrounded by piles and"
                    " piles of dice",
                    "'...yjrm yjr tsmfpz esal...'\n'...yjrm yjr appq yjtpihj...'\n'...yjrm yjr tsmfpz esal...'\nYou"
                    " notice that they are scrawling 2's and 1's on the wall.",
                    "'mp... upi str yjr seslr zr...'\n'...smf yjrm yjr quyjpm esd s zpimyu!'\n'pg vpitdr yjr eptaf od"
                    " gasy, jpe radr epiaf oy goy pm yjr rarqjsmyd smf yjr yityar?'\nYou notice they have scrawled some"
                    " form of art using only the characters from a printing press on the wall."]
    if player_profile.human:
        if generate_room_rng_number(room_info) == r.randint(0, generate_room_based_rng_number(rooms)):
            # Wanted to use AI for this because I thought it would be funny, but the AI writing was really bad
            print("\nYou enter the room and see a small pill on a pedestal. As you walk up to it, you feel compelled to"
                  " take it. Before you can even think, you have swallowed the pill. You suddenly feel,\n djogyrf?"
                  " *INSERT CODED DESCRIPTION OF DRUG TRIP HERE*. Rbrmyisaau upi nasvl piy. \n\nWhen you come to,"
                  " everything feels as if it has slid back into place. You groggily get to your feet and try once more"
                  " to continue on.")
        else:
            print("\n You enter the room and see a person chained to the wall murmuring something to themselves. As you"
                  f" get closer you hear what they are saying:\n{r.choice(crazy_people)}")
        display_players_in_room(room_info)


def wise_old_man(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Houses an old man who tries to give advice"""
    put_player_in_room(player_profile, room_info, rooms)
    # Make sure that there is never more joke wisdoms than there is real wisdoms
    # Joke to real ratio: 2/5
    old_man_wisdoms = ["'The best way to not get lost is to make your own map.'",
                       "'My child, have you tried crossing the streams?'",
                       "'It's dangerous to go alone! Take this.'\n The old man does not give you anything, but you feel"
                       " sharper",
                       "'The shop holds the means to progress'",
                       "'The last path is often the best'",
                       "'There is no shame in taking the path of less resistance in the name of fun'",
                       "'While the items sold in the shop are powerful, they are all flawed'"]
    if player_profile.human:
        print(
            "\nYou enter the room and see an old man sitting in the middle of it with a sign around his neck that says"
            " 'Free Wisdom'.\nAs you finish reading the sign, he turns to face you and says:\n"
            f"{r.choice(old_man_wisdoms)}")
        display_players_in_room(room_info)


# Good room styles
def small_treasure(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Gives 2-ish gold"""
    put_player_in_room(player_profile, room_info, rooms)
    player_profile.gold += 2 - player_profile.difficulty
    if player_profile.human:
        print("\nYou enter the room and see a large treasure chest overflowing with golden coins. On top of the chest"
              f" is a sign that says 'Please take only {2 - player_profile.difficulty}'. Since your a good person you"
              f" do as the sign says.\n+{2 - player_profile.difficulty} Gold!")
        display_players_in_room(room_info)


def large_treasure(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Gives 3-ish Gold"""
    put_player_in_room(player_profile, room_info, rooms)
    player_profile.gold += 3 - player_profile.difficulty
    if player_profile.human:
        print("\nYou enter the room and see a large pile of golden coins siting in the middle of the room. In front of"
              f" the pile is a sign saying 'Please take only {3 - player_profile.difficulty}'. Since your a good person"
              f" you do as the sign says.\n+{3 - player_profile.difficulty} Gold!")
        display_players_in_room(room_info)


def huge_treasure(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Gives 5-ish Gold"""
    put_player_in_room(player_profile, room_info, rooms)
    player_profile.gold += 5 - player_profile.difficulty
    if player_profile.human:
        print("\nYou enter the room and are overwhelmed by the sheer number of coins that have been crammed into the"
              " room. Once you come to your senses you see a small sign floating near the coins that says 'Please only"
              f" take {5 - player_profile.difficulty}'. Since your a good person you do as the sign says.\n+"
              f"{5 - player_profile.difficulty} Gold!")
        display_players_in_room(room_info)


def gold_machine(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Doubles gold"""
    put_player_in_room(player_profile, room_info, rooms)
    player_profile.gold *= 2
    if player_profile.human:
        if player_profile.gold > 0:
            print("\nAs you enter the room you see a small machine in the corner advertising to double your gold. You"
                  " decide to take the machine up on it's offer and you put in all your gold. After a few moments it"
                  " really does spit out double the gold. You pocket it all and walk away quite satisfied.\nGold now"
                  f" {player_profile.gold}!")
        elif player_profile.gold == 0:
            print("\nAs you enter the room you see a small machine in the corner advertising to double your gold. You"
                  " are filled with an immense feeling of sorrow due to your poverty. You give one last look at the"
                  " machine as you move on.")
        else:
            print("\nAs you enter the room you see a small machine in the corner advertising to double your gold."
                  " Hoping that it does not understand the concept of negative numbers you try hastily to put your debt"
                  " papers into the machine. After a few moments it spits out another piece of paper and you have the"
                  " dawning realization that it has just doubled your debt. You walk away slowly, trying to hold"
                  f" yourself together.\nDebt now {-player_profile.gold}!")
        display_players_in_room(room_info)


def match_machine(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Gives match"""
    put_player_in_room(player_profile, room_info, rooms)
    player_profile.inventory.append(i.match)
    if player_profile.human:
        print("\nYou enter the room and see a small machine sitting against the wall. As you get close to the machine"
              " you realize that it is full of matches. As you try to figure out how to get at one of the matches, a"
              " single match is pushed thought what you had thought was a glass pane. You pick it up and put it in your"
              " pack.\nAcquired match!")
        display_players_in_room(room_info)


def pit_lever(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Sends another player to the pit"""
    put_player_in_room(player_profile, room_info, rooms)
    if player_profile.human:
        if r.randint(0, 2 - player_profile.difficulty) != 0:  # Can fail to prevent suffering
            print("\nYou enter the room and notice that along one of the walls is a large row of levers, each with a"
                  " painting above them. You realize that each painting is of one of your fellow explorers (including"
                  " you) and that pulling a lever will send that person to the pit. You decide to take a further look"
                  " around before you pick a lever.")
            display_players_in_room(room_info)
            print("After your look round, you decide to pick the unfortunate soul to send to the pit.\n")
            for player_number, player in enumerate(players):
                print(f"{player_number + 1}: {player.name}")
            player_selected = False
            while not player_selected:
                try:
                    selected_player = int(input()) - 1
                    selected_player = players[selected_player]  # Tests to make sure they selected a valid player
                    player_selected = True
                except ValueError:
                    print("Enter the number of the player you want to select")
                except IndexError:
                    print("Please select a valid player number")
            if player_profile is selected_player:  # Lets you do this because comedy and im lazy
                print("\nYou pull the lever. Your surprised to see nothing happen and feel quite proud of yourself."
                      " Then you blink. Now your in the pit. What did you expect?")
            else:
                print("\nYou pull the lever. You expect more to come out of it, but it remains silent.")
            lever_pulled = True
        else:
            print("\nYou enter the room and notice that along one of the walls is a large row of levers, each with a"
                  " paining above them. Something about the machine gives you a bad feeling, so you decide not to"
                  " mess with it.")
            display_players_in_room(room_info)
            lever_pulled = False
    else:
        if r.randint(1, 3 + player_profile.difficulty) != 1:  # Can fail to prevent suffering
            selected_player = r.choice(players)
            lever_pulled = True
            if selected_player.human:
                print(f"\n{player_profile.name} has sent {selected_player.name} to the pit.")
        else:
            lever_pulled = False

    if lever_pulled:
        for room in rooms:
            if selected_player.name in room.occupants:
                room.occupants.remove(selected_player.name)
                break
        for room in rooms:
            if room.style == pit:
                pit_room = room
                break
        selected_player.x = pit_room.x
        selected_player.y = pit_room.y
        selected_player.state = [in_pit, False]
        if pit_room not in selected_player.visited_rooms:
            selected_player.visited_rooms.append(pit_room)
        pit_room.occupants.append(selected_player.name)


def gold_vacuum(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Steals gold from another player"""
    put_player_in_room(player_profile, room_info, rooms)
    if player_profile.human:
        print("\nYou enter the room and see a simple looking vacuum sitting in the middle of the room. As you get you"
              " get closer to the vacuum, you notice that the manuel is attached by a string to the vacuum. Before you"
              " read it, you decide to look around.")
        display_players_in_room(room_info)
        print("\nAfter having read the manuel, you understand that it is a trans-dimensional pocket vacuum, and that"
              " you can select any of your fellow explorers to have some gold stolen from there pockets. You ponder who"
              " to select.")
        for player_number, player in enumerate(players):
            print(f"{player_number + 1}: {player.name}")
        player_selected = False
        while not player_selected:
            try:
                selected_player = int(input()) - 1
                selected_player = players[selected_player]  # Tests to make sure they selected a valid player
                player_selected = True
            except ValueError:
                print("Enter the number of the player you want to select")
            except IndexError:
                print("Please select a valid player number")
        if player_profile is selected_player:  # Lets you do this because comedy and im lazy
            print("\nYou decide to try the vacuum on yourself. When you turn the vacuum on, you feel your pockets get a"
                  " little lighter as your coins come out of the back of the vacuum. You feel like you wasted your"
                  " time.")
        else:
            print("\nYou target the vacuum and turn it on. After a few moments, some gold pops out of the vacuum. Your"
                  " now a little richer.")
    else:
        selected_player = player_profile
        while selected_player != player_profile:
            selected_player = r.choice(players)
        if selected_player.human:
            print(f"{player_profile} has stolen some gold from {selected_player.name}.")

    coins_stolen = r.randint(1, len(players) - player_profile.difficulty)
    selected_player.gold -= coins_stolen
    player_profile.gold += coins_stolen


# Bad room styles
def teleport(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Teleports them to a random room"""
    put_player_in_room(player_profile, room_info, rooms)  # Prevents crashing
    room_info.occupants.remove(player_profile.name)
    new_room = r.choice(rooms[:-1])  # Prevents teleporting to the goal room and getting trapped
    player_profile.x = new_room.x
    player_profile.y = new_room.y
    if new_room not in player_profile.visited_rooms:
        player_profile.visited_rooms.append(new_room)
    new_room.occupants.append(player_profile.name)

    if player_profile.human:
        print("\nYou enter a large empty room. Before you can start feeling lost, you get an extremely strange"
              " sensation and the room around you seems different. You also have a strong desire to go on a trek where"
              " no one else has trek-ed before.")  # 🖖


def pit_slide(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Sends them to the pit"""
    put_player_in_room(player_profile, room_info, rooms)
    if r.randint(0, 2 - player_profile.difficulty) == 0:  # Can fail for sanity
        room_info.occupants.remove(player_profile.name)
        for room in rooms:
            if room.style == pit:
                pit_room = room
                break
        player_profile.x = pit_room.x
        player_profile.y = pit_room.y
        player_profile.state = [in_pit, False]
        if pit_room not in player_profile.visited_rooms:
            player_profile.visited_rooms.append(pit_room)
        pit_room.occupants.append(player_profile.name)
        used_slide = True
    else:
        used_slide = False

    if player_profile.human:
        if used_slide:
            print("\nYou enter the room and see a slide in it, how exciting! You jump into the slide and ride it along."
                  " You get to the end and feel quite elated! You then look around to see where you ended up and"
                  " realize your in the pit. Darn.")
        else:
            print("\nYou enter the room and see a slide in it. You are about to go over and use it when you get an"
                  " extremely bad feeling about it and you decide otherwise.")
            display_players_in_room(room_info)


def swapper(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Swaps them with another player"""
    put_player_in_room(player_profile, room_info, rooms)  # Should prevent odd crashing issue
    swapped_player = r.choice(players)
    if swapped_player != player_profile:
        room_info.occupants.remove(player_profile.name)
        for room in rooms:
            if swapped_player.name in room.occupants:
                room.occupants.remove(swapped_player.name)
                new_room = room
                break
        new_room.occupants.append(player_profile.name)
        player_profile.x, player_profile.y = new_room.x, new_room.y
        if new_room not in player_profile.visited_rooms:
            player_profile.visited_rooms.append(new_room)
        room_info.occupants.append(swapped_player.name)
        swapped_player.x, swapped_player.y = room_info.x, room_info.y
        if room_info not in swapped_player.visited_rooms:
            swapped_player.visited_rooms.append(room_info)
        swapped_player.state = ["default", None]  # Prevents stuck spot from carrying over

    if player_profile.human:
        print("\nYou enter a large empty room. Before you can start feeling lost you feel a large surge of energy flow"
              " through you and find yourself in an abstract room of blue.")
        if swapped_player == player_profile:
            print("As you take a look around, the deep blue color of the void room turns a violent red and starts to"
                  " churn violently. All around you turns into the most violent lighting storm you have ever seen,"
                  " always shifting shape and flashing every shade of red imaginable. You are trapped in this realm of"
                  " chaos for what seems like an eternity, when suddenly the room returns to the deep blue and all"
                  " calms itself. Before you can react to the change in your surroundings you find yourself back in the"
                  " empty room.")
        else:
            print(f"As you look around you also see {swapped_player.name}. They seem even more confused than you. You"
                  f" are about to call out to them when suddenly your back in a room. Despite your disorientation, you"
                  f" realize that this is not the same room you entered.")
    else:
        if swapped_player.human:
            print(f"\n{player_profile.name} has swapped places with {swapped_player.name}")


def magnet(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Sets gold to 0"""
    put_player_in_room(player_profile, room_info, rooms)
    if player_profile.human:
        if player_profile.gold > 0:
            print("\nYou enter the room and notice that attached to the ceiling is a large magnet. Suddenly you hear a"
                  " loud whirring sound as the magnet turns on. In a sudden panic you realize it is sucking your coins"
                  " away from you. Despite your best efforts you can not stop it from stealing all your coins.\nGold"
                  " now 0!")
        elif player_profile.gold == 0:
            print("\nYou enter the room and notice that attached to the ceiling is a large magnet. Suddenly you hear a"
                  " loud whirring sound as the magnet turns on. Since nothing else seems to happen, you take a moment"
                  " to look at the magent further. You notice it is covered in coins and realize that this room was"
                  " supposed to steal your gold. As you leave you take a moment to think about how gold is supposed to"
                  " stick to a magnet.")
        else:
            print("\nYou enter the room and notice that attached to the ceiling is a large magnet. Suddenly you hear a"
                  " loud whirring sound as the magnet turns on. Suddenly you see your debt papers whip out and get"
                  " stuck onto the magnet. At first you are confused how a magnet attracts paper, but quickly push"
                  " that thought out of your mind as you enjoy the fact that you are now debt free.\nDebt now 0!")
        display_players_in_room(room_info)
    player_profile.gold = 0


def recall(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Sends them to the home square"""
    put_player_in_room(player_profile, room_info, rooms)
    if r.randint(0, 2 - player_profile.difficulty) == 0:  # Can fail for sanity
        room_info.occupants.remove(player_profile.name)
        rooms[0].occupants.append(player_profile.name)
        player_profile.x, player_profile.y = 0, 0  # Room generation always starts at 0, 0 with the home room
        sent_home = True
    else:
        sent_home = False
    if player_profile.human:
        if sent_home:
            if generate_room_rng_number(room_info) == r.randint(0, generate_room_based_rng_number(rooms)):
                players.remove(player_profile)
                rooms[0].occupants.remove(player_profile.name)
                print("\nYou enter a large empty room. You then realize that this room has a hole in it. You did not"
                      " think you where near your start location. As you are trying to work out where you got turned"
                      " around, you slowly get filled with a desire to return to your home. What are you doing here?"
                      " Putting your neck on the line just to find some silly trinket for the king? You stop thinking"
                      " about where you are and where you where and decide that all you really want to do is go"
                      " home. As you begin to start thinking about how to get out, you realize that there is a ladder"
                      " leading out the hole. You were sure that ladder was not there just a moment ago, but you don't"
                      " care anymore. Your going home. You climb the ladder and begin the trek home, vowing to never"
                      " think of the preceding events ever again.")
            else:
                print("\nYou enter a large empty room. Wait, never mind it has a hole in the roof.\nDid it always have"
                      " a hole in the roof?")
        else:
            print("\nYou enter a large empty room. It reminds you of home.")
            display_players_in_room(room_info)


def charity(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Gives 1 of the players gold to each other player plus 1 gold for the charity"""
    put_player_in_room(player_profile, room_info, rooms)
    # Takes an extra gold from the player, and then gives it right back because im lazy
    player_profile.gold -= len(players) + 1
    for player in players:
        player.gold += 1
    if player_profile.human:
        print("\nYou enter the room and see that there has been a tent sent up in the middle of the room. When you walk"
              " to the font of the tent you see that they are a charity service. You are surprised to realize that"
              " there is nobody behind the tent and that instead is simply a jar that leads into a tube labeled"
              f" 'Donations'. Despite how odd this situation is, you feel compelled to donate and put {len(players)}"
              " gold in the tin. The bottem of the jar opens and you watch the coins fall into the tube and go off to"
              " wherever this charity sends its money. You feel cheated for some reason.")
        display_players_in_room(room_info)
    else:
        print(f"\n{player_profile.name} has given to the charity!")


def pickpocket(room_info: v.Room, player_profile: v.Player, rooms: list, players: list):
    """Lose 1 random item"""
    put_player_in_room(player_profile, room_info, rooms)
    if player_profile.human:
        if len(player_profile.inventory) > 0:
            print("\nYou enter a large empty room with a man standing in the center holding a sign that says 'Free"
                  " Hugs!'. You of course decide to give the man a hug. After the hug is over, he tips his fedora to"
                  " you and runs out of the room. All though strange, you don't think much of it, though you do feel"
                  " lighter.")
        else:
            print("\nYou enter a large empty room with a man standing in the center holding a sign that says 'Free"
                  " Hugs!'. You of course decide to give the man a hug. After the hug is over, the man looks at you"
                  " with disdain, spits at you and runs out of the room. All though strange, you don't think much of"
                  " it.")
        display_players_in_room(room_info)
    if len(player_profile.inventory) > 0:
        player_profile.inventory.remove(r.choice(player_profile.inventory))
