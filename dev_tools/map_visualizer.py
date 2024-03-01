"""Shows a graphical representation of a generated map to visualize maze generation.

Note: As with all dev tools, written without usability in mind, use at your own risk.

If you move the room generation code to a different file, please change the import statement."""

from time import sleep
from main_game_loop import generate_maze_layout

room_count = int(input("room count: "))
while True:
    rooms = generate_maze_layout(room_count)
    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0
    for room in rooms:
        if room.x > max_x:
            max_x = room.x
        if room.x < min_x:
            min_x = room.x
        if room.y > max_y:
            max_y = room.y
        if room.y < min_y:
            min_y = room.y
    print(f"width of {max_x-min_x} with a max of {max_x} and a min of {min_x}")
    print(f"height of {max_y-min_y} with a max of {max_y} and a min of {min_y}\n")
    sleep(5)
    empty_row = []
    for _ in range((max_x-min_x) + 1):
        empty_row.append(None)
    location_sorted_rooms = []
    for _ in range((max_y-min_y) + 1):
        location_sorted_rooms.append(empty_row.copy())
    for room in rooms:  # I have no idea how or why this translation code works
        translated_x = room.x + abs(min_x)
        translated_y = max_y - room.y
        location_sorted_rooms[translated_y][translated_x] = room
    for row in location_sorted_rooms:
        printed_room_row = ["", "", "", "", ""]
        for room in row:
            if room is None:
                for text_row_number in range(len(printed_room_row)):
                    printed_room_row[text_row_number] += "     "
            else:
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
                    printed_room_row[2] += f"◄│{room.style.__name__[0]}│"
                else:
                    printed_room_row[2] += f" │{room.style.__name__[0]}│"
                if "EAST" in room.paths:
                    printed_room_row[2] += "►"
                else:
                    printed_room_row[2] += " "
        for text_row in printed_room_row:
            print(text_row)
    sleep(10)
