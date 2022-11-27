use eframe::egui::{self, Context, ImageButton, Response, TextureHandle};

const BUTTON_SIZE: [f32; 2] = [20.0, 20.0];

fn texture_from_bytes(name: &str, bytes: &[u8], ctx: &Context) -> TextureHandle {
    let image = image::io::Reader::new(std::io::Cursor::new(bytes))
        .with_guessed_format()
        .unwrap()
        .decode()
        .unwrap();

    let size = [image.width() as _, image.height() as _];
    let image_buffer = image.to_rgba8();
    let pixels = image_buffer.as_flat_samples();
    let image = egui::ColorImage::from_rgba_unmultiplied(size, pixels.as_slice());

    ctx.load_texture(name, image, egui::TextureFilter::Linear)
}

pub struct Images {
    icons: std::collections::HashMap<String, TextureHandle>,
}

impl Images {
    #[inline(always)]
    fn new(icons: Vec<(&str, &[u8])>, ctx: &Context) -> Self {
        Images {
            icons: icons
                .into_iter()
                .map(|(name, data)| (name.to_string(), texture_from_bytes(name, data, ctx)))
                .collect(),
        }
    }

    pub(crate) fn menu(ctx: &Context) -> Self {
        Self::new(
            vec![
                ("menu", include_bytes!("../icons/menu.png")),
                ("menu-hide", include_bytes!("../icons/hide-menu.png")),
                (
                    "change-language",
                    include_bytes!("../icons/change-language.png"),
                ),
                ("settings", include_bytes!("../icons/settings.png")),
                (
                    "about-simplet",
                    include_bytes!("../icons/about-simplet.png"),
                ),
                ("swap", include_bytes!("../icons/swap.png")),
                (
                    "window-minimize",
                    include_bytes!("../icons/window-minimize.png"),
                ),
                ("window-close", include_bytes!("../icons/window-close.png")),
            ],
            ctx,
        )
    }

    pub(crate) fn app(ctx: &Context) -> Self {
        let document = include_bytes!("../icons/document-save.png");
        let play = include_bytes!("../icons/play.png");
        Self::new(vec![("document-save", document), ("play", play)], ctx)
    }

    #[inline(always)]
    pub fn button(&self, name: &str) -> ImageButton {
        ImageButton::new(&self.icons[name], BUTTON_SIZE)
    }

    #[inline(always)]
    pub fn add_button(&self, ui: &mut egui::Ui, is_select: bool, name: &str) -> Response {
        ui.add_enabled(!is_select, self.button(name))
    }
}
