import board
import busio
import rotaryio
import digitalio
import time
from lcd import LCD
from i2c_pcf8574_interface import I2CPCF8574Interface

lcd_i2c = busio.I2C(board.GP1, board.GP0)
pcf_interface = I2CPCF8574Interface(lcd_i2c, 0x27)
lcd = LCD(pcf_interface, num_rows=2, num_cols=16)

# Initialize rotary encoder and buttons
encoder = rotaryio.IncrementalEncoder(board.GP2, board.GP3)
last_position = encoder.position

ENC = digitalio.DigitalInOut(board.GP4)
RED = digitalio.DigitalInOut(board.GP5)
BLUE = digitalio.DigitalInOut(board.GP6)
for button in [ENC, RED, BLUE]:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

# Define menu options and corresponding program names
menu_options = ["KotH", "Attrition", "Death Clicks"]
menu_option_index = 0

# Function to manage LCD messages
def display_message(message):
    lcd.clear()
    lcd.print(message)

# Function to fetch timer string from game length
def timer_string(game_length):
    return f"{game_length // 60:02d}:{game_length % 60:02d}"

# Function to translate encoder input to scrolling in the main menu
def scroll_menu(direction):
    global menu_option_index
    if direction == "down":
        print("down")
        menu_option_index += 1
        if menu_option_index == len(menu_options):
            menu_option_index = 0
    elif direction == "up":
        menu_option_index -= 1
        print("up")
        if menu_option_index < 0:
            menu_option_index = len(menu_options)-1
    display_message(f"Select a game:\n{menu_options[menu_option_index]}")

# Main menu
def main_menu():
    global encoder, last_position
    display_message("You're a nerd")
    time.sleep(.5)    
    display_message(f"Select a game:\n{menu_options[menu_option_index]}")
    last_position = encoder.position
    while True:
        if encoder.position > last_position:
            scroll_menu("down")
        elif encoder.position < last_position:
            scroll_menu("up")

        last_position = encoder.position

        if not ENC.value:
            run_program(menu_options[menu_option_index])

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
    global GAME_LENGTH, encoder, last_position
    GAME_LENGTH = 0
    display_message(f"{game_mode} Time?\n{timer_string(GAME_LENGTH)}")
    while True:
        if encoder.position > last_position:   # clockwise rotation
            GAME_LENGTH += 30            
        elif encoder.position < last_position:   # counterclockwise rotation
            GAME_LENGTH -= 30            
        elif not ENC.value:
            break
        if GAME_LENGTH < 0:
            GAME_LENGTH = 0
        if encoder.position != last_position:
            display_message(f"{game_mode} Time?\n{timer_string(GAME_LENGTH)}")
        last_position = encoder.position
        time.sleep(.1)
    standby_screen(game_mode)

# Screen used to set lives for Attrition
def counter_screen(game_mode):
    time.sleep(.5)
    global LIVES_COUNT, encoder, last_position
    LIVES_COUNT = 0
    display_message(f"{game_mode} \nLives? {LIVES_COUNT}")
    while True:
        if encoder.position > last_position:   # clockwise rotation
            LIVES_COUNT += 1            
        elif encoder.position < last_position:   # counterclockwise rotation
            LIVES_COUNT -= 1            
        elif not ENC.value:
                break
        if LIVES_COUNT < 0:
            LIVES_COUNT = 0
        if encoder.position != last_position:
            display_message(f"{game_mode}\nLives? {LIVES_COUNT}")
        last_position = encoder.position
        time.sleep(.1)
    team_screen(game_mode)

# Screen for selecting team counter for Attrition and Death Clicks
def team_screen(game_mode):
    time.sleep(.5)
    global TEAM
    TEAM = "Green"
    display_message(f"{game_mode}\nTeam?")
    while True:
        if not RED.value:
            TEAM = "Red"
            display_message(f"{game_mode}\nTeam {TEAM}")
        elif not BLUE.value:
            TEAM = "Blue"
            display_message(f"{game_mode}\nTeam {TEAM}")
        if not ENC.value:
            break
        time.sleep(.1)
    standby_screen(game_mode)

# Pre-game confirmation screen
def standby_screen(game_mode):
    time.sleep(.5)
    if game_mode == "KotH":
        display_message(f"{game_mode} Ready\n {timer_string(GAME_LENGTH)}")
    elif game_mode == "Attrition":
            display_message(f"{game_mode} Ready\nTeam {TEAM} {LIVES_COUNT} Lives")
    elif game_mode == "Death Clicks":
        display_message(f"{game_mode}\nReady Team {TEAM}")
    time.sleep(.5)
    while True:
        if not ENC.value:
            break
        time.sleep(0.1)
    game_screen(game_mode)

# Displays the initial game start screen before either team has activated a timer
def game_screen(game_mode):
    time.sleep(.5)
    if game_mode == "KotH":
        display_message(f"RED: {timer_string(GAME_LENGTH)}\nBLUE: {timer_string(GAME_LENGTH)}")
        time.sleep(1)
        while True:
            if not RED.value or not BLUE.value:
                    start_koth_timer()
            time.sleep(0.1)
    elif game_mode == "Attrition":
        display_message(f"{TEAM} Lives Left\n{LIVES_COUNT}")
        time.sleep(1)
        while True:
            if not RED.value or not BLUE.value:
                    start_attrition_counter()
            time.sleep(0.1)
    elif game_mode == "Death Clicks":
        display_message(f"{TEAM} Death Count\n0")
        time.sleep(1)
        while True:
            if not RED.value or not BLUE.value:
                    start_clicks_counter()
            time.sleep(0.1)

# Function for KotH timers
def start_koth_timer():
    red_time = GAME_LENGTH
    blue_time = GAME_LENGTH
    red_time_str = timer_string(red_time)
    blue_time_str = timer_string(blue_time)
    red_timer_started = False
    blue_timer_started = False
    while True:
        if red_time <= 0 or blue_time <= 0:
            break
        if red_timer_started:            
            if red_time <= 0:
                break
            red_time -= 1
        elif blue_timer_started:                  
            if blue_time <= 0:
                break
            blue_time -= 1         
        if not RED.value and not red_timer_started:
            red_timer_started = True
            blue_timer_started = False
            print("red timer started")
        elif not BLUE.value and not blue_timer_started:
            blue_timer_started = True
            red_timer_started = False
            print("blue timer started")
        red_time_str = timer_string(red_time)
        blue_time_str = timer_string(blue_time)
        display_message(f"RED: {red_time_str}\nBLUE: {blue_time_str}")
        time.sleep(1)
    while True:
        display_message(f"RED: {red_time_str}\nBLUE: {blue_time_str}")
        for i in range(8):
            if not ENC.value:
                main_menu()
            time.sleep(.1)
        lcd.clear()        
        time.sleep(.1)

# Function for Attrition countdown
def start_attrition_counter():
    global TEAM, LIVES_COUNT
    display_message(f"{TEAM} Lives Left\n{LIVES_COUNT}")
    while True:
        if not RED.value or not BLUE.value:
            if LIVES_COUNT > 0:
                LIVES_COUNT -=1
            else:
                LIVES_COUNT = 0
                break
        display_message(f"{TEAM} Lives Left\n{LIVES_COUNT}")
        time.sleep(.2)
    while True:
        display_message(f"{TEAM} Lives Left\n{LIVES_COUNT}")
        for i in range(8):
            if not ENC.value:
                main_menu()
            time.sleep(.1)
        lcd.clear()        
        time.sleep(.1)

# Function for Death Clicks countdown
def start_clicks_counter():
    global TEAM, DEATH_COUNT
    DEATH_COUNT = 0
    display_message(f"{TEAM} TEAM\n Deaths {DEATH_COUNT}")
    while True:
        if not RED.value or not BLUE.value:
            DEATH_COUNT += 1
        if not ENC.value:
                main_menu()
        display_message(f"{TEAM} TEAM\n Deaths {DEATH_COUNT}")
        time.sleep(.2)

main_menu()
