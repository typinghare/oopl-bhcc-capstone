"""
Loop module.
"""
from typing import Callable, List


class Loop:
    """
    A frame-based loop that triggers a callback at specified intervals.
    """

    def __init__(self, fps: float, count_per_period: int, callback: Callable[[int], None]):
        # Frame per second, or count per second
        self.fps: float = fps

        # Number of counts per period
        self.count_per_period: int = count_per_period

        # Callback function to be triggered
        self.callback: Callable[[int], None] = callback

        # Time in milliseconds for one count
        self.each_count_time: float = 1000 / fps

        # Time elapsed since the last update
        self.elapsed_time: float = 0

        # Current count
        self.current_count: int = -1

        # Whether it is paused
        self.paused: bool = False

    def update(self, dt: float) -> None:
        """
        Update the frame-based loop. The callback is triggered at each count.
        :param dt: The delta time.
        """
        self.elapsed_time += dt

        if self.elapsed_time > (self.current_count + 1) * self.each_count_time:
            self.current_count += 1
            if self.current_count >= self.count_per_period:
                self.reset()

            self.callback(self.current_count)

    def reset(self) -> None:
        """
        Resets this loop.
        """
        self.elapsed_time = 0
        self.current_count = 0


class LoopManager:
    """
    Loop manager.
    """

    def __init__(self):
        # List of loops
        self._loop_list: List[Loop] = []

    def loop(self, fps: float, count_per_period: int, callback: Callable[[int], None]) -> Loop:
        """
        Registers a loop.
        :param fps: Frame per second, or count per second.
        :param count_per_period: Number of counts per period.
        :param callback: Callback function to be called.
        :return: The loop registered.
        """
        loop = Loop(fps, count_per_period, callback)
        self._loop_list.append(loop)

        return loop

    def once(self, fps: float, count_per_period: int, callback: Callable[[int], None]) -> Loop:
        """
        Registers a once loop.
        :param fps: Frame per second, or count per second.
        :param count_per_period: Number of counts per period.
        :param callback: Callback function to be called.
        :return: The once loop registered.
        """

        def func(index: int) -> None:
            callback(index)
            if index == count_per_period - 1:
                self._loop_list.remove(loop)

        loop = Loop(fps, count_per_period, func)
        self._loop_list.append(loop)

        return loop

    def delay(self, delay_ms: int, callback: Callable[[], None]) -> Loop:
        """
        Schedule a callback function to be executed after a specified delay.
        :param delay_ms: The delay time in milliseconds.
        :param callback: The function to be called after the delay.
        :return: The registered loop.
        """

        def delay_func(index: int) -> None:
            if index == 1:
                callback()

        return self.once(1000 / delay_ms, 2, delay_func)

    def remove(self, loop: Loop) -> None:
        """
        Removes a loop from the list if it exists.
        :param loop: The loop to remove.
        """
        if loop in self._loop_list:
            self._loop_list.remove(loop)

    def update(self, dt: float) -> None:
        """
        Updates all loops.
        """
        for loop in self._loop_list:
            if not loop.paused:
                loop.update(dt)
