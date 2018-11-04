import matplotlib.pyplot as plt

def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5

# Find places where the player tapped.
def find_tap_data(replay_data_list, speed_multiplier):
    current_time  = 0
    left_pressed  = False
    right_pressed = False
    tap_list      = []

    for i in replay_data_list:
        current_time += i.time_since_previous_action

        if i.keys_pressed & 0b100 | i.keys_pressed & 0b1:
            if not left_pressed:
                tap_list.append((i.x, i.y, int(current_time/speed_multiplier)))
            left_pressed = True
        else:
            left_pressed = False

        if i.keys_pressed & 0b1000 | i.keys_pressed & 0b10:
            if not right_pressed:
                tap_list.append((i.x, i.y, int(current_time/speed_multiplier)))
            right_pressed = True
        else:
            right_pressed = False

    return tap_list

# Find tapped places which correspond to hit objects.
def find_hitobject_tap_data(tap_list, hitobject_list, cs_radius):
    hit_window_error         = 300
    hitobject_duplicate_list = hitobject_list[:]
    tap_duplicate_list       = tap_list[:]
    hitobject_tap_list       = []

    i = 0
    while i < len(hitobject_duplicate_list):
        hitobject = hitobject_duplicate_list[i]
        for j in range(len(tap_duplicate_list)):
            tap           = tap_duplicate_list[j]
            touching_note = distance((tap[0], tap[1]), (hitobject[0], hitobject[1])) < cs_radius

            if hitobject[2] - hit_window_error < tap[2] < hitobject[2] + hit_window_error and touching_note:
                hitobject_duplicate_list.pop(i)
                tap_duplicate_list.pop(j)
                hitobject_tap_list.append(tap)
                i -= 1
                break
        i += 1

    return hitobject_tap_list

# Find tap error
def tap_error(hitobject_tap_data, hitobject_list, cs_radius):
    hit_window_error = 300

    hitobject_duplicate_tap_data = hitobject_tap_data[:]
    hitobject_duplicate_list     = hitobject_list[:]

    time_list  = []
    error_list = []

    i = 0
    while i < len(hitobject_duplicate_list):
        hitobject = hitobject_duplicate_list[i]
        for j in range(len(hitobject_duplicate_tap_data)):
            tap           = hitobject_duplicate_tap_data[j]
            touching_note = distance((tap[0], tap[1]), (hitobject[0], hitobject[1])) < cs_radius

            if hitobject[2] - hit_window_error < tap[2] < hitobject[2] + hit_window_error and touching_note:
                hitobject_duplicate_list.pop(i)
                hitobject_duplicate_tap_data.pop(j)
                time_list.append(hitobject[2])
                error_list.append(tap[2] - hitobject[2])
                i -= 1
                break
        i += 1

    return time_list, error_list

# Graph tap error
def graph_tap_error(time_list, error_list):

    absolute_error_list = [abs(i) for i in error_list]

    average_values = 20

    graph = plt.figure()

    ax_1 = graph.add_subplot(211)
    ax_1.plot(time_list, error_list, color='red', label="Error")
    ax_1.plot(time_list[int(average_values / 2):int(-average_values / 2)],
              [sum(error_list[i:i + average_values]) / average_values for i in
               range(len(error_list) - average_values)], color='blue', label="Moving Average")

    ax_1.legend(loc="upper right")

    ax_2 = graph.add_subplot(212)
    ax_2.plot(time_list, absolute_error_list, color='red', label="Absolute Error")
    ax_2.plot(time_list[int(average_values / 2):int(-average_values / 2)],
              [sum(absolute_error_list[i:i + average_values]) / average_values for i in
               range(len(absolute_error_list) - average_values)], color='blue', label="Moving Average")

    ax_2.legend(loc="upper right")

    plt.show()

# Check if hitcircle needs to be highlighted
def hitcircle_highlight(hitobject_time, hitobject_list, error_list, highlight_threshold):
    for i in range(len(hitobject_list)):
        hitobject = hitobject_list[i]
        if hitobject == hitobject_time:
            error = error_list[i]
            if abs(error) > highlight_threshold:
                return True
    return False