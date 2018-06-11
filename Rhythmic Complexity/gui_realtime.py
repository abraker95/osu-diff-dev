from tkinter import filedialog
from tkinter import *
import find_complexity
import beatmap_parser
import numpy
import time
import sys


# Function to be used to initialize the timer.

def first_load():
    # Variable relative_time is the time when the user has clicked the button to start timer.
    global relative_time
    relative_time = int(round(time.time() * 1000)) + 2000
    tick()


# Function to be used to run the timer and update the real time stuff

def tick():
    # Variable ms is the time that constantly goes up during the timer.
    global ms, left_times, right_times, left_weights, right_weights, realtime_graph
    time_label.after(30, tick)
    ms = int(round(time.time() * 1000)) - relative_time
    time_label["text"] = "Timer: {}ms".format(ms)

    realtime_graph.delete("all")

    realtime_graph.create_rectangle(247, 0, 253, 500, fill="#00ff00")

    draw_pulses(ms, left_times, 200)
    draw_pulses(ms, right_times, 450)
    draw_graph(ms, left_times, left_weights, 200)
    draw_graph(ms, right_times, right_weights, 450)


def draw_pulses(time, pulse_list, top_left_y):
    global realtime_graph

    for i in pulse_list:
        fill_color = "#dddddd"
        if time + 1000 > i > time - 1000:
            if time + 50 > i > time - 50:
                fill_color = "#ff0000"
            x1 = (1000 + i - time) / 4 - 3
            y1 = top_left_y
            x2 = x1 + 6
            y2 = y1 + 50
            realtime_graph.create_rectangle(x1, y1, x2, y2, fill=fill_color)


def draw_graph(time, pulse_list, weight_list, bottom_y):
    global realtime_graph

    fill_color = "#ff0000"

    draw_list_indexes = [i for i in range(len(pulse_list)) if time + 1000 > pulse_list[i] > time - 1000]
    draw_list = [weight_list[3][i] for i in draw_list_indexes if i < len(weight_list[3])]
    draw_coords = []

    for i, j in zip(draw_list, draw_list_indexes):
        x = (1000 + pulse_list[j] - time) / 4
        y = (bottom_y - 200) + (200 - 200 * (i / max(weight_list[3]))) + 3
        draw_coords.append((x, y))

    for i in range(len(draw_coords) - 1):
        realtime_graph.create_line(draw_coords[i][0], draw_coords[i][1],
                                   draw_coords[i + 1][0], draw_coords[i + 1][1], fill=fill_color)

    '''
    these ugly things are for drawing points which aren't visible on the screen
    but the line is still visible on the screen
    '''

    if len(draw_list_indexes) != 0:
        if draw_list_indexes[0] > 0:
            x = (1000 + pulse_list[draw_list_indexes[0] - 1] - time) / 4
            y = (bottom_y - 200) + (200 - 200 * (weight_list[3][draw_list_indexes[0] - 1] / max(weight_list[3]))) + 3

            realtime_graph.create_line(x, y,
                                       draw_coords[0][0], draw_coords[0][1], fill=fill_color)

        if draw_list_indexes[-1] < len(pulse_list):
            x = (1000 + pulse_list[draw_list_indexes[-1] + 1] - time) / 4
            y = (bottom_y - 200) + (200 - 200 * (weight_list[3][draw_list_indexes[-1] + 1] / max(weight_list[3]))) + 3

            realtime_graph.create_line(x, y,
                                       draw_coords[-1][0], draw_coords[-1][1], fill=fill_color)


# Function used to kill the GUI.

def stop():
    root.quit()
    root.destroy()


# Function used to kill the program entirely.

def kill():
    sys.exit()


while True:
    Tk().withdraw()
    osu_file_path = filedialog.askopenfilename(title="Select an osu file", filetypes=(("osu files", "*.osu"),))

    osu_file = open(osu_file_path, 'r', encoding="utf-8")

    osu_lines = [line.rstrip('\n') for line in osu_file]
    map_lines = osu_lines[beatmap_parser.find_start(osu_lines):]

    map_times = beatmap_parser.return_times(map_lines)
    left_times, right_times = find_complexity.find_finger_placement(map_times)
    left_weights, right_weights = find_complexity.abraker_triplet(map_times)

    root = Tk()
    root.title("Weighted Objects")

    # Stuff for the timer.
    ms = -2000

    realtime_graph = Canvas(root, width=500, height=500)
    realtime_graph.pack()

    time_label = Label(root, fg="black")
    time_label.pack()

    Button(root, fg="blue", text="Start Realtime!", command=first_load).pack()

    Button(root, fg="red", text="Choose another map", command=stop).pack()

    # If window is closed, stop the program.
    root.protocol("WM_DELETE_WINDOW", kill)

    root.mainloop()
