from tkinter import *
import time
import sys
import analyse
from winsound import PlaySound, SND_FILENAME, SND_ASYNC, SND_NOSTOP


# Function to be used to initialize the timer.

def first_load():
    # Variable relative_time is the time when the user has clicked the button to start timer.
    global relative_time, ms, ms_values, realtime_canvas, user_data, sound_list, user_can_input

    user_data      = []
    ms             = 0
    relative_time  = int(round(time.time() * 1000)) + 2000
    user_can_input = True

    sound_list = [x[0] for x in ms_values if x[1][-1].isupper()]

    tick()
                                             

# Function to be used to run the timer and update the real time stuff

def tick():
    # Variable ms is the time that constantly goes up during the timer.
    global ms, ms_values, realtime_canvas, results, user_data, sound_list, user_can_input
    time_label.after(30, tick)
    ms = int(round(time.time() * 1000)) - relative_time
    time_label["text"] = "Timer: {}ms".format(ms)

    realtime_canvas.delete("all")

    if ms > ms_values[-1][0]:  # User can't input once pattern ends.
        user_can_input = False

    if analyse.order_messed(user_data, ms_values) != -1:  # User can't input if they mess up.
        user_can_input = False

    judgeline_ypos   = 372 # px from top
    judgeline_height = 6   # px
    realtime_canvas.create_rectangle(0, judgeline_ypos, 500, judgeline_ypos + judgeline_height, fill="#00ff00")

    if user_can_input:
        draw_pulses(ms, ms_values, realtime_canvas)
        sound_list = play_sounds(sound_list, ms)

def play_sounds(sound_list, time):
    return_sound_list = sound_list
    offset            = -100
    for i in sound_list:
        if time > i+offset:
            return_sound_list = sound_list[1:]
            PlaySound("tick.wav", SND_FILENAME|SND_ASYNC)
    return return_sound_list

def draw_pulses(time, pattern, canvas):
    judgeline_ypos   = 372  # px from top
    judgeline_height = 6    # px
    
    # ms/px
    scale = 0.5

    # px
    note_height = 20
    note_width  = 100
    
    # ms from judge line
    t_start = judgeline_ypos/scale
    t_end   = 0
    t_judge = 50


    column_seperation = 100 # px the left side and right side are sepreated by
    column_x_offset   = 200  # px the column are move to the right

    def left():  return column_x_offset - column_seperation
    def right(): return column_x_offset + column_seperation

    for note in pattern:
        note_xpos = left() if note[1].lower() == "l" else right()
        fill_color = "#dddddd"
        
        if time + t_start > note[0] > time - t_end:
            if time + t_judge > note[0] > time - t_judge:
                fill_color = "#ff0000"
            
            x1 = note_xpos
            y1 = (t_start - note[0] + time)*scale
            x2 = x1 + note_width
            y2 = y1 + note_height
            
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)


def generate_pattern(pattern_string):
    pattern      = []
    split_string = pattern_string.split("|")[1]

    for i in range(len(split_string)):
        if split_string[i] in ["l", "r", "L", "R"]: pattern.append([i, split_string[i]])

    return pattern


def generate_ms_values(pattern, meter, end):
    last_end     = 0
    total_length = end
    pattern_list = []
    for bpm in range(120, 185, 5):
        local_bpm_list = pattern
        ms_between = 60000 / (bpm * meter)
        local_bpm_list = [[x[0]*ms_between + last_end, x[1]] for x in local_bpm_list]
        last_end += total_length * ms_between
        pattern_list += local_bpm_list

    return pattern_list


def record_left(e):
    global ms, user_data, ms_values, user_can_input
    if user_can_input: user_data.append((ms, "l"))


def record_right(e):
    global ms, user_data, ms_values, user_can_input
    if user_can_input: user_data.append((ms, "r"))


def show_results():
    global user_data, ms_values, results, error_list

    error = analyse.order_messed(user_data, ms_values)

    print(error)
    analyse.show_hit_error_plot(user_data, ms_values)
    error_list.append(error)
    print(error_list)

# Function used to kill the program entirely.

def kill():
    sys.exit()

def send_results():
    nickname = user_entry.get()
    print(nickname)

    if(nickname != ""):
        try: user_file  = open("user_data.txt", 'r', encoding="utf-8")
        except FileNotFoundError as e:
            print(str(e))
            print('If the file really exist, make sure you are you running gui.py from within the folder it is? cd inside of it if not')
            exit(-1 )

        user_lines = [line.rstrip('\n') for line in user_file]

        for i, line in user_lines:
            if(nickname in user_lines):
                print("Username found.")

    else:
        print("Nickname can't be empty : " + nickname)
    

while True:
    Tk().withdraw()

    ms         = 0
    user_data  = []
    error_list = []

    try: patterns_file  = open("patterns.txt", 'r', encoding="utf-8")
    except FileNotFoundError as e:
        print(str(e))
        print('If the file really exist, make sure you are you running gui.py from within the folder it is? cd inside of it if not')
        exit(-1 )

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

    v = StringVar()

    Label(root, fg="black", text="Insert your nickname").pack()
    user_entry = Entry(root)
    user_entry.pack()
    
    Button(root, fg="blue", text="Start!", command=first_load).pack()
    
    realtime_canvas = Canvas(root, width=500, height=500)
    realtime_canvas.pack()

    results = Label(root, fg="black")
    results.pack()

    Button(root, fg="red", text="Show Results", command=show_results).pack()
    Button(root, fg="red", text="Send Results", command=send_results).pack()

    # If window is closed, stop the program.
    root.protocol("WM_DELETE_WINDOW", kill)

    root.mainloop()
