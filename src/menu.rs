use crate::{
    app::{image_button, BUTTON_SIZE},
    engines::start as engines_start,
    icons::menu::Images,
};
use eframe::egui::{self, pos2, Id, ImageButton, Rect, Response, Sense, Ui, Vec2};
use std::{collections::HashMap, env::var as env_var, path::PathBuf};

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
    pub(crate) dark_theme: bool,
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

fn switch(ui: &mut egui::Ui, on: &mut bool) -> egui::Response {
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
        let center = egui::pos2(circle_x, rect.center().y);
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

    pub fn update(
        &mut self,
        text: (&mut String, &mut String),
        ctx: &egui::Context,
        frame: &mut eframe::Frame,
    ) {
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
            dark_theme,
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
                            if (index + 1) % 5 == 0 {
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
                .resizable(false)
                .show(ctx, |ui| {
                    ui.vertical_centered(|ui| {
                        ui.label(format!("SimpleT - v{}", env!("CARGO_PKG_VERSION")));

                        ui.add_space(15.0);
                        ui.hyperlink_to("Author", "https://t.me/asraelxyz");
                    });

                    ui.horizontal(|ui| {
                        ui.hyperlink_to("View Source", "https://github.com/ismaelxyz/simplet");

                        ui.with_layout(egui::Layout::top_down(egui::Align::RIGHT), |ui| {
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
                language,
                translator,
                about,
            };

            let mut active = Some(());
            egui::TopBottomPanel::top("top-panel").show(ctx, |ui| {
                ui.add_space(5.0);

                ui.horizontal(|ui| {
                    if ui
                        .add(ImageButton::new(&images.hide, BUTTON_SIZE))
                        .clicked()
                    {
                        setting.save();
                        active = None;
                    }

                    ui.spacing_mut().item_spacing.x = 10.0;

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

                    if ui
                        .add(ImageButton::new(&images.swap, BUTTON_SIZE))
                        .clicked()
                    {
                        std::mem::swap(text.0, text.1);
                    }

                    ui.label("Dark Theme: ");
                    let old = setting.dark_theme;
                    switch(ui, &mut setting.dark_theme);

                    if old != setting.dark_theme {
                        if setting.dark_theme {
                            ctx.set_visuals(egui::Visuals::dark());
                        } else {
                            ctx.set_visuals(egui::Visuals::light());
                        }
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
