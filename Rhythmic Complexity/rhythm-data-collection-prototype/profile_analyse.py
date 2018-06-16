def get_profiles(name, idpattern):

    profile = []
    try: user_file = open("user_data.txt", 'r', encoding="utf-8")
    except FileNotFoundError as e:
        print(str(e))
        print('If the file really exist, make sure you are you running gui.py from within the folder it is? cd inside of it if not')
        exit(-1)

    user_lines = [line.rstrip('\n') for line in user_file]
    profile.append(name)

    averagevalue = 0
    losingpoints = []

    for line in user_lines:
        # Something strange with the if
        if(line.split(":")[0] == name and line.split(":")[1] == idpattern):
            # Get the last value
            number = line.split[line.count(':')]
            # Remove the l or r
            number.replace("l", "").replace("r", "")
            # Keep it on a list
            losingpoints.append(int(number))
            # Do a sum up with previous one to...
            averagevalue += int(number)
    # Do an average at the end
    averagevalue = averagevalue / len(losingpoints)

    # Insert value and return it
    profile.append(averagevalue, losingpoints)

    return profile

# Test
profile = get_profiles("Arrcival", 1)
print(profile[0], profile[1], profile[2])