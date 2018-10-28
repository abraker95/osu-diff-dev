# Return hitobject data on screen, based on hitobject list, AR and current ms time
def return_onscreen_hitobjects(hitobject_list, ar, current_ms):
    hitobjects_on_screen = []

    if ar <= 5:
        on_screen_time = 1800 - 120*ar
    else:
        on_screen_time = 1950 - 150*ar
    amount_of_fadein_time = 200

    for hitobject in hitobject_list:
        hitobject_x    = hitobject[0]
        hitobject_y    = hitobject[1]
        hitobject_time = hitobject[2]

        hitobject_start_on_screen    = hitobject_time - on_screen_time
        hitobject_start_full_opacity = hitobject_start_on_screen + amount_of_fadein_time

        if hitobject_start_on_screen < current_ms < hitobject_time:
            if current_ms > hitobject_start_full_opacity:
                hitobject_opacity = 1
            else:
                hitobject_opacity = (current_ms - hitobject_start_on_screen) / amount_of_fadein_time

            hitobjects_on_screen.append((hitobject_x, hitobject_y, hitobject_opacity))

    return hitobjects_on_screen

# Return approach circle data on screen, based on hitobject list, AR, CS radius and current ms time
def return_onscreen_approach_circles(hitobject_list, ar, cs_radius, current_ms):
    approach_circles_on_screen = []

    if ar <= 5:
        on_screen_time = 1800 - 120*ar
    else:
        on_screen_time = 1950 - 150*ar
    amount_of_fadein_time = 200

    for hitobject in hitobject_list:
        hitobject_x    = hitobject[0]
        hitobject_y    = hitobject[1]
        hitobject_time = hitobject[2]

        approach_circle_start_on_screen    = hitobject_time - on_screen_time
        approach_circle_start_full_opacity = approach_circle_start_on_screen + amount_of_fadein_time

        if approach_circle_start_on_screen < current_ms < hitobject_time:
            if current_ms > approach_circle_start_full_opacity:
                approach_circle_opacity = 1
            else:
                approach_circle_opacity = (current_ms - approach_circle_start_on_screen) / amount_of_fadein_time

            time_from_end = hitobject_time - current_ms
            approach_circle_radius = (1 + time_from_end / on_screen_time) * cs_radius

            approach_circles_on_screen.append((hitobject_x, hitobject_y, approach_circle_radius, approach_circle_opacity))

    return approach_circles_on_screen