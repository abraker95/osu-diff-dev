import matplotlib.pyplot as plt


def get_pattern(idpattern):
    try: patterns_file = open("patterns.txt", 'r', encoding="utf-8")
    except FileNotFoundError as e:
        print(str(e))
        print('If the file really exist, make sure you are you running gui.py from within the folder it is? cd inside of it if not')
        exit(-1)

    patterns_lines = [pattern.rstrip('\n') for pattern in patterns_file]

    for i in patterns_lines:
        if int(i.split("|")[0]) == idpattern:
            return i.split("|")[4], int(i.split("|")[1]), int(i.split("|")[2]), int(i.split("|")[3])

    return ""


def get_hit_errors(idpattern, lines):
    # all this stuff is just converting the pattern into ms values
    hit_errors = []

    pattern_string, meter, start_bpm, end_bpm = get_pattern(idpattern)
    pattern_list = []

    for i in range(len(pattern_string)):
        if pattern_string[i] in ["l", "r", "L", "R"]: pattern_list.append([i, pattern_string[i]])

    last_end = 0
    total_length = len(pattern_string)
    pattern_ms_values = []

    for bpm in range(start_bpm, end_bpm+5, 5):
        local_bpm_list = pattern_list
        ms_between = 60000 / (bpm * meter)
        local_bpm_list = [x[0] * ms_between + last_end for x in local_bpm_list]
        last_end += total_length * ms_between
        pattern_ms_values += local_bpm_list

    # calculate hit error
    for line in lines:
        # turn user line into a list of ms values
        user_ms_values = line.split(":")[2:]
        user_ms_values = [int(i[:-1]) for i in user_ms_values]

        # make pattern list same length as user data
        pattern_ms_values = pattern_ms_values[:len(user_ms_values)]

        error_list = [[j, i - j] for i, j in zip(user_ms_values, pattern_ms_values)]

        for i in range(len(error_list)):
            print("{} {} {}".format(user_ms_values[i], pattern_ms_values[i], error_list[i]))

        hit_errors += error_list

    return hit_errors


def get_profiles(name, idpattern):
    profile = []

    try: user_file = open("user_data.txt", 'r', encoding="utf-8")
    except FileNotFoundError as e:
        print(str(e))
        print('If the file really exist, make sure you are you running gui.py from within the folder it is? cd inside of it if not')
        exit(-1)

    user_lines = [line.rstrip('\n') for line in user_file]
    profile.append(name)

    losingpoints = []

    for line in user_lines:
        if (line.split(":")[0] == name and int(line.split(":")[1]) == idpattern):
            number = line.split(":")[-1][:-1] # Get the last value and remove l/r
            losingpoints.append(int(number))  # Keep it on a list

    # Do an average at the end
    averagevalue = sum(losingpoints) / len(losingpoints)

    # Get hit errors
    hit_errors = get_hit_errors(idpattern, user_lines)

    # Insert value and return it
    profile += [averagevalue, losingpoints, hit_errors]

    return profile


def show_graphs(user, losingpoints, hit_error):
    graph = plt.figure()

    # plot fail point plot
    ax_1 = graph.add_subplot(211)
    ax_1.violinplot([losingpoints], showmeans=False, showmedians=True, widths=0.3)
    ax_1.set_title('User Fail Points')

    # plot hit error plot
    ax_2 = graph.add_subplot(212)
    ax_2.scatter([i[0] for i in hit_error], [i[1] for i in hit_error], color='red')
    ax_2.set_title('Hit Error vs Time Elapsed')

    # adding labels
    ax_1.set_xlabel('User')
    ax_1.set_ylabel('Fail Point')
    ax_2.set_xlabel('Time Elapsed')
    ax_2.set_ylabel('Hit Error')

    # add x-tick labels
    #ax_1.set_xticks(user)

    plt.show()

# Test
profile = get_profiles("Arrcival", 2)

show_graphs(profile[0], profile[2], profile[3])