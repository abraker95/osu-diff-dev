import diff_calc
import beatmap_parser
import matplotlib.pyplot as plt


b_id    = int(input("beatmap id "))
ms_list = beatmap_parser.beatmap_times(b_id)

delay_list, difficulty_list, delay_difficulty_list                  = diff_calc.delay_difficulty(ms_list)
rate_change_list, rate_difficulty_list, rate_change_difficulty_list = diff_calc.rate_change_difficulty(ms_list)

total_delay_difficulty       = diff_calc.total_difficulty(delay_difficulty_list)
total_rate_change_difficulty = diff_calc.total_difficulty(rate_change_difficulty_list)

print("Total Delay Difficulty: {:.4f}".format(total_delay_difficulty))
print("Total Rate Change Difficulty: {:.4f}".format(total_rate_change_difficulty))

strains_graph = plt.figure()

ax_1 = strains_graph.add_subplot(321)
ax_1.plot(ms_list[3:], delay_list, color='red', label="Delay")
ax_1.legend(loc="upper right")

ax_2 = strains_graph.add_subplot(323)
ax_2.plot(ms_list[3:], difficulty_list, color='red', label="Difficulty")
ax_2.legend(loc="upper right")

ax_3 = strains_graph.add_subplot(325)
ax_3.plot(ms_list[3:], delay_difficulty_list, color='red', label="Difficulty * Delay")
ax_3.plot(ms_list[13:-10], [sum(delay_difficulty_list[i:i+20])/20 for i in range(len(delay_difficulty_list)-20)], color='blue', label="Moving Average")
ax_3.legend(loc="upper right")

ax_4 = strains_graph.add_subplot(322)
ax_4.plot(ms_list[4:], rate_change_list, color='red', label="Rate Change")
ax_4.legend(loc="upper right")

ax_5 = strains_graph.add_subplot(324)
ax_5.plot(ms_list[4:], rate_difficulty_list, color='red', label="Difficulty")
ax_5.legend(loc="upper right")

ax_6 = strains_graph.add_subplot(326)
ax_6.plot(ms_list[4:], rate_change_difficulty_list, color='red', label="Difficulty * Rate Change")
ax_6.plot(ms_list[14:-10], [sum(rate_change_difficulty_list[i:i+20])/20 for i in range(len(rate_change_difficulty_list)-20)], color='blue', label="Moving Average")
ax_6.legend(loc="upper right")

plt.show()