import requests


# To find where the hit objects start in the .osu file
def find_start(lines):
    line_number = 0
    for x in lines:
        if x == "[HitObjects]":
            return line_number + 1
        line_number += 1

# Return the ms times of the hit objects.
def return_times(lines):
    times = []

    for line in lines:
        split_line = line.split(",")
        time = int(split_line[2])

        if not (int(split_line[3]) & 0b1000):
            times.append(time)

    return times

# Input is a beatmap id, output the times of the hit objects.
def beatmap_times(b_id):
    b_link    = "https://osu.ppy.sh/osu/{}".format(b_id)
    file      = requests.get(b_link).text.splitlines()
    map_lines = file[find_start(file):]

    return return_times(map_lines)