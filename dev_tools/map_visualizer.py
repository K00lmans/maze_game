"""Shows a graphical representation of a generated map to visualize maze generation.

Note: As with all dev tools, written without usability in mind, use at your own risk.

If you move the room generation code to a different file, please change the import statement."""

from time import sleep
from maze_generation import generate_maze_layout
from global_vars import generate_maze_image

room_count = int(input("room count: "))
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
print(f"height of {max_y-min_y} with a max of {max_y} and a min of {min_y}")
sleep(2.5)
file = open("maze_visualization.txt", "w", encoding="utf-8")
file.write(generate_maze_image(rooms))
file.close()
print("\nNew visualisation saved to file")
