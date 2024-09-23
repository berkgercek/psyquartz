use pyo3::{exceptions::PyRuntimeError, prelude::*};
use std::thread;
use std::time::{Duration, SystemTime};

#[pyclass(subclass)]
pub struct MonotonicClock {
    pub _timeAtLastReset: f64,
    pub _epochTimeAtLastReset: f64,
}

const CLOCK_PROBLEMS: &str = "Uh oh. The system clock took a shit.";

#[pymethods]
impl MonotonicClock {
    #[new]
    pub fn new() -> PyResult<MonotonicClock> {
        let t0 = SystemTime::now().duration_since(SystemTime::UNIX_EPOCH);
        match t0 {
            Ok(t) => Ok(MonotonicClock {
                _timeAtLastReset: t.as_secs_f64(),
                _epochTimeAtLastReset: t.as_secs_f64(),
            }),
            Err(_) => Err(PyRuntimeError::new_err(CLOCK_PROBLEMS)),
        }
    }

    #[pyo3(signature = (applyZero=true))]
    pub fn getTime(&self, applyZero: bool) -> PyResult<f64> {
        let t = SystemTime::now().duration_since(SystemTime::UNIX_EPOCH);
        match t {
            Ok(t) => {
                if applyZero {
                    let t = t.as_secs_f64();
                    return Ok(t - &self._timeAtLastReset);
                } else {
                    return Ok(t.as_secs_f64());
                }
            }
            Err(_) => return Err(PyRuntimeError::new_err(CLOCK_PROBLEMS)),
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
        self_.as_super()._timeAtLastReset = 0.0 + newT;
        let t = SystemTime::now().duration_since(SystemTime::UNIX_EPOCH);
        match t {
            Ok(t) => {
                self_.as_super()._epochTimeAtLastReset = t.as_secs_f64();
                Ok(self_.as_super()._timeAtLastReset = t.as_secs_f64())
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
    let start = SystemTime::now();
    let microsleep_dur = Duration::from_micros(1);
    let sleep_dur = Duration::from_secs_f64(t);
    if (microsleep_dur * 200) < sleep_dur {
        thread::sleep(sleep_dur - microsleep_dur * 200)
    }
    loop {
        thread::sleep(microsleep_dur);
        match SystemTime::now().duration_since(start) {
            Ok(t) => {
                if t >= sleep_dur {
                    return Ok(());
                }
            }
            Err(_) => return Err(PyRuntimeError::new_err(CLOCK_PROBLEMS)),
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn psyquartz(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sleepers, m)?);
    m.add_class::<MonotonicClock>()?;
    m.add_class::<Clock>()?;
    Ok(())
}
