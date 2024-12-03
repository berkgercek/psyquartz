A very simple clock to replace the Psychopy core clock, written in Rust with Python bindings. Yields ~20x speedup for basic operations like `clock.getTime()`, going from ~1.5 microseconds to ~70 nanoseconds. Not very useful unless you're doing very frequent polling of the clock, but I made this primarily for debugging a badly-drifting system clock.

Also provides a high-accuracy sleep function, `psyquartz.sleepers`, which offers better precision than the default python implementation `time.sleep`.
