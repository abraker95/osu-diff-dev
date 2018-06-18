import matplotlib.pyplot as plt


'''
# @param hits:     list of hit timings the user made on the notes
# @param pattern:  list of note timings the user attempts to make hits on
# @param max_hits: look at the last N hits
# @return: A list of max_hits size containing hit errors between the user's hit timing and note's timing
'''
def get_hit_errors(hits, pattern, max_hits=10):
    if len(hits) == 0: return []
    hit_errors = []

    # Starts from last note
    start = len(hits) - 1

    # count -> 0 if we dont have enough notes to fill in number of max_hits, otherwise it goes from count -> count-max_hits
    stop = -1 if len(hits) < max_hits else len(hits) - max_hits - 1

    for i in range(start, stop, -1):
        # Since we are counting high -> low, count until we have reached
        # lower set of hit to which we can relate to the pattern
        if i >= len(pattern): continue

        # If we recorded more hits than there are notes, we can stop because
        # every hit corresponds to one note, and others don't count
        if len(hit_errors) > len(pattern): break

        # Correlate the hit to the note 1:1
        hit_ms = hits[i][0]
        note_ms = pattern[i][0]
        hit_errors.append(hit_ms - note_ms)

    return hit_errors


def get_user_fail(user_data, pattern, current_time):
    errors = 0

    # If the user hasn't made an input and the pattern has reached its 3rd note, fail.
    if len(user_data) == 0 and current_time > pattern[2][0]: return 0

    if len(user_data) > 0:
        for i in range(min(len(pattern), len(user_data))):
            # If the user is out of the timing window,
            # or their finger pattern doesn't match the pattern given, it is an error.

            max_hit_window = 129.5  # ms

            in_timing_window          = (abs(pattern[i][0] - user_data[i][0]) < max_hit_window)
            pattern_placement_correct = (pattern[i][1].lower() == user_data[i][1])

            if not (in_timing_window and pattern_placement_correct):
                errors += 1

            # The user fails once they hit 3 errors.
            if errors == 3:
                return user_data[0][0]

    # If the user hasn't made an input in a while, fail.
    inactivity_time = 500  # ms
    if len(user_data) > 0:
        if user_data[-1][0] < current_time-500: return user_data[-1][0]

    return pattern[-1][0]


def show_hit_error_plot(user, pattern):
    # make pattern list same length as user data
    pattern_check = pattern[:len(user)]

    error = [i[0] - j[0] for i, j in zip(user, pattern_check)]

    graph = plt.figure()

    ax_1 = graph.add_subplot(111)
    ax_1.plot([i[0] for i in pattern_check], error, color='red')
    ax_1.set_xlabel("Time Elapsed in ms")
    ax_1.set_ylabel("Hit Error in ms")
    plt.title("Hit Error vs Time Elapsed")

    plt.show()