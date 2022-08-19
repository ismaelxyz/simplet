use eframe::egui::{ColorImage, Context, TextureHandle};
use std::io::Cursor;
// macro_rules!  Rigth now!

pub(crate) mod menu {
    use super::texture_from_bytes;
    use eframe::egui::{Context, TextureHandle};

    const DEACTIVE: &[u8] = include_bytes!("../icons/menu.png");
    const HIDE: &[u8] = include_bytes!("../icons/hide_menu.png");
    const CHANGE_LANGUAGE: &[u8] = include_bytes!("../icons/change_language.png");
    const CHANGE_TRANSLATOR: &[u8] = include_bytes!("../icons/change_translator.png");
    const ABOUT: &[u8] = include_bytes!("../icons/about_simplet.png");

    pub(crate) struct Images {
        pub(crate) deactive: TextureHandle,
        pub(crate) hide: TextureHandle,
        pub(crate) change_language: TextureHandle,
        pub(crate) change_translator: TextureHandle,
        pub(crate) about_simplet: TextureHandle,
    }

    impl Images {
        pub(crate) fn new(ctx: &Context) -> Self {
            Images {
                deactive: texture_from_bytes("icon-deactive", DEACTIVE, ctx),
                hide: texture_from_bytes("icon-hide", HIDE, ctx),
                change_language: texture_from_bytes("icon-change-language", CHANGE_LANGUAGE, ctx),
                change_translator: texture_from_bytes(
                    "icon-change-translator",
                    CHANGE_TRANSLATOR,
                    ctx,
                ),
                about_simplet: texture_from_bytes("icon-about", ABOUT, ctx),
            }
        }
    }
}

pub(crate) mod app {
    use super::texture_from_bytes;
    use eframe::egui::{Context, TextureHandle};

    const DOCUMENT_SAVE: &[u8] = include_bytes!("../icons/document-save.png");
    const PLAY: &[u8] = include_bytes!("../icons/play.png");

    pub(crate) struct Images {
        pub(crate) document_save: TextureHandle,
        pub(crate) play: TextureHandle,
    }

    impl Images {
        pub(crate) fn new(ctx: &Context) -> Self {
            use crate::icons::app::*;

            Images {
                document_save: texture_from_bytes("document-save", DOCUMENT_SAVE, ctx),
                play: texture_from_bytes("play", PLAY, ctx),
            }
        }
    }
}

pub fn texture_from_bytes(name: &str, bytes: &[u8], ctx: &Context) -> TextureHandle {
    let image = image::io::Reader::new(Cursor::new(bytes))
        .with_guessed_format()
        .unwrap()
        .decode()
        .unwrap();

    let size = [image.width() as _, image.height() as _];
    let image_buffer = image.to_rgba8();
    let pixels = image_buffer.as_flat_samples();
    let image = ColorImage::from_rgba_unmultiplied(size, pixels.as_slice());

    ctx.load_texture(name, image)
}
