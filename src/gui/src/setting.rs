use crate::menu;
use std::{env::var as env_var, path::PathBuf};

#[derive(Default, Eq, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
pub(crate) struct Menu {
    pub(crate) language: menu::Language,
    pub(crate) translator: menu::Translator,
    pub(crate) about: menu::AboutSimplet,
}

#[derive(Default, Eq, PartialEq, Clone, serde::Deserialize, serde::Serialize)]
pub(crate) struct Setting {
    pub(crate) text_source: String,
    pub(crate) text_target: String,
    pub(crate) dark_theme: bool,
    #[cfg(all(feature = "debug", not(target_arch = "wasm32")))]
    pub(crate) decoration: bool,
    pub(crate) menu: Menu,
}

impl Setting {
    fn file() -> PathBuf {
        PathBuf::from(
            env_var("HOME")
                .or_else(|_| env_var("HOMEPATH"))
                .unwrap_or_default(),
        )
        .join(".simplet")
        .join("setting.json")
    }

    pub fn load() -> Result<Self, String> {
        // let source = std::fs::read_to_string(Setting::file()).map_err(|err| err.to_string())?;
        // let mut this: Self = serde_json::from_str(&source).map_err(|err| err.to_string())?;

        // this.translator.alternatives = Translator::alternatives();
        // this.language.alternatives = Language::alternatives(&this.translator.current);

        Ok(Self::default()) //
    }

    pub fn save(&self) {
        let data = serde_json::to_string(&self).unwrap();
        std::fs::write(Setting::file(), data).unwrap();
    }
}
