use crate::{
    icons::Images,
    menu::{Menu, Setting},
};
use eframe::egui::{self, InnerResponse, Ui};

#[allow(clippy::ptr_arg)] // it not is true
fn area(
    name: &str,
    images: &Images,
    text: &mut String,
    hint_text: &str,
    ui: &mut Ui,
) -> InnerResponse<()> {
    ui.vertical(|ui| {
        ui.horizontal(|ui| {
            ui.scope(|ui| {
                ui.spacing_mut().item_spacing.x = 10.0;
                ui.add(images.button("play"))
                    .on_hover_text("Text to Speech");
                if ui
                    .add(images.button("document-save"))
                    .on_hover_text("Save as…")
                    .clicked()
                {
                    let path = std::env::current_dir().unwrap();

                    let file_to_save = rfd::FileDialog::new()
                        .set_file_name(&(hint_text.replace(' ', "-").to_lowercase() + ".txt"))
                        .set_directory(path)
                        .save_file();

                    if let Some(absolute_path) = file_to_save {
                        std::fs::write(absolute_path, &*text).unwrap();
                    }
                }
            });
        });

        ui.add_space(10.0);

        ui.push_id(format!("{}-area", name), |ui| {
            egui::ScrollArea::vertical()
                .min_scrolled_height(300.0)
                .show(ui, |ui| {
                    egui::TextEdit::multiline(text)
                        .font(egui::TextStyle::Monospace)
                        .hint_text(hint_text) // "Sorce text"
                        .desired_rows(20)
                        //.lock_focus(true)
                        .desired_width(f32::INFINITY)
                        .show(ui)
                });
        });
    })
}

#[derive(Default)]
pub struct App {
    text_source: String,
    text_target: String,
    once: Option<(Menu, Images)>,
}

impl App {
    fn configure(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) -> (Menu, Images) {
        let setting = Setting::load().unwrap_or_default();
        self.text_source = setting.text_source;
        self.text_target = setting.text_target;
        #[cfg(all(feature = "debug", not(target_arch = "wasm32")))]
        _frame.set_decorations(setting.decoration);
        if setting.dark_theme {
            ctx.set_visuals(egui::Visuals::dark());
        } else {
            ctx.set_visuals(egui::Visuals::light());
        }

        (Menu::default(), Images::app(ctx))
    }
}

impl eframe::App for App {
    fn on_exit(&mut self, _gl: Option<&eframe::glow::Context>) {
        let mut setting = self
            .once
            .take()
            .unwrap()
            .0
            .active
            .take()
            .or_else(|| Setting::load().ok())
            .unwrap_or_default();

        setting.text_source = self.text_source.to_owned();
        setting.text_target = self.text_target.to_owned();
        setting.save();
    }

    fn update(&mut self, ctx: &egui::Context, frame: &mut eframe::Frame) {
        let (mut menu, images) = self
            .once
            .take()
            .unwrap_or_else(|| self.configure(ctx, frame));

        menu.update((&mut self.text_source, &mut self.text_target), ctx, frame);
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.scope(|ui| {
                ui.columns(2, |uis| {
                    uis[0].horizontal(|ui| {
                        area("source", &images, &mut self.text_source, "Sorce text", ui);
                        ui.add_space(10.0);
                    });

                    uis[1].horizontal(|ui| {
                        ui.add_space(10.0);
                        let dummy = &mut self.text_target.clone();
                        area("target", &images, dummy, "Target text", ui);
                    });
                });
            });
        });

        self.once.replace((menu, images));
    }
}
