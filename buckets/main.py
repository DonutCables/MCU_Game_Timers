from time import sleep, monotonic
from gc import enable
from random import randint
from hardware import DISPLAY, ENCODER, ENC, RED, BLUE, RED_LED, BLUE_LED
from audio_commands import play_track, set_vol
from led_commands import rgb_control

# Setting initial variables for use
position = ENCODER.position
last_position = position
MENU = [
    "KotH",
    "Attrition",
    "Death Clicks",
    "Domination",
    "Basic Timer",
]
menu_index = 0
RESTART_OPTIONS = ["Yes", "No"]
restart_option_index = 0
EXTRAS = [
    "You're a nerd",
    "Weiners",
    "Ooh, a piece of candy",
    "Oatmeal",
    "You're my little pogchamp",
    "Anything is a   hammer once",
    "Watch out for   them pointy bits",
    "This bucket kills fascists",
    "Taco Tuesday",
]


def display_message(message):
    """Displays a string to the 1602 LCD"""
    DISPLAY.clear()
    DISPLAY.print(message)


###


def main_menu():
    """Main menu for scrolling and displaying game options"""
    global position, last_position, menu_index
    display_message(EXTRAS[randint(0, len(EXTRAS) - 1)])
    rgb_control("Off", "solid")
    for color in ["Red", "Blue", "Green"]:
        rgb_control(color, "chase", 0.0075)
    RED_LED.value = False
    BLUE_LED.value = False
    display_message(f"Select a game:\n{MENU[menu_index]}")
    sleep(0.5)
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                menu_index = (menu_index + 1) % len(MENU)
            elif position < last_position:
                menu_index = (menu_index - 1) % len(MENU)
            last_position = position
            display_message(f"Select a game:\n{MENU[menu_index]}")
    run_program(MENU[menu_index])


def run_program(menu_choice):
    """Used to run a function when the respective menu item is selected"""
    display_message(f"Running:\n{menu_choice}")
    sleep(1)
    if menu_choice in ["KotH", "Domination", "Basic Timer"]:
        timer_screen(menu_choice)
    elif menu_choice == "Attrition":
        counter_screen(menu_choice)
    elif menu_choice == "Death Clicks":
        team_screen(menu_choice)


def timer_screen(game_mode):
    """Screen used to set time for KotH and Domination"""
    sleep(0.5)
    global position, last_position, game_length
    game_length = 0
    display_message(
        f"{game_mode}\nTime: {game_length // 60:02d}:{game_length % 60:02d}"
    )
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:  # clockwise rotation
                game_length += 15
            elif position < last_position:  # counterclockwise rotation
                if game_length > 0:
                    game_length -= 15
            display_message(
                f"{game_mode}\nTime: {game_length // 60:02d}:{game_length % 60:02d}"
            )
            last_position = position
    sleep(0.1)
    standby_screen(game_mode)


def counter_screen(game_mode):
    """Screen used to set lives for Attrition"""
    sleep(0.5)
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
    sleep(0.1)
    team_screen(game_mode)


def team_screen(game_mode):
    """Screen for selecting team counter for Attrition and Death Clicks"""
    sleep(0.5)
    global team
    team = "Green"
    display_message(f"{game_mode}\nTeam:")
    while ENC.value:
        if not RED.value:
            team = "Red"
            RED_LED.value = True
            BLUE_LED.value = False
            display_message(f"{game_mode}\nTeam {team}")
            rgb_control(team, "chase")
            sleep(0.1)
        if not BLUE.value:
            team = "Blue"
            RED_LED.value = False
            BLUE_LED.value = True
            display_message(f"{game_mode}\nTeam {team}")
            rgb_control(team, "chase")
            sleep(0.1)
    sleep(0.1)
    standby_screen(game_mode)


def standby_screen(game_mode):
    """Pre-game confirmation screen"""
    sleep(0.5)
    if game_mode == "KotH":
        display_message(
            f"{game_mode} Ready\n{game_length // 60:02d}:{game_length % 60:02d}"
        )
    elif game_mode == "Attrition":
        display_message(f"{game_mode} Ready\nTeam {team} {lives_count} Life")
    elif game_mode == "Death Clicks":
        display_message(f"{game_mode}\nReady Team {team}")
    elif game_mode == "Domination":
        display_message(
            f"{game_mode}\nReady {game_length // 60:02d}:{game_length % 60:02d}"
        )
    elif game_mode == "Basic Timer":
        display_message(
            f"{game_mode}\nReady {game_length // 60:02d}:{game_length % 60:02d}"
        )
    rgb_control("Off", "chase")
    sleep(1)
    while ENC.value:
        sleep(0.1)
    sleep(0.1)
    if game_mode == "KotH":
        display_message(f"{game_mode}\nStarting...")
        start_koth_timer()
    elif game_mode == "Attrition":
        display_message(f"{game_mode}\nStarting...")
        start_attrition_counter()
    elif game_mode == "Death Clicks":
        display_message(f"{game_mode}\nStarting...")
        start_clicks_counter()
    elif game_mode == "Domination":
        display_message(f"{game_mode}\nStarting...")
        start_domination_timer()
    elif game_mode == "Basic Timer":
        display_message(f"{game_mode}\nStarting...")
        start_basic_timer()


def start_koth_timer():
    """Function for KotH timers"""
    sleep(0.5)
    global position, last_position, restart_option_index
    red_time = game_length
    blue_time = game_length
    red_time_str = f"{red_time // 60:02d}:{red_time % 60:02d}"
    blue_time_str = f"{blue_time // 60:02d}:{blue_time % 60:02d}"
    red_timer_started = False
    blue_timer_started = False
    timer_state = (False, False)
    RED_LED.value = False
    BLUE_LED.value = False
    display_message(f"RED: {red_time_str}\nBLUE: {blue_time_str}")
    rgb_control("Green", "chase")
    sleep(0.5)
    while RED.value and BLUE.value:
        sleep(0.01)
    clock = monotonic()
    while red_time > 0 and blue_time > 0:
        if monotonic() - clock >= 1:
            if red_timer_started:
                red_time -= 1
                red_time_str = f"{red_time // 60:02d}:{red_time % 60:02d}"
            elif blue_timer_started:
                blue_time -= 1
                blue_time_str = f"{blue_time // 60:02d}:{blue_time % 60:02d}"
            display_message(f"RED:  {red_time_str}\nBLUE: {blue_time_str}")
            clock = monotonic()
        if not RED.value and not red_timer_started:
            red_timer_started = True
            blue_timer_started = False
            rgb_control("Red", "chase", 0.0025)
            RED_LED.value = True
            BLUE_LED.value = False
            print("red timer started")
        elif not BLUE.value and not blue_timer_started:
            red_timer_started = False
            blue_timer_started = True
            rgb_control("Blue", "chase", 0.0025)
            RED_LED.value = False
            BLUE_LED.value = True
            print("blue timer started")
        if not ENC.value:
            if red_timer_started == True or blue_timer_started == False:
                timer_state = (red_timer_started, blue_timer_started)
                red_timer_started, blue_timer_started = False, False
            else:
                red_timer_started, blue_timer_started = timer_state
                timer_state = (False, False)
            sleep(0.1)
    display_message(f"RED:  {red_time_str}\nBLUE: {blue_time_str}")
    while ENC.value:
        if red_timer_started == True:
            rgb_control("Red", "chase")
        elif blue_timer_started == True:
            rgb_control("Blue", "chase")
        rgb_control("Off", "chase")
    sleep(1)
    rgb_control("Off", "chase")
    display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                restart_option_index = (restart_option_index + 1) % len(RESTART_OPTIONS)
            elif position < last_position:
                restart_option_index = (restart_option_index - 1) % len(RESTART_OPTIONS)
            last_position = position
            display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    if restart_option_index == 0:
        RED_LED.value = False
        BLUE_LED.value = False
        standby_screen("KotH")
    elif restart_option_index == 1:
        main_menu()


def start_attrition_counter():
    """Function for Attrition countdown"""
    sleep(0.5)
    global position, last_position, restart_option_index, team
    lives_attr = lives_count
    display_message(f"{team} Lives Left\n{lives_attr}")
    rgb_control(team, "chase")
    while lives_attr > 0:
        if not RED.value or not BLUE.value:
            lives_attr -= 1
            rgb_control("Off", "chase", 0.001)
            rgb_control(team, "chase", 0.001)
            display_message(f"{team} Lives Left\n{lives_attr}")
    display_message(f"{team} Lives Left\n{lives_attr}")
    while ENC.value:
        rgb_control(team, "chase")
        rgb_control("Off", "chase")
    sleep(1)
    display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    rgb_control("Off", "chase")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                restart_option_index = (restart_option_index + 1) % len(RESTART_OPTIONS)
            elif position < last_position:
                restart_option_index = (restart_option_index - 1) % len(RESTART_OPTIONS)
            last_position = position
            display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    if restart_option_index == 0:
        team = not team
        RED_LED.value = not RED_LED.value
        BLUE_LED.value = not BLUE_LED.value
        rgb_control(team, "chase")
        standby_screen("Attrition")
    elif restart_option_index == 1:
        main_menu()


def start_clicks_counter():
    """Function for Death Clicks countdown"""
    sleep(0.5)
    global position, last_position, restart_option_index, team
    death_count = 0
    display_message(f"{team} team\nDeaths {death_count}")
    rgb_control(team, "chase")
    while ENC.value:
        if not RED.value or not BLUE.value:
            death_count += 1
            rgb_control("Off", "chase", 0.001)
            rgb_control(team, "chase", 0.001)
            display_message(f"{team} team\nDeaths {death_count}")
    sleep(1)
    display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    rgb_control("Off", "chase")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                restart_option_index = (restart_option_index + 1) % len(RESTART_OPTIONS)
            elif position < last_position:
                restart_option_index = (restart_option_index - 1) % len(RESTART_OPTIONS)
            last_position = position
            display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    if restart_option_index == 0:
        team = not team
        RED_LED.value = not RED_LED.value
        BLUE_LED.value = not BLUE_LED.value
        rgb_control(team, "chase")
        standby_screen("Death Clicks")
    elif restart_option_index == 1:
        main_menu()


def start_domination_timer():
    sleep(0.5)
    global position, last_position, restart_option_index, team
    team = "Green"
    RED_LED.value = False
    BLUE_LED.value = False
    dom_time = game_length
    dom_time_started = True
    red_time = 0
    blue_time = 0
    display_message(f"{team} Team\n{dom_time // 60:02d}:{dom_time % 60:02d}")
    rgb_control(team, "chase")
    clock = monotonic()
    while dom_time > 0:
        if monotonic() - clock >= 1:
            if dom_time_started == True:
                dom_time -= 1
            display_message(f"{team} Team\n{dom_time // 60:02d}:{dom_time % 60:02d}")
            clock = monotonic()
        if not RED.value:
            red_time = monotonic()
            while not RED.value:
                if monotonic() - red_time >= 1:
                    team = "Red"
                    RED_LED.value = True
                    BLUE_LED.value = False
                    display_message(
                        f"{team} Team \n{dom_time // 60:02d}:{dom_time % 60:02d}"
                    )
                    rgb_control(team, "solid")
                    print(f"{team} point control")
                    red_time = monotonic()
        elif not BLUE.value:
            blue_time = monotonic()
            while not BLUE.value:
                if monotonic() - blue_time >= 1:
                    team = "Blue"
                    RED_LED.value = False
                    BLUE_LED.value = True
                    display_message(
                        f"{team} Team \n{dom_time // 60:02d}:{dom_time % 60:02d}"
                    )
                    rgb_control(team, "solid")
                    print(f"{team} point control")
                    blue_time = monotonic()
        if not ENC.value:
            dom_time_started = not dom_time_started
            sleep(0.5)
    display_message(f"{team} Team\nPoint Locked")
    while ENC.value:
        rgb_control(team, "chase")
        rgb_control("Off", "chase")
    sleep(1)
    display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    rgb_control("Off", "chase")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                restart_option_index = (restart_option_index + 1) % len(RESTART_OPTIONS)
            elif position < last_position:
                restart_option_index = (restart_option_index - 1) % len(RESTART_OPTIONS)
            last_position = position
            display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    if restart_option_index == 0:
        rgb_control("Green", "chase")
        standby_screen("Domination")
    elif restart_option_index == 1:
        main_menu()


def start_basic_timer():
    sleep(0.5)
    global position, last_position, restart_option_index
    basic_time = game_length
    basic_timer_started = True
    display_message(f"{basic_time // 60:02d}:{basic_time % 60:02d}")
    clock = monotonic()
    while basic_time > 0:
        if monotonic() - clock >= 1:
            if basic_timer_started:
                basic_time -= 1
            if basic_time < 11:
                play_track(basic_time + 15)
            display_message(f"{basic_time // 60:02d}:{basic_time % 60:02d}")
            clock = monotonic()
        if not ENC.value:
            basic_timer_started = not basic_timer_started
        if basic_time == 30:
            play_track(26)
    sleep(1)
    display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    while ENC.value:
        position = ENCODER.position
        if position != last_position:
            if position > last_position:
                restart_option_index = (restart_option_index + 1) % len(RESTART_OPTIONS)
            elif position < last_position:
                restart_option_index = (restart_option_index - 1) % len(RESTART_OPTIONS)
            last_position = position
            display_message(f"Restart?:\n{RESTART_OPTIONS[restart_option_index]}")
    if restart_option_index == 0:
        rgb_control("Green", "chase")
        standby_screen("Basic Timer")
    elif restart_option_index == 1:
        main_menu()


enable()

set_vol(30)

if __name__ == "__main__":
    main_menu()
