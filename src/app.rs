use crate::{
    icons::app::Images,
    menu::{Menu, Setting},
};
use eframe::egui::{self, InnerResponse, Response, Ui};
pub const BUTTON_SIZE: [f32; 2] = [20.0, 20.0];

pub fn image_button(is_select: bool, ui: &mut Ui, image: &egui::TextureHandle) -> Response {
    //ui.add_space(10.0);
    ui.add_enabled(!is_select, egui::ImageButton::new(image, BUTTON_SIZE))
}

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
                image_button(false, ui, &images.play).on_hover_text("Text to Speech");
                image_button(false, ui, &images.document_save).on_hover_text("Save as…");
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

impl eframe::App for App {
    fn on_exit(&mut self, _gl: &eframe::glow::Context) {
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
        let Self {
            text_source,
            text_target,
            once,
        } = self;

        let (mut menu, images) = if let Some((menu, images)) = once.take() {
            (menu, images)
        } else {
            let setting = Setting::load().unwrap_or_default();
            *text_source = setting.text_source;
            *text_target = setting.text_target;
            if setting.dark_theme {
                ctx.set_visuals(egui::Visuals::dark());
            } else {
                ctx.set_visuals(egui::Visuals::light());
            }

            (Menu::default(), Images::new(ctx))
        };

        menu.update((text_source, text_target), ctx, frame);
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.scope(|ui| {
                ui.columns(2, |uis| {
                    uis[0].horizontal(|ui| {
                        area("source", &images, text_source, "Sorce text", ui);
                        ui.add_space(10.0);
                    });

                    uis[1].horizontal(|ui| {
                        ui.add_space(10.0);
                        let mut dummy = text_target.clone();
                        area("target", &images, &mut dummy, "Target text", ui);
                    });
                });
            });
        });

        once.replace((menu, images));
    }
}
