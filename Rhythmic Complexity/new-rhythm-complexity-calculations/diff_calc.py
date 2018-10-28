import math


# Return sameness of two intervals
def eq(value1, value2, sigma):
    return math.e ** -((1-value1/value2) * 1/(2*sigma)) ** 2

# Find an interval length
def interval(index, list):
    return (list[index] - list[index-1])

# Find a total map value based on its list of difficulty values
def total_difficulty(difficulty_list):
    sorted_difficulty_list   = sorted(difficulty_list, reverse=True)
    weighted_difficulty_list = [sorted_difficulty_list[i] * 0.95 ** i for i in
                                range(len(sorted_difficulty_list))]

    return sum(weighted_difficulty_list)

# Return lists of delay difficulty from a list of ms values
def delay_difficulty(pattern_list):
    delay_list = []
    difficulty_list = []
    delay_difficulty_list = []

    pattern_list = [i/1 for i in pattern_list]

    for i in range(3, len(pattern_list)):
        delay = ((eq(interval(i, pattern_list), interval(i - 2, pattern_list), 0.09)) *
                 (1 - eq(interval(i - 1, pattern_list), interval(i, pattern_list), 0.09)) *
                 (1 - eq(interval(i - 1, pattern_list), interval(i - 2, pattern_list), 0.09)))

        '''
        print(eq(interval(i, pattern_list), interval(i - 1, pattern_list), 0.09))
        print(1 - eq(interval(i - 1, pattern_list), interval(i, pattern_list), 0.09))
        print(1 - eq(interval(i - 1, pattern_list), interval(i - 2, pattern_list), 0.09))
        '''

        A = 140
        B = 1.25
        C = 1

        difficulty = (A / interval(i - 2, pattern_list) +
                      B * interval(i - 2, pattern_list) /
                      (interval(i - 1, pattern_list) + (interval(i - 2, pattern_list) / C)))

        #print("{} {} {} {}: {}".format(pattern_list[i-3], pattern_list[i-2], pattern_list[i-1], pattern_list[i], delay))

        delay_list.append(delay)
        difficulty_list.append(difficulty)
        delay_difficulty_list.append(delay * difficulty)

    return delay_list, difficulty_list, delay_difficulty_list

# Return lists of rate change difficulty from a list of ms values
def rate_change_difficulty(pattern_list):
    rate_change_list = []
    difficulty_list = []
    rate_change_difficulty_list = []

    pattern_list = [i/1 for i in pattern_list]

    for i in range(4, len(pattern_list)):
        rate_change = ((eq(interval(i, pattern_list), interval(i - 1, pattern_list), 0.09)) *
                       (1 - eq(interval(i - 1, pattern_list), interval(i - 2, pattern_list), 0.09)) *
                       (eq(interval(i - 2, pattern_list), interval(i - 3, pattern_list), 0.09)))

        A = 100
        B = 0.1
        C = 1

        difficulty = (A / interval(i, pattern_list) +
                      B * interval(i - 2, pattern_list) /
                      (interval(i - 1, pattern_list) + (interval(i - 2, pattern_list) / C)))

        #print("{} {} {} {} {}: {}".format(pattern_list[i - 4], pattern_list[i - 3], pattern_list[i - 2], pattern_list[i - 1], pattern_list[i],
        #                                  rate_change * difficulty))

        rate_change_list.append(rate_change)
        difficulty_list.append(difficulty)
        rate_change_difficulty_list.append(rate_change * difficulty)

    return rate_change_list, difficulty_list, rate_change_difficulty_list