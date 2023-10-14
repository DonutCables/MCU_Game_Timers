try:  # If running in CircuitPython
    from time import monotonic  # type: ignore
except ImportError:  # If running in MicroPython
    from hardware import monotonic

from asyncio import sleep, create_task, gather, run, Event
from gc import enable, mem_free  # type: ignore
from random import randint
from hardware import (
    DISPLAY,
    AUDIO_OUT,
    RGB_LED,
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
from audio_commands import Sound_Control
from led_commands import RGB_Control, RGB_Settings

"""
Setting initial variables for use
"""
# region
MODES = []
BUCKET_IDS = ["A", "B", "C", "D", "E", "F"]
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
    "Dino nuggies",
    "Bumper cars",
]
# endregion
"""
Important state management
"""
# region


class Game_States:
    """
    Captures all needed state variables for a game mode

    Attributes:
        menu_index (int): The current menu index.
        restart_index (int): The current restart index.
        lives_count (int): The number of lives remaining.
        team (str): The team name: "Red", "Blue", or "Green".
        game_length (int): The duration of the game in seconds.
        cap_length (int): The capture point length in seconds.
        checkpoint (int): The checkpoint value.
        timer_state (bool): The state of the timer (True for running, False for paused).
        cap_state (bool): The state of the capture.
        red_time (int): The remaining time for the red team.
        blue_time (int): The remaining time for the blue team.
    """

    def __init__(self):
        self.menu_index = 0
        self.restart_index = 0
        self.lives_count = 0
        self.id_index = 5
        self.bucket_count = 3
        self.team = "Green"
        self.game_length = 0
        self.cap_length = 0
        self.checkpoint = 1
        self.timer_state = True
        self.cap_state = False
        self.red_time = 0
        self.blue_time = 0

    @property
    def bucket_id(self):
        """The current bucket ID"""
        return BUCKET_IDS[self.id_index]

    @property
    def bucket_interval_upper(self):
        """The upper interval for the current bucket"""
        interval = self.game_length // (self.bucket_count * 2)
        start = interval * (self.bucket_count * 2 - self.id_index)
        stop = interval * (self.bucket_count * 2 - (self.id_index + 1))
        return (start, stop, -1)

    @property
    def bucket_interval_lower(self):
        """The lower interval for the current bucket"""
        interval = self.game_length // (self.bucket_count * 2)
        start = interval * (self.bucket_count - self.id_index)
        stop = interval * (self.bucket_count - (self.id_index + 1))
        return (start, stop, -1)

    @property
    def game_length_str(self):
        """A formatted string representation of game length"""
        return time_string(self.game_length)

    @property
    def cap_length_str(self):
        """A formatted string representation of cap length"""
        return time_string(self.cap_length)

    @property
    def red_time_str(self):
        """A formatted string representation of red team time"""
        return time_string(self.red_time)

    @property
    def blue_time_str(self):
        """A formatted string representation of blue team time"""
        return time_string(self.blue_time)

    def reset(self):
        """Resets all state variables to their initial values"""
        self.menu_index = 0
        self.restart_index = 0
        self.lives_count = 0
        self.id_index = 5
        self.bucket_count = 3
        self.team = "Green"
        self.game_length = 0
        self.cap_length = 0
        self.checkpoint = 1
        self.timer_state = True
        self.cap_state = False
        self.red_time = 0
        self.blue_time = 0


class ENC_States:
    """Manages encoder pressed state and rotation"""

    def __init__(self, enc=ENC, encoder=ENCODER):
        self.enc = enc
        self.encoder = encoder
        self._was_pressed = Event()
        self.last_position = self.encoder.position
        self._was_rotated = Event()

    async def update(self):
        """Updates the pressed state of the encoder"""
        while True:
            if not self.enc.value and not self._was_pressed.is_set():
                self._was_pressed.set()
                await sleep(0.2)
            if (
                self.encoder.position != self.last_position
                and not self._was_rotated.is_set()
            ):
                self._was_rotated.set()
            await sleep(0)

    def encoder_handler(self, x, y):
        """Handles encoder rotation"""
        while True:
            if self.encoder.position > self.last_position:
                self.last_position = self.encoder.position
                self._was_rotated.clear()
                return x + y
            elif self.encoder.position < self.last_position:
                self.last_position = self.encoder.position
                self._was_rotated.clear()
                return x - y


async def button_monitor():
    """Async function for monitoring button presses"""
    while True:
        ENCB.update()
        REDB.update()
        BLUEB.update()
        await sleep(0)


initial_state = Game_States()
ENCS = ENC_States()
SOUND = Sound_Control(AUDIO_OUT)
RGB = RGB_Control(RGB_LED)
RGBS = RGB_Settings()

# endregion
"""
Simple helper functions
"""
# region


def shallow_copy(obj):
    """Returns a shallow copy of an object"""
    new_instance = obj.__class__()
    for key, value in obj.__dict__.items():
        setattr(new_instance, key, value)
    return new_instance


def time_string(seconds):
    """Returns a formatted string representation of time in seconds"""
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def display_message(message):
    """
    Displays a string to the 1602 LCD

    Note: if a line is already 16chars when a n\\ is added, it will skip the next line
    """
    DISPLAY.clear()
    DISPLAY.write(message)


def update_team(
    team="Green", pattern="chase", delay=0.005, state=initial_state, hold=False
):
    """Updates button LED and RGB state based on team"""
    state.team = team
    RED_LED.value = "Red" in team
    BLUE_LED.value = "Blue" in team
    RGBS.update(team, pattern, delay, hold=hold)


# endregion
"""
More substantial game mode helper functions
"""
# region


async def counter_screen(game_mode):
    """Screen used to set lives for Attrition"""
    await sleep(0.5)
    ENCS._was_pressed.clear()
    display_message(f"{game_mode.name} \nLives: {initial_state.lives_count}")
    while True:
        if ENCS._was_rotated.is_set():
            initial_state.lives_count = max(
                0, ENCS.encoder_handler(initial_state.lives_count, 1)
            )
            display_message(f"{game_mode.name}\nLives: {initial_state.lives_count}")
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    await sleep(0)


async def identity_screen(game_mode):
    """Screen to set bucket identifier for swapping-based game modes"""
    await sleep(0.5)
    ENCS._was_pressed.clear()
    display_message(f"{game_mode.name}\nBucket ID: {initial_state.bucket_id}")
    while True:
        if ENCS._was_rotated.is_set():
            initial_state.id_index = ENCS.encoder_handler(
                initial_state.id_index, 1
            ) % len(BUCKET_IDS)
            display_message(f"{game_mode.name}\nBucket ID: {initial_state.bucket_id}")
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    display_message(f"{game_mode.name}\nBucket Count: {initial_state.bucket_count}")
    while True:
        if ENCS._was_rotated.is_set():
            initial_state.bucket_count = ENCS.encoder_handler(
                initial_state.bucket_count, 1
            ) % len(BUCKET_IDS)
            display_message(
                f"{game_mode.name}\nBucket Count: {initial_state.bucket_count}"
            )
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    await sleep(0)


async def team_screen(game_mode):
    """Screen for selecting team counter for Attrition and Death Clicks"""
    await sleep(0.5)
    ENCS._was_pressed.clear()
    display_message(f"{game_mode.name}\nTeam:")
    while True:
        if REDB.rose:
            update_team("Red", delay=0.0025)
            display_message(f"{game_mode.name}\nTeam {initial_state.team}")
            await sleep(0.1)
        if BLUEB.rose:
            update_team("Blue", delay=0.0025)
            display_message(f"{game_mode.name}\nTeam {initial_state.team}")
            await sleep(0.1)
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    await sleep(0)


async def timer_screen(game_mode):
    """Screen used to set time for game modes with built in timers"""
    await sleep(0.5)
    ENCS._was_pressed.clear()
    display_message(f"{game_mode.name}\nTime: {initial_state.game_length_str}")
    while True:
        if ENCS._was_rotated.is_set():
            initial_state.game_length = max(
                0, ENCS.encoder_handler(initial_state.game_length, 15)
            )
            display_message(f"{game_mode.name}\nTime: {initial_state.game_length_str}")
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    if game_mode.has_cap_length:
        display_message(f"{game_mode.name}\nCap time: {initial_state.cap_length_str}")
        while True:
            if ENCS._was_rotated.is_set():
                initial_state.cap_length = max(
                    0, ENCS.encoder_handler(initial_state.cap_length, 5)
                )
                display_message(
                    f"{game_mode.name}\nCap time: {initial_state.cap_length_str}"
                )
            if ENCS._was_pressed.is_set():
                ENCS._was_pressed.clear()
                break
            await sleep(0)
    if game_mode.has_checkpoint:
        display_message(f"{game_mode.name}\nCheckpoint: {initial_state.checkpoint}s")
        while True:
            if ENCS._was_rotated.is_set():
                initial_state.checkpoint = max(
                    0, ENCS.encoder_handler(initial_state.checkpoint, 1)
                )
                display_message(
                    f"{game_mode.name}\nCheckpoint: {initial_state.checkpoint}s"
                )
            if ENCS._was_pressed.is_set():
                ENCS._was_pressed.clear()
                break
            await sleep(0)
    await sleep(0)


# endregion
"""
Primary function to select GameMode instance, then pass control to it
"""
# region


async def main_menu():
    """Main menu for scrolling and displaying game options"""
    display_message(EXTRAS[randint(0, len(EXTRAS) - 1)])
    RGBS.update(pattern="solid")
    await sleep(0.5)
    for color in ["Red", "Blue", "Green"]:
        update_team(color, hold=True)
        while RGBS.hold:
            await sleep(0)
    display_message(f"Select a game:\n{MODES[initial_state.menu_index].name}")
    ENCS._was_pressed.clear()
    while True:
        if ENCS._was_rotated.is_set():
            initial_state.menu_index = ENCS.encoder_handler(
                initial_state.menu_index, 1
            ) % len(MODES)
            display_message(f"Select a game:\n{MODES[initial_state.menu_index].name}")
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    await sleep(0.1)
    display_message(f"Running:\n{MODES[initial_state.menu_index].name}")
    await MODES[initial_state.menu_index].game_setup()


# endregion
"""
Per game mode functions
"""
# region


async def start_attrition(game_mode):
    """Function for Attrition game mode"""
    local_state = shallow_copy(initial_state)
    await sleep(0.5)
    display_message(f"{local_state.team} Lives Left\n{local_state.lives_count}")
    RGBS.update(local_state.team)
    while local_state.lives_count > 0:
        if REDB.short_count > 0 or BLUEB.short_count > 0:
            local_state.lives_count -= 1
            display_message(f"{local_state.team} Lives Left\n{local_state.lives_count}")
            RGBS.update(local_state.team, "chase_off_on", 0.001)
            await sleep(0)
        if REDB.long_press or BLUEB.long_press:
            local_state.lives_count = min(
                initial_state.lives_count, local_state.lives_count + 1
            )
            display_message(f"{local_state.team} Lives Left\n{local_state.lives_count}")
            await sleep(0)
        if ENCB.long_press:
            break
        await sleep(0)
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    display_message(f"{local_state.team} Lives Left\n{local_state.lives_count}")
    await sleep(0.1)
    while True:
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_basictimer(game_mode):
    """Function for Basic Timer mode"""
    local_state = shallow_copy(initial_state)
    await sleep(0.5)
    display_message(local_state.game_length_str)
    SOUND.play_track(28)
    await sleep(6)
    clock = monotonic()
    while local_state.game_length > 0:
        if monotonic() - clock >= 1:
            if local_state.timer_state:
                local_state.game_length -= 1
                if local_state.game_length < 11:
                    SOUND.play_track(local_state.game_length + 15)
            display_message(local_state.game_length_str)
            clock = monotonic()
        if local_state.game_length == 30 and local_state.timer_state:
            SOUND.play_track(26)
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            RGBS.update(local_state.team, "chase_on_off", 0.0025)
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_control(game_mode):
    """Function for Control game mode"""
    local_state = shallow_copy(initial_state)
    await sleep(0.5)
    display_message(
        f"{game_mode.name} {local_state.game_length_str}\n{local_state.team} {local_state.cap_length_str}"
    )
    clock = monotonic()
    while (local_state.game_length > 0 and not local_state.cap_state) or (
        local_state.cap_length > 0 and local_state.cap_state
    ):
        if REDB.rose or BLUEB.rose and local_state.timer_state:
            local_state.cap_state = False
            local_state.cap_length = (
                (local_state.cap_length - 1) // local_state.checkpoint + 1
            ) * local_state.checkpoint
            RGBS.update(delay=0.001)
        if REDB.fell or BLUEB.fell and local_state.timer_state:
            local_state.cap_state = True
            RGBS.update(local_state.team, delay=0.001)
        if monotonic() - clock >= 1:
            if local_state.timer_state:
                local_state.game_length = max(0, local_state.game_length - 1)
                if local_state.cap_state:
                    local_state.cap_length -= 1
            display_message(
                f"{game_mode.name} {local_state.game_length_str}\n{local_state.team} {local_state.cap_length_str}"
            )
            clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            break
        await sleep(0)
    if local_state.cap_length == 0:
        display_message(f"{game_mode.name} {local_state.cap_length_str}\nPoint Locked")
    else:
        display_message(
            f"{game_mode.name} {local_state.game_length_str}\n{local_state.team} {local_state.cap_length_str}"
        )
    await sleep(0.5)
    if local_state.cap_length == 0:
        RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    else:
        RGBS.update()
    while True:
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_deathclicks(game_mode):
    """Function for Death Clicks game mode"""
    local_state = shallow_copy(initial_state)
    await sleep(0.5)
    display_message(f"{local_state.team} team\nDeaths {local_state.lives_count}")
    RGBS.update(local_state.team)
    while not ENCB.long_press:
        if REDB.short_count > 0 or BLUEB.short_count > 0:
            local_state.lives_count += 1
            display_message(
                f"{local_state.team} team\nDeaths {local_state.lives_count}"
            )
            RGBS.update(local_state.team, "chase_off_on", 0.001)
            await sleep(0)
        if REDB.long_press or BLUEB.long_press:
            local_state.lives_count = max(0, local_state.lives_count - 1)
            display_message(
                f"{local_state.team} team\nDeaths {local_state.lives_count}"
            )
            await sleep(0)
        await sleep(0)
    RGBS.update(local_state.team, "chase_off_on", 0.0025)
    await sleep(0.1)
    await game_mode.restart()


async def start_domination2(game_mode):
    """Function for Domination v2 game mode"""
    local_state = shallow_copy(initial_state)
    await sleep(0.5)
    display_message(f"{local_state.team} Team\n{local_state.game_length_str}")
    update_team(state=local_state)
    clock = monotonic()
    while local_state.game_length > 0:
        if REDB.long_press and local_state.timer_state:
            update_team("Red", delay=0.0025, state=local_state)
            display_message(f"{local_state.team} Team \n{local_state.game_length_str}")
            print(f"{local_state.team} point control")
        elif BLUEB.long_press and local_state.timer_state:
            update_team("Blue", delay=0.0025, state=local_state)
            display_message(f"{local_state.team} Team \n{local_state.game_length_str}")
            print(f"{local_state.team} point control")
        if monotonic() - clock >= 1:
            if local_state.timer_state:
                local_state.game_length -= 1
            display_message(f"{local_state.team} Team\n{local_state.game_length_str}")
            clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
            await sleep(0.1)
        if ENCB.long_press:
            break
        await sleep(0)
    display_message(f"{local_state.team} Team\nPoint Locked")
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    while True:
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_domination3(game_mode):
    """Function for Domination v3 game mode"""
    local_state = shallow_copy(initial_state)
    await sleep(0.5)
    local_state.red_time = local_state.game_length
    local_state.blue_time = local_state.game_length
    display_message(
        f"RED: {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    update_team(state=local_state)
    await sleep(0.5)
    while RED.value and BLUE.value:
        await sleep(0)
    clock = monotonic()
    while local_state.red_time > 0 and local_state.blue_time > 0:
        if REDB.long_press and local_state.team != "Red" and local_state.timer_state:
            update_team("Red", delay=0.0025, state=local_state)
        elif (
            BLUEB.long_press and local_state.team != "Blue" and local_state.timer_state
        ):
            update_team("Blue", delay=0.0025, state=local_state)
        if monotonic() - clock >= 1:
            if local_state.timer_state:
                if local_state.team == "Red":
                    local_state.red_time -= 1
                elif local_state.team == "Blue":
                    local_state.blue_time -= 1
            display_message(
                f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
            )
            clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            break
        await sleep(0)
    display_message(f"{local_state.team} Team\nPoint Locked")
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    while True:
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_koth(game_mode):
    """Function for KotH timers"""
    local_state = shallow_copy(initial_state)
    await sleep(0.5)
    local_state.red_time = local_state.game_length
    local_state.blue_time = local_state.game_length
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    update_team(state=local_state)
    await sleep(0.5)
    while REDB.value and BLUEB.value:
        await sleep(0)
    clock = monotonic()
    while local_state.red_time > 0 and local_state.blue_time > 0:
        if local_state.timer_state:
            if not RED.value and local_state.team != "Red" and local_state.timer_state:
                update_team("Red", delay=0.0025, state=local_state)
                print(f"{local_state.team} timer started")
            elif (
                not BLUE.value
                and local_state.team != "Blue"
                and local_state.timer_state
            ):
                update_team("Blue", delay=0.0025, state=local_state)
                print(f"{local_state.team} timer started")
            if monotonic() - clock >= 1:
                if local_state.team == "Red":
                    local_state.red_time -= 1
                elif local_state.team == "Blue":
                    local_state.blue_time -= 1
                display_message(
                    f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
                )
                clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            break
        await sleep(0)
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    while True:
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_kothmoving(game_mode):
    """Function for moving KotH game mode"""
    local_state = shallow_copy(initial_state)
    await sleep(0.5)
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    update_team(state=local_state)
    clock = monotonic()
    while local_state.game_length > 0:
        if local_state.timer_state:
            if local_state.game_length in range(
                *initial_state.bucket_interval_upper
            ) or local_state.game_length in range(*initial_state.bucket_interval_lower):
                if not local_state.cap_state:
                    update_team(state=local_state)
                    local_state.cap_state = True
                    print("cap on")
            else:
                if local_state.cap_state:
                    RGBS.update(delay=0.0025)
                    local_state.cap_state = False
                    print("cap off")
            if local_state.cap_state:
                if not RED.value and local_state.team != "Red":
                    update_team("Red", delay=0.0025, state=local_state)
                    print(f"{local_state.team} timer started")
                elif not BLUE.value and local_state.team != "Blue":
                    update_team("Blue", delay=0.0025, state=local_state)
                    print(f"{local_state.team} timer started")
            if monotonic() - clock >= 1:
                local_state.game_length -= 1
                if local_state.cap_state:
                    if local_state.team == "Red":
                        local_state.red_time += 1
                    elif local_state.team == "Blue":
                        local_state.blue_time += 1
                display_message(
                    f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
                )
                print(local_state.game_length, local_state.cap_state)
                clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            break
        await sleep(0)
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    if local_state.red_time > local_state.blue_time:
        update_team("Red", delay=0.0025, state=local_state)
    elif local_state.blue_time > local_state.red_time:
        update_team("Blue", delay=0.0025, state=local_state)
    else:
        update_team("Green", delay=0.0025, state=local_state)
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    while True:
        if ENCS._was_pressed.is_set():
            ENCS._was_pressed.clear()
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


# endregion
"""
Program initialization
"""
# region


class GameMode:
    def __init__(
        self,
        name,
        has_lives=False,
        has_id=False,
        has_team=False,
        has_game_length=False,
        has_cap_length=False,
        has_checkpoint=False,
    ):
        self.name = name
        self.has_lives = has_lives
        self.has_id = has_id
        self.has_team = has_team
        self.has_game_length = has_game_length
        self.has_cap_length = has_cap_length
        self.has_checkpoint = has_checkpoint
        self.final_func_str = f"start_{self.name.replace(' ', '').lower()}"

    def set_message(self):
        self.display_messages = {
            1: f"{self.name} Ready\nTeam lives {initial_state.lives_count}",
            2: f"{self.name}\nReady {initial_state.game_length_str}",
            3: f"{self.name} Ready\n{initial_state.team} {initial_state.game_length_str} {initial_state.cap_length_str}",
            4: f"{self.name}\nReady Team {initial_state.team}",
            5: f"{self.name}\nReady {initial_state.game_length_str} {initial_state.bucket_id}",
        }
        message = 1
        if self.has_lives:
            message = 1
        elif self.has_id:
            message = 5
        elif self.has_team:
            if self.has_game_length:
                message = 3
            else:
                message = 4
        elif self.has_game_length:
            message = 2
        return self.display_messages[message]

    async def game_setup(self):
        if self.has_lives:
            await counter_screen(self)
        if self.has_id:
            await identity_screen(self)
        if self.has_team:
            await team_screen(self)
        if self.has_game_length:
            await timer_screen(self)
        await self.standby_screen()

    async def standby_screen(self):
        """
        Pre-game confirmation screen.
        Also handles restarting or reseting the mode.
        """
        while True:
            await sleep(0.5)
            display_message(self.set_message())
            RGBS.update()
            await sleep(0.5)
            while True:
                if ENCS._was_pressed.is_set():
                    ENCS._was_pressed.clear()
                    break
                await sleep(0)
            display_message(f"{self.name}\nStarting...")
            await sleep(0)
            await self.run_final_function()
            if initial_state.restart_index == 0:
                break
            elif initial_state.restart_index == 1:
                pass
        return

    async def restart(self):
        """Function for restarting the program"""
        await sleep(0.5)
        RESTART_OPTIONS = ["No", "Yes"]
        RGBS.update()
        display_message(f"Restart?:\n{RESTART_OPTIONS[initial_state.restart_index]}")
        await sleep(0.5)
        ENCS._was_pressed.clear()
        while True:
            if ENCS._was_rotated.is_set():
                initial_state.restart_index = ENCS.encoder_handler(
                    initial_state.restart_index, 1
                ) % len(RESTART_OPTIONS)
                display_message(
                    f"Restart?:\n{RESTART_OPTIONS[initial_state.restart_index]}"
                )
            if ENCS._was_pressed.is_set():
                ENCS._was_pressed.clear()
                break
            await sleep(0)
        await sleep(0.5)
        print(mem_free())
        if initial_state.restart_index == 1:
            if self.has_team:
                update_team("Blue" if initial_state.team == "Red" else "Red")
            else:
                update_team()
        await sleep(0.5)
        return

    async def run_final_function(self):
        final_func = globals().get(self.final_func_str, None)
        if callable(final_func):
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
    GameMode("Koth Moving", has_id=True, has_game_length=True),
]


enable()

SOUND.set_vol(30)


async def game_task_chain():
    """Task chain for running the program"""
    while True:
        await main_menu()
        initial_state.reset()


async def main():
    rgb_task = create_task(RGBS.rgb_control(RGB))
    enc_task = create_task(ENCS.update())
    button_task = create_task(button_monitor())
    game_task = create_task(game_task_chain())
    await gather(game_task, rgb_task, enc_task, button_task)


if __name__ == "__main__":
    run(main())
# endregion
