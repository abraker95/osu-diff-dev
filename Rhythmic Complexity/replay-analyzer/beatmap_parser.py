import requests


# To find where the hit objects start in the .osu file
def find_start(lines):
    line_number = 0
    for x in lines:
        if x == "[HitObjects]":
            return line_number + 1
        line_number += 1

# Return the lines that contain hit object data.
def return_hitobject_lines(lines):
    return lines[find_start(lines):]

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

# Input is a .osu file, output the times of the hit objects.
def file_times(lines):
    map_lines = lines[find_start(lines):]

    return return_times(map_lines)

# Input is a .osu file, output the times/x/y positions of the hit objects.
def return_hitobject_data(lines, speed_multiplier, hardrock):
    hitobject_lines     = return_hitobject_lines(lines)
    hitobject_data_list = []

    for line in hitobject_lines:
        hitobject_comma_split = line.split(",")

        x = int(hitobject_comma_split[0])
        y = int(hitobject_comma_split[1])

        if hardrock:
            y = 384 - y

        time = int(int(hitobject_comma_split[2]) / speed_multiplier)

        if not (int(hitobject_comma_split[3]) & 0b1000): hitobject_data_list.append((x, y, time))

    return hitobject_data_list

# Input is a .osu file, output the AR of that map.
def return_ar(lines, hardrock, easy):
    od = 0

    multiplier = 1
    if hardrock: multiplier = 1.4
    if easy: multiplier = 0.5

    for line in lines:
        if line.split(":")[0] == "OverallDifficulty":
            od = float(line.split(":")[1])
        if line.split(":")[0] == "ApproachRate":
            return min(10, multiplier * float(line.split(":")[1]))
    return min(10, multiplier * od)

# Input is a .osu file, output the CS radius of that map.
def return_cs_radius(lines, hardrock, easy):
    multiplier = 1
    if hardrock: multiplier = 1.3
    if easy: multiplier = 0.5

    for line in lines:
        if line.split(":")[0] == "CircleSize":
            cs = multiplier * float(line.split(":")[1])

    return (109 - 9*cs)/2

# Output the name of the mp3 file.
def mp3_name(lines):
    for i in lines:
        space_split_line = i.split(" ")
        if space_split_line[0] == "AudioFilename:":
            return " ".join(space_split_line[1:])