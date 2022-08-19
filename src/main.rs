#![feature(let_else)]
// hide console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
mod app;
mod engines;
mod icons;
mod menu;

use app::App;

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
    let options = eframe::NativeOptions {
        // decorated: false,
        icon_data: load_icon(std::path::Path::new("./icons/simplet.png")),
        ..eframe::NativeOptions::default()
    };
    eframe::run_native("SimpleT", options, Box::new(|_cc| Box::new(App::default())));
}

// cargo build --release --bin simplet-gui
