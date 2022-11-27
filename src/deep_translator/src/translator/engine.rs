use super::qcri::Qcri;
use std::{fmt, str::FromStr};

#[macro_export]
macro_rules! codes_to_languages {
    ( $($key:expr => $value:expr),* ) => {{
        let mut map = std::collections::HashMap::new();
        $( map.insert($key.to_string(), $value.to_string()); )*
        map
    }}
}

pub type LanguagesToCodes = std::collections::HashMap<String, String>;

#[derive(Debug, Default, Copy, Clone, Eq, PartialEq, Ord, PartialOrd)]
pub enum Version {
    V1,
    #[default]
    V2,
}

impl FromStr for Version {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "v1" => Ok(Version::V1),
            "v2" => Ok(Version::V2),
            _ => Err(()),
        }
    }
}

impl fmt::Display for Version {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Version::V1 => "v1",
            Version::V2 => "v2",
        }
        .fmt(f)
    }
}

/// Enum that wraps engines, which use the translator under the hood to translate word(s)
#[derive(Debug, Default, Clone, Eq, PartialEq)]
pub enum Engine {
    #[default]
    Google,
    /// Get one api key here: https://www.deepl.com/docs-api/accessing-the-api/
    Deepl {
        api_key: String,
        version: Version,
        use_free_api: bool,
    },
    Libre {
        api_key: String,
        url: String,
    },
    Linguee {
        return_all: bool,
    },
    Microsoft {
        api_key: String,
        region: String,
    },
    MyMemory {
        email: String,
        /// set to True to return all synonym/similars of the translated text
        return_all: bool,
    },
    Papago {
        client_id: String,
        secret_key: String,
    },
    Pons {
        return_all: bool,
    },
    Qcri(Qcri),
    Yandex {
        api_key: String,
        //api_version: String,
    },
}

impl Engine {
    #[inline(always)]
    pub fn base_url(&self) -> String {
        match &self {
            Self::Google => "https://translate.google.com/m".into(),
            Self::Deepl {
                use_free_api,
                version,
                ..
            } => {
                let free = if *use_free_api { "-free" } else { "" };
                format!("https://api{free}/{version}/translate")
            }
            Self::Libre { url, .. } => format!("{url}/translate"),
            Self::Linguee { .. } => "https://www.linguee.com/".into(),
            Self::Microsoft { .. } => {
                "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0".into()
            }
            Self::MyMemory { .. } => "http://api.mymemory.translated.net/get".into(),
            // "https://papago.naver.com/"
            Self::Papago { .. } => "https://openapi.naver.com/v1/papago/n2mt".into(),
            Self::Pons { .. } => "https://en.pons.com/translate/".into(),
            Self::Qcri(..) => Qcri::base_url("translate"),
            Self::Yandex { .. } => "https://translate.yandex.net/api/v1.5/tr.json/translate".into(),
        }
    }

    #[inline(always)]
    pub fn supported_languages(&self) -> LanguagesToCodes {
        match &self {
            Self::Google | Self::MyMemory { .. } | Self::Yandex { .. } => {
                crate::codes_to_languages! {
                    "Afrikaans" => "af",
                    "Albanian" => "sq",
                    "Amharic" => "am",
                    "Arabic" => "ar",
                    "Armenian" => "hy",
                    "Azerbaijani" => "az",
                    "Basque" => "eu",
                    "Belarusian" => "be",
                    "Bengali" => "bn",
                    "Bosnian" => "bs",
                    "Bulgarian" => "bg",
                    "Catalan" => "ca",
                    "Cebuano" => "ceb",
                    "Chichewa" => "ny",
                    "Chinese (simplified)" => "zh-CN",
                    "Chinese (traditional)" => "zh-TW",
                    "Corsican" => "co",
                    "Croatian" => "hr",
                    "Czech" => "cs",
                    "Danish" => "da",
                    "Dutch" => "nl",
                    "English" => "en",
                    "Esperanto" => "eo",
                    "Estonian" => "et",
                    "Filipino" => "tl",
                    "Finnish" => "fi",
                    "French" => "fr",
                    "Frisian" => "fy",
                    "Galician" => "gl",
                    "Georgian" => "ka",
                    "German" => "de",
                    "Greek" => "el",
                    "Gujarati" => "gu",
                    "Haitian creole" => "ht",
                    "Hausa" => "ha",
                    "Hawaiian" => "haw",
                    "Hebrew" => "iw",
                    "Hindi" => "hi",
                    "Hmong" => "hmn",
                    "Hungarian" => "hu",
                    "Icelandic" => "is",
                    "Igbo" => "ig",
                    "Indonesian" => "id",
                    "Irish" => "ga",
                    "Italian" => "it",
                    "Japanese" => "ja",
                    "Javanese" => "jw",
                    "Kannada" => "kn",
                    "Kazakh" => "kk",
                    "Khmer" => "km",
                    "Kinyarwanda" => "rw",
                    "Korean" => "ko",
                    "Kurdish" => "ku",
                    "Kyrgyz" => "ky",
                    "Lao" => "lo",
                    "Latin" => "la",
                    "Latvian" => "lv",
                    "Lithuanian" => "lt",
                    "Luxembourgish" => "lb",
                    "Macedonian" => "mk",
                    "Malagasy" => "mg",
                    "Malay" => "ms",
                    "Malayalam" => "ml",
                    "Maltese" => "mt",
                    "Maori" => "mi",
                    "Marathi" => "mr",
                    "Mongolian" => "mn",
                    "Myanmar" => "my",
                    "Nepali" => "ne",
                    "Norwegian" => "no",
                    "Odia" => "or",
                    "Pashto" => "ps",
                    "Persian" => "fa",
                    "Polish" => "pl",
                    "Portuguese" => "pt",
                    "Punjabi" => "pa",
                    "Romanian" => "ro",
                    "Russian" => "ru",
                    "Samoan" => "sm",
                    "Scots gaelic" => "gd",
                    "Serbian" => "sr",
                    "Sesotho" => "st",
                    "Shona" => "sn",
                    "Sindhi" => "sd",
                    "Sinhala" => "si",
                    "Slovak" => "sk",
                    "Slovenian" => "sl",
                    "Somali" => "so",
                    "Spanish" => "es",
                    "Sundanese" => "su",
                    "Swahili" => "sw",
                    "Swedish" => "sv",
                    "Tajik" => "tg",
                    "Tamil" => "ta",
                    "Tatar" => "tt",
                    "Telugu" => "te",
                    "Thai" => "th",
                    "Turkish" => "tr",
                    "Turkmen" => "tk",
                    "Ukrainian" => "uk",
                    "Urdu" => "ur",
                    "Uyghur" => "ug",
                    "Uzbek" => "uz",
                    "Vietnamese" => "vi",
                    "Welsh" => "cy",
                    "Xhosa" => "xh",
                    "Yiddish" => "yi",
                    "Yoruba" => "yo",
                    "Zulu" => "zu"
                }
            }
            Self::Libre { .. } => crate::codes_to_languages! {
                "English" => "en",
                "Arabic" => "ar",
                "Chinese" => "zh",
                "French" => "fr",
                "German" => "de",
                "Hindi" => "hi",
                "Indonesian" => "id",
                "Irish" => "ga",
                "Italian" => "it",
                "Japanese" => "ja",
                "Korean" => "ko",
                "Polish" => "pl",
                "Portuguese" => "pt",
                "Russian" => "ru",
                "Spanish" => "es",
                "Turkish" => "tr",
                "Vietnamese" => "vi"
            },
            Self::Linguee { .. } => crate::codes_to_languages! {
                "maltese" => "mt",
                "english" => "en",
                "german" => "de",
                "bulgarian" => "bg",
                "polish" => "pl",
                "portuguese" => "pt",
                "hungarian" => "hu",
                "romanian" => "ro",
                "russian" => "ru",
                // "serbian" => "sr",
                "dutch" => "nl",
                "slovakian" => "sk",
                "greek" => "el",
                "slovenian" => "sl",
                "danish" => "da",
                "italian" => "it",
                "spanish" => "es",
                "finnish" => "fi",
                "chinese" => "zh",
                "french" => "fr",
                // "croatian" => "hr",
                "czech" => "cs",
                "laotian" => "lo",
                "swedish" => "sv",
                "latvian" => "lv",
                "estonian" => "et",
                "japanese" => "ja"
            },
            Self::Microsoft { .. } => crate::codes_to_languages! {
                "Afrikaans" => "af",
                "Amharic" => "am",
                "Arabic" => "ar",
                "Assamese" => "as",
                "Azerbaijani" => "az",
                "Bashkir" => "ba",
                "Bulgarian" => "bg",
                "Bangla" => "bn",
                "Tibetan" => "bo",
                "Bosnian" => "bs",
                "Catalan" => "ca",
                "Czech" => "cs",
                "Welsh" => "cy",
                "Danish" => "da",
                "German" => "de",
                "Divehi" => "dv",
                "Greek" => "el",
                "English" => "en",
                "Spanish" => "es",
                "Estonian" => "et",
                "Basque" => "eu",
                "Persian" => "fa",
                "Finnish" => "fi",
                "Filipino" => "fil",
                "Fijian" => "fj",
                "Faroese" => "fo",
                "French" => "fr",
                "French (Canada)" => "fr-CA",
                "Irish" => "ga",
                "Galician" => "gl",
                "Gujarati" => "gu",
                "Hebrew" => "he",
                "Hindi" => "hi",
                "Croatian" => "hr",
                "Upper Sorbian" => "hsb",
                "Haitian Creole" => "ht",
                "Hungarian" => "hu",
                "Armenian" => "hy",
                "Indonesian" => "id",
                "Inuinnaqtun" => "ikt",
                "Icelandic" => "is",
                "Italian" => "it",
                "Inuktitut" => "iu",
                "Inuktitut (Latin)" => "iu-Latn",
                "Japanese" => "ja",
                "Georgian" => "ka",
                "Kazakh" => "kk",
                "Khmer" => "km",
                "Kurdish (Northern)" => "kmr",
                "Kannada" => "kn",
                "Korean" => "ko",
                "Kurdish (Central)" => "ku",
                "Kyrgyz" => "ky",
                "Lao" => "lo",
                "Lithuanian" => "lt",
                "Latvian" => "lv",
                "Chinese (Literary)" => "lzh",
                "Malagasy" => "mg",
                "Māori" => "mi",
                "Macedonian" => "mk",
                "Malayalam" => "ml",
                "Mongolian (Cyrillic)" => "mn-Cyrl",
                "Mongolian (Traditional)" => "mn-Mong",
                "Marathi" => "mr",
                "Malay" => "ms",
                "Maltese" => "mt",
                "Hmong Daw" => "mww",
                "Myanmar (Burmese)" => "my",
                "Norwegian" => "nb",
                "Nepali" => "ne",
                "Dutch" => "nl",
                "Odia" => "or",
                "Querétaro Otomi" => "otq",
                "Punjabi" => "pa",
                "Polish" => "pl",
                "Dari" => "prs",
                "Pashto" => "ps",
                "Portuguese (Brazil)" => "pt",
                "Portuguese (Portugal)" => "pt-PT",
                "Romanian" => "ro",
                "Russian" => "ru",
                "Slovak" => "sk",
                "Slovenian" => "sl",
                "Samoan" => "sm",
                "Somali" => "so",
                "Albanian" => "sq",
                "Serbian (Cyrillic)" => "sr-Cyrl",
                "Serbian (Latin)" => "sr-Latn",
                "Swedish" => "sv",
                "Swahili" => "sw",
                "Tamil" => "ta",
                "Telugu" => "te",
                "Thai" => "th",
                "Tigrinya" => "ti",
                "Turkmen" => "tk",
                "Klingon (Latin)" => "tlh-Latn",
                "Klingon (pIqaD)" => "tlh-Piqd",
                "Tongan" => "to",
                "Turkish" => "tr",
                "Tatar" => "tt",
                "Tahitian" => "ty",
                "Uyghur" => "ug",
                "Ukrainian" => "uk",
                "Urdu" => "ur",
                "Uzbek (Latin)" => "uz",
                "Vietnamese" => "vi",
                "Yucatec Maya" => "yua",
                "Cantonese (Traditional)" => "yue",
                "Chinese Simplified" => "zh-Hans",
                "Chinese Traditional" => "zh-Hant",
                "Zulu" => "zu"
            },
            Self::Deepl { .. } => crate::codes_to_languages! {
                "bulgarian" => "bg",
                "czech" => "cs",
                "danish" => "da",
                "german" => "de",
                "greek" => "el",
                "english" => "en",
                "spanish" => "es",
                "estonian" => "et",
                "finnish" => "fi",
                "french" => "fr",
                "hungarian" => "hu",
                "italian" => "it",
                "japanese" => "ja",
                "lithuanian" => "lt",
                "latvian" => "lv",
                "dutch" => "nl",
                "polish" => "pl",
                "portuguese" => "pt",
                "romanian" => "ro",
                "russian" => "ru",
                "slovak" => "sk",
                "slovenian" => "sl",
                "swedish" => "sv",
                "chinese" => "zh"
            },

            Self::Papago { .. } => crate::codes_to_languages! {
                "ko" => "Korean",
                "en" => "English",
                "ja" => "Japanese",
                "zh-CN" => "Chinese",
                "zh-TW" => "Chinese traditional",
                "es" => "Spanish",
                "fr" => "French",
                "vi" => "Vietnamese",
                "th" => "Thai",
                "id" => "Indonesia"
            },

            Self::Pons { .. } => crate::codes_to_languages! {
                "ar" => "arabic",
                "bg" => "bulgarian",
                "zh-cn" => "chinese",
                "cs" => "czech",
                "da" => "danish",
                "nl" => "dutch",
                "en" => "english",
                "fr" => "french",
                "de" => "german",
                "el" => "greek",
                "hu" => "hungarian",
                "it" => "italian",
                "la" => "latin",
                "no" => "norwegian",
                "pl" => "polish",
                "pt" => "portuguese",
                "ru" => "russian",
                "sl" => "slovenian",
                "es" => "spanish",
                "sv" => "swedish",
                "tr" => "turkish",
                "elv" => "elvish"
            },

            Self::Qcri(..) => crate::codes_to_languages! {
                "Arabic" => "ar",
                "English" => "en",
                "Spanish" => "es"
            },
        }
    }
}
