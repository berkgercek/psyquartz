from __future__ import annotations

class MonotonicClock:
    """A PsychoPy-compatible monotonic clock using the system time.

    On creation, the current UNIX epoch time is recorded as the baseline. All subsequent
    calls to :meth:`getTime` return the elapsed time since that baseline.

    Attributes
    ----------
    _timeAtLastReset : float
        UNIX epoch time (in seconds) recorded at clock creation or last reset.
    _epochTimeAtLastReset : float
        UNIX epoch time (in seconds) recorded at clock creation or last reset.

    Examples
    --------
    >>> import psyquartz
    >>> clock = psyquartz.MonotonicClock()
    >>> elapsed = clock.getTime()  # seconds since creation
    """

    _timeAtLastReset: float
    _epochTimeAtLastReset: float

    def __init__(self) -> None:
        """Create a new :class:`MonotonicClock`.

        The current UNIX epoch time is recorded as the baseline for all future
        :meth:`getTime` calls.

        Raises
        ------
        RuntimeError
            If the system clock cannot be read.
        """

    def getTime(self, applyZero: bool = True) -> float:
        """Get the current time from the clock.

        Parameters
        ----------
        applyZero : bool
            If ``True`` (default), return the elapsed time in seconds since the
            clock was created (or last reset for :class:`Clock`). If ``False``,
            return the raw UNIX epoch time in seconds.

        Returns
        -------
        float
            Time in seconds.

        Raises
        ------
        RuntimeError
            If the system clock cannot be read.

        Examples
        --------
        >>> import psyquartz
        >>> clock = psyquartz.MonotonicClock()
        >>> elapsed = clock.getTime()
        >>> raw_epoch = clock.getTime(applyZero=False)
        """

    def getLastResetTime(self) -> float:
        """Get the UNIX epoch time recorded at clock creation or last reset.

        Returns
        -------
        float
            UNIX epoch time in seconds.

        Examples
        --------
        >>> import psyquartz
        >>> clock = psyquartz.MonotonicClock()
        >>> clock.getLastResetTime()  # doctest: +SKIP
        1741193045.123456
        """

class Clock(MonotonicClock):
    """A PsychoPy-compatible resettable clock.

    Extends :class:`MonotonicClock` with :meth:`reset`, :meth:`addTime`, and
    :meth:`add` methods to manipulate the clock's baseline.

    Examples
    --------
    >>> import psyquartz
    >>> clock = psyquartz.Clock()
    >>> elapsed = clock.getTime()
    >>> clock.reset()  # restart from 0
    >>> clock.getTime()  # close to 0
    """

    def __init__(self) -> None:
        """Create a new :class:`Clock`.

        Raises
        ------
        RuntimeError
            If the system clock cannot be read.
        """

    def reset(self, newT: float = 0.0) -> None:
        """Reset the clock by re-capturing the current system time as baseline.

        Parameters
        ----------
        newT : float
            Currently unused. Reserved for PsychoPy API compatibility.

        Raises
        ------
        RuntimeError
            If the system clock cannot be read.

        Examples
        --------
        >>> import psyquartz
        >>> clock = psyquartz.Clock()
        >>> psyquartz.sleep(0.1)
        >>> clock.reset()
        >>> clock.getTime()  # close to 0
        """

    def addTime(self, t: float) -> None:
        """Shift the clock's baseline forward by ``t`` seconds.

        Adding time to the baseline makes future :meth:`getTime` calls return a smaller
        value, effectively subtracting ``t`` from the elapsed time.

        Parameters
        ----------
        t : float
            The amount of time to add to the baseline, in seconds.

        Examples
        --------
        >>> import psyquartz
        >>> clock = psyquartz.Clock()
        >>> clock.addTime(1.0)
        >>> clock.getTime()  # close to -1.0
        """

    def add(self, t: float) -> None:
        """Shift the clock's baseline forward by ``t`` seconds.

        Alias for :meth:`addTime`.

        Parameters
        ----------
        t : float
            The amount of time to add to the baseline, in seconds.

        Examples
        --------
        >>> import psyquartz
        >>> clock = psyquartz.Clock()
        >>> clock.add(1.0)
        >>> clock.getTime()  # close to -1.0
        """

def sleepers(t: float) -> None:
    """Sleep for ``t`` seconds with high accuracy.

    Uses a hybrid strategy for precise timing: sleeps for half the remaining duration
    while more than 200 microseconds remain, then spin-waits for the final stretch.
    Substantially more accurate than :func:`time.sleep`.

    If ``t`` is zero or negative, returns immediately.

    Parameters
    ----------
    t : float
        The duration to sleep, in seconds.

    Examples
    --------
    >>> import psyquartz
    >>> psyquartz.sleepers(0.01)  # accurate 10 ms sleep
    """

def sleep(t: float) -> None:
    """Sleep for ``t`` seconds with high accuracy.

    Alias for :func:`sleepers`.

    If ``t`` is zero or negative, returns immediately.

    Parameters
    ----------
    t : float
        The duration to sleep, in seconds.

    Examples
    --------
    >>> import psyquartz
    >>> psyquartz.sleep(0.01)  # accurate 10 ms sleep
    """
