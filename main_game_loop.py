from time import sleep, time
import random as r

import global_vars as v
import room_styles as rm
import items as i

v.init()  # Creates all the global variables for all the files to use


def assign_rooms(maze_layout: list, special_rooms: list, good_room_count: int, bad_room_count: int, shop_count: int):
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


def generate_maze_layout(room_count: int) -> list:
    """Creates an entity, called room_crawler, which is randomly shifted north, east, south, and west. Each time this
    entity moves, it first adds a path from the room at its old location to its new one if it does not already exist.
    This allows the dynamic creation of oneway paths. After it moves, it checks if there is a room in its new location,
    and if there is not adds an empty room to that location. It starts by adding the start room at (0, 0) and once it
    has added the number of rooms stored in the room_count variable, it continues to move till it has found an empty
    spot once more and then creates the goal room at that spot. This guarantees the goal room will have only one
    entrance."""
    generated_rooms = []
    room_crawler = [0, 0]
    generated_rooms.append(v.Room(rm.start, room_crawler[0], room_crawler[1]))

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
            generated_rooms.append(v.Room(rm.empty if room_count != 0 else rm.goal, room_crawler[0], room_crawler[1]))
            room_count -= 1
    if __name__ == "__main__":  # Prevents excess printing when testing
        print("\nRoom layout generated...")
    return generated_rooms


def generate_players(human_players: int, total_players: int, starter_gold: int) -> list:
    generated_players = []
    for player in range(total_players):
        if human_players > 0:
            generated_players.append(
                v.Player(True, input(f"\nPlayer {player + 1}, what would you like to name your character?\n"),
                       starter_gold))
            human_players -= 1
        else:
            generated_players.append(v.Player(False, r.choice(NPC_NAME_LIST), starter_gold))
    return generated_players


if __name__ == "__main__":  # Allows for testing of this file's functions, also just good practice
    try:
        file = open("npc_names.txt", "r")
    except FileNotFoundError:  # Allows this code to be run complied
        file = open("_internal\\npc_names.txt", "r")
    NPC_NAME_LIST = file.read().split('\n')  # Stolen from StackOverflow
    file.close()

    print("Welcome to:\n\nMAZE GAME")  # Replace with splash art
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

    # Removes special rooms if adding all enabled special rooms would make too many rooms not empty
    try:
        enabled_special_rooms = r.sample(enabled_special_rooms,
                                         int((total_rooms / 2) - (good_rooms + bad_rooms + shops)))
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
    rooms = generate_maze_layout(total_rooms)
    assign_rooms(rooms, enabled_special_rooms, good_rooms, bad_rooms, shops)
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
            if type(player.state[0]) is not str:  # Activates stuck spots
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
