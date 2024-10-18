import global_vars as v

v.init()  # Creates all the global variables for all the files to use


def generate_players(human_players: int, total_players: int, starter_gold: float) -> list:
    generated_players = []
    difficulty_modifiers = [-1, 0, 1]
    human_difficulties = []
    for player in range(total_players):
        if human_players > 0:
            player_name = input(f"\nPlayer {player + 1}, what would you like to name your character?\n")
            accepted_values = ["0", "1", "2"]
            answer = None
            while answer not in accepted_values:
                answer = input(f"Player {player + 1}, select your difficulty:\n0: Easy\n1: Normal\n2: Hard\n")
            chosen_difficulty = difficulty_modifiers[int(answer)]
            human_difficulties.append(chosen_difficulty)
            generated_players.append(v.Player(True, player_name, starter_gold, chosen_difficulty))
            human_players -= 1
        else:
            generated_players.append(v.Player(False, v.r.choice(NPC_NAME_LIST), starter_gold,
                                              -round(sum(human_difficulties) / len(human_difficulties))))
    return generated_players


if __name__ == "__main__":  # Allows for testing of this file's functions, also just good practice
    try:
        file = open("npc_names.txt", "r", encoding='utf-8')
    except FileNotFoundError:  # Allows this code to be run "complied"
        file = open("_internal\\npc_names.txt", "r", encoding='utf-8')
    NPC_NAME_LIST = file.read().split('\n')  # Stolen from StackOverflow
    file.close()

    print("Welcome to:\n\nMAZE GAME")  # Replace with splash art
    v.t.sleep(5)
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
    starting_gold = float(total_player_count)  # Compensates for charity room style
    total_rooms = 75
    enabled_special_rooms = list(v.ROOMS["special_rooms"].values())
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
                starting_gold = float(
                    input(f"\nHow much gold will each of you start with?\n(Default: {total_player_count})\n"))
                total_rooms = int(input("\nHow many rooms do you want this maze to have?\n(Default: 75)\n"))
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
                    for special_room_count, special_room in enumerate(list(v.ROOMS["special_rooms"].values())):
                        if special_room in enabled_special_rooms:
                            print(
                                f"{special_room_count}: "
                                f"{special_room.__name__.replace('_', ' ').capitalize()} room, Enabled!")
                        else:
                            print(
                                f"{special_room_count}: "
                                f"{special_room.__name__.replace('_', ' ').capitalize()} room, Disabled!")
                    selected_room = int(input(
                        f"Enter a rooms number to toggle it and {len(v.ROOMS['special_rooms'])} to submit room "
                        f"selection\n"))
                    if selected_room == len(v.ROOMS["special_rooms"]):
                        modifying_special_rooms = False
                    else:
                        if list(v.ROOMS["special_rooms"].values())[selected_room] in enabled_special_rooms:
                            enabled_special_rooms.remove(list(v.ROOMS["special_rooms"].values())[selected_room])
                        else:
                            enabled_special_rooms.append(list(v.ROOMS["special_rooms"].values())[selected_room])
                customizing_settings = False
            except ValueError:
                print("Inappropriate value")
            except OverflowError:
                print("Too many non-empty rooms")

    # Removes special rooms if adding all enabled special rooms would make too many rooms not empty
    try:
        enabled_special_rooms = v.r.sample(enabled_special_rooms,
                                           int((total_rooms / 2) - (good_rooms + bad_rooms + shops)))
    except ValueError:
        pass
    # Removes rooms related to a special room if the special room is not enabled
    if v.ROOMS["special_rooms"]["pit"] not in enabled_special_rooms:
        v.ROOMS["good_rooms"].pop("pit_lever")
        v.ROOMS["bad_rooms"].pop("pit_slide")

    players = generate_players(human_player_count, total_player_count, starting_gold)
    print("\nGenerating Maze...")
    rooms = v.MAZE_GENERATION["generate_maze_layout"](total_rooms)
    print("\nAssigning room styles...")
    v.MAZE_GENERATION["assign_rooms"](rooms, enabled_special_rooms, good_rooms, bad_rooms, shops)
    print("\nRefactoring room data...")
    v.MAZE_GENERATION["find_room_neighbors"](rooms)
    print("\nMaze generated! Your game will begin shortly.")
    v.ROOM_LIST = rooms

    v.t.sleep(1)

    game_start_time = v.t.time()
    print("\n\nIt was a direct order from the king. The first to find it would be showered in glory and gold. While you"
          " may have all been good friends before, this mandate changed things. You all headed out to the great"
          " underground maze and while the journey was peaceful, you knew that the second you all entered, all gloves"
          " would be off. After many days of traveling, you finally reach it. The only sign that there is even a vast"
          " underground maze here at all is the simple, yet perfectly square hole in the ground. You all hop in and the"
          " hunt begins.")
    for player in players:  # Puts all the players in the starting room
        v.STARTING_ROOM.occupants.append(player.name)
        player.visited_rooms.append(v.STARTING_ROOM)
        player.current_room = v.STARTING_ROOM
    winner = False
    while not winner:
        for player_number, player in enumerate(players):
            print(f"\nIt is player {player_number + 1}'s ({player.name}) turn!{'' if player.human else ' (AI)'}")
            if type(player.state[0]) is not str:  # Activates stuck spots
                player.current_room.entered(player, rooms, players)
                player.state[0](player)
                v.t.sleep(2.5)
            if player.state[0] == "default":  # Allows for players to move the turn they escape from stuck spots
                if player.human:
                    chosen_direction = False
                    while not chosen_direction:
                        print("\nYou decide you have spent enough time in this room, and survey the room to figure out"
                              " where you can go next.\n")
                        for direction_count, direction in enumerate(player.current_room.paths):
                            print(f"{direction_count + 1}: {direction}")
                        print(f"{len(player.current_room.paths) + 1}: Check inventory")
                        print(f"{len(player.current_room.paths) + 2}: Check who else is in the room")
                        selected_input = False
                        while not selected_input:
                            try:
                                player_selection = int(input())
                                selected_input = True
                            except ValueError:
                                print("Enter only a number for your selection")
                        if 0 < player_selection <= len(player.current_room.paths):
                            chosen_direction = player.current_room.paths[player_selection - 1]
                        elif player_selection == len(player.current_room.paths) + 1:
                            player.check_inventory(player.current_room, rooms, players)
                        else:
                            v.ROOM_HELPER_FUNCTIONS["display_players_in_room"](player.current_room, player.name)
                            v.t.sleep(2.5)
                else:
                    chosen_direction = v.r.choice(player.current_room.paths)  # Add AI logic here

                player.current_room = player.current_room.neighbors[chosen_direction]
                if player.current_room not in player.visited_rooms:
                    player.visited_rooms.append(player.current_room)
                if player.state[0] != "nope":
                    player.current_room.entered(player, rooms, players)
                else:
                    v.ROOM_HELPER_FUNCTIONS["put_player_in_room"](player, player.current_room, rooms)
                    player.state = ["default", None]
                    if player.human:
                        print("\nYou enter the room and care not for what is inside. You smile, and then"
                              " realize the image has fallen off your head. You are sad, but you know that it"
                              " was what that heavy man would have wanted.")
                v.t.sleep(2.5)

                if player.state[0] == "winner":
                    winner = True
                    winning_player = player
                    time_taken = int(v.t.time() - game_start_time)
                    break
        for room in rooms:  # Moves any moving placed items
            for item in room.placed_items:
                if item == v.ITEM_HELPER_FUNCTIONS["encountered_goblin"]:
                    v.ITEM_HELPER_FUNCTIONS["move_goblin"](rooms, room)

    time_taken_seconds = time_taken % 60
    time_taken_minutes = time_taken // 60
    time_taken_hours = time_taken_minutes // 60
    print(f"\n{winning_player.name} has won the game!\nThe game took {time_taken_hours} hours, {time_taken_minutes}"
          f" minutes, and {time_taken_seconds} seconds!\nDuring that time, they entered"
          f" {len(winning_player.visited_rooms)} rooms out of {len(rooms)} total!")
    v.t.sleep(5)
    print("\nThe full map:")
    v.t.sleep(.5)
    print(v.generate_maze_image(rooms))
    v.t.sleep(10)
