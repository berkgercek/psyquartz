# psyquartz

A high-performance clock and sleep library for Python, written in Rust with
[PyO3](https://pyo3.rs) bindings. Drop-in replacement for
[PsychoPy](https://www.psychopy.org/) core clocks with ~20x speedup on
`clock.getTime()` (~70 ns vs ~1.5 μs).

Also provides a high-accuracy sleep function that substantially outperforms
Python's `time.sleep`.

## Installation

```bash
pip install psyquartz
```

## Usage

### Clocks

`MonotonicClock` records the current time at creation. Calling `getTime()`
returns the elapsed seconds since then.

```python
import psyquartz

clock = psyquartz.MonotonicClock()
elapsed = clock.getTime()       # seconds since creation
raw = clock.getTime(applyZero=False)  # raw UNIX epoch time
```

`Clock` extends `MonotonicClock` with the ability to reset and shift the
baseline.

```python
clock = psyquartz.Clock()
print(clock.getTime())  # seconds since creation

clock.reset()           # restart from 0
print(clock.getTime())  # close to 0

clock.addTime(1.0)      # shift baseline forward by 1 s
print(clock.getTime())  # close to -1.0
```

### High-accuracy sleep

`sleep` (and its alias `sleepers`) uses a hybrid strategy — sleeping for half
the remaining duration while more than 200 μs remain, then spin-waiting for the
final stretch.

```python
import psyquartz

psyquartz.sleep(0.01)  # accurate 10 ms sleep
```
