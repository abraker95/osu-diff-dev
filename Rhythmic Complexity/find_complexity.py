import random

def find_finger_placement(input_rhythm):
    '''
    slider_ends = [i for i in range(len(input_rhythm) - 1) if input_rhythm[i] == "=" and input_rhythm[i + 1] != "="]
    slider = [i for i in range(len(input_rhythm) - 1) if input_rhythm[i] == "="]
    '''
    left_pulses = [input_rhythm[0]]
    right_pulses = []
    for i in range(len(input_rhythm) - 1):
        if input_rhythm[i + 1] - input_rhythm[i] < 111:
            if input_rhythm[i] in right_pulses:
                left_pulses.append(input_rhythm[i + 1])
            else:
                right_pulses.append(input_rhythm[i + 1])
        else:
            '''
            if pulses[i + 1] - 1 in slider_ends:
                if pulses[i] in right_pulses:
                    left_pulses.append(pulses[i + 1])
                else:
                    right_pulses.append(pulses[i + 1])
            else:
                left_pulses.append(pulses[i + 1])
            '''
            left_pulses.append(input_rhythm[i + 1])

    return left_pulses, right_pulses


def evaluate_rhythm(pulses):
    offset_weights = []
    speed_bonuses = []

    for n in range(len(pulses) - 2):
        first_pulse  = pulses[n]
        second_pulse = pulses[n + 1]
        third_pulse  = pulses[n + 2]

        average     = (first_pulse + third_pulse) / 2    # half meter
        beat_length = third_pulse - first_pulse          # meter time interval

        speed_bonus = 10 ** (450 / max(second_pulse - first_pulse, third_pulse - second_pulse))
        speed_bonuses.append(speed_bonus)

        offset_distance = abs(second_pulse - average)        # note offset from half meter
        offset_weight   = 1 + (offset_distance/beat_length)  # 1.0 + ratio
        offset_weights.append(offset_weight)

    final_weights = [ offset_weights[i]*speed_bonuses[i] for i in range(len(speed_bonuses) - 1) ]

    '''
    for i, j, k in zip(speed_bonuses, meters, pulses):
        print("{} | {} | {}".format(i, j, k))
    '''

    return [offset_weights, pulses, speed_bonuses, final_weights]

def determine_difficulty(left_weights, right_weights):
    final_weights = left_weights + right_weights
    sorted_weights = sorted(final_weights, reverse=True)
    print(sorted_weights)
    final_difficulty = sum([sorted_weights[i] * 0.9 ** i for i in range(len(sorted_weights))])

    return final_difficulty

def abraker_triplet(rhythms):
    left_pulses, right_pulses = find_finger_placement(rhythms)

    left_finger = evaluate_rhythm(left_pulses)
    right_finger = evaluate_rhythm(right_pulses)

    return left_finger, right_finger





'''
chatting space

so how far is the code updated with the stuff from repl?
The strains are calculated differently. We got rid of meter, added speed bonus, and added the determine difficulty function
'''