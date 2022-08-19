use crate::menu::{Menu, Setting};
use eframe::egui;

pub struct App {
    text_source: String,
    text_target: String,
    menu: Menu,
}

impl Default for App {
    fn default() -> Self {
        let Setting {
            text_source,
            text_target,
            ..
        } = Setting::load().unwrap_or_default();

        Self {
            text_source,
            text_target,
            menu: Menu::default(),
        }
    }
}

impl eframe::App for App {
    fn on_exit(&mut self, _gl: &eframe::glow::Context) {
        let mut setting = Setting::load().unwrap_or_default();
        setting.text_source = self.text_source.to_owned();
        setting.text_target = self.text_target.to_owned();
        setting.save();
    }

    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        let Self {
            text_source,
            text_target,
            menu,
        } = self;

        menu.ui(ctx);
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.add_space(25.0);

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

                ui.add_space(10.0);

                if ui.button("Swap").clicked() {
                    std::mem::swap(text_source, text_target);
                }

                ui.add_space(10.0);

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
            });
        });
    }
}
