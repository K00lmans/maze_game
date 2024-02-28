from time import sleep, time
import random as r

import global_vars as v
import room_styles as rm
import items as i

v.init()  # Creates all the global variables for all the files to use


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
        if player.gold >= 0:
            print(f"\nYou check your pockets and find you have {self.gold} gold coins.")
        else:
            print(f"\nYou check your pockets and find a paper saying you are {-self.gold} gold"
                  f" coins in debt.")
        if len(player.inventory) == 0:
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


class Room:
    def __init__(self, room_style: callable, x: int, y: int):
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


def assign_rooms(maze_layout, special_rooms, good_room_count, bad_room_count, shop_count):
    if __name__ == "__main__":  # Prevents excess printing when testing
        print("\nAssigning room styles...")

    for count, room_style in enumerate(special_rooms):
        chosen_room = r.choice(maze_layout)
        while chosen_room.style != rm.empty:
            chosen_room = r.choice(maze_layout)
        chosen_room.style = room_style

    while good_room_count != 0:
        chosen_room = r.choice(maze_layout)
        if chosen_room.style == rm.empty:
            chosen_room.style = r.choice(v.GOOD_ROOMS)
            good_room_count -= 1

    while bad_room_count != 0:
        chosen_room = r.choice(maze_layout)
        if chosen_room.style == rm.empty:
            chosen_room.style = r.choice(v.BAD_ROOMS)
            bad_room_count -= 1

    while shop_count != 0:
        chosen_room = r.choice(maze_layout)
        if chosen_room.style == rm.empty:
            chosen_room.style = rm.shop
            shop_count -= 1

    return maze_layout


def generate_maze_layout(room_count: int) -> list:
    generated_rooms = []
    room_crawler = [0, 0]
    generated_rooms.append(Room(rm.start, room_crawler[0], room_crawler[1]))

    while room_count >= 0:

        direction = r.choice(["NORTH", "EAST", "SOUTH", "WEST"])
        for room in generated_rooms:  # Tries to add path to next room
            if room_crawler[0] == room.x and room_crawler[1] == room.y:
                if direction not in room.paths:
                    room.paths.append(direction)
                break

        room_crawler[0] += v.Directions[direction].value[0]
        room_crawler[1] += v.Directions[direction].value[1]

        new_room = True
        for room in generated_rooms:
            if room_crawler[0] == room.x and room_crawler[1] == room.y:
                new_room = False
                break
        if new_room:
            generated_rooms.append(Room(rm.empty if room_count != 0 else rm.goal, room_crawler[0], room_crawler[1]))
            room_count -= 1
    if __name__ == "__main__":  # Prevents excess printing when testing
        print("\nRoom layout generated...")
    return generated_rooms


def generate_players(human_players, total_players, starter_gold):
    generated_players = []
    for player in range(total_players):
        if human_players > 0:
            generated_players.append(
                Player(True, input(f"\nPlayer {player + 1}, what would you like to name your character?\n"),
                       starter_gold))
            human_players -= 1
        else:
            generated_players.append(Player(False, r.choice(NPC_NAME_LIST), starter_gold))
    return generated_players


if __name__ == "__main__":
    try:
        file = open("npc_names", "r")
    except FileNotFoundError:  # Allows this code to be run complied
        file = open("_internal\\npc_names", "r")
    NPC_NAME_LIST = file.read().split('\n')
    file.close()

    print("Welcome to:\n\nMAZE GAME")
    sleep(5)
    human_player_count = 0
    while human_player_count == 0 or human_player_count > 10:
        try:
            human_player_count = int(input("\nHow many players are there? (Max 10)\n"))
        except ValueError:
            print("Enter only a number")
    selection_options = ["y", "n"]
    customization_selection = None
    while customization_selection not in selection_options:
        customization_selection = input("\nWould you like to customize game settings? (Y/N)\n").lower()

    # Default game values
    total_player_count = 4 if (human_player_count % 5) != 0 else human_player_count
    starting_gold = total_player_count  # Compensates for charity room styles
    total_rooms = 50
    enabled_special_rooms = v.SPECIAL_ROOMS.copy()
    # Recommended ratios
    good_rooms = total_rooms // 8
    bad_rooms = total_rooms // 8
    shops = total_rooms // 9

    if customization_selection == "y":
        customizing_settings = True
        while customizing_settings:
            try:
                total_player_count = human_player_count + int(input(
                    f"\nHow many NPC's will join you?\n({0 if human_player_count >= 3 else 3 - human_player_count} - "
                    f"{10 - human_player_count})\n"))
                if not (3 <= total_player_count <= 10):
                    raise ValueError
                starting_gold = int(
                    input(f"\nHow much gold will each of you start with?\n(Default: {total_player_count})\n"))
                total_rooms = int(input("\nHow many rooms do you want this maze to have?\n(Default: 50)\n"))
                good_rooms = int(
                    input(f"\nHow many positive rooms do you want this maze to have?\n(Default: {total_rooms // 8})\n"))
                bad_rooms = int(
                    input(f"\nHow many negative rooms do you want this maze to have?\n(Default: {total_rooms // 8})\n"))
                shops = int(
                    input(f"\nHow many shop rooms do you want this maze to have?\n(Default: {total_rooms // 9})\n"))
                if (good_rooms + bad_rooms + shops) > (total_rooms / 2):
                    raise OverflowError
                modifying_special_rooms = True
                while modifying_special_rooms:
                    print(
                        "\nEnabled special rooms\n(Disabled rooms never show up but enabled ones are not guaranteed!)")
                    for special_room_count, special_room in enumerate(v.SPECIAL_ROOMS):
                        if special_room in enabled_special_rooms:
                            print(
                                f"{special_room_count}: "
                                f"{special_room.__name__.replace('_', ' ').capitalize()} room, Enabled!")
                        else:
                            print(
                                f"{special_room_count}: "
                                f"{special_room.__name__.replace('_', ' ').capitalize()} room, Disabled!")
                    selected_room = int(input(
                        f"Enter a rooms number to toggle it and {len(v.SPECIAL_ROOMS)} to submit room selection\n"))
                    if selected_room == len(v.SPECIAL_ROOMS):
                        modifying_special_rooms = False
                    else:
                        if v.SPECIAL_ROOMS[selected_room] in enabled_special_rooms:
                            enabled_special_rooms.remove(v.SPECIAL_ROOMS[selected_room])
                        else:
                            enabled_special_rooms.append(v.SPECIAL_ROOMS[selected_room])
                customizing_settings = False
            except ValueError:
                print("Inappropriate value")
            except OverflowError:
                print("Too many non-empty rooms")

    # Makes sure at least half of the rooms are empty
    try:
        enabled_special_rooms = r.sample(v.SPECIAL_ROOMS, int((total_rooms / 2) - (good_rooms + bad_rooms + shops)))
    except ValueError:
        pass
    # Removes rooms related to a special room if the special room is not enabled
    if rm.pit not in enabled_special_rooms:
        v.GOOD_ROOMS.remove(rm.pit_lever)
        v.BAD_ROOMS.remove(rm.pit_slide)

    players = generate_players(human_player_count, total_player_count, starting_gold)
    print("\nGenerating Maze...")
    if total_rooms > 1500:  # After about that many rooms, maze generation can really slow down
        print("(This may take a moment, but you should have expected that you maniac)")
    rooms = assign_rooms(generate_maze_layout(total_rooms), enabled_special_rooms, good_rooms, bad_rooms, shops)
    print("\nMaze generated! Your game will begin shortly.")

    sleep(1)

    game_start_time = time()
    print("\n\nIt was a direct order from the king. The first to find it would be showered in glory and gold. While you"
          " may have all been good friends before, this mandate changed things. You all headed out to the great"
          " underground maze and while the journey was peaceful, you knew that the second you all entered, all gloves"
          " would be off. After many days of traveling, you finally reach it. The only sign that there is even a vast"
          " underground maze here at all is the simple, yet perfectly square hole in the ground. You all hop in and the"
          " hunt begins.")
    for player in players:  # Puts all the players in the starting room
        rooms[0].occupants.append(player.name)
    winner = False
    while not winner:
        for player_number, player in enumerate(players):
            print(f"\nIt is player {player_number + 1}'s ({player.name}) turn!{'' if player.human else ' (AI)'}")
            for room in rooms:
                if player.x == room.x and player.y == room.y:
                    player_room = room
                    break
            if type(player.state[0]) is not str:
                player_room.entered(player, rooms, players)
                player.state[0](player)
                sleep(2.5)
            if player.state[0] == "default":  # Allows for players to move the turn they escape from stuck spots
                if player.human:
                    chosen_direction = False
                    while not chosen_direction:
                        print("\nYou decide you have spent enough time in this room, and survey the room to figure out"
                              " where you can go next.\n")
                        for direction_count, direction in enumerate(player_room.paths):
                            print(f"{direction_count + 1}: {direction}")
                        print(f"{len(player_room.paths) + 1}: Check inventory")
                        print(f"{len(player_room.paths) + 2}: Check who else is in the room")
                        selected_input = False
                        while not selected_input:
                            try:
                                player_selection = int(input())
                                selected_input = True
                            except ValueError:
                                print("Enter only a number for your selection")
                        if 0 < player_selection <= len(player_room.paths):
                            chosen_direction = player_room.paths[player_selection - 1]
                        elif player_selection == len(player_room.paths) + 1:
                            player.check_inventory(player_room, rooms, players)
                        else:
                            rm.display_players_in_room(player_room, player.name)
                            sleep(2.5)
                else:
                    chosen_direction = r.choice(player_room.paths)  # Add AI logic here

                player.x += v.Directions[chosen_direction].value[0]
                player.y += v.Directions[chosen_direction].value[1]
                for room in rooms:
                    if player.x == room.x and player.y == room.y:
                        if room not in player.visited_rooms:
                            player.visited_rooms.append(room)
                        if player.state[0] != "nope":
                            room.entered(player, rooms, players)
                        else:
                            rm.put_player_in_room(player, room, rooms)
                            player.state = ["default", None]
                            if player.human:
                                print("\nYou enter the room and care not for what is inside. You smile, and then"
                                      " realize the image has fallen off your head. You are sad, but you know that it"
                                      " was what that heavy man would have wanted.")
                        sleep(2.5)
                        break

                if player.state[0] == "winner":
                    winner = True
                    winning_player = player
                    time_taken = int(time() - game_start_time)
                    break
        for room in rooms:  # Moves any moving placed items
            for item in room.placed_items:
                if item == i.encountered_goblin:
                    i.move_goblin(rooms, room)

    time_taken_seconds = time_taken % 60
    time_taken_minutes = time_taken // 60
    time_taken_hours = time_taken_minutes // 60
    print(f"\n{winning_player.name} has won the game!\nThe game took {time_taken_hours} hours, {time_taken_minutes}"
          f" minutes, and {time_taken_seconds} seconds!\nDuring that time, they entered"
          f" {len(winning_player.visited_rooms)} rooms out of {len(rooms)} total!")
    sleep(10)
