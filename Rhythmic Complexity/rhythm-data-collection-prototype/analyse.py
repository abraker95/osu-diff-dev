import matplotlib.pyplot as plt

def order_messed(user, pattern):
    errors = 0
    current_user    = user
    current_pattern = pattern

    for i in current_pattern:
        current_pattern = current_pattern[1:]
        current_user = current_user[1:]
        if len(current_pattern) == 0 or len(current_user) == 0: return -1

        if not (abs(current_pattern[0][0] - current_user[0][0]) < 200
                and current_pattern[0][1].lower() == current_user[0][1]):
            errors += 1

        if errors == 3:
            return current_user[0][0]


def show_hit_error_plot(user, pattern):
    # make pattern list same length as user data
    pattern_check = pattern[:len(user)]

    error         = [i[0]-j[0] for i,j in zip(user, pattern_check)]

    graph = plt.figure()

    ax_1 = graph.add_subplot(111)
    ax_1.plot([i[0] for i in pattern_check], error, color='red')
    ax_1.set_xlabel("Time Elapsed in ms")
    ax_1.set_ylabel("Hit Error in ms")
    plt.title("Hit Error vs Time Elapsed")

    plt.show()