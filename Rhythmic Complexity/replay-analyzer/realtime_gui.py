import pygame
import mutagen.mp3
import beatmap_parser
import time
import numpy
import beatmap_visualiser_data
import analyze
from osrparse import parse_replay_file
from tkinter import filedialog
from tkinter import *


# Function used to start the map.
def start_map():
    global relative_time, delay_timer_line, rate_change_timer_line

    relative_time = int(round(time.time() * 1000))

    pygame.mixer.music.play()

    tick()
    draw_map()

    analyze.graph_tap_error(tap_time_list, tap_error_list)

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

    ar        = beatmap_parser.return_ar(osu_lines, hardrock, easy)

    closest_data_index = min(range(len(cumulative_time)), key=lambda i: abs(cumulative_time[i]-ms))

    # Draw keys pressed
    replay_pressed     = replay_data[closest_data_index].keys_pressed
    left_pressed       = False
    right_pressed      = False
    left_fill          = "#ff0000"
    right_fill          = "#ff0000"

    if replay_pressed & 0b100 | replay_pressed & 0b1: left_pressed = True
    if replay_pressed & 0b1000 | replay_pressed & 0b10: right_pressed = True
    if left_pressed: left_fill = "#00ff00"
    if right_pressed: right_fill = "#00ff00"

    map_canvas.create_rectangle(0, 0, 50, 50, fill=left_fill, width=0)
    map_canvas.create_rectangle(50, 0, 100, 50, fill=right_fill, width=0)

    # Draw hit error bar
    line_x = 325
    line_y = 500
    line_h = 50
    scale  = 2

    line_base_colour = (0, 0, 255)
    bg_colour        = (240, 240, 240)

    for i, j in zip(tap_time_list[::-1], tap_error_list[::-1]):
        on_screen_length = 2000

        if i < ms < i + on_screen_length:
            # Because of Tkinter not allowing RGBA, this shit code exists :)
            red = line_base_colour[0] + ((ms - i) *
                                         (bg_colour[0] - line_base_colour[0]) /
                                         on_screen_length)
            red = str(hex(int(red)))[2:].zfill(2)
            green = line_base_colour[1] + ((ms - i) *
                                           (bg_colour[1] - line_base_colour[1]) /
                                           on_screen_length)
            green = str(hex(int(green)))[2:].zfill(2)
            blue = line_base_colour[2] + ((ms - i) *
                                          (bg_colour[2] - line_base_colour[2]) /
                                          on_screen_length)
            blue = str(hex(int(blue)))[2:].zfill(2)

            line_colour = "#{}{}{}".format(red, green, blue)

            map_canvas.create_line(line_x + scale*j, line_y,
                                   line_x + scale*j, line_y + line_h,
                                   fill=line_colour, width=2)

    map_canvas.create_line(line_x, line_y, line_x, line_y + line_h, width=5)

    # Draw hit circles
    onscreen_hitobjects = beatmap_visualiser_data.return_onscreen_hitobjects(hitobject_list, ar, ms, speed_multiplier)

    for hitobject in onscreen_hitobjects[::-1]:

        # Because of Tkinter not allowing RGBA, this shit code exists :)
        hex_opacity = str(hex(int(255 - hitobject[2] * 255)))[2:]
        hex_opacity = hex_opacity.zfill(2)
        fill        = "#ff" + hex_opacity * 2
        outline     = "#" + hex_opacity * 3

        map_canvas.create_oval(hitobject[0] + cs_radius + offset_x, hitobject[1] + cs_radius + offset_y,
                               hitobject[0] - cs_radius + offset_x, hitobject[1] - cs_radius + offset_y,
                               fill=fill, outline=outline, width=1)

    # Draw approach circles
    onscreen_approach_circles = beatmap_visualiser_data.return_onscreen_approach_circles(hitobject_list, ar, cs_radius, ms, speed_multiplier)

    for hitobject in onscreen_approach_circles[::-1]:

        # Because of Tkinter not allowing RGBA, this shit code exists :)
        hex_opacity = str(hex(int(255 - hitobject[3] * 255)))[2:]
        hex_opacity = hex_opacity.zfill(2)
        outline = "#" + hex_opacity * 3

        map_canvas.create_oval(hitobject[0] + hitobject[2] + offset_x, hitobject[1] + hitobject[2] + offset_y,
                               hitobject[0] - hitobject[2] + offset_x, hitobject[1] - hitobject[2] + offset_y,
                               fill="", outline=outline, width=2)

    # Draw cursor, cursor trail
    cursor_radius     = 12
    cursors_on_screen = 15

    cursor_base_colour = (100, 100, 255)

    for i in range(cursors_on_screen):
        replay_x      = replay_data[max(0, closest_data_index-(cursors_on_screen-i))].x
        replay_y      = replay_data[max(0, closest_data_index-(cursors_on_screen-i))].y

        # Because of Tkinter not allowing RGBA, this shit code exists :)
        red   = cursor_base_colour[0] + ((cursors_on_screen-i) *
                                         (bg_colour[0] - cursor_base_colour[0]) /
                                         cursors_on_screen)
        red   = str(hex(int(red)))[2:]
        green = cursor_base_colour[1] + ((cursors_on_screen-i) *
                                         (bg_colour[1] - cursor_base_colour[1]) /
                                         cursors_on_screen)
        green = str(hex(int(green)))[2:]
        blue  = cursor_base_colour[2] + ((cursors_on_screen-i) *
                                         (bg_colour[2] - cursor_base_colour[2]) /
                                         cursors_on_screen)
        blue  = str(hex(int(blue)))[2:]
        cursor_colour = "#{}{}{}".format(red, green, blue)

        map_canvas.create_oval(replay_x + cursor_radius + offset_x, replay_y + cursor_radius + offset_y,
                               replay_x - cursor_radius + offset_x, replay_y - cursor_radius + offset_y,
                               fill=cursor_colour, outline="")

    # Draw tapped places.
    for i in tap_list:
        tap_circle_radius      = 3
        on_screen_length       = 500

        if i[2] < ms < i[2] + on_screen_length:
            map_canvas.create_oval(i[0] + tap_circle_radius + offset_x, i[1] + tap_circle_radius + offset_y,
                                   i[0] - tap_circle_radius + offset_x, i[1] - tap_circle_radius + offset_y,
                                   fill="#000000", outline="")

    time_label.after(30, draw_map)

# Function used to kill the program entirely.
def kill():
    sys.exit()


Tk().withdraw()

osr_file_path = filedialog.askopenfilename(title="Select an osr file", filetypes=(("osr files", "*.osr"),))
osu_file_path = filedialog.askopenfilename(title="Select an osu file", filetypes=(("osu files", "*.osu"),))
osu_file      = open(osu_file_path, 'r', encoding="utf-8")
osu_lines     = [line.rstrip('\n') for line in osu_file]
mp3_name      = beatmap_parser.mp3_name(osu_lines)
mp3_file_path = "/".join(osu_file_path.split("/")[:-1]) + "/{}".format(mp3_name)

replay_file  = parse_replay_file(osr_file_path)
replay_mods  = [str(mod)[4:] for mod in list(replay_file.mod_combination)]
replay_data  = replay_file.play_data
replay_times = [i.time_since_previous_action for i in replay_data]

speed_multiplier = 1

if "DoubleTime" in replay_mods or "Nightcore" in replay_mods:
    speed_multiplier = 1.5
if "HalfTime" in replay_mods:
    speed_multiplier = 0.75

hardrock = False
if "HardRock" in replay_mods:
    hardrock = True

easy = False
if "Easy" in replay_mods:
    easy = True

cumulative_time = [sum(replay_times[:i]) / speed_multiplier for i in range(len(replay_times))]
hitobject_list  = beatmap_parser.return_hitobject_data(osu_lines, speed_multiplier, hardrock)
time_list       = [hitobject_list[2] for hitobject in hitobject_list]

tap_list                      = analyze.find_tap_data(replay_data, speed_multiplier)
cs_radius                     = beatmap_parser.return_cs_radius(osu_lines, hardrock, easy)
hitobject_tap_list            = analyze.find_hitobject_tap_data(tap_list, hitobject_list, cs_radius)
tap_time_list, tap_error_list = analyze.tap_error(hitobject_tap_list, hitobject_list, cs_radius)

mp3 = mutagen.mp3.MP3(mp3_file_path)
pygame.mixer.init(frequency=int(mp3.info.sample_rate * speed_multiplier))
pygame.mixer.music.load(mp3_file_path)

while True:
    root = Tk()

    Button(root, fg="blue", text="Start Realtime!", command=start_map).grid(row=0, column=0)

    time_label = Label(root, fg="black")
    time_label.grid(row=1, column=0)

    map_canvas = Canvas(root, width=650, height=550)
    map_canvas.grid(row=2, column=0)

    root.protocol("WM_DELETE_WINDOW", kill)
    root.mainloop()