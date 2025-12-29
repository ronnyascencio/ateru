use pyo3::prelude::*;

#[pyfunction]
fn get_core_version() -> PyResult<String> {
    Ok("0.1.0-rust-core".to_string())
}

/// module python writen in  Rust
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_core_version, m)?)?;
    Ok(())
}