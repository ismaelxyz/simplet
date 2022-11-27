#[cfg(target_arch = "wasm32")]
use wasm_bindgen::prelude::*;

mod app;
mod engines;
mod icons;
mod menu;

#[cfg(target_arch = "wasm32")]
use app::App;

/// Start point
#[cfg(target_arch = "wasm32")]
#[wasm_bindgen(start)]
pub fn start() -> Result<(), JsValue> {
    Ok(())
}

/// Display the graphics
#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
pub fn display(canvas_id: &str) -> Result<(), JsValue> {
    eframe::start_web(
        canvas_id,
        eframe::WebOptions::default(),
        Box::new(|_cc| Box::new(App::default())),
    )
    .unwrap();
    Ok(())
}
