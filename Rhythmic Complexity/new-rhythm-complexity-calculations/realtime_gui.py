import pygame
import mutagen.mp3
import beatmap_parser
import beatmap_visualiser_data
import time
import diff_calc
import numpy
from tkinter import filedialog
from tkinter import *


# Function used to start the map.
def start_map():
    global relative_time, delay_timer_line, rate_change_timer_line

    relative_time = int(round(time.time() * 1000)) + 400

    mp3 = mutagen.mp3.MP3(mp3_file_path)
    pygame.mixer.init(frequency=mp3.info.sample_rate)
    pygame.mixer.music.load(mp3_file_path)
    pygame.mixer.music.play()

    tick()
    draw_map()
    draw_difficulty_graphs()

    delay_timer_line       = delay_graph_canvas.create_line(0, 0, 0, 200, fill="#77ff77")
    rate_change_timer_line = rate_change_graph_canvas.create_line(0, 0, 0, 200, fill="#77ff77")
    draw_difficulty_graphs_timers()

# Function used to tick ms counter
def tick():
    global relative_time, ms

    ms = int(round(time.time() * 1000)) - relative_time
    time_label["text"] = "Timer: {}ms".format(ms)

    time_label.after(30, tick)

# Function used to draw the map
def draw_map():
    global ms, time_list

    map_canvas.delete("all")

    offset_x = 50
    offset_y = 50

    ar                        = beatmap_parser.return_ar(osu_lines)
    cs_radius                 = beatmap_parser.return_cs_radius(osu_lines)
    hitobject_list            = beatmap_parser.return_hitobject_data(osu_lines)
    onscreen_hitobjects       = beatmap_visualiser_data.return_onscreen_hitobjects(hitobject_list, ar, ms)
    onscreen_approach_circles = beatmap_visualiser_data.return_onscreen_approach_circles(hitobject_list, ar, cs_radius, ms)

    # Draw hit circles
    for hitobject in onscreen_hitobjects[::-1]:
        hex_opacity = str(hex(int(255 - hitobject[2] * 255)))[2:]
        hex_opacity = hex_opacity.zfill(2)
        fill        = "#ff" + hex_opacity * 2
        outline     = "#" + hex_opacity * 3

        map_canvas.create_oval(hitobject[0] + cs_radius + offset_x, hitobject[1] + cs_radius + offset_y,
                               hitobject[0] - cs_radius + offset_x, hitobject[1] - cs_radius + offset_y,
                               fill=fill, outline=outline, width=1)

    # Draw approach circles
    for hitobject in onscreen_approach_circles[::-1]:
        hex_opacity = str(hex(int(255 - hitobject[3] * 255)))[2:]
        hex_opacity = hex_opacity.zfill(2)
        outline = "#" + hex_opacity * 3

        map_canvas.create_oval(hitobject[0] + hitobject[2] + offset_x, hitobject[1] + hitobject[2] + offset_y,
                               hitobject[0] - hitobject[2] + offset_x, hitobject[1] - hitobject[2] + offset_y,
                               fill="", outline=outline, width=2)

    time_label.after(30, draw_map)


# Function used to draw a graph.
def draw_full_graph(canvas, time_list, difficulty_list):
    global ms, timer_line

    width  = 600
    height = 200

    max_difficulty = max(difficulty_list)

    # Separate list into multiple lists when breaks exist.
    time_break_separated_list = [[]]
    list_number = 0
    for i in range(len(time_list) - 1):
        if time_list[i + 1] - time_list[i] > 3000:
            # Create new list.
            list_number += 1
            time_break_separated_list.append([])
        time_break_separated_list[list_number].append(time_list[i])

    # Coordinates to be later used in the canvas.
    canvas_difficulty_list = []
    canvas_time_list       = []

    # Calculating coordinates.
    for i in time_list:
        canvas_time_list.append(width * (i - time_list[0]) / (time_list[-1] - time_list[0]))
    for i in difficulty_list:
        canvas_difficulty_list.append(height - i * (height/max_difficulty))

    canvas.create_rectangle(0, 0, width, height, fill="#dddddd")
    canvas.create_line(0, height*0.2, width, height*0.2, fill="#cccccc")
    canvas.create_line(0, height*0.4, width, height*0.4, fill="#cccccc")
    canvas.create_line(0, height*0.6, width, height*0.6, fill="#cccccc")
    canvas.create_line(0, height*0.8, width, height*0.8, fill="#cccccc")
    canvas.create_line(width*0.2, 0, width*0.2, height, fill="#cccccc")
    canvas.create_line(width*0.4, 0, width*0.4, height, fill="#cccccc")
    canvas.create_line(width*0.6, 0, width*0.6, height, fill="#cccccc")
    canvas.create_line(width*0.8, 0, width*0.8, height, fill="#cccccc")

    # Draw blue line graph, difficulty.
    for i in range(len(difficulty_list) - 1):
        # Don't continue the graph if there is a break.
        if time_list[i + 1] - time_list[i] < 3000:
            canvas.create_line(canvas_time_list[i], canvas_difficulty_list[i],
                                          canvas_time_list[i + 1], canvas_difficulty_list[i + 1],
                                          fill="#9999ff")

    # Draw red line graph, the moving average.
    average_values = 20
    for n in range(len(time_break_separated_list)):
        for x in range(len(time_break_separated_list[n]) - average_values):
            if n == 0:
                i = x
            else:
                i = x + sum([len(i) for i in time_break_separated_list[:n]])

            # Don't continue graph if there's a break.
            if time_list[i + 1 + int(average_values/2)] - time_list[i + int(average_values/2)] < 3000:
                canvas.create_line(canvas_time_list[i + int(average_values/2)],
                                             sum(canvas_difficulty_list[i:i + average_values]) / average_values,
                                             canvas_time_list[i + 1 + int(average_values/2)],
                                             sum(canvas_difficulty_list[i + 1:i + average_values+1]) / average_values,
                                             fill="#990000")


# Function used to draw the graph timer.
def draw_full_graph_timer(canvas, ms, time_list, timer_line):
    width  = 600
    height = 200

    if ms < time_list[-1]:
        draw_x = width * (ms - time_list[0]) / (time_list[-1] - time_list[0])
        canvas.coords(timer_line, draw_x, 0, draw_x, height)

# Draw difficulty graphs.
def draw_difficulty_graphs():
    time_list                   = beatmap_parser.file_times(osu_lines)
    delay_difficulty_list       = diff_calc.delay_difficulty(time_list)[2]
    rate_change_difficulty_list = diff_calc.rate_change_difficulty(time_list)[2]

    draw_full_graph(delay_graph_canvas, time_list, delay_difficulty_list)
    draw_full_graph(rate_change_graph_canvas, time_list, rate_change_difficulty_list)

# Draw difficulty graphs' timers.
def draw_difficulty_graphs_timers():
    global ms, delay_timer_line, rate_change_timer_line

    time_list = beatmap_parser.file_times(osu_lines)
    draw_full_graph_timer(delay_graph_canvas, ms, time_list, delay_timer_line)
    draw_full_graph_timer(rate_change_graph_canvas, ms, time_list, rate_change_timer_line)

    time_label.after(30, draw_difficulty_graphs_timers)

# Function used to kill the program entirely.
def kill():
    sys.exit()


Tk().withdraw()

osu_file_path = filedialog.askopenfilename(title="Select an osu file", filetypes=(("osu files", "*.osu"),))
osu_file      = open(osu_file_path, 'r', encoding="utf-8")
osu_lines     = [line.rstrip('\n') for line in osu_file]
mp3_name      = beatmap_parser.mp3_name(osu_lines)
mp3_file_path = "/".join(osu_file_path.split("/")[:-1]) + "/{}".format(mp3_name)

time_list       = beatmap_parser.file_times(osu_lines)

while True:
    root = Tk()

    Button(root, fg="blue", text="Start Realtime!", command=start_map).grid(row=0, column=1)

    time_label = Label(root, fg="black")
    time_label.grid(row=1, column=1)

    map_canvas = Canvas(root, width=650, height=550)
    map_canvas.grid(row=2, column=1, rowspan=2)

    delay_graph_canvas = Canvas(root, width=600, height=200)
    delay_graph_canvas.grid(row=3, column=0)

    rate_change_graph_canvas = Canvas(root, width=600, height=200)
    rate_change_graph_canvas.grid(row=3, column=2)

    Label(root, text="Delay Difficulty Graph").grid(row=2, column=0)
    Label(root, text="Rate Change Difficulty Graph").grid(row=2, column=2)

    delay_list, difficulty_list, delay_difficulty_list                  = diff_calc.delay_difficulty(time_list)
    rate_change_list, rate_difficulty_list, rate_change_difficulty_list = diff_calc.rate_change_difficulty(time_list)

    total_delay_difficulty       = diff_calc.total_difficulty(delay_difficulty_list)
    total_rate_change_difficulty = diff_calc.total_difficulty(rate_change_difficulty_list)

    Label(root, text="Total Delay Difficulty: {:.4f}\nTotal Rate Change Difficulty: {:.4f}".format(total_delay_difficulty, total_rate_change_difficulty)).grid(row=4, column=1)

    root.protocol("WM_DELETE_WINDOW", kill)
    root.mainloop()