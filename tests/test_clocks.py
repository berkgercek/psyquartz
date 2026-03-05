from __future__ import annotations

import numpy as np
import pytest

from psyquartz import Clock, MonotonicClock, sleepers


@pytest.fixture
def monotonic_clock():
    return MonotonicClock()


@pytest.fixture
def clock():
    return Clock()


def test_monotonic_private_attributes(monotonic_clock: MonotonicClock):
    """Make sure the private attributes needed by PsychoPy are there."""
    assert hasattr(monotonic_clock, "_timeAtLastReset")
    assert hasattr(monotonic_clock, "_epochTimeAtLastReset")


def test_monotonic_increases(monotonic_clock: MonotonicClock):
    """Make sure the monotonic clock is monotonic, and the reset time is 0.0."""
    t_first = monotonic_clock.getTime()
    t_last = t_first
    while (t := monotonic_clock.getTime()) < t_first + 0.5:
        assert monotonic_clock.getLastResetTime() == 0.0
        assert t >= t_last
        t_last = t


def test_monotonic_epoch_time(monotonic_clock: MonotonicClock):
    """Make sure the epoch time at last reset does not change."""
    t_first = monotonic_clock.getTime()
    epoch_time_first = monotonic_clock._epochTimeAtLastReset
    while monotonic_clock.getTime() < t_first + 0.5:
        assert monotonic_clock._epochTimeAtLastReset == epoch_time_first


def test_clock_inheritance(clock: Clock):
    assert isinstance(clock, MonotonicClock)
    assert hasattr(clock, "reset")
    assert hasattr(clock, "getLastResetTime")
    assert hasattr(clock, "_timeAtLastReset")
    assert hasattr(clock, "_epochTimeAtLastReset")


def test_clock_reset(clock: Clock):
    """Make sure the reset method changes private attributes and behavior."""
    sleepers(0.1)
    t_first = clock.getTime()
    clock.reset()
    t_after_reset = clock.getTime()
    assert t_after_reset < t_first
    assert clock.getLastResetTime() != 0.0
    assert clock._timeAtLastReset != 0.0
    assert clock._epochTimeAtLastReset != 0.0


def test_clock_reset_newT(clock: Clock):
    """Make sure the reset method's newT argument works."""
    sleepers(0.1)
    t_first = clock.getTime()
    clock.reset(newT=100.0)
    t_after_reset = clock.getTime()
    assert t_after_reset < t_first
    assert np.isclose(t_after_reset, -100, atol=0.01)


def test_clock_addTime(clock: Clock):
    """Make sure addTime shifts the clock forward."""
    sleepers(0.1)
    t_first = clock.getTime()
    clock.addTime(0.5)
    t_after_add = clock.getTime()
    assert np.isclose(t_after_add, t_first + 0.5, atol=0.01, rtol=0.0)


def test_clock_add(clock: Clock):
    """Make sure add shifts the clock backward."""
    sleepers(0.1)
    t_first = clock.getTime()
    clock.add(0.5)
    t_after_add = clock.getTime()
    assert np.isclose(t_after_add, t_first - 0.5, atol=0.01, rtol=0.0)
