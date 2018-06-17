from tkinter import *
import time
import sys
import analyse
from winsound import PlaySound, SND_FILENAME, SND_ASYNC


# Function to be used to initialize the timer.

def start_action():
    # Variable relative_time is the time when the user has clicked the button to start timer.
    global relative_time, note_hits, ms, pattern_data, realtime_canvas, user_data, sound_list, user_can_input, id_pattern, user_entry, bpm_entry

    user_data      = []
    id_pattern     = patterns_lines[0].split("|")[0]
    ms             = 0
    relative_time  = int(round(time.time() * 1000)) + 2000
    user_can_input = True
    sound_list     = [x[0] for x in pattern_data if x[1][-1].isupper()]

    user_entry['state'] = DISABLED
    bpm_entry['state']  = DISABLED

    tick()
                                             

# Function to be used to run the timer and update the real time stuff

def tick():
    # Variable ms is the time that constantly goes up during the timer.
    global ms, pattern_data, realtime_canvas, user_data, sound_list, user_can_input
    
    time_label.after(30, tick)
    ms = int(round(time.time() * 1000)) - relative_time

    realtime_canvas.delete("all")

    pattern_ended  = (ms > pattern_data[-1][0])
    user_messed_up = (analyse.get_user_fail(user_data, pattern_data, ms) != pattern_data[-1][0])

    # User can't input once pattern ends and can't input if they mess up.
    if pattern_ended or user_messed_up: user_can_input = False

    # Set timer to 0 if user can't input
    if not user_can_input: ms = 0
    time_label["text"] = "Timer: {}ms".format(ms)

    draw_judgeline(realtime_canvas, user_can_input)

    if user_can_input:
        draw_pulses(realtime_canvas, ms, pattern_data)
        sound_list = play_sounds(sound_list, ms)

    draw_hiterror_bar(realtime_canvas)


def play_sounds(sound_list, time):
    return_sound_list = sound_list
    offset            = -100

    for i in sound_list:
        if time > i+offset:
            return_sound_list = sound_list[1:]
            PlaySound("tick.wav", SND_FILENAME|SND_ASYNC)

    return return_sound_list


def draw_pulses(canvas, time, pattern):
    judgeline_ypos   = 372  # px from top
    judgeline_height = 6    # px
    
    # ms/px
    scale = 0.7

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


def draw_judgeline(canvas, user_can_input):
    # Set judgeline color to red if user can input, green if user can't input
    if user_can_input: judgeline_color = "#00ff00"
    else:              judgeline_color = "#ff0000"

    # Judgeline draw parameters
    judgeline_ypos   = 372 # px from top
    judgeline_height = 6   # px

    canvas.create_rectangle(0, judgeline_ypos, 500, judgeline_ypos + judgeline_height, fill=judgeline_color)
    

def draw_hiterror_bar(canvas):
    # Hit error bar draw parameters
    hit_error_draw_offset = 250
    hit_error_scale       = 1.5
    hit_error_thickness   = 2

    # Draw the 0ms hit error reference point
    canvas.create_rectangle(hit_error_draw_offset, 440, hit_error_draw_offset + hit_error_thickness, 450, fill="#0000ff")

    # Draw the 50 hit window.
    canvas.create_rectangle(hit_error_draw_offset - hit_error_scale*129.5,
                                     450,
                                     hit_error_draw_offset + hit_error_scale*129.5,
                                     500, fill="#FE9A2E")

    # Draw the 100 hit window.
    canvas.create_rectangle(hit_error_draw_offset - hit_error_scale * 83.5,
                                     450,
                                     hit_error_draw_offset + hit_error_scale * 83.5,
                                     500, fill="#2EFE2E")

    # Draw the 300 hit window.
    canvas.create_rectangle(hit_error_draw_offset - hit_error_scale * 37.5,
                                     450,
                                     hit_error_draw_offset + hit_error_scale * 37.5,
                                     500, fill="#00FFFF")

    # Draw the hit error ticks
    hit_errors = analyse.get_hit_errors(user_data, pattern_data)
    if hit_errors:
        for hit_error in hit_errors:
            xpos = hit_error*hit_error_scale + hit_error_draw_offset
            canvas.create_rectangle(xpos, 450, xpos + hit_error_thickness, 500, fill="#ffffff")
 

def generate_pattern(pattern_string):
    pattern = []

    for i in range(len(pattern_string)):
        if pattern_string[i] in ["l", "r", "L", "R"]: pattern.append([i, pattern_string[i]])

    return pattern


def generate_ms_values(meter, repeat, pattern, total_length):
    last_end     = 0    # Keeps track the end of the last repeat
    pattern_list = []   # Final, processed, notes
    bpm          = 180
    ms_between   = 60000 / (bpm * meter)

    for i in range(repeat):
        pattern_list += [[x[0]*ms_between + last_end, x[1]] for x in pattern]
        last_end += total_length * ms_between

    return pattern_list


def record_left(e):
    global ms, user_data, pattern_data, user_can_input
    if user_can_input: user_data.append((ms, "l"))


def record_right(e):
    global ms, user_data, pattern_data, user_can_input
    if user_can_input: user_data.append((ms, "r"))


def show_results():
    global user_data, pattern_data, error_list

    error = analyse.get_user_fail(user_data, pattern_data, pattern_data[-1][0])
    print(error)

    analyse.show_hit_error_plot(user_data, pattern_data)
    error_list.append(error)
    print(error_list)


# Function used to kill the program entirely.
def kill():
    sys.exit()


def send_results():
    global user_data, id_pattern
    nickname = user_entry.get()

    if nickname == "":
        print("Nickname can't be empty")
        return

    if not user_data:
        print("You have to start before sending infos")
        return

    try: user_file = open("user_data.txt", 'a', encoding="utf-8")
    except FileNotFoundError as e:
        print(str(e))
        print('If the file really exist, make sure you are you running gui.py from within the folder it is? cd inside of it if not')
        exit(-1)

    datas = ""
    for data in user_data:
        # Concatenate every data with ':' + ms + key
        datas += ":" + str(data[0]) + data[1]

    user_file.write("\n" + nickname + ":" + id_pattern + datas)
    user_data = []
    print("Saved !")    


while True:
    Tk().withdraw()
    
    user_can_input = False
    ms             = 0
    user_data      = []
    error_list     = []

    try: patterns_file  = open("patterns.txt", 'r', encoding="utf-8")
    except FileNotFoundError as e:
        print(str(e))
        print('If the file really exist, make sure you are you running gui.py from within the folder it is? cd inside of it if not')
        exit(-1 )

    patterns_lines = [line.rstrip('\n') for line in patterns_file]
    pattern_param  = patterns_lines[0].split("|")

    meter        = int(pattern_param[1])
    repeat       = int(pattern_param[2])
    pattern      = pattern_param[3]
    total_length = len(pattern_param[3])

    if len(pattern) == 0:
        print('No pattern loaded! Check patterns.txt')
        exit(-1 )

    pattern = generate_pattern(pattern)
    pattern_data = generate_ms_values(meter, repeat, pattern, total_length)

    root = Tk()
    root.title("Rhythm Data Collecting")

    root.bind("x", record_left)
    root.bind("c", record_right)

    time_label = Label(root, fg="black")
    time_label.pack()

    keys_label = Label(root, fg="red", text="Use x/c to tap pattern.")
    keys_label.pack()

    # BPM input
    bpm_frame = Frame(root)

    Label(bpm_frame, fg="black", text="Enter pattern BPM: ").pack(side="left")

    bpm_entry = Entry(bpm_frame)
    bpm_entry.pack()

    bpm_frame.pack()

    # Username input
    username_frame = Frame(root)

    Label(username_frame, fg="black", text="Username: ").pack(side="left")

    user_entry = Entry(username_frame)
    user_entry.pack(side="right")

    username_frame.pack()

    start_button = Button(root, fg="blue", text="Start!", command=start_action)
    start_button.pack()
    
    realtime_canvas = Canvas(root, width=500, height=500)
    realtime_canvas.pack()

    results = Label(root, text="^ This is the timing window. ^\nAny taps out of this range count as an error\nThis is the hit error bar for OD7.", fg="black").pack()

    button_frame = Frame(root)
    Button(button_frame, fg="red", text="Show Results", command=show_results).pack(side="left")
    Button(button_frame, fg="red", text="Send Results", command=send_results).pack(side="right")
    button_frame.pack()

    # If window is closed, stop the program.
    root.protocol("WM_DELETE_WINDOW", kill)
    root.mainloop()
