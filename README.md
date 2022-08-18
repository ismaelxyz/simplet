# SimpleT Gui

Una interfaz gráfica de usuario para la aplicación [SimpleT](https://github.com/ismaelxyz/simplet/),
su dependencia principal [eframe ](https://github.com/emilk/egui) (egui realmente) permite usar el entorno web y el de escritorio sin dejar de utilizar Rust.

## Build Native
```sh
cargo build --release --bin simplet-gui
```

## Build Web

```sh
# cargo install wasm-pack # for install crate wasm-pack and work with WASM
wasm-pack build . -t web --release
```

