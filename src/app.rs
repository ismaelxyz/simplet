use crate::menu::{Menu, Setting};
use eframe::egui;

#[derive(Default)]
pub struct App {
    text_source: String,
    text_target: String,
    menu: Option<Menu>,
}

// impl  for App {
//     fn default() -> Self {
//         let Setting {
//             text_source,
//             text_target,
//             ..
//         } = Setting::load().unwrap_or_default();

//         Self {
//             text_source,
//             text_target,
//             angle: std::f32::consts::TAU / 3.0,
//             menu: Menu::default(),
//         }
//     }
// }

impl eframe::App for App {
    fn on_exit(&mut self, _gl: &eframe::glow::Context) {
        let mut setting = self
            .menu
            .take()
            .unwrap()
            .active
            .take()
            .or_else(|| Setting::load().ok())
            .unwrap_or_default();

        setting.text_source = self.text_source.to_owned();
        setting.text_target = self.text_target.to_owned();
        setting.save();
    }

    fn update(&mut self, ctx: &egui::Context, frame: &mut eframe::Frame) {
        let Self {
            text_source,
            text_target,
            menu,
        } = self;

        let mut var_menu = if let Some(menu) = menu.take() {
            menu
        } else {
            let setting = Setting::load().unwrap_or_default();
            *text_source = setting.text_source;
            *text_target = setting.text_target;
            if setting.dark_theme {
                ctx.set_visuals(egui::Visuals::dark());
            } else {
                ctx.set_visuals(egui::Visuals::light());
            }

            Menu::default()
        };

        var_menu.update(ctx, frame);
        egui::CentralPanel::default().show(ctx, |ui| {
            // egui::Align::Center

            ui.horizontal(|ui| {
                ui.add_space(20.0);
                ui.spacing_mut().item_spacing.x = 20.0;
                egui::ScrollArea::vertical()
                    .min_scrolled_height(200.0)
                    .show(ui, |ui| {
                        egui::TextEdit::multiline(text_source)
                            .font(egui::TextStyle::Monospace)
                            .hint_text("Sorce text")
                            .desired_rows(20)
                            .lock_focus(true)
                            .desired_width(350.0)
                            .show(ui)
                    });

                if ui.button("Swap").clicked() {
                    std::mem::swap(text_source, text_target);
                }

                ui.push_id("target-area", |ui| {
                    egui::ScrollArea::vertical()
                        .min_scrolled_height(200.0)
                        .show(ui, |ui| {
                            egui::TextEdit::multiline(text_target)
                                .font(egui::TextStyle::Monospace)
                                .hint_text("Target text")
                                .desired_rows(20)
                                .lock_focus(false)
                                .desired_width(350.0)
                                .show(ui)
                        });
                });

                ui.add_space(20.0);
            });
        });

        menu.replace(var_menu);
    }
}
