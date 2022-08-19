use crate::engines::start as engines_start;
use eframe::egui;
use egui::{ImageButton, TextureHandle};
use std::{collections::HashMap, env::var as env_var, path::PathBuf};

fn load_texture_from_path(path: &str, ctx: &egui::Context) -> TextureHandle {
    let image = image::io::Reader::open(path).unwrap().decode().unwrap();
    let size = [image.width() as _, image.height() as _];
    let image_buffer = image.to_rgba8();
    let pixels = image_buffer.as_flat_samples();
    let image = egui::ColorImage::from_rgba_unmultiplied(size, pixels.as_slice());

    ctx.load_texture(path, image)
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
        Images {
            deactive: load_texture_from_path("./icons/menu.png", ctx),
            hide: load_texture_from_path("./icons/hide_menu.png", ctx),
            change_language: load_texture_from_path("./icons/change_language.png", ctx),
            change_translator: load_texture_from_path("./icons/change_translator.png", ctx),
            about_simplet: load_texture_from_path("./icons/about_simplet.png", ctx),
        }
    }
}

fn image_button(is_select: bool, ui: &mut egui::Ui, image: &TextureHandle) -> egui::Response {
    ui.add_space(10.0);
    ui.add_enabled(!is_select, ImageButton::new(image, [20.0, 20.0]))
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

#[derive(Default)]
pub(crate) struct Menu {
    images: Option<Images>,
    active: Option<Setting>,
}

impl Menu {
    pub fn ui(&mut self, ctx: &egui::Context) {
        let images = if let Some(images) = self.images.as_mut() {
            images
        } else {
            self.images.replace(Images::new(ctx));
            self.images.as_mut().unwrap()
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
                    if image_button(false, ui, &images.hide).clicked() {
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
            });

            active.map(|_| setting)
        } else {
            let mut active = None;
            egui::TopBottomPanel::top("top_panel").show(ctx, |ui| {
                ui.add_space(5.0);
                if ui
                    .add(ImageButton::new(&images.deactive, [20.0, 20.0]))
                    .clicked()
                {
                    active = Some(Setting::load().unwrap_or_default());
                }

                ui.add_space(5.0);
            });

            active
        };
    }
}
