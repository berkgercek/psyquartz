#![allow(non_snake_case)]
// We're matching the Psychopy API so unfortunately we have stupid snake case names.
// Sorry clippy.
use pyo3::{exceptions::PyRuntimeError, prelude::*};
use std::thread;
use std::time::{Duration, Instant, SystemTime};

#[pyclass(subclass)]
pub struct MonotonicClock {
    t0: Instant,
    pub _timeAtLastReset: f64,
    pub _epochTimeAtLastReset: f64,
}

const CLOCK_PROBLEMS: &str = "Uh oh. The system clock took a shit.";

#[pymethods]
impl MonotonicClock {
    #[new]
    pub fn new() -> PyResult<MonotonicClock> {
        let t0 = Instant::now();
        let _epochTimeAtLastReset = SystemTime::now().duration_since(SystemTime::UNIX_EPOCH);
        if let Ok(t) = _epochTimeAtLastReset {
            Ok(MonotonicClock {
                t0,
                _timeAtLastReset: 0.0f64,
                _epochTimeAtLastReset: t.as_secs_f64(),
            })
        } else {
            Err(PyRuntimeError::new_err(CLOCK_PROBLEMS))
        }
    }

    #[pyo3(signature = (applyZero=true))]
    pub fn getTime(&self, applyZero: bool) -> PyResult<f64> {
        let t = self.t0.elapsed();
        if applyZero {
            let t = t.as_secs_f64();
            return Ok(t - &self._timeAtLastReset);
        } else {
            return Ok(t.as_secs_f64());
        }
    }

    pub fn getLastResetTime(&self) -> f64 {
        let lrt = &self._timeAtLastReset;
        lrt.clone()
    }
}

#[pyclass(extends=MonotonicClock, subclass)]
struct Clock;

#[pymethods]
impl Clock {
    #[new]
    pub fn new() -> PyResult<(Self, MonotonicClock)> {
        let mc = MonotonicClock::new();
        match mc {
            Ok(mc) => Ok((Clock {}, mc)),
            Err(_) => Err(PyRuntimeError::new_err(CLOCK_PROBLEMS)),
        }
    }
    #[pyo3(signature = (newT=0f64))]
    pub fn reset(mut self_: PyRefMut<'_, Self>, newT: f64) -> PyResult<()> {
        self_.as_super()._timeAtLastReset = self_.as_super().t0.elapsed().as_secs_f64() + newT;
        let t = SystemTime::now().duration_since(SystemTime::UNIX_EPOCH);
        match t {
            Ok(t) => {
                self_.as_super()._epochTimeAtLastReset = t.as_secs_f64();
                Ok(())
            }
            Err(_) => Err(PyRuntimeError::new_err(CLOCK_PROBLEMS)),
        }
    }

    pub fn addTime(mut self_: PyRefMut<'_, Self>, t: f64) {
        self_.as_super()._timeAtLastReset += t;
        self_.as_super()._epochTimeAtLastReset += t;
    }

    pub fn add(mut self_: PyRefMut<'_, Self>, t: f64) {
        self_.as_super()._timeAtLastReset += t;
        self_.as_super()._epochTimeAtLastReset += t;
    }
}

#[pyfunction]
pub fn sleepers(t: f64) -> PyResult<()> {
    if t <= 0.0 {
        return Ok(());
    }
    let start = Instant::now();
    let sleep_dur = Duration::from_secs_f64(t);
    let spin_threshold = Duration::from_micros(200);

    loop {
        let elapsed = start.elapsed();
        if elapsed >= sleep_dur {
            return Ok(());
        }
        let remaining = sleep_dur - elapsed;
        if remaining > spin_threshold {
            // Sleep for half the remaining time — safe, never overshoots target
            thread::sleep(remaining / 2);
        } else {
            // Pure spin-wait for the final <200μs
            std::hint::spin_loop();
        }
    }
}

#[pyfunction]
pub fn sleep(t: f64) -> PyResult<()> {
    sleepers(t)
}

/// A Python module implemented in Rust.
#[pymodule(gil_used = false)]
#[allow(unused)]
fn psyquartz(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sleepers, m)?);
    m.add_function(wrap_pyfunction!(sleep, m)?);
    m.add_class::<MonotonicClock>()?;
    m.add_class::<Clock>()?;
    Ok(())
}
