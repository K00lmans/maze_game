"""This file contains all the room generation code

If you add any additional generation steps, make sure they are ordered in the order in which they are run for clarity"""

import global_vars as v


def generate_maze_layout(room_count: int) -> list:
    """Creates an entity, called room_crawler, which is randomly shifted north, east, south, and west. Each time this
    entity moves, it first adds a path from the room at its old location to its new one if it does not already exist.
    This allows the dynamic creation of oneway paths. After it moves, it checks if there is a room in its new location,
    and if there is not adds an empty room to that location. It starts by adding the start room at (0, 0) and once it
    has added the number of rooms stored in the room_count variable, it continues to move till it has found an empty
    spot once more and then creates the goal room at that spot. This guarantees the goal room will have only one
    entrance."""
    time_of_last_player_update = v.t.time()
    starting_room_count = room_count
    generated_rooms = []
    room_crawler = [0, 0]
    generated_rooms.append(v.Room(v.ROOMS["other_rooms"]["start"], room_crawler[0], room_crawler[1]))

    room_crawler_room = generated_rooms[0]  # Keeps track of the room the room crawler is at to reduce repeated searches
    max_x_y = [0, 0]
    min_x_y = [0, 0]
    while room_count >= 0:
        possible_directions = ["NORTH", "NORTH", "EAST", "EAST", "SOUTH", "SOUTH", "WEST", "WEST"]
        # The 1.125, 1.25, and 1.5 are damper values to limit overcorrection
        if max_x_y[0] > abs(min_x_y[0] * 1.125):
            possible_directions.remove("EAST")
            if max_x_y[0] > abs(min_x_y[0] * 1.25):
                possible_directions.append("WEST")
                if max_x_y[0] > abs(min_x_y[0] * 1.5):
                    possible_directions.remove("EAST")
        elif abs(min_x_y[0]) > (max_x_y[0] * 1.125):
            possible_directions.remove("WEST")
            if abs(min_x_y[0]) > (max_x_y[0] * 1.25):
                possible_directions.append("EAST")
                if abs(min_x_y[0]) > (max_x_y[0] * 1.5):
                    possible_directions.remove("WEST")
        if max_x_y[1] > abs(min_x_y[1] * 1.125):
            possible_directions.remove("NORTH")
            if max_x_y[1] > abs(min_x_y[1] * 1.25):
                possible_directions.append("SOUTH")
                if max_x_y[1] > abs(min_x_y[1] * 1.5):
                    possible_directions.remove("NORTH")
        elif abs(min_x_y[1]) > (max_x_y[1] * 1.125):
            possible_directions.remove("SOUTH")
            if abs(min_x_y[1]) > (max_x_y[1] * 1.25):
                possible_directions.append("NORTH")
                if abs(min_x_y[1]) > (max_x_y[1] * 1.5):
                    possible_directions.remove("SOUTH")

        direction = v.r.choice(possible_directions)
        if direction not in room_crawler_room.paths:
            room_crawler_room.paths.append(direction)

        room_crawler[0] += v.Directions[direction].value[0]
        room_crawler[1] += v.Directions[direction].value[1]
        if room_crawler[0] > max_x_y[0]:
            max_x_y[0] = room_crawler[0]
        elif room_crawler[0] < min_x_y[0]:
            min_x_y[0] = room_crawler[0]
        if room_crawler[1] > max_x_y[1]:
            max_x_y[1] = room_crawler[1]
        elif room_crawler[1] < min_x_y[1]:
            min_x_y[1] = room_crawler[1]

        new_room = True
        for room in generated_rooms:
            if room_crawler[0] == room.x and room_crawler[1] == room.y:
                new_room = False
                room_crawler_room = room
                break
        if new_room:
            generated_rooms.append(
                v.Room(v.ROOMS["other_rooms"]["empty"] if room_count != 0 else v.ROOMS["other_rooms"]["goal"],
                       room_crawler[0], room_crawler[1]))
            room_crawler_room = generated_rooms[-1]
            room_count -= 1
            # Make sure the player is updated every second or so on generation progress
            if (v.t.time() - time_of_last_player_update) >= 1:  # Done only when a room is added to keep speed up
                print(f"\nRoom generation {int(100 - ((room_count / starting_room_count) * 100))}% done.")
                time_of_last_player_update = v.t.time()

    return generated_rooms


def assign_rooms(maze_layout: list, special_rooms: list, good_room_count: int, bad_room_count: int, shop_count: int):
    time_of_last_player_update = v.t.time()
    total_rooms_to_assign = good_room_count + bad_room_count + shop_count + len(special_rooms)
    completed_assignments = 0

    for count, room_style in enumerate(special_rooms):
        chosen_room = v.r.choice(maze_layout)
        while chosen_room.style != v.ROOMS["other_rooms"]["empty"]:
            chosen_room = v.r.choice(maze_layout)
        chosen_room.style = room_style
        if (v.t.time() - time_of_last_player_update) >= 1:
            print(f"\nRoom assignment {int((count / total_rooms_to_assign) * 100)}% done.")
            time_of_last_player_update = v.t.time()
    completed_assignments += len(special_rooms)

    # Since room counts count down, preemptively add the total then subtract the remaining
    completed_assignments += good_room_count
    while good_room_count != 0:
        chosen_room = v.r.choice(maze_layout)
        if chosen_room.style == v.ROOMS["other_rooms"]["empty"]:
            chosen_room.style = v.r.choice(list(v.ROOMS["good_rooms"].values()))
            good_room_count -= 1
            if (v.t.time() - time_of_last_player_update) >= 1:  # Done only when a room is added to reduce checks
                print(f"\nRoom assignment"
                      f" {int(((completed_assignments - good_room_count) / total_rooms_to_assign) * 100)}% done.")
                time_of_last_player_update = v.t.time()

    completed_assignments += bad_room_count
    while bad_room_count != 0:
        chosen_room = v.r.choice(maze_layout)
        if chosen_room.style == v.ROOMS["other_rooms"]["empty"]:
            chosen_room.style = v.r.choice(list(v.ROOMS["bad_rooms"].values()))
            bad_room_count -= 1
            if (v.t.time() - time_of_last_player_update) >= 1:
                print(f"\nRoom assignment"
                      f" {int(((completed_assignments - bad_room_count) / total_rooms_to_assign) * 100)}% done.")
                time_of_last_player_update = v.t.time()

    completed_assignments += shop_count
    while shop_count != 0:
        chosen_room = v.r.choice(maze_layout)
        if chosen_room.style == v.ROOMS["other_rooms"]["empty"]:
            chosen_room.style = v.ROOMS["other_rooms"]["shop"]
            shop_count -= 1
            if (v.t.time() - time_of_last_player_update) >= 1:
                print(f"\nRoom assignment"
                      f" {int(((completed_assignments - shop_count) / total_rooms_to_assign) * 100)}% done.")
                time_of_last_player_update = v.t.time()


def find_room_neighbors(rooms: list):
    time_of_last_update = v.t.time()
    for count, room in enumerate(rooms):
        room.find_neighboring_rooms(rooms)
        if (v.t.time() - time_of_last_update) >= 1:
            print(f"\nData refactoring {int(((count + 1) / len(rooms)) * 100)}% done.")
            time_of_last_update = v.t.time()
