use wasm_bindgen::prelude::JsValue;
mod app;
use app::App;

/// Start point
#[wasm_bindgen(start)]
pub fn start() -> Result<(), JsValue> {

    Ok(())
}

/// Display the graphics
#[wasm_bindgen]
pub fn display(canvas_id: &str) -> Result<(), JsValue> {
    eframe::start_web(canvas_id, Box::new(|_cc| Box::new(App::default())))
}
