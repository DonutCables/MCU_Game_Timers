"""
Imports
"""
# region
import espnow  # type: ignore
from binascii import unhexlify
from os import getenv
from time import monotonic
from asyncio import sleep, create_task, gather, run, Event
from gc import enable, mem_free  # type: ignore
from random import randint
from hardware import (
    DISPLAY,
    # AUDIO_OUT,
    RGB_LED,
    ENCODER,
    RED_LED,
    BLUE_LED,
    ENCB,
    REDB,
    BLUEB,
)

# from audio_commands import Sound_Control
from led_commands import RGB_Control, RGB_Settings

# endregion
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
        self.dd_loop = 2
        self.timer_state = True
        self.cap_state = False
        self.red_time = 0
        self.blue_time = 0

    @property
    def bucket_id(self):
        """The current bucket ID"""
        return BUCKET_IDS[self.id_index]

    @property
    def bucket_interval(self):
        interval = self.game_length // (self.bucket_count * self.dd_loop)
        return interval

    @property
    def bucket_interval_upper(self):
        """The upper interval for the current bucket"""
        start = self.bucket_interval * (
            self.bucket_count * self.dd_loop - self.id_index
        )
        stop = self.bucket_interval * (
            self.bucket_count * self.dd_loop - (self.id_index + 1)
        )
        return (start, stop, -1)

    @property
    def bucket_interval_lower(self):
        """The lower interval for the current bucket"""
        start = self.bucket_interval * (self.bucket_count - self.id_index)
        stop = self.bucket_interval * (self.bucket_count - (self.id_index + 1))
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

    def shallow_copy(self):
        """Returns a shallow copy of an object"""
        new_instance = self.__class__()
        for key, value in self.__dict__.items():
            setattr(new_instance, key, value)
        return new_instance

    def update_team(
        self,
        team="Green",
        pattern="chase",
        delay=0.005,
        hold=False,
    ):
        """Updates button LED and RGB state based on team"""
        self.team = team
        RED_LED.value = "Red" in team
        BLUE_LED.value = "Blue" in team
        print(team)
        RGBS.update(team, pattern, delay, hold=hold)

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
        self.dd_loop = 2
        self.timer_state = True
        self.cap_state = False
        self.red_time = 0
        self.blue_time = 0


class ENC_States:
    """Manages encoder rotation"""

    def __init__(self, encoder=ENCODER):
        self.encoder = encoder
        self.last_position = self.encoder.position
        self._was_rotated = Event()

    async def update(self):
        """Updates the pressed state of the encoder"""
        while True:
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
# SOUND = Sound_Control(AUDIO_OUT)
RGB = RGB_Control(RGB_LED)
RGBS = RGB_Settings()

# endregion
"""
Simple helper functions
"""
# region


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
        initial_state.update_team(color, hold=True)
        while RGBS.hold:
            await sleep(0)
    display_message(f"Select a game:\n{MODES[initial_state.menu_index].name}")
    while True:
        if ENCS._was_rotated.is_set():
            initial_state.menu_index = ENCS.encoder_handler(
                initial_state.menu_index, 1
            ) % len(MODES)
            display_message(f"Select a game:\n{MODES[initial_state.menu_index].name}")
        if ENCB.short_count > 0:
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
    local_state = initial_state.shallow_copy()
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
            display_message("exiting...")
            await sleep(0.5)
            break
        await sleep(0)
    display_message(f"{local_state.team} Lives Left\n{local_state.lives_count}")
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    while True:
        if ENCB.short_count > 0:
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_control(game_mode):
    """Function for Control game mode"""
    local_state = initial_state.shallow_copy()
    await sleep(0.5)
    display_message(
        f"{game_mode.name} {local_state.game_length_str}\n{local_state.team} {local_state.cap_length_str}"
    )
    RGBS.update("Green")
    clock = monotonic()
    while (local_state.game_length > 0 and not local_state.cap_state) or (
        local_state.cap_length > 0 and local_state.cap_state
    ):
        if local_state.timer_state:
            if REDB.rose or BLUEB.rose:
                local_state.cap_state = False
                local_state.cap_length = (
                    (local_state.cap_length - 1) // local_state.checkpoint + 1
                ) * local_state.checkpoint
                RGBS.update("Green", delay=0.001)
            if REDB.fell or BLUEB.fell:
                local_state.cap_state = True
                RGBS.update(local_state.team, delay=0.001)
            if monotonic() - clock >= 1:
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
            display_message("exiting...")
            await sleep(0.5)
            break
        await sleep(0)
    if local_state.cap_length == 0:
        display_message(f"{game_mode.name} {local_state.cap_length_str}\nPoint Locked")
    else:
        display_message(
            f"{game_mode.name} {local_state.game_length_str}\n{local_state.team} {local_state.cap_length_str}"
        )
    if local_state.cap_length == 0:
        RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    else:
        RGBS.update()
    while True:
        if ENCB.short_count > 0:
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_deathclicks(game_mode):
    """Function for Death Clicks game mode"""
    local_state = initial_state.shallow_copy()
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
    await sleep(0.1)
    await game_mode.restart()


async def start_domination2(game_mode):
    """Function for Domination v2 game mode"""
    local_state = initial_state.shallow_copy()
    await sleep(0.5)
    display_message(f"{local_state.team} Team\n{local_state.game_length_str}")
    local_state.update_team()
    clock = monotonic()
    while local_state.game_length > 0:
        if local_state.timer_state:
            if REDB.long_press:
                local_state.update_team("Red", delay=0.0025)
                display_message(
                    f"{local_state.team} Team \n{local_state.game_length_str}"
                )
            elif BLUEB.long_press:
                local_state.update_team("Blue", delay=0.0025)
                display_message(
                    f"{local_state.team} Team \n{local_state.game_length_str}"
                )
            if monotonic() - clock >= 1:
                local_state.game_length -= 1
                display_message(
                    f"{local_state.team} Team\n{local_state.game_length_str}"
                )
                clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
            await sleep(0.1)
        if ENCB.long_press:
            display_message("exiting...")
            await sleep(0.5)
            break
        await sleep(0)
    display_message(f"{local_state.team} Team\nPoint Locked")
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    while True:
        if ENCB.short_count > 0:
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_domination3(game_mode):
    """Function for Domination v3 game mode"""
    local_state = initial_state.shallow_copy()
    await sleep(0.5)
    local_state.red_time = local_state.game_length
    local_state.blue_time = local_state.game_length
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    local_state.update_team()
    clock = monotonic()
    while local_state.red_time > 0 and local_state.blue_time > 0:
        if local_state.timer_state:
            if REDB.long_press and local_state.team != "Red":
                local_state.update_team("Red", delay=0.0025)
            elif BLUEB.long_press and local_state.team != "Blue":
                local_state.update_team("Blue", delay=0.0025)
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
            display_message("exiting...")
            await sleep(0.5)
            break
        await sleep(0)
    display_message(f"{local_state.team} Team\nPoint Locked")
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    while True:
        if ENCB.short_count > 0:
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_domination(game_mode):
    """Function for Domination game mode"""
    local_state = initial_state.shallow_copy()
    await sleep(0.5)
    local_state.red_time = 0
    local_state.blue_time = 0
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    local_state.update_team()
    clock = monotonic()
    while local_state.game_length > 0:
        if local_state.timer_state:
            if REDB.long_press and local_state.team != "Red":
                local_state.update_team("Red", delay=0.0025)
            elif BLUEB.long_press and local_state.team != "Blue":
                local_state.update_team("Blue", delay=0.0025)
            if monotonic() - clock >= 1:
                local_state.game_length -= 1
                if local_state.team == "Red":
                    local_state.red_time += 1
                elif local_state.team == "Blue":
                    local_state.blue_time += 1
                display_message(
                    f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
                )
                clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            display_message("exiting...")
            await sleep(0.5)
            break
        await sleep(0)
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    if local_state.red_time > local_state.blue_time:
        local_state.update_team("Red", delay=0.0025)
    elif local_state.blue_time > local_state.red_time:
        local_state.update_team("Blue", delay=0.0025)
    else:
        local_state.update_team("Green", delay=0.0025)
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    while True:
        if ENCB.short_count > 0:
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_koth(game_mode):
    """Function for KotH timers"""
    local_state = initial_state.shallow_copy()
    await sleep(0.5)
    local_state.red_time = local_state.game_length
    local_state.blue_time = local_state.game_length
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    local_state.update_team()
    clock = monotonic()
    while local_state.red_time > 0 and local_state.blue_time > 0:
        if local_state.timer_state:
            if REDB.fell and local_state.team != "Red":
                local_state.update_team("Red", delay=0.0025)
            if BLUEB.fell and local_state.team != "Blue":
                local_state.update_team("Blue", delay=0.0025)
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
            display_message("exiting...")
            await sleep(0.5)
            break
        await sleep(0)
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    while True:
        if ENCB.short_count > 0:
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_doordash1(game_mode):
    """Function for DoorDash/moving KotH game mode"""
    local_state = initial_state.shallow_copy()
    await sleep(0.5)
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    clock = monotonic()
    while local_state.game_length > 0:
        if local_state.timer_state:
            if local_state.game_length in range(
                *initial_state.bucket_interval_upper
            ) or local_state.game_length in range(*initial_state.bucket_interval_lower):
                if not local_state.cap_state:
                    local_state.update_team()
                    local_state.cap_state = True
            else:
                if local_state.cap_state:
                    RGBS.update(delay=0.0025)
                    local_state.cap_state = False
            if local_state.cap_state:
                if REDB.fell and local_state.team != "Red":
                    local_state.update_team("Red", delay=0.0025)
                elif BLUEB.fell and local_state.team != "Blue":
                    local_state.update_team("Blue", delay=0.0025)
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
                clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            display_message("exiting...")
            await sleep(0.5)
            break
        await sleep(0)
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    if local_state.red_time > local_state.blue_time:
        local_state.update_team("Red", delay=0.0025)
    elif local_state.blue_time > local_state.red_time:
        local_state.update_team("Blue", delay=0.0025)
    else:
        local_state.update_team("Green", delay=0.0025)
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)

    while True:
        if ENCB.short_count > 0:
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


async def start_doordash2(game_mode):
    """Function for DoorDash/moving KotH game mode"""
    local_state = initial_state.shallow_copy()
    await sleep(0.5)
    message = b"empty"
    msg_dec = message.decode()
    display_message("Waiting for timer...")
    while True:
        if e:
            msg = e.read()
            if msg.msg is not None and msg.msg != message:
                message = msg.msg
                msg_dec = message.decode()
                if msg_dec == "Start":
                    await sleep(6)
                    break
        if ENCB.short_count > 1:
            break
        await sleep(0)
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    local_state.update_team()
    clock = monotonic()
    while True:
        if local_state.timer_state:
            if local_state.cap_state:
                if REDB.fell and local_state.team != "Red":
                    local_state.update_team("Red", delay=0.0025)
                elif BLUEB.fell and local_state.team != "Blue":
                    local_state.update_team("Blue", delay=0.0025)
            if monotonic() - clock >= 1:
                if local_state.cap_state:
                    if local_state.team == "Red":
                        local_state.red_time += 1
                    elif local_state.team == "Blue":
                        local_state.blue_time += 1
                display_message(
                    f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
                )
                clock = monotonic()
        if ENCB.short_count > 1:
            local_state.timer_state = not local_state.timer_state
        if ENCB.long_press:
            display_message("exiting...")
            await sleep(0.5)
            break
        if e:
            msg = e.read()
            if msg is not None and msg != message:
                print(msg.msg)
                message = msg.msg
                msg_dec = message.decode()
                if msg_dec == "Pause":
                    local_state.timer_state = False
                    RGBS.update("Purple", delay=0.0025)
                elif msg_dec == "Resume":
                    local_state.timer_state = True
                    if local_state.cap_state:
                        RGBS.update(local_state.team, delay=0.0025)
                    else:
                        RGBS.update(delay=0.0025)
                elif msg_dec == "Active":
                    local_state.cap_state = True
                    local_state.update_team()
                    await sleep(0.1)
                elif msg_dec == "Inactive":
                    local_state.cap_state = False
                    RGBS.update(delay=0.0025)
                elif msg_dec == "End":
                    break
        await sleep(0)
    display_message(
        f"RED:  {local_state.red_time_str}\nBLUE: {local_state.blue_time_str}"
    )
    if local_state.red_time > local_state.blue_time:
        local_state.update_team("Red", delay=0.0025)
    elif local_state.blue_time > local_state.red_time:
        local_state.update_team("Blue", delay=0.0025)
    else:
        local_state.update_team("Green", delay=0.0025)
    RGBS.update(local_state.team, "chase_on_off", repeat=-1)
    while True:
        if ENCB.short_count > 0:
            break
        await sleep(0)
    await sleep(0.1)
    await game_mode.restart()


# endregion
"""
GameMode class and instantiation
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
        has_loop=False,
    ):
        self.name = name
        self.has_lives = has_lives
        self.has_id = has_id
        self.has_team = has_team
        self.has_game_length = has_game_length
        self.has_cap_length = has_cap_length
        self.has_checkpoint = has_checkpoint
        self.has_loop = has_loop
        self.final_func_str = f"start_{self.name.replace(' ', '').lower()}"

    def set_message(self):
        self.display_messages = {
            1: f"{self.name} Ready\nTeam lives {initial_state.lives_count}",
            2: f"{self.name}\nReady {initial_state.game_length_str}",
            3: f"{self.name} Ready\n{initial_state.team} {initial_state.game_length_str} {initial_state.cap_length_str}",
            4: f"{self.name}\nReady Team {initial_state.team}",
            5: f"{self.name} Ready\n{initial_state.game_length_str} {initial_state.bucket_id}",
        }
        message = 2
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
            await self.counter_screen()
        if self.has_id:
            await self.identity_screen()
        if self.has_team:
            await self.team_screen()
        if self.has_game_length:
            await self.timer_screen()
        await self.standby_screen()

    async def counter_screen(self):
        """Screen used to set lives for Attrition"""
        await sleep(0.5)
        display_message(f"{self.name} \nLives: {initial_state.lives_count}")
        while True:
            if ENCS._was_rotated.is_set():
                initial_state.lives_count = max(
                    0, ENCS.encoder_handler(initial_state.lives_count, 1)
                )
                display_message(f"{self.name}\nLives: {initial_state.lives_count}")
            if ENCB.short_count > 0:
                break
            await sleep(0)
        await sleep(0)

    async def identity_screen(self):
        """Screen to set bucket identifier for swapping-based game modes"""
        await sleep(0.5)
        display_message(f"{self.name}\nBucket ID: {initial_state.bucket_id}")
        while True:
            if ENCS._was_rotated.is_set():
                initial_state.id_index = ENCS.encoder_handler(
                    initial_state.id_index, 1
                ) % len(BUCKET_IDS)
                display_message(f"{self.name}\nBucket ID: {initial_state.bucket_id}")
            if ENCB.short_count > 0:
                break
            await sleep(0)
        display_message(f"{self.name}\nBucket Count: {initial_state.bucket_count}")
        await sleep(0)
        while True:
            if ENCS._was_rotated.is_set():
                initial_state.bucket_count = ENCS.encoder_handler(
                    initial_state.bucket_count, 1
                ) % len(BUCKET_IDS)
                display_message(
                    f"{self.name}\nBucket Count: {initial_state.bucket_count}"
                )
            if ENCB.short_count > 0:
                break
            await sleep(0)
        display_message(f"{self.name}\nLoop Count: {initial_state.dd_loop}")
        await sleep(0)
        while True:
            if ENCS._was_rotated.is_set():
                initial_state.dd_loop = max(
                    1, (ENCS.encoder_handler(initial_state.dd_loop, 1) % 3)
                )
                display_message(f"{self.name}\nLoop Count: {initial_state.dd_loop}")
            if ENCB.short_count > 0:
                break
            await sleep(0)
        await sleep(0)

    async def team_screen(self):
        """Screen for selecting team counter for Attrition and Death Clicks"""
        await sleep(0.5)
        display_message(f"{self.name}\nTeam:")
        while True:
            if REDB.rose:
                initial_state.update_team("Red", delay=0.0025)
                display_message(f"{self.name}\nTeam {initial_state.team}")
                await sleep(0.1)
            if BLUEB.rose:
                initial_state.update_team("Blue", delay=0.0025)
                display_message(f"{self.name}\nTeam {initial_state.team}")
                await sleep(0.1)
            if ENCB.short_count > 0:
                break
            await sleep(0)
        await sleep(0)

    async def timer_screen(self):
        """Screen used to set time for game modes with built in timers"""
        await sleep(0.5)
        display_message(f"{self.name}\nTime: {initial_state.game_length_str}")
        while True:
            if ENCS._was_rotated.is_set():
                initial_state.game_length = max(
                    0, ENCS.encoder_handler(initial_state.game_length, 15)
                )
                display_message(f"{self.name}\nTime: {initial_state.game_length_str}")
            if ENCB.short_count > 0:
                break
            await sleep(0)
        if self.has_cap_length:
            display_message(f"{self.name}\nCap time: {initial_state.cap_length_str}")
            await sleep(0)
            while True:
                if ENCS._was_rotated.is_set():
                    initial_state.cap_length = max(
                        0, ENCS.encoder_handler(initial_state.cap_length, 5)
                    )
                    display_message(
                        f"{self.name}\nCap time: {initial_state.cap_length_str}"
                    )
                if ENCB.short_count > 0:
                    break
                await sleep(0)
        if self.has_checkpoint:
            display_message(f"{self.name}\nCheckpoint: {initial_state.checkpoint}s")
            await sleep(0)
            while True:
                if ENCS._was_rotated.is_set():
                    initial_state.checkpoint = max(
                        0, ENCS.encoder_handler(initial_state.checkpoint, 1)
                    )
                    display_message(
                        f"{self.name}\nCheckpoint: {initial_state.checkpoint}s"
                    )
                if ENCB.short_count > 0:
                    break
                await sleep(0)
        await sleep(0)

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
                if ENCB.short_count > 0:
                    break
                e.read()
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

        while True:
            if ENCS._was_rotated.is_set():
                initial_state.restart_index = ENCS.encoder_handler(
                    initial_state.restart_index, 1
                ) % len(RESTART_OPTIONS)
                display_message(
                    f"Restart?:\n{RESTART_OPTIONS[initial_state.restart_index]}"
                )
            if ENCB.short_count > 0:
                break
            await sleep(0)
        await sleep(0.5)
        print(mem_free())
        if initial_state.restart_index == 1:
            if self.has_team:
                initial_state.update_team(
                    "Blue" if initial_state.team == "Red" else "Red"
                )
            else:
                initial_state.update_team()
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
    GameMode("Domination", has_game_length=True),
    GameMode("DoorDash 1", has_id=True, has_game_length=True),
    GameMode("DoorDash 2", has_id=True),
    GameMode("KotH", has_game_length=True),
]
# endregion
"""
ESP-NOW setup
"""
# region

e = espnow.ESPNow()

# endregion
"""
Main program
"""
# region

enable()

# SOUND.set_vol(30)


async def game_task_chain():
    """Task chain for running the program"""
    while True:
        await main_menu()
        initial_state.reset()


async def main():
    game_task = create_task(game_task_chain())
    rgb_task = create_task(RGBS.rgb_control(RGB))
    enc_task = create_task(ENCS.update())
    button_task = create_task(button_monitor())
    await gather(game_task, rgb_task, enc_task, button_task)


if __name__ == "__main__":
    run(main())
# endregion
