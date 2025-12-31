use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use reqwest::blocking;
use serde::Deserialize;

#[pyfunction]
fn get_core_version() -> PyResult<String> {
    Ok("core version: v0.1.0".to_string())
}
#[derive(Deserialize)]
struct GitHubRelease {
    tag_name: String,
}

#[pyfunction]
pub fn pipe_version() -> PyResult<String> {
    let url = "https://api.github.com/repos/xololab/xolo-pipeline/releases/latest";

    let client = blocking::Client::builder()
        .user_agent("xolo-pipeline-app") // GitHub requiere un User-Agent
        .build()
        .map_err(|e| PyRuntimeError::new_err(format!("Error al crear cliente: {}", e)))?;

    // Hacemos la petición y la convertimos directamente a nuestra estructura
    let release: GitHubRelease = client
        .get(url)
        .send()
        .map_err(|e| PyRuntimeError::new_err(format!("Error de red: {}", e)))?
        .json() // Esto parsea el JSON automáticamente
        .map_err(|e| PyRuntimeError::new_err(format!("Error al parsear JSON: {}", e)))?;

    Ok(format!("pipe version: {}", release.tag_name))
}

/// module python writen in  Rust
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_core_version, m)?)?;
    m.add_function(wrap_pyfunction!(pipe_version, m)?)?;
    Ok(())
}
