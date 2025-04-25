from __future__ import annotations

class MonotonicClock:
    """
    A psychopy-compatible monotonic clock using accurate system time.
    """
    def __init__(self) -> None:
        """
        Initialize a new MonotonicClock instance. Time will begin at 0.
        """
        pass

    def getTime(self) -> float:
        """
        Get the current time in seconds since the clock was started or last reset (only Clock,
        not MonotonicClock).
        """
        pass

    def getLastResetTime(self) -> float:
        """
        Get the time of the last reset in seconds.
        """
        pass

class Clock(MonotonicClock):
    """
    A psychopy-compatible clock that can be used to measure time intervals.
    """
    def __init__(self) -> None:
        """
        Initialize a new Clock instance. Will use accurate system time.
        """
        super().__init__()

    def reset(self, newT: float) -> None:
        """
        Reset the clock to the specified time value.

        Parameters
        ----------
        newT : float
            The time to reset the clock to, in seconds.
        """
        pass

    def addTime(self, t: float) -> None:
        """
        Add a specified amount of time to the clock.

        Parameters
        ----------
        t : float
            The amount of time to add, in seconds.
        """
        pass

def sleepers(t: float) -> None:
    """
    Sleep for a specified amount of time. Substantially more accurate than
    time.sleep().

    Parameters
    ----------
    t : float
        The amount of time to sleep, in seconds.
    """
    pass
