// hide console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
mod app;
mod engines;
mod icons;
mod menu;
use app::App;

//use pyo3::prelude::*;
//use pyo3::types::IntoPyDict;

fn load_icon(path: &std::path::Path) -> Option<eframe::IconData> {
    let image = image::open(path)
        .expect("Failed to open icon path")
        .into_rgba8();
    let (width, height) = image.dimensions();
    let rgba = image.into_raw();

    Some(eframe::IconData {
        rgba,
        width,
        height,
    })
}

fn main() {
    /*let _: PyResult<()> = Python::with_gil(|py| {
        let sys = py.import("sys")?;
        let version: String = sys.getattr("version")?.extract()?;

        let locals = [("os", py.import("os")?)].into_py_dict(py);
        let code = "os.getenv('USER') or os.getenv('USERNAME') or 'Unknown'";
        let user: String = py.eval(code, None, Some(&locals))?.extract()?;

        println!("Hello {}, I'm Python {}", user, version);
        Ok(())
    });*/
    let options = eframe::NativeOptions {
        // decorated: false,
        icon_data: load_icon(std::path::Path::new("./icons/simplet.png")),
        ..eframe::NativeOptions::default()
    };
    eframe::run_native("SimpleT", options, Box::new(|_cc| Box::new(App::default())));
}
