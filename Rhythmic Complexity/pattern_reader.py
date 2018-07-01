def read_pattern_file(pattern_file):
    try: patterns_file  = open(pattern_file, 'r', encoding="utf-8")
    except FileNotFoundError as e:
        print(str(e))
        print('If the file really exist, make sure you are you running gui.py from within the folder it is? cd inside of it if not')
        exit(-1 )

    patterns_lines = [line.rstrip('\n') for line in patterns_file]
    pattern_param  = patterns_lines[0].split("|")

    id_pattern     = str(pattern_param[0])
    meter          = int(pattern_param[1])
    repeat         = int(pattern_param[2])
    pattern_string = str(pattern_param[3])
    total_length   = len(pattern_param[3])

    if len(pattern_string) == 0:
        print('No pattern loaded! Check patterns.txt')
        exit(-1)

    pattern_data = (id_pattern, meter, repeat, pattern_string, total_length)
    return pattern_data


def read_pattern(pattern_string):
    left_pattern = []
    right_pattern = []

    for i in range(len(pattern_string)):
        if pattern_string[i] in ["l", "L"]: left_pattern.append(i)
        if pattern_string[i] in ["r", "R"]: right_pattern.append(i)

    return left_pattern, right_pattern


def generate_ms_values(meter, repeat, pattern_string, total_length, bpm):
    left_pattern, right_pattern = read_pattern(pattern_string)

    last_end   = 0    # Keeps track the end of the last repeat
    left_ms    = []   # Final, processed, notes
    right_ms   = []
    ms_between = 60000 / (bpm * meter)

    for i in range(repeat):
        left_ms  += [x*ms_between + last_end for x in left_pattern]
        right_ms += [x*ms_between + last_end for x in right_pattern]
        last_end += total_length * ms_between

    return left_ms, right_ms