// hide console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")] 
mod app;
use app::App;

fn main() {
    let options = eframe::NativeOptions::default();
    eframe::run_native("SimpleT", options, Box::new(|_cc| Box::new(App::default())));
}
