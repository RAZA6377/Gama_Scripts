import bascenev1 as bs

from bascenev1lib.actor import playerspaz

import time


class NewPlayerSpaz(playerspaz.PlayerSpaz):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_input_time = time.time()

    def on_move_up_down(self, value: float) -> None:
        if not self.node:
            return
        super().on_move_up_down(value)
        self._last_input_time = time.time()

    def on_move_left_right(self, value: float) -> None:
        if not self.node:
            return
        super().on_move_left_right(value)
        self._last_input_time = time.time()

    def on_jump_press(self) -> None:
        if not self.node:
            return
        super().on_jump_press()
        self._last_input_time = time.time()

    def on_pickup_press(self) -> None:
        if not self.node:
            return
        super().on_pickup_press()
        self._last_input_time = time.time()

    def on_hold_position_press(self) -> None:
        if not self.node:
            return
        super().on_hold_position_press()
        self._last_input_time = time.time()

    def on_punch_press(self) -> None:
        if not self.node:
            return
        super().on_punch_press()
        self._last_input_time = time.time()

    def on_bomb_press(self) -> None:
        if not self.node:
            return
        super().on_bomb_press()
        self._last_input_time = time.time()

    def on_bomb_release(self) -> None:
        if not self.node:
            return
        super().on_bomb_release()
        self._last_input_time = time.time()

    def on_run(self, value: float) -> None:
        if not self.node:
            return
        super().on_run(value)
        self._last_input_time = time.time()

    def on_fly_press(self) -> None:
        if not self.node:
            return
        super().on_fly_press()
        self._last_input_time = time.time()


def enable():
    playerspaz.PlayerSpaz = NewPlayerSpaz
