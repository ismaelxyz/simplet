# SimpleT Gui

A graphical user interface for the [SimpleT](https://github.com/ismaelxyz/simplet/) application, its main dependency [eframe ](https://github.com/emilk/egui) (egui actually) allows to use both the web and desktop environment while still using Rust.

## Build Native
```sh
cargo build --release --bin simplet-gui
```

## Build Web

```sh
# cargo install wasm-pack # for install crate wasm-pack and work with WASM
cargo build --release --lib --target wasm32-unknown-unknown
wasm-bindgen ./target/wasm32-unknown-unknown/release/simplet_gui.wasm --out-dir public/wasm --target web --no-typescript
```

