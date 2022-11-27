pub mod detection;
mod translator;

use std::{error::Error as StdError, fmt};
pub use translator::*;
#[derive(Debug)]
pub enum StatusCode {
    BadRequest,
    KeyBlocked,
    DailyReqLimitExceeded,
    DailyCharLimitExceeded,
    TextTooLong,
    TooManyRequests,
    UnprocessableText,
    InternalServerError,
    LangNotSupported,
}

impl From<StatusCode> for usize {
    fn from(code: StatusCode) -> usize {
        use StatusCode::*;

        match code {
            BadRequest => 400,
            KeyBlocked => 402,
            DailyReqLimitExceeded => 403,
            DailyCharLimitExceeded => 404,
            TextTooLong => 413,
            TooManyRequests => 429,
            UnprocessableText => 422,
            InternalServerError => 500,
            LangNotSupported => 501,
        }
    }
}

#[derive(Debug)]
pub enum Error {
    /// Error occurred during the request call, e.g a connection problem.
    TooManyRequests,
    /// Error occurred during the request call, e.g a connection problem.
    Request,
    /// The provided text exceed the length limit of the translator
    NotValidLength {
        min: usize,
        max: usize,
    },
    EngineNotSupported(String),
    Server(StatusCode),
    /// Translation was found for the text provided by the user
    TranslationNotFound,
    Reqwest(reqwest::Error),
    CssParser(String),
    InputOutput(std::io::Error),
}

impl StdError for Error {}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        use Error::*;

        match &self {
            TooManyRequests => "Server Error: You made too many requests to the server. \
            According to google, you are allowed to make 5 requests per \
            second and up to 200k requests per day. You can wait and \
            try again later or you can try the translate_batch function"
                .to_string(),
            Request => "Request exception can happen due to an api connection error. \n\
            Please check your connection and try again"
                .into(),
            TranslationNotFound => {
                "No translation was found using the current translator. Try another translator?"
                    .into()
            }
            NotValidLength { min, max } => format!(
                "Text length need to be between {min} and {max} characters"
            ),
            EngineNotSupported(engine) => format!(
                "Translator {} is not supported.\n\
                Supported translators: `deepl`, `google`, `libre`, `linguee`, `microsoft`, `mymemory`, `papago`, `pons`, `qcri`, `yandex`.",
                engine
            ),
            Error::Server(code) => format!("{code:?}"),
            Reqwest(err) => err.to_string(),
            CssParser(err) => err.clone(),
            InputOutput(err) => err.to_string(),
        }
        .fmt(f)
    }
}

impl From<reqwest::Error> for Error {
    fn from(err: reqwest::Error) -> Self {
        Error::Reqwest(err)
    }
}

impl From<std::io::Error> for Error {
    fn from(err: std::io::Error) -> Self {
        Error::InputOutput(err)
    }
}
