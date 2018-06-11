def find_start(lines):
    line_number = 0
    for x in lines:
        if x == "[HitObjects]":
            return line_number + 1
        line_number += 1

def return_times(lines):
    times = []

    for line in lines:
        split_line = line.split(",")
        time = int(split_line[2])

        if not (int(split_line[3]) & 0b1000):
            times.append(time)

    return times