# SimpleT - Translating without complications

## Introduction

This is a monumental improvement of my "Open Translation"* application, sometimes I don't want to open my browser to translate a small text, but at the same time I want different interpretations, listen to the pronunciation and have that data stored locally for later use. SimpleT is the solution to that.

* This repository used to be called "Open Translation".

## Requirements

* [Python 3.10](https://www.python.org/) or later, with the packages:
```bash
pip install -r requirements
```

* [Rust 1.62.0](https://www.rust-lang.org/) or later, for the graphics interface.
  Compile with:
  
```bash
cargo install wasm-pack
# "basic-http-server" maybe replace for:
# python3 -m http.server 8888 --bind 127.0.0.1
cargo install basic-http-server
  
wasm-pack build . -t web      # Web Version
cargo build --bin simplet-gui # Native version
```
