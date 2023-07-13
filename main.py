import board
import time
from hardware import DISPLAY, ENCODER, ENC, RED, BLUE

# Setting initial variables for use
position = ENCODER.position
last_position = position
MENU_OPTIONS = ["KotH", "Attrition", "Death Clicks"]
menu_option_index = 0

# Function to display LCD messages
def display_message(message):
    DISPLAY.clear()
    DISPLAY.print(message)

# Placeholder function for LED control
def led_control(color, pattern, time):
    #insert led functionality here later
    print(color, pattern, time)

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
    global position, last_position
    led_control("main menu")
    display_message("You're a nerd")
    time.sleep(.5)
    display_message(f"Select a game:\n{MENU_OPTIONS[menu_option_index]}")
    while True:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                scroll_menu("down")
            elif position < last_position:
                scroll_menu("up")
            last_position = position
        if not ENC.value:
            break
    time.sleep(.1)
    run_program(MENU_OPTIONS[menu_option_index])

# Function to translate ENCODER input to scrolling in the main menu
def scroll_menu(direction):
    global menu_option_index
    if direction == "down":
        menu_option_index += 1
        if menu_option_index == len(MENU_OPTIONS):
            menu_option_index = 0
    elif direction == "up":
        menu_option_index -= 1
        if menu_option_index < 0:
            menu_option_index = len(MENU_OPTIONS)-1
    display_message(f"Select a game:\n{MENU_OPTIONS[menu_option_index]}")

# Used to run a function when the respective menu item is selected
def run_program(menu_choice):
    display_message(f"Running:\n{menu_choice}")
    time.sleep(1)
    if menu_choice == "KotH":
        timer_screen(menu_choice)
    elif menu_choice == "Attrition":
        counter_screen(menu_choice)
    elif menu_choice == "Death Clicks":
        team_screen(menu_choice)

# Screen used to set time for KotH
def timer_screen(game_mode):
    time.sleep(.5)
    global game_length, position, last_position
    game_length = 0
    display_message(f"{game_mode} Time?\n{timer_string(game_length)}")
    while True:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:   # clockwise rotation
                game_length += 30            
            elif position < last_position:   # counterclockwise rotation
                if game_length > 0:
                    game_length -= 30
            display_message(f"{game_mode} Time?\n{timer_string(game_length)}")
            last_position = position
        if not ENC.value:
            break
    time.sleep(.1)
    standby_screen(game_mode)

# Screen used to set lives for Attrition
def counter_screen(game_mode):
    time.sleep(.5)
    global lives_count, position, last_position
    lives_count = 0
    display_message(f"{game_mode} \nLives? {lives_count}")
    while True:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                lives_count += 1
            elif position < last_position:
                if lives_count > 0:
                    lives_count -= 1
            display_message(f"{game_mode}\nLives? {lives_count}")
            last_position = position
        if not ENC.value:
            break
    time.sleep(.1)
    team_screen(game_mode)

# Screen for selecting team counter for Attrition and Death Clicks
def team_screen(game_mode):
    time.sleep(.5)
    global team
    team = "Green"
    display_message(f"{game_mode}\nTeam?")
    while True:
        if not RED.value:
            team = "Red"
            led_control("red team")
            display_message(f"{game_mode}\nTeam {team}")
        if not BLUE.value:
            team = "Blue"
            led_control("blue team")
            display_message(f"{game_mode}\nTeam {team}")
        if not ENC.value:
            break
    time.sleep(.1)
    standby_screen(game_mode)

# Pre-game confirmation screen
def standby_screen(game_mode):
    time.sleep(.5)
    if game_mode == "KotH":
        display_message(f"{game_mode} Ready\n {timer_string(game_length)}")
    elif game_mode == "Attrition":
            display_message(f"{game_mode} Ready\nTeam {team} {lives_count} Lives")
    elif game_mode == "Death Clicks":
        display_message(f"{game_mode}\nReady team {team}")
    time.sleep(1)
    while True:
        if not ENC.value:
            break
    time.sleep(.1)
    if game_mode == "KotH":
        display_message(f"{game_mode}\nStarting...")
        start_koth_timer()
    elif game_mode == "Attrition":
        display_message(f"{game_mode}\nStarting...")
        start_attrition_counter()
    elif game_mode == "Death Clicks":
        display_message(f"{game_mode}\nStarting...")
        start_clicks_counter()

# Function for KotH timers
def start_koth_timer():
    time.sleep(.5)
    red_time = game_length
    blue_time = game_length
    red_time_str = timer_string(red_time)
    blue_time_str = timer_string(blue_time)
    red_timer_started = False
    blue_timer_started = False
    display_message(f"RED: {timer_string(game_length)}\nBLUE: {timer_string(game_length)}")
    led_control("koth timer ready")
    time.sleep(1)
    while True:
        if not RED.value or not BLUE.value:
            break
    while True:
        if red_timer_started:            
            red_time -= 1
            red_time_str = timer_string(red_time)
        elif blue_timer_started:                  
            blue_time -= 1
            blue_time_str = timer_string(blue_time)
        if not RED.value or not red_timer_started:
            red_timer_started = True
            blue_timer_started = False
            led_control("red timer")
            print("red timer started")
        elif not BLUE.value or not blue_timer_started:
            blue_timer_started = True
            red_timer_started = False
            led_control("blue timer")
            print("blue timer started")
        display_message(f"RED: {red_time_str}\nBLUE: {blue_time_str}")
        if red_time <= 0 or blue_time <= 0:
            break
        time.sleep(1)
    display_message(f"RED: {red_time_str}\nBLUE: {blue_time_str}")
    while True:
        if not ENC.value:
            break
    time.sleep(.1)
    main_menu()

# Function for Attrition countdown
def start_attrition_counter():
    time.sleep(.5)
    global lives_count
    display_message(f"{team} Lives Left\n{lives_count}")
    time.sleep(1)
    while True:
        if not RED.value or not BLUE.value:
            if lives_count > 1:
                lives_count -=1
                display_message(f"{team} Lives Left\n{lives_count}")
            else:
                lives_count = 0
                break
    display_message(f"{team} Lives Left\n{lives_count}")
    while True:
        if not ENC.value:
            break
    time.sleep(.1)
    main_menu()

# Function for Death Clicks countdown
def start_clicks_counter():
    time.sleep(.5)
    global death_count
    death_count = 0
    display_message(f"{team} team\n Deaths {death_count}")
    time.sleep(1)
    while True:
        if not RED.value or not BLUE.value:
            death_count += 1
            display_message(f"{team} team\n Deaths {death_count}")
        if not ENC.value:
            break
    time.sleep(.1)
    main_menu()

if __name__ == '__main__':
    main_menu()
