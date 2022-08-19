use crate::engines::start as engines_start;
use eframe::egui;
use egui::{pos2, Id, ImageButton, Rect, Response, Sense, TextureHandle, Ui, Vec2};
use std::io::Cursor;
use std::{collections::HashMap, env::var as env_var, path::PathBuf};

const BUTTON_SIZE: [f32; 2] = [20.0, 20.0];
mod icons {
    pub const DEACTIVE: &[u8] = include_bytes!("../icons/menu.png");
    pub const HIDE: &[u8] = include_bytes!("../icons/hide_menu.png");
    pub const CHANGE_LANGUAGE: &[u8] = include_bytes!("../icons/change_language.png");
    pub const CHANGE_TRANSLATOR: &[u8] = include_bytes!("../icons/change_translator.png");
    pub const ABOUT: &[u8] = include_bytes!("../icons/about_simplet.png");
}

fn texture_from_bytes(name: &str, bytes: &[u8], ctx: &egui::Context) -> TextureHandle {
    let image = image::io::Reader::new(Cursor::new(bytes))
        .with_guessed_format()
        .unwrap()
        .decode()
        .unwrap();

    let size = [image.width() as _, image.height() as _];
    let image_buffer = image.to_rgba8();
    let pixels = image_buffer.as_flat_samples();
    let image = egui::ColorImage::from_rgba_unmultiplied(size, pixels.as_slice());

    ctx.load_texture(name, image)
}

struct Images {
    deactive: TextureHandle,
    hide: TextureHandle,
    change_language: TextureHandle,
    change_translator: TextureHandle,
    about_simplet: TextureHandle,
}

impl Images {
    fn new(ctx: &egui::Context) -> Self {
        use icons::*;

        Images {
            deactive: texture_from_bytes("icon-deactive", DEACTIVE, ctx),
            hide: texture_from_bytes("icon-hide", HIDE, ctx),
            change_language: texture_from_bytes("icon-change-language", CHANGE_LANGUAGE, ctx),
            change_translator: texture_from_bytes("icon-change-translator", CHANGE_TRANSLATOR, ctx),
            about_simplet: texture_from_bytes("icon-about", ABOUT, ctx),
        }
    }
}

fn image_button(is_select: bool, ui: &mut egui::Ui, image: &TextureHandle) -> egui::Response {
    ui.add_space(10.0);
    ui.add_enabled(!is_select, ImageButton::new(image, BUTTON_SIZE))
}

#[derive(Eq, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
struct Language {
    source_select: bool,
    source: String,
    target: String,
    open: bool,
    #[serde(skip)]
    alternatives: HashMap<String, String>,
}

impl Language {
    fn alternatives(engine: &str) -> HashMap<String, String> {
        engines_start()[engine].clone()
    }
}

impl Default for Language {
    fn default() -> Self {
        Language {
            source_select: true,
            source: "Spanish".to_string(),
            target: "English".to_string(),
            open: false,
            alternatives: Self::alternatives("Google"),
        }
    }
}

#[derive(Eq, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
struct Translator {
    current: String,
    open: bool,
    #[serde(skip)]
    alternatives: Vec<String>,
}

impl Translator {
    fn alternatives() -> Vec<String> {
        engines_start().into_keys().collect()
    }
}

impl Default for Translator {
    fn default() -> Self {
        Translator {
            current: "Google".to_string(),
            open: false,
            alternatives: Translator::alternatives(),
        }
    }
}

#[derive(Default, Eq, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
struct AboutSimplet {
    open: bool,
}

#[derive(Default, Eq, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
pub(crate) struct Setting {
    pub(crate) text_source: String,
    pub(crate) text_target: String,
    language: Language,
    translator: Translator,
    about: AboutSimplet,
}

impl Setting {
    fn file() -> PathBuf {
        PathBuf::from(env_var("HOME").or_else(|_| env_var("HOMEPATH")).unwrap())
            .join(".simplet")
            .join("setting.json")
    }

    pub fn load() -> Result<Self, String> {
        let source = std::fs::read_to_string(Setting::file()).map_err(|err| err.to_string())?;
        let mut this: Self = serde_json::from_str(&source).map_err(|err| err.to_string())?;

        this.translator.alternatives = Translator::alternatives();
        this.language.alternatives = Language::alternatives(&this.translator.current);

        Ok(this)
    }

    pub fn save(&self) {
        let string = serde_json::to_string(&self).unwrap();
        std::fs::write(Setting::file(), &string).unwrap();
    }
}

pub(crate) struct Menu {
    images: Option<Images>,
    pub(crate) active: Option<Setting>,
}

impl Default for Menu {
    fn default() -> Self {
        Menu {
            images: None,
            active: None,
        }
    }
}

impl Menu {
    fn close_button_ui(&self, ui: &mut Ui, rect: Rect) -> Response {
        let button_size = Vec2::splat(ui.spacing().icon_width);
        // calculated so that the icon is on the diagonal (if window padding
        // is symmetrical)
        let pad = (rect.height() - button_size.y) / 2.0;
        let button_rect = Rect::from_min_size(
            pos2(
                rect.right() - pad - button_size.x,
                rect.center().y - 0.5 * button_size.y,
            ),
            button_size,
        );

        close_button(ui, button_rect)
    }

    pub fn update(&mut self, ctx: &egui::Context, frame: &mut eframe::Frame) {
        let images = if let Some(images) = self.images.take() {
            images
        } else {
            // Pos2
            self.images.replace(Images::new(ctx));
            self.images.take().unwrap()
        };

        self.active = if let Some(Setting {
            text_source,
            text_target,
            mut language,
            mut translator,
            mut about,
        }) = self.active.take()
        {
            egui::Window::new("Change Language")
                .vscroll(true)
                .open(&mut language.open)
                .show(ctx, |ui| {
                    ui.horizontal(|ui| {
                        ui.radio_value(&mut language.source_select, true, "Source");
                        ui.radio_value(&mut language.source_select, false, "Target");
                    });

                    ui.add_space(10.0);

                    egui::Grid::new("button_grid1").show(ui, |ui| {
                        let mut current = &mut language.source;
                        if language.source_select {
                            current = &mut language.target;
                        }

                        for (index, alternative) in language.alternatives.keys().enumerate() {
                            ui.radio_value(current, alternative.to_string(), alternative);
                            if (index + 1) % 4 == 0 {
                                ui.end_row();
                            }
                        }
                    });
                });

            egui::Window::new("Change Engine")
                .open(&mut translator.open)
                .show(ctx, |ui| {
                    egui::Grid::new("button_grid0").show(ui, |ui| {
                        for (index, alternative) in translator.alternatives.iter().enumerate() {
                            if ui
                                .radio_value(
                                    &mut translator.current,
                                    alternative.to_string(),
                                    alternative,
                                )
                                .clicked()
                            {
                                language.alternatives = Language::alternatives(alternative);
                                let mut keys = language.alternatives.keys();
                                if !language.alternatives.contains_key(&language.source) {
                                    language.source = keys.next().cloned().unwrap();
                                }
                                if !language.alternatives.contains_key(&language.target) {
                                    language.target = keys.next().cloned().unwrap();
                                }
                            }
                            if (index + 1) % 4 == 0 {
                                ui.end_row();
                            }
                        }
                    });
                });

            egui::Window::new("About")
                .open(&mut about.open)
                .show(ctx, |ui| {
                    ui.vertical_centered(|ui| {
                        ui.label("SimpleT");

                        ui.add_space(5.0);
                        // BUG: horizontal_centered is not compatible with
                        // vertical_centered
                        ui.horizontal_wrapped(|ui| {
                            ui.add_space(80.0);

                            ui.hyperlink_to("View Source", "https://github.com/ismaelxyz/simplet");
                            ui.add_space(5.0);
                            ui.hyperlink_to("Author", "https://t.me/asraelxyz");
                            ui.add_space(5.0);
                            // TODO: Dude, it is the link?
                            ui.hyperlink_to("Donate", "https://algorithmssite.github.io");
                        });
                        ui.add_space(10.0);

                        ui.label("Copyright © 2022 Ismael Belisario, All Rights Reserved.");
                    });
                });

            let mut setting = Setting {
                text_source,
                text_target,
                language,
                translator,
                about,
            };

            let mut active = Some(());
            egui::TopBottomPanel::top("top-panel").show(ctx, |ui| {
                ui.add_space(5.0);

                ui.horizontal(|ui| {
                    if ui
                        .add(ImageButton::new(&images.hide, [20.0, 20.0]))
                        .clicked()
                    {
                        setting.save();
                        active = None;
                    }

                    if image_button(setting.language.open, ui, &images.change_language).clicked() {
                        setting.language.open = true;
                    }

                    if image_button(setting.translator.open, ui, &images.change_translator)
                        .clicked()
                    {
                        setting.translator.open = true;
                    }

                    if image_button(setting.about.open, ui, &images.about_simplet).clicked() {
                        setting.about.open = true;
                    }
                });

                ui.add_space(5.0);

                let Rect { mut min, mut max } = ctx.input().screen_rect();

                min.y = 20.0;
                min.x = max.x - 30.0;
                max.x -= 20.0;
                max.y = 30.0;

                if self.close_button_ui(ui, Rect { min, max }).clicked() {
                    frame.quit();
                }
            });

            active.map(|_| setting)
        } else {
            let mut active = None;
            egui::TopBottomPanel::top("top_panel").show(ctx, |ui| {
                ui.add_space(5.0);
                if ui
                    .add(ImageButton::new(&images.deactive, BUTTON_SIZE))
                    .clicked()
                {
                    active = Some(Setting::load().unwrap_or_default());
                }

                ui.add_space(5.0);
            });

            active
        };

        self.images = Some(images);
    }
}

/// Paints the "Close" button of the window and processes clicks on it.
///
/// The close button is just an `X` symbol painted by a current stroke
/// for foreground elements (such as a label text).
///
/// # Parameters
/// - `ui`:
/// - `rect`: The rectangular area to fit the button in
///
/// Returns the result of a click on a button if it was pressed
fn close_button(ui: &mut Ui, rect: Rect) -> Response {
    let close_id = Id::new(1).with("window-close-button");
    let response = ui.interact(rect, close_id, Sense::click());
    ui.expand_to_include_rect(response.rect);

    let visuals = ui.style().interact(&response);
    let rect = rect.shrink(2.0).expand(visuals.expansion);
    let stroke = visuals.fg_stroke;
    ui.painter() // paints \
        .line_segment([rect.left_top(), rect.right_bottom()], stroke);
    ui.painter() // paints /
        .line_segment([rect.right_top(), rect.left_bottom()], stroke);
    response
}
