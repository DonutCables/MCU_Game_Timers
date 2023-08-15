from time import sleep, monotonic
from hardware import DISPLAY, RGB_LED, ENCODER, ENC, RED, RED_LED, BLUE, BLUE_LED

# Setting initial variables for use
position = ENCODER.position
last_position = position
MENU_OPTIONS = ["KotH", "Attrition", "Death Clicks", "Domination"]
menu_option_index = 0
RESTART_OPTIONS = ["Yes", "No"]
restart_option_index = 0
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_OFF = (0, 0, 0)

# Function to display LCD messages
def display_message(message):
    DISPLAY.clear()
    DISPLAY.print(message)

# Placeholder function for LED control
def rgb_control(color, pattern="solid", delay=0.005):
    global RGB_LED
    if pattern == "solid":
        RGB_LED.fill(color)
        RGB_LED.show()
    elif pattern == "chase":
        for i in range(RGB_LED.n):
            RGB_LED[i] = color
            sleep(delay)
            RGB_LED.show()
    elif pattern == "single_blink":
        for i in range(RGB_LED.n):
            RGB_LED[i] = color
            RGB_LED.show()
            sleep(delay)
            RGB_LED[i] = COLOR_OFF
            RGB_LED.show()
            sleep(delay)
    elif pattern == "all_blink":
        RGB_LED.fill(color)
        RGB_LED.show()
        sleep(delay)
        RGB_LED.fill(COLOR_OFF)
        RGB_LED.show()
        sleep(delay)
    print(color, pattern)

# Placeholder function for audio control
def audio_control(sound_id):
    #insert audio functionality here
    print(sound_id)

# Function to fetch human-readable strings from timer values
def timer_string(game_length):
    return f"{game_length // 60:02d}:{game_length % 60:02d}"

###

# Main menu for scrolling game options
def main_menu():
    global position, last_position, menu_option_index
    display_message("You're a nerd")
    rgb_control(COLOR_OFF, "solid")
    rgb_control(COLOR_RED, "chase", .0075)
    rgb_control(COLOR_BLUE, "chase", .0075)
    rgb_control(COLOR_GREEN, "chase", .0075)
    RED_LED.value = False
    BLUE_LED.value = False
    display_message(f"Select a game:\n{MENU_OPTIONS[menu_option_index]}")
    sleep(.5)
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                menu_option_index += 1
                if menu_option_index == len(MENU_OPTIONS):
                    menu_option_index = 0
            elif position < last_position:
                menu_option_index -= 1
                if menu_option_index < 0:
                    menu_option_index = len(MENU_OPTIONS)-1
            last_position = position
            display_message(f"Select a game:\n{MENU_OPTIONS[menu_option_index]}")
    sleep(.1)
    run_program(MENU_OPTIONS[menu_option_index])

# Used to run a function when the respective menu item is selected
def run_program(menu_choice):
    display_message(f"Running:\n{menu_choice}")
    sleep(1)
    if menu_choice == "KotH":
        timer_screen(menu_choice)
    elif menu_choice == "Attrition":
        counter_screen(menu_choice)
    elif menu_choice == "Death Clicks":
        team_screen(menu_choice)
    elif menu_choice == "Domination":
        timer_screen(menu_choice)

# Screen used to set time for KotH and Domination
def timer_screen(game_mode):
    sleep(.5)
    global position, last_position, game_length
    game_length = 0
    display_message(f"{game_mode}\nTime: {timer_string(game_length)}")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:   # clockwise rotation
                game_length += 15            
            elif position < last_position:   # counterclockwise rotation
                if game_length > 0:
                    game_length -= 15
            display_message(f"{game_mode}\nTime: {timer_string(game_length)}")
            last_position = position
    sleep(.1)
    standby_screen(game_mode)

# Screen used to set lives for Attrition
def counter_screen(game_mode):
    sleep(.5)
    global position, last_position, lives_count
    lives_count = 0
    display_message(f"{game_mode} \nLives: {lives_count}")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                lives_count += 1
            elif position < last_position:
                if lives_count > 0:
                    lives_count -= 1
            display_message(f"{game_mode}\nLives: {lives_count}")
            last_position = position
    sleep(.1)
    team_screen(game_mode)

# Screen for selecting team counter for Attrition and Death Clicks
def team_screen(game_mode):
    sleep(.5)
    global team
    team = "Green"
    display_message(f"{game_mode}\nTeam:")
    while ENC.value:
        if not RED.value:
            team = "Red"
            RED_LED.value = True
            BLUE_LED.value = False
            display_message(f"{game_mode}\nTeam {team}")
            rgb_control(COLOR_RED, "chase")
            sleep(.1)
        if not BLUE.value:
            team = "Blue"
            RED_LED.value = False
            BLUE_LED.value = True
            display_message(f"{game_mode}\nTeam {team}")
            rgb_control(COLOR_BLUE, "chase")
            sleep(.1)
    sleep(.1)
    standby_screen(game_mode)

# Pre-game confirmation screen
def standby_screen(game_mode):
    sleep(.5)
    if game_mode == "KotH":
        display_message(f"{game_mode} Ready\n{timer_string(game_length)}")
    elif game_mode == "Attrition":
            display_message(f"{game_mode} Ready\nTeam {team} {lives_count} Lives")
    elif game_mode == "Death Clicks":
        display_message(f"{game_mode}\nReady Team {team}")
    elif game_mode == "Domination":
        display_message(f"{game_mode}\nReady {timer_string(game_length)}")
    rgb_control(COLOR_OFF, "chase")
    sleep(1)
    while ENC.value:
        sleep(.1)
    sleep(.1)
    if game_mode == "KotH":
        display_message(f"{game_mode}\nStarting...")
        start_koth_timer()
    elif game_mode == "Attrition":
        display_message(f"{game_mode}\nStarting...")
        start_attrition_counter()
    elif game_mode == "Death Clicks":
        display_message(f"{game_mode}\nStarting...")
        start_clicks_counter()
    if game_mode == "Domination":
        display_message(f"{game_mode}\nStarting...")
        start_domination_timer()

# Function for KotH timers
def start_koth_timer():
    sleep(.5)
    global position, last_position, restart_option_index
    red_time = game_length
    blue_time = game_length
    red_time_str = timer_string(red_time)
    blue_time_str = timer_string(blue_time)
    red_timer_started = False
    blue_timer_started = False
    RED_LED.value = False
    BLUE_LED.value = False
    display_message(f"RED: {timer_string(game_length)}\nBLUE: {timer_string(game_length)}")
    rgb_control(COLOR_GREEN, "chase")
    sleep(.5)
    while RED.value and BLUE.value:
        sleep(.01)
    clock = monotonic()
    while red_time > 0 and blue_time > 0:
        if monotonic()-clock >= 1:
            if red_timer_started:            
                red_time -= 1
                red_time_str = timer_string(red_time)
            elif blue_timer_started:                  
                blue_time -= 1
                blue_time_str = timer_string(blue_time)
            display_message(f"RED:  {red_time_str}\nBLUE: {blue_time_str}")
            clock = monotonic()
        if not RED.value and not red_timer_started:
            red_timer_started = True
            blue_timer_started = False
            rgb_control(COLOR_RED, "chase", 0.0025)
            RED_LED.value = True
            BLUE_LED.value = False
            print("red timer started")
        elif not BLUE.value and not blue_timer_started:
            red_timer_started = False
            blue_timer_started = True
            rgb_control(COLOR_BLUE, "chase", 0.0025)
            RED_LED.value = False
            BLUE_LED.value = True
            print("blue timer started")
    display_message(f"RED:  {red_time_str}\nBLUE: {blue_time_str}")
    while ENC.value:
        if red_timer_started == True:
            rgb_control(COLOR_RED, "chase")
            rgb_control(COLOR_OFF, "chase")
        elif blue_timer_started == True:
            rgb_control(COLOR_BLUE, "chase")
            rgb_control(COLOR_OFF, "chase")
    sleep(1)
    rgb_control(COLOR_OFF, "chase")
    display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                restart_option_index += 1
                if restart_option_index == len(RESTART_OPTIONS):
                    restart_option_index = 0
            elif position < last_position:
                restart_option_index -= 1
                if restart_option_index < 0:
                    restart_option_index = len(RESTART_OPTIONS)-1
            last_position = position
            display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    if restart_option_index == 0:
        RED_LED.value = False
        BLUE_LED.value = False
        standby_screen("KotH")
    elif restart_option_index == 1:
        main_menu()

# Function for Attrition countdown
def start_attrition_counter():
    sleep(.5)
    global position, last_position, restart_option_index, team
    lives_attr = lives_count
    display_message(f"{team} Lives Left\n{lives_attr}")
    if team == "Red":
        rgb_control(COLOR_RED, "chase")
    elif team == "Blue":
        rgb_control(COLOR_BLUE, "chase")
    while lives_attr > 0:
        if not RED.value or not BLUE.value:
            lives_attr -=1
            if team == "Red":
                rgb_control(COLOR_OFF, "chase", .001)
                rgb_control(COLOR_RED, "chase", .001)
            elif team == "Blue":
                rgb_control(COLOR_OFF, "chase", .001)
                rgb_control(COLOR_BLUE, "chase", .001)
            display_message(f"{team} Lives Left\n{lives_attr}")
        sleep(.2)
    display_message(f"{team} Lives Left\n{lives_attr}")
    while ENC.value:
        if team == "Red":
            rgb_control(COLOR_RED, "chase")
            rgb_control(COLOR_OFF, "chase")
        elif team == "Blue":
            rgb_control(COLOR_BLUE, "chase")
            rgb_control(COLOR_OFF, "chase")
    sleep(1)
    display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    rgb_control(COLOR_OFF, "chase")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                restart_option_index += 1
                if restart_option_index == len(RESTART_OPTIONS):
                    restart_option_index = 0
            elif position < last_position:
                restart_option_index -= 1
                if restart_option_index < 0:
                    restart_option_index = len(RESTART_OPTIONS)-1
            last_position = position
            display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    if restart_option_index == 0:
        if team == "Red":
            team = "Blue"
            RED_LED.value = False
            BLUE_LED.value = True
            rgb_control(COLOR_BLUE, "chase")
        elif team == "Blue":
            team = "Red"
            RED_LED.value = True
            BLUE_LED.value = False
            rgb_control(COLOR_RED, "chase")
        standby_screen("Attrition")
    elif restart_option_index == 1:
        main_menu()


# Function for Death Clicks countdown
def start_clicks_counter():
    sleep(.5)
    global position, last_position, restart_option_index, team
    death_count = 0
    display_message(f"{team} team\nDeaths {death_count}")
    if team == "Red":
        rgb_control(COLOR_RED, "chase")
    elif team == "Blue":
        rgb_control(COLOR_BLUE, "chase")
    while ENC.value:
        if not RED.value or not BLUE.value:
            death_count += 1
            if team == "Red":
                rgb_control(COLOR_OFF, "chase", .001)
                rgb_control(COLOR_RED, "chase", .001)
            elif team == "Blue":
                rgb_control(COLOR_OFF, "chase", .001)
                rgb_control(COLOR_BLUE, "chase", .001)
            display_message(f"{team} team\nDeaths {death_count}")
    sleep(1)
    display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    rgb_control(COLOR_OFF, "chase")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                restart_option_index += 1
                if restart_option_index == len(RESTART_OPTIONS):
                    restart_option_index = 0
            elif position < last_position:
                restart_option_index -= 1
                if restart_option_index < 0:
                    restart_option_index = len(RESTART_OPTIONS)-1
            last_position = position
            display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    if restart_option_index == 0:
        if team == "Red":
            team = "Blue"
            RED_LED.value = False
            BLUE_LED.value = True
            rgb_control(COLOR_BLUE, "chase")
        elif team == "Blue":
            team = "Red"
            RED_LED.value = True
            BLUE_LED.value = False
            rgb_control(COLOR_RED, "chase")
        standby_screen("Death Clicks")
    elif restart_option_index == 1:
        main_menu()

def start_domination_timer():
    sleep(.5)
    global position, last_position, restart_option_index, team
    team = "Green"
    RED_LED.value = False
    BLUE_LED.value = False
    dom_time = game_length
    red_time = 0
    blue_time = 0
    display_message(f"{team} Team\n {timer_string(dom_time)}")
    rgb_control(COLOR_GREEN, "chase")
    clock = monotonic()
    while dom_time > 0:
        if monotonic()-clock >= 1:
            dom_time -= 1
            display_message(f"{team} Team\n{timer_string(dom_time)}")
            clock = monotonic()
        if not RED.value:
            red_time = monotonic()
            while not RED.value:
                if monotonic()-red_time >= 1:
                    team = "Red"
                    RED_LED.value = True
                    BLUE_LED.value = False
                    display_message(f"Red Team \n{timer_string(dom_time)}")
                    rgb_control(COLOR_RED, "solid")
                    print("red point control")
                    red_time = monotonic()
        elif not BLUE.value:
            blue_time = monotonic()
            while not BLUE.value:
                if monotonic()-blue_time >= 1:
                    team = "Blue"
                    RED_LED.value = False
                    BLUE_LED.value = True
                    display_message(f"Blue Team \n{timer_string(dom_time)}")
                    rgb_control(COLOR_BLUE, "solid")
                    print("blue point control")
                    blue_time = monotonic()
    display_message(f"{team} Team\nPoint Locked")
    while ENC.value:
        if team == "Red":
            rgb_control(COLOR_RED, "chase")
            rgb_control(COLOR_OFF, "chase")
        elif team == "Blue":
            rgb_control(COLOR_BLUE, "chase")
            rgb_control(COLOR_OFF, "chase")
    sleep(1)
    display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    rgb_control(COLOR_OFF, "chase")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                restart_option_index += 1
                if restart_option_index == len(RESTART_OPTIONS):
                    restart_option_index = 0
            elif position < last_position:
                restart_option_index -= 1
                if restart_option_index < 0:
                    restart_option_index = len(RESTART_OPTIONS)-1
            last_position = position
            display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    if restart_option_index == 0:
        rgb_control(COLOR_GREEN, "chase")
        standby_screen("Domination")
    elif restart_option_index == 1:
        main_menu()

if __name__ == '__main__':
    main_menu()
