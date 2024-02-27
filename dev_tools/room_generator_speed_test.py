"""Used to test if changes to the room generation code improves its speed

If you move the room generation code to a different file, please change the import statement

All past times are stored in the room_generator_time_records file as average time to generate 50, 300, 550, 1050, 1550,
1800, 2050 and 2300 rooms in milliseconds

This code is not written for usability, use at your own risk

Because I'm lazy, you have to put the times into the file yourself"""

from main_game_loop import generate_maze_layout
from time import time


runtime = 0
loops = 1
average_times = []
while loops <= 46:
    set_average_times = []
    for test in range(100):
        start_time = time()
        generate_maze_layout(50 * loops)
        stop_time = time()
        set_average_times.append((stop_time - start_time) * 1000)
        print(f"\n{test + 1}% done with set {loops} of 46")
    average_times.append(sum(set_average_times)/len(set_average_times))
    loops += 1

concise_average_times = []
for time_location, time in enumerate(average_times):
    if (time_location + 1) * 50 in [50, 300, 550, 1050, 1550, 1800, 2050, 2300]:
        concise_average_times.append(time)
for time_location, time in enumerate(average_times):
    average_times[time_location] = str(time)
printable_average_times = ", ".join(average_times)
print(f"\nFull data:\n{printable_average_times}")
for time_location, time in enumerate(concise_average_times):
    concise_average_times[time_location] = str(time)
printable_average_times = ", ".join(concise_average_times)
print(f"\nConcise data:\n{printable_average_times}")
