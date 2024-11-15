"""Shows a step by step view of what the pathfinding algorithm is doing.

Note: As with all dev tools, written without usability in mind, use at your own risk.

If any of the imports change, make sure to update their locations

Because I am a low tier programmer this whole thing works by copying the pathfinding code into the main run area and
then splicing in some function calls into the code to allow for seeing what it's doing so if you change the pathfinding
code, change it here as well. To be fair, if you change it without running it through this, and it works you are clearly
too good of a programmer to be looking at this mess of a codebase."""

import global_vars as v
import maze_generation as mg


def update_room_as_checked(room):
    pass

def update_room_as_to_be_checked(room):
    pass

def show_room_visualization(maze):
    print("\n\n\n\n\n" + v.generate_maze_image(maze))
