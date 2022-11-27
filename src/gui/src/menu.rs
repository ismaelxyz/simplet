use crate::{
    engines::start as engines_start,
    icons::Images,
    setting::{self, Setting},
};
use deeptrans as dt;
use eframe::egui::{self, pos2, Align, Id, Layout, Ui};
use std::collections::HashMap;

#[derive(Eq, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
pub(crate) struct Language {
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
pub(crate) struct Translator {
    current: usize,
    open: bool,
    // #[serde(skip)]
    alternatives: Vec<dt::Translator>,
}

impl Translator {
    fn current(&self) -> &dt::Translator {
        &self.alternatives[self.current]
    }

    fn current_engine(&self) -> &dt::Engine {
        &self.current().engine
    }
}

impl Default for Translator {
    fn default() -> Self {
        use dt::{Engine::*, Translator as DtTrans, Version};

        Translator {
            current: 0,
            open: false,
            alternatives: vec![
                DtTrans::new("es", "en"),
                DtTrans::with_engine(
                    "de",
                    "en",
                    Deepl {
                        api_key: String::new(),
                        version: Version::V2,
                        use_free_api: true,
                    },
                ),
                DtTrans::with_engine(
                    "en",
                    "es",
                    Libre {
                        api_key: String::new(),
                        url: "https://libretranslate.de/".into(),
                    },
                ),
                DtTrans::with_engine("en", "de", Linguee { return_all: false }),
                DtTrans::with_engine(
                    "es",
                    "de",
                    Microsoft {
                        api_key: String::new(),
                        region: String::new(),
                    },
                ),
                DtTrans::with_engine(
                    "it",
                    "es",
                    MyMemory {
                        email: String::new(),
                        return_all: false,
                    },
                ),
                DtTrans::with_engine(
                    "fr",
                    "en",
                    Papago {
                        client_id: String::new(),
                        secret_key: String::new(),
                    },
                ),
                DtTrans::with_engine("ar", "bg", Pons { return_all: false }),
                DtTrans::with_engine(
                    "es",
                    "en",
                    Qcri(dt::Qcri {
                        api_key: String::new(),
                        domain: String::new(),
                    }),
                ),
                DtTrans::with_engine(
                    "en",
                    "de",
                    Yandex {
                        api_key: String::new(),
                    },
                ),
            ],
        }
    }
}

#[derive(Default, Eq, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
pub(crate) struct AboutSimplet {
    open: bool,
}

fn switch(ui: &mut Ui, on: &mut bool) -> egui::Response {
    let desired_size = ui.spacing().interact_size.y * egui::vec2(2.0, 1.0);
    let (rect, mut response) = ui.allocate_exact_size(desired_size, egui::Sense::click());
    if response.clicked() {
        *on = !*on;
        response.mark_changed();
    }
    response.widget_info(|| egui::WidgetInfo::selected(egui::WidgetType::Checkbox, *on, ""));

    if ui.is_rect_visible(rect) {
        let how_on = ui.ctx().animate_bool(response.id, *on);
        let visuals = ui.style().interact_selectable(&response, *on);
        let rect = rect.expand(visuals.expansion);
        let radius = 0.5 * rect.height();
        ui.painter()
            .rect(rect, radius, visuals.bg_fill, visuals.bg_stroke);
        let circle_x = egui::lerp((rect.left() + radius)..=(rect.right() - radius), how_on);
        let center = pos2(circle_x, rect.center().y);
        ui.painter()
            .circle(center, 0.75 * radius, visuals.bg_fill, visuals.fg_stroke);
    }

    response
}

#[derive(Default)]
pub(crate) struct Menu {
    images: Option<Images>,
    pub(crate) active: Option<Setting>,
}

impl Menu {
    pub fn update(
        &mut self,
        text: (&mut String, &mut String),
        ctx: &egui::Context,
        _frame: &mut eframe::Frame,
    ) {
        let _response;
        let images = self.images.take().unwrap_or_else(|| Images::menu(ctx));
        let mut buttons = Vec::new();

        self.active = if let Some(Setting {
            text_source,
            text_target,
            mut dark_theme,
            #[cfg(all(feature = "debug", not(target_arch = "wasm32")))]
            mut decoration,
            menu:
                setting::Menu {
                    mut language,
                    mut translator,
                    mut about,
                },
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
                            if (index + 1) % 5 == 0 {
                                ui.end_row();
                            }
                        }
                    });
                });

            let mut is_open = translator.open;

            egui::Window::new("Setting")
                .open(&mut is_open)
                .show(ctx, |ui| {
                    egui::collapsing_header::CollapsingState::load_with_default_open(
                        ui.ctx(),
                        Id::new("collapsing"),
                        true,
                    )
                    .show_header(ui, |ui| {
                        // ...
                        ui.label(format!(
                            "Change Engine - {}",
                            translator.current_engine().name()
                        ));
                    })
                    .body(|ui| {
                        egui::Grid::new("button_grid0").show(ui, |ui| {
                            let current = translator.current;
                            for (index, alt) in (0..translator.alternatives.len())
                                .filter(|alt| current != *alt)
                                .enumerate()
                            {
                                let name = translator.alternatives[alt].name().to_owned();
                                if ui
                                    .radio_value(&mut translator.current, alt, &name)
                                    .clicked()
                                {
                                    language.alternatives = Language::alternatives(&name);
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

                    ui.add_space(20.);

                    ui.horizontal(|ui| {
                        ui.add_space(10.);
                        ui.spacing_mut().item_spacing.x = 10.0;

                        ui.label("Dark Theme: ");
                        if switch(ui, &mut dark_theme).clicked() {
                            if dark_theme {
                                ctx.set_visuals(egui::Visuals::dark());
                            } else {
                                ctx.set_visuals(egui::Visuals::light());
                            }
                        }

                        ui.add_space(10.);

                        #[cfg(all(feature = "debug", not(target_arch = "wasm32")))]
                        {
                            ui.label("Window Decoration: ");
                            if switch(ui, &mut decoration).clicked() {
                                frame.set_decorations(decoration);
                            }
                            ui.add_space(10.);
                        }
                    });
                });
            translator.open = is_open;
            egui::Window::new("About")
                .open(&mut about.open)
                .resizable(false)
                .show(ctx, |ui| {
                    ui.vertical_centered(|ui| {
                        ui.label(format!("SimpleT - v{}", env!("CARGO_PKG_VERSION")));

                        ui.add_space(15.0);
                        ui.hyperlink_to("Author", "https://t.me/asraelxyz");
                    });

                    ui.horizontal(|ui| {
                        ui.hyperlink_to("View Source", "https://github.com/ismaelxyz/simplet");

                        ui.with_layout(Layout::top_down(Align::RIGHT), |ui| {
                            // TODO: Dude, it is the link?
                            ui.hyperlink_to("Donate", "https://algorithmssite.github.io");
                        });
                    });
                    ui.add_space(40.0);

                    ui.vertical_centered(|ui| {
                        ui.label("Copyright © 2022 Ismael Belisario, All Rights Reserved.");
                    });
                });

            let mut setting = Setting {
                text_source,
                text_target,
                dark_theme,
                #[cfg(all(feature = "debug", not(target_arch = "wasm32")))]
                decoration,
                menu: setting::Menu {
                    language,
                    translator,
                    about,
                },
            };

            let mut active = Some(());

            _response = egui::TopBottomPanel::top("top-panel").show(ctx, |ui| {
                ui.add_space(5.0);

                ui.horizontal(|ui| {
                    buttons = vec![
                        ui.add(images.button("menu-hide")),
                        images.add_button(ui, setting.menu.language.open, "change-language"),
                        images.add_button(ui, setting.menu.translator.open, "settings"),
                        images.add_button(ui, setting.menu.about.open, "about-simplet"),
                        ui.add(images.button("swap")),
                    ];

                    if buttons[0].clicked() {
                        setting.save();
                        active = None;
                    }

                    ui.spacing_mut().item_spacing.x = 10.0;

                    if buttons[1].clicked() {
                        setting.menu.language.open = true;
                    }

                    if buttons[2].clicked() {
                        setting.menu.translator.open = true;
                    }

                    if buttons[3].clicked() {
                        setting.menu.about.open = true;
                    }

                    if buttons[4].clicked() {
                        std::mem::swap(text.0, text.1);
                    }

                    #[cfg(all(feature = "debug", not(target_arch = "wasm32")))]
                    {
                        let mut center_x =
                            (ui.available_width() - buttons[4].rect.max.x - 43.5) / 2.0;

                        if center_x < 0.0 {
                            center_x = 0.0;
                        }

                        ui.add_space(center_x);
                        ui.label("SimpleT");
                    }

                    #[cfg(all(feature = "debug", not(target_arch = "wasm32")))]
                    ui.with_layout(Layout::right_to_left(Align::LEFT), |ui| {
                        buttons.append(&mut vec![
                            ui.add(images.button("window-close")),
                            ui.add(images.button("window-minimize")),
                        ]);

                        if buttons[5].clicked() {
                            frame.close();
                        }

                        if buttons[6].clicked() {
                            //frame.set_visible(false);
                            //frame.output.window_pos = None;
                        }
                    });
                });

                ui.add_space(5.0);
            });

            active.map(|_| setting)
        } else {
            let mut active = None;
            _response = egui::TopBottomPanel::top("top_panel").show(ctx, |ui| {
                ui.add_space(5.0);
                buttons = vec![ui.add(images.button("menu"))];

                if buttons[0].clicked() {
                    active = Some(Setting::load().unwrap_or_default());
                }

                ui.add_space(5.0);
            });

            active
        };

        #[cfg(all(feature = "debug", not(target_arch = "wasm32")))]
        if !buttons.iter().any(|btn| btn.hovered()) && _response.response.hovered() {
            frame.drag_window();
        }

        self.images = Some(images);
    }
}
