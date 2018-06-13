from tkinter import *
import time
import sys
import analyse


# Function to be used to initialize the timer.

def first_load():
    # Variable relative_time is the time when the user has clicked the button to start timer.
    global relative_time, ms, realtime_canvas, user_data

    user_data     = []
    ms            = 0
    relative_time = int(round(time.time() * 1000)) + 2000

    tick()


# Function to be used to run the timer and update the real time stuff

def tick():
    # Variable ms is the time that constantly goes up during the timer.
    global ms, ms_values, realtime_canvas, results, user_data
    time_label.after(30, tick)
    ms = int(round(time.time() * 1000)) - relative_time
    time_label["text"] = "Timer: {}ms".format(ms)

    realtime_canvas.delete("all")

    realtime_canvas.create_rectangle(0, 372, 500, 378, fill="#00ff00")

    draw_pulses(ms, ms_values, realtime_canvas)


def draw_pulses(time, pattern, canvas):
    for i in pattern:
        left_x = 75 if i[1] == "l" else 325
        fill_color = "#dddddd"
        if time + 1500 > i[0] > time - 500:
            if time + 50 > i[0] > time - 50:
                fill_color = "#ff0000"
            x1 = left_x
            y1 = 500 - (i[0] - time + 500) / 4 - 3
            x2 = x1 + 100
            y2 = y1 + 6
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)


def generate_pattern(pattern_string):
    pattern = []
    split_string = pattern_string.split("|")[1]
    for i in range(len(split_string)):
        if split_string[i] == "l": pattern.append((i, "l"))
        if split_string[i] == "r": pattern.append((i, "r"))

    return pattern


def generate_ms_values(pattern, meter, end):
    last_end     = 0
    total_length = end
    pattern_list = []
    for bpm in range(120, 185, 5):
        local_bpm_list = pattern
        ms_between = 60000 / (bpm * meter)
        local_bpm_list = [(x[0]*ms_between + last_end, x[1]) for x in local_bpm_list]
        last_end += total_length * ms_between
        pattern_list += local_bpm_list

    return pattern_list


def record_left(e):
    global ms, user_data
    user_data.append((ms, "l"))


def record_right(e):
    global ms, user_data
    user_data.append((ms, "r"))


def show_results():
    global user_data, ms_values, results, error_list

    error = analyse.order_messed(user_data, ms_values)[0][0][0]

    print(error)
    analyse.show_hit_error_plot(user_data, ms_values)
    error_list.append(error)
    print(error_list)

# Function used to kill the program entirely.

def kill():
    sys.exit()


while True:
    Tk().withdraw()

    ms         = 0
    user_data  = []
    error_list = []

    patterns_file  = open("patterns.txt", 'r', encoding="utf-8")
    patterns_lines = [line.rstrip('\n') for line in patterns_file]

    pattern = generate_pattern(patterns_lines[0])
    meter   = int(patterns_lines[0].split("|")[0])
    end     = len(patterns_lines[0].split("|")[1])

    ms_values = generate_ms_values(pattern, meter, end)

    root = Tk()
    root.title("Rhythm Data Collecting")

    root.bind("z", record_left)
    root.bind("x", record_right)

    time_label = Label(root, fg="black")
    time_label.pack()

    Label(root, fg="red", text="Use z/x to tap pattern.").pack()

    Button(root, fg="blue", text="Start!", command=first_load).pack()

    realtime_canvas = Canvas(root, width=500, height=500)
    realtime_canvas.pack()

    results = Label(root, fg="black")
    results.pack()

    Button(root, fg="red", text="Show Results", command=show_results).pack()

    # If window is closed, stop the program.
    root.protocol("WM_DELETE_WINDOW", kill)

    root.mainloop()
