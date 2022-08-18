use crate::menu::Setting;
use eframe::egui;
//use egui::vec2; // text::LayoutJob,
// use egui::util::cache::FrameCache;

// theme: &CodeTheme, code: &str, language: &str
//fn memoized(_ctx: &egui::Context) -> LayoutJob {
/*
impl egui::util::cache::ComputerMut<(), LayoutJob> for () {
    fn compute(&mut self, _: ()) -> LayoutJob {
        self.highlight(theme, code, lang)
    }
}


type VoidCache = egui::util::cache::FrameCache<LayoutJob, ()>;

let mut memory = ctx.memory();
let highlight_cache = memory.caches.cache::<VoidCache>();
highlight_cache.get(())

//    LayoutJob::default()
//}


pub const LOREM_IPSUM_LONG: &str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris. Integer in mauris eu nibh euismod gravida. Duis ac tellus et risus vulputate vehicula. Donec lobortis risus a elit. Etiam tempor. Ut ullamcorper, ligula eu tempor congue, eros est euismod turpis, id tincidunt sapien risus a quam. Maecenas fermentum consequat mi. Donec fermentum. Pellentesque malesuada nulla a mi. Duis sapien sem, aliquet nec, commodo eget, consequat quis, neque. Aliquam faucibus, elit ut dictum aliquet, felis nisl adipiscing sapien, sed malesuada diam lacus eget erat. Cras mollis scelerisque nunc. Nullam arcu. Aliquam consequat. Curabitur augue lorem, dapibus quis, laoreet et, pretium ac, nisi. Aenean magna nisl, mollis quis, molestie eu, feugiat in, orci. In hac habitasse platea dictumst.";

fn lorem_ipsum(ui: &mut egui::Ui) {
    ui.with_layout(
        egui::Layout::top_down(egui::Align::LEFT).with_cross_justify(true),
        |ui| {
            ui.label(egui::RichText::new(LOREM_IPSUM_LONG).small().weak());
        },
    );
}

#[derive(Default)]
struct LanguageSelect {
    selected: String,
    alternatives: Vec<String>,
    is_active: bool,
}

impl LanguageSelect {
    fn show(&mut self, ctx: &egui::Context /*, kind: Source | Target*/) {
        egui::Window::new("Language Select") //format!("Select {} Language", kind)
            .default_width(320.0)
            // .resizable(true) Without effect
            .collapsible(false)
            .open(&mut self.is_active)
            .show(ctx, |ui| {
                ui.horizontal(|ui| {
                    ui.label("Slider orientation:");
                    ui.radio_value(&mut 0, 2, "Horizontal");
                    ui.radio_value(&mut 1, 3, "Vertical");
                });
            });
    }
}*/

use crate::menu::Menu;

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
        //egui::Window::new(self.about.name())

        let Self {
            text_source,
            text_target,
            menu,
        } = self;

        menu.ui(ctx);
        egui::CentralPanel::default().show(ctx, |ui| {
            // ui.add_space(10.0);

            ui.horizontal(|ui| {
                ui.add_space(25.0);

                // ui.label("Your name: ");
                //ui.text_edit_singleline(&mut self.name);

                // $ language_select.show(ctx);

                /*let mut layouter = |ui: &egui::Ui, _string: &str, wrap_width: f32| {
                    let mut layout_job: LayoutJob = memoized(ui.ctx());
                    layout_job.wrap.max_width = wrap_width; //420.0; // wrap_width
                    ui.fonts().layout_job(layout_job)
                };*/

                egui::ScrollArea::vertical()
                    .min_scrolled_height(200.0)
                    .show(ui, |ui| {
                        egui::TextEdit::multiline(text_source)
                            .font(egui::TextStyle::Monospace) // for cursor height
                            .hint_text("Sorce text")
                            .desired_rows(20)
                            .lock_focus(true)
                            .desired_width(350.0)
                            //.layouter(&mut layouter)
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
                                .font(egui::TextStyle::Monospace) // for cursor height
                                .hint_text("Target text")
                                //.code_editor()
                                .desired_rows(20)
                                .lock_focus(false)
                                .desired_width(350.0) //.layouter(&mut layouter),
                                .show(ui)
                        });
                });
            });
        });
    }
}
