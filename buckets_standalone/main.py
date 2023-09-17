import asyncio
from time import sleep, monotonic
from gc import enable
from random import randint
from hardware import (
    DISPLAY,
    ENCODER,
    ENC,
    RED,
    BLUE,
    RED_LED,
    BLUE_LED,
    ENCB,
    REDB,
    BLUEB,
)
from audio_commands import play_track, set_vol
from led_commands import RGB_Control, RGB_Settings

# Setting initial variables for use
position = ENCODER.position
last_position = position
MODES = []
RESTART_OPTIONS = ["Yes", "No"]
EXTRAS = [
    "You're a nerd",
    "Weiners",
    "Ooh, a piece of candy",
    "Oatmeal",
    "Poggers in the \nchat",
    "Anything is a \nhammer once",
    "Watch out for \nthem pointy bits",
    "This bucket \nkills fascists",
    "Taco Tuesday",
    "Amongus",
    "Dino Nuggies",
]


class Game_States:
    """
    Represents the state variables and settings for a game.

    This class stores various game-related attributes and settings
    such as menu indices, restart indices, team information, game
    lengths, timer states, and more.

    Attributes:
        menu_index (int): The current menu index.
        restart_index (int): The current restart index.
        lives_count (int): The number of lives remaining.
        team (str): The team name, e.g., "Green."
        game_length (int): The duration of the game in seconds.
        game_length_str (str): A formatted string representation of game length.
        cap_length (int): The capture point length in seconds.
        cap_length_str (str): A formatted string representation of cap length.
        checkpoint (int): The checkpoint value.
        timer_state (bool): The state of the timer (True for running, False for paused).
        cap_state (bool): The state of the capture.
        red_time (int): The remaining time for the red team.
        red_time_str (str): A formatted string representation of red team time.
        blue_time (int): The remaining time for the blue team.
        blue_time_str (str): A formatted string representation of blue team time.
    """

    def __init__(self):
        self.menu_index = 0
        self.restart_index = 0
        self.lives_count = 0
        self.team = "Green"
        self.game_length = 0
        self.game_length_str = (
            f"{self.game_length // 60:02d}:{self.game_length % 60:02d}"
        )
        self.cap_length = 0
        self.cap_length_str = f"{self.cap_length // 60:02d}:{self.cap_length % 60:02d}"
        self.checkpoint = 1
        self.timer_state = True
        self.cap_state = False
        self.red_time = 0
        self.red_time_str = f"{self.red_time // 60:02d}:{self.red_time % 60:02d}"
        self.blue_time = 0
        self.blue_time_str = f"{self.blue_time // 60:02d}:{self.blue_time % 60:02d}"


initial_state = Game_States()
leds = RGB_Control()
led_state = RGB_Settings()


###


def display_message(message):
    """Displays a string to the 1602 LCD"""
    DISPLAY.clear()
    DISPLAY.print(message)


def update_team(teamp: str, speed=0.005, state=initial_state):
    """Updates button LED state based on team"""
    state.team = teamp
    RED_LED.value = "Red" in teamp
    BLUE_LED.value = "Blue" in teamp
    led_state.update(teamp, delay=speed)


def encoder_handler(x, y):
    """Handles encoder rotation"""
    global position, last_position
    if position > last_position:
        last_position = position
        return x + y
    elif position < last_position:
        last_position = position
        return x - y
    else:
        last_position = position
        return x


async def rgb_control(led_state):
    """Async function for controlling RGB LEDs"""
    while True:
        if led_state.repeat > 0 or led_state.repeat == -1:
            pattern = getattr(leds, led_state.pattern, "chase")
            if callable(pattern):
                pattern(led_state.color, led_state.delay)
            if led_state.repeat > 0:
                led_state.repeat -= 1
        await asyncio.sleep(0.1)


###


async def main_menu():
    """Main menu for scrolling and displaying game options"""
    global position, last_position
    last_position = position
    display_message(EXTRAS[randint(0, len(EXTRAS) - 1)])
    led_state.update(pattern="chase")
    for color in ["Red", "Blue", "Green"]:
        update_team(color)
        await asyncio.sleep(0.75)
    display_message(f"Select a game:\n{MODES[initial_state.menu_index].name}")
    ENCB.update()
    while ENCB.short_count < 1:
        ENCB.update()
        position = ENCODER.position
        if position != last_position:
            initial_state.menu_index = encoder_handler(
                initial_state.menu_index, 1
            ) % len(MODES)
            display_message(f"Select a game:\n{MODES[initial_state.menu_index].name}")
        await asyncio.sleep(0.1)
    await asyncio.sleep(0.1)
    ENCB.update()
    await run_program(MODES[initial_state.menu_index])


async def run_program(menu_choice):
    """Used to run a function when the respective menu item is selected"""
    display_message(f"Running:\n{menu_choice.name}")
    await asyncio.sleep(1)
    if menu_choice.has_lives:
        await counter_screen(menu_choice)
    elif menu_choice.has_team:
        await team_screen(menu_choice)
    elif menu_choice.has_game_length:
        await timer_screen(menu_choice)


async def counter_screen(game_mode):
    """Screen used to set lives for Attrition"""
    await asyncio.sleep(0.5)
    global position, last_position
    position = ENCODER.position
    last_position = position
    display_message(f"{game_mode.name} \nLives: {initial_state.lives_count}")
    while ENCB.short_count < 1:
        ENCB.update()
        position = ENCODER.position
        if position != last_position:
            initial_state.lives_count = max(
                0, encoder_handler(initial_state.lives_count, 1)
            )
            display_message(f"{game_mode.name}\nLives: {initial_state.lives_count}")
        await asyncio.sleep(0.1)
    await asyncio.sleep(0.1)
    ENCB.update()
    if game_mode.has_team:
        await team_screen(game_mode)
    else:
        await standby_screen(game_mode)


async def team_screen(game_mode):
    """Screen for selecting team counter for Attrition and Death Clicks"""
    await asyncio.sleep(0.5)
    display_message(f"{game_mode.name}\nTeam:")
    while ENCB.short_count < 1:
        ENCB.update()
        REDB.update()
        BLUEB.update()
        if not RED.value:
            update_team("Red", 0.0025)
            display_message(f"{game_mode.name}\nTeam {initial_state.team}")
        if not BLUE.value:
            update_team("Blue", 0.0025)
            display_message(f"{game_mode.name}\nTeam {initial_state.team}")
        await asyncio.sleep(0.1)
    await asyncio.sleep(0.1)
    ENCB.update()
    if game_mode.has_game_length:
        await timer_screen(game_mode)
    else:
        await standby_screen(game_mode)


async def timer_screen(game_mode):
    """Screen used to set time for game modes with built in timers"""
    await asyncio.sleep(0.5)
    global position, last_position
    position = ENCODER.position
    last_position = position
    display_message(f"{game_mode.name}\nTime: {initial_state.game_length_str}")
    while ENCB.short_count < 1:
        ENCB.update()
        position = ENCODER.position
        if position != last_position:
            initial_state.game_length = max(
                0, encoder_handler(initial_state.game_length, 15)
            )
            initial_state.game_length_str = f"{initial_state.game_length // 60:02d}:{initial_state.game_length % 60:02d}"
            display_message(f"{game_mode.name}\nTime: {initial_state.game_length_str}")
        await asyncio.sleep(0.1)
    if game_mode.has_cap_length:
        display_message(f"{game_mode.name}\nCap time: {initial_state.cap_length_str}")
        ENCB.update()
        while ENCB.short_count < 1:
            ENCB.update()
            position = ENCODER.position
            if position != last_position:
                initial_state.cap_length = max(
                    0, encoder_handler(initial_state.cap_length, 5)
                )
                initial_state.cap_length_str = f"{initial_state.cap_length // 60:02d}:{initial_state.cap_length % 60:02d}"
                display_message(
                    f"{game_mode.name}\nCap time: {initial_state.cap_length_str}"
                )
            await asyncio.sleep(0.1)
    if game_mode.has_checkpoint:
        display_message(f"{game_mode.name}\nCheckpoint: {initial_state.checkpoint}s")
        ENCB.update()
        while ENCB.short_count < 1:
            ENCB.update()
            position = ENCODER.position
            if position != last_position:
                initial_state.checkpoint = max(
                    0, encoder_handler(initial_state.checkpoint, 1)
                )
                display_message(
                    f"{game_mode.name}\nCheckpoint: {initial_state.checkpoint}s"
                )
            await asyncio.sleep(0.1)
    await asyncio.sleep(0.1)
    ENCB.update()
    await standby_screen(game_mode)


async def standby_screen(game_mode):
    """Pre-game confirmation screen"""
    await asyncio.sleep(0.5)
    ENCB.update()
    display_message(
        game_mode.set_message(
            initial_state.lives_count,
            initial_state.team,
            initial_state.game_length_str,
            initial_state.cap_length_str,
        )
    )
    led_state.update()
    await asyncio.sleep(0.5)
    while ENCB.value:
        ENCB.update()
    await asyncio.sleep(0.1)
    display_message(f"{game_mode.name}\nStarting...")
    await asyncio.sleep(0.1)
    ENCB.update()
    await game_mode.run_final_function()


async def start_attrition(game_mode):
    """Function for Attrition game mode"""
    local_state = initial_state
    await asyncio.sleep(0.5)
    display_message(f"{local_state.team} Lives Left\n{local_state.lives_count}")
    led_state.update(local_state.team)
    while local_state.lives_count > 0:
        ENCB.update()
        if not RED.value or not BLUE.value:
            local_state.lives_count -= 1
            led_state.update(local_state.team, "chase_off_on", 0.001)
            display_message(f"{local_state.team} Lives Left\n{local_state.lives_count}")
        if ENCB.long_press:
            break
        await asyncio.sleep(0.1)
    display_message(f"{local_state.team} Lives Left\n{local_state.lives_count}")
    led_state.update(local_state.team, "chase_on_off", repeat=-1)
    while not ENC.value:
        await asyncio.sleep(0.025)
    await restart(game_mode)


async def start_basic(game_mode):
    """Function for Basic Timer mode"""
    local_state = initial_state
    await asyncio.sleep(0.5)
    display_message(
        f"{local_state.game_length // 60:02d}:{local_state.game_length % 60:02d}"
    )
    play_track(28)
    await asyncio.sleep(6)
    ENCB.update()
    clock = monotonic()
    while local_state.game_length > 0:
        ENCB.update()
        if monotonic() - clock >= 1:
            if local_state.timer_state:
                local_state.game_length -= 1
                if local_state.game_length < 11:
                    play_track(local_state.game_length + 15)
            display_message(
                f"{local_state.game_length // 60:02d}:{local_state.game_length % 60:02d}"
            )
            clock = monotonic()
        if local_state.game_length == 30 and local_state.timer_state:
            play_track(26)
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            led_state.update(local_state.team, "chase_on_off", 0.0025)
            break
    await asyncio.sleep(0.1)
    ENCB.update()
    await restart(game_mode)


async def start_control(game_mode):
    """Function for Control game mode"""
    local_state = initial_state
    await asyncio.sleep(0.5)
    display_message(
        f"{game_mode.name} {local_state.game_length_str}\n{local_state.team} {local_state.cap_length_str}"
    )
    ENCB.update()
    clock = monotonic()
    while (local_state.game_length > 0 and not local_state.cap_state) or (
        local_state.cap_length > 0 and local_state.cap_state
    ):
        ENCB.update()
        REDB.update()
        BLUEB.update()
        if REDB.rose or BLUEB.rose and local_state.timer_state:
            local_state.cap_state = False
            local_state.cap_length = (
                (local_state.cap_length - 1) // local_state.checkpoint + 1
            ) * local_state.checkpoint
            led_state.update(delay=0.001)
        if REDB.fell or BLUEB.fell and local_state.timer_state:
            local_state.cap_state = True
            led_state.update(local_state.team, delay=0.001)
        if monotonic() - clock >= 1:
            if local_state.timer_state:
                local_state.game_length = max(0, local_state.game_length - 1)
                local_state.game_length_str = f"{local_state.game_length // 60:02d}:{local_state.game_length % 60:02d}"
                if local_state.cap_state:
                    local_state.cap_length -= 1
                local_state.cap_length_str = f"{local_state.cap_length // 60:02d}:{local_state.cap_length % 60:02d}"
            display_message(
                f"{game_mode.name} {local_state.game_length_str}\n{local_state.team} {local_state.cap_length_str}"
            )
            clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            break
    if local_state.cap_length == 0:
        display_message(f"{game_mode.name} {local_state.cap_length_str}\nPoint Locked")
    else:
        display_message(
            f"{game_mode.name} {local_state.cap_length_str}\n{local_state.team} {local_state.cap_length_str}"
        )
    await asyncio.sleep(0.5)
    ENCB.update()
    while ENCB.value:
        ENCB.update()
        if local_state.cap_length == 0:
            led_state.update(local_state.team, "chase_on_off")
        else:
            led_state.update()
    await asyncio.sleep(0.1)
    ENCB.update()
    await restart(game_mode)


async def start_deathclicks(game_mode):
    """Function for Death Clicks game mode"""
    local_state = initial_state
    await asyncio.sleep(0.5)
    display_message(f"{local_state.team} team\nDeaths {local_state.lives_count}")
    led_state.update(local_state.team)
    while not ENCB.long_press:
        ENCB.update()
        if not RED.value or not BLUE.value:
            local_state.lives_count += 1
            led_state.update(local_state.team, "chase_off_on", 0.001)
            display_message(
                f"{local_state.team} team\nDeaths {local_state.lives_count}"
            )
    led_state.update(local_state.team, "chase_off_on", 0.0025)
    await asyncio.sleep(0.1)
    ENCB.update()
    await restart(game_mode)


async def start_domination2(game_mode):
    """Function for Domination v2 game mode"""
    local_state = initial_state
    await asyncio.sleep(0.5)
    display_message(
        f"{local_state.team} Team\n{local_state.game_length // 60:02d}:{local_state.game_length % 60:02d}"
    )
    update_team("Green", state=local_state)
    clock = monotonic()
    while local_state.game_length > 0:
        ENCB.update()
        REDB.update()
        BLUEB.update()
        if REDB.long_press and local_state.timer_state:
            update_team("Red", 0.0025, local_state)
            display_message(
                f"{local_state.team} Team \n{local_state.game_length // 60:02d}:{local_state.game_length % 60:02d}"
            )
            print(f"{local_state.team} point control")
        elif BLUEB.long_press and local_state.timer_state:
            update_team("Blue", 0.0025, local_state)
            display_message(
                f"{local_state.team} Team \n{local_state.game_length // 60:02d}:{local_state.game_length % 60:02d}"
            )
            print(f"{local_state.team} point control")
        if monotonic() - clock >= 1:
            if local_state.timer_state:
                local_state.game_length -= 1
                local_state.game_length_str = f"{local_state.game_length // 60:02d}:{local_state.game_length % 60:02d}"
            display_message(f"{local_state.team} Team\n{local_state.game_length_str}")
            clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
            await asyncio.sleep(0.1)
        if ENCB.long_press:
            break
    display_message(f"{local_state.team} Team\nPoint Locked")
    while ENCB.value:
        ENCB.update()
        led_state.update(local_state.team, "chase_on_off")
    await asyncio.sleep(0.5)
    ENCB.update()
    await restart(game_mode)


async def start_domination3(game_mode):
    """Function for Domination v3 game mode"""
    local_state = initial_state
    await asyncio.sleep(0.5)
    local_state.timer_state = True
    display_message(
        f"RED: {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    update_team("Green", state=local_state)
    await asyncio.sleep(0.5)
    while RED.value and BLUE.value:
        ENCB.update()
        REDB.update()
        BLUEB.update()
    clock = monotonic()
    while local_state.red_time > 0 and local_state.blue_time > 0:
        ENCB.update()
        REDB.update()
        BLUEB.update()
        if REDB.long_press and local_state.team != "Red" and local_state.timer_state:
            update_team("Red", 0.0025, local_state)
        elif (
            BLUEB.long_press and local_state.team != "Blue" and local_state.timer_state
        ):
            update_team("Blue", 0.0025, local_state)
        if monotonic() - clock >= 1:
            if local_state.timer_state:
                if local_state.team == "Red":
                    local_state.red_time -= 1
                    local_state.red_time_str = f"{local_state.red_time // 60:02d}:{local_state.red_time % 60:02d}"
                elif local_state.team == "Blue":
                    local_state.blue_time -= 1
                    local_state.blue_time_str = f"{local_state.blue_time // 60:02d}:{local_state.blue_time % 60:02d}"
            display_message(
                f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
            )
            clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            break
    display_message(f"{local_state.team} Team\nPoint Locked")
    while ENCB.value:
        ENCB.update()
        led_state.update(local_state.team, "chase_on_off")
    await asyncio.sleep(0.5)
    ENCB.update()
    await restart(game_mode)


async def start_koth(game_mode):
    """Function for KotH timers"""
    local_state = initial_state
    await asyncio.sleep(0.5)
    display_message(
        f"RED: {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    update_team("Green", state=local_state)
    await asyncio.sleep(0.5)
    while REDB.value and BLUEB.value:
        ENCB.update()
        REDB.update()
        BLUEB.update()
    clock = monotonic()
    while local_state.red_time > 0 and local_state.blue_time > 0:
        ENCB.update()
        REDB.update()
        BLUEB.update()
        if not RED.value and local_state.team != "Red" and local_state.timer_state:
            update_team("Red", 0.0025, local_state)
            print(f"{local_state.team} timer started")
        elif not BLUE.value and local_state.team != "Blue" and local_state.timer_state:
            update_team("Blue", 0.0025, local_state)
            print(f"{local_state.team} timer started")
        if monotonic() - clock >= 1:
            if local_state.timer_state:
                if local_state.team == "Red":
                    local_state.red_time -= 1
                    local_state.red_time_str = f"{local_state.red_time // 60:02d}:{local_state.red_time % 60:02d}"
                elif local_state.team == "Blue":
                    local_state.blue_time -= 1
                    local_state.blue_time_str = f"{local_state.blue_time // 60:02d}:{local_state.blue_time % 60:02d}"
            display_message(
                f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
            )
            clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            break
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    while ENCB.value:
        ENCB.update()
        led_state.update(local_state.team, "chase_on_off")
    await asyncio.sleep(0.5)
    ENCB.update()
    await restart(game_mode)


async def restart(game_mode):
    """Function for restarting the program"""
    await asyncio.sleep(0.5)
    global position, last_position, initial_state
    position = ENCODER.position
    last_position = position
    led_state.update()
    display_message(f"Restart?:\n{RESTART_OPTIONS[initial_state.restart_index]}")
    await asyncio.sleep(0.5)
    ENCB.update()
    while ENCB.value:
        ENCB.update()
        position = ENCODER.position
        if position != last_position:
            initial_state.restart_index = encoder_handler(
                initial_state.restart_index, 1
            ) % len(RESTART_OPTIONS)
            display_message(
                f"Restart?:\n{RESTART_OPTIONS[initial_state.restart_index]}"
            )
    await asyncio.sleep(0.5)
    ENCB.update()
    if initial_state.restart_index == 0:
        if game_mode.has_team:
            update_team("Blue" if initial_state.team == "Red" else "Red")
            await standby_screen(game_mode)
        else:
            update_team("Green")
            await standby_screen(game_mode)
    elif initial_state.restart_index == 1:
        initial_state = Game_States()
        await main_menu()


###


class GameMode:
    def __init__(
        self,
        name,
        has_lives=False,
        has_team=False,
        has_game_length=False,
        has_cap_length=False,
        has_checkpoint=False,
    ):
        self.name = name
        self.has_lives = has_lives
        self.has_team = has_team
        self.has_game_length = has_game_length
        self.has_cap_length = has_cap_length
        self.has_checkpoint = has_checkpoint
        self.final_func_str = f"start_{self.name.replace(' ', '').lower()}"

    def set_message(self, lives=0, team="Green", length_str=0, cap_str=0):
        self.display_messages = {
            1: f"{self.name} Ready\nTeam lives {lives}",
            2: f"{self.name}\nReady {length_str}",
            3: f"{self.name} Ready\n{team} {length_str} {cap_str}",
            4: f"{self.name}\nReady Team {team}",
        }
        message = 1
        if self.has_lives:
            message = 1
        elif self.has_team:
            if self.has_game_length:
                message = 3
            else:
                message = 4
        elif self.has_game_length:
            message = 2
        return self.display_messages[message]

    async def run_final_function(self):
        final_func = globals().get(self.final_func_str, None)
        if callable(final_func):
            print(f"Running {self.final_func_str}")
            await final_func(self)
        else:
            print(f"Function {self.final_func_str} not found")


MODES = [
    GameMode("Attrition", has_lives=True, has_team=True),
    GameMode("Basic Timer", has_game_length=True),
    GameMode(
        "Control",
        has_team=True,
        has_game_length=True,
        has_cap_length=True,
        has_checkpoint=True,
    ),
    GameMode("Death Clicks", has_team=True),
    GameMode("Domination 2", has_game_length=True),
    GameMode("Domination 3", has_game_length=True),
    GameMode("KotH", has_game_length=True),
]


enable()

set_vol(30)


async def main():
    rgb_task = asyncio.create_task(rgb_control(led_state))
    game_task = asyncio.create_task(main_menu())
    await asyncio.gather(game_task, rgb_task)


if __name__ == "__main__":
    asyncio.run(main())
