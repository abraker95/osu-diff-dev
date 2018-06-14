import matplotlib.pyplot as plt

def order_messed(user, pattern):
    errors = 0
    current_user    = user
    current_pattern = pattern

    for i in current_pattern:
        current_pattern = current_pattern[1:]
        current_user = current_user[1:]
        if len(current_pattern) == 0 or len(current_user) == 0: return [[[-1]]]

        if not (abs(current_pattern[0][0] - current_user[0][0]) < 200
                and current_pattern[0][1].lower() == current_user[0][1]):
            errors += 1

        if errors == 3:
            if len(current_user) > 10:
                user_error = current_user[0:10]
            else:
                user_error = current_user[0:]

            if len(current_pattern) > 10:
                pattern_error = current_pattern[0:10]
            else:
                pattern_error = current_pattern[0:]

            return [user_error, pattern_error]


def show_hit_error_plot(user, pattern):
    errors = 0
    messing_up_index = min(len(pattern), len(user))

    for i in range(min(len(pattern), len(user))):
        if pattern[i][1].lower() != user[i][1]:
            errors += 1
        if errors == 3:
            messing_up_index = i

    user_check    = user[:messing_up_index]
    pattern_check = pattern[:messing_up_index]
    error         = [i[0]-j[0] for i,j in zip(user_check, pattern_check)]

    graph = plt.figure()

    ax_1 = graph.add_subplot(111)
    ax_1.plot([i[0] for i in pattern_check], error, color='red')
    ax_1.set_xlabel("Time Elapsed in ms")
    ax_1.set_ylabel("Hit Error in ms")
    plt.title("Hit Error vs Time Elapsed")

    plt.show()