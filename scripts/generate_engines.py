from simplet.langscode import ENGINES_LANGUAGES

base = """
//! This file is autogenerate : (, Edit `scripts/generate_engines.py` instance.

use std::collections::HashMap;

#[inline(always)]
fn hash_map(source: &[(&str, &str)]) -> HashMap<String, String> {
    source
        .iter()
        .map(|(key, value)| (key.to_string(), value.to_string()))
        .collect()
}
"""

def languages_codes(codes_to_languages):
    return dict(zip(codes_to_languages.values(),  codes_to_languages.keys()))


def languages(engine: str):
    langs = ENGINES_LANGUAGES[engine]
    
    if engine in ['papago', 'pons']:
        langs = languages_codes(langs)

    keys = iter([name.title() for name in langs.keys()])
    return dict(zip(keys, langs.values()))


def hash_map(item):
    if item == "google()":
        return item

    return "hash_map(&" + str([*item.items()]).replace("'", '"') + ")"


def main():
    engines_languages = {}

    for engine in ENGINES_LANGUAGES:
        if engine == 'mymemory':
            name = 'MyMemory'
        else:
            name = engine.title()

        if name in ["Microsoft", "MyMemory", "Yandex"]:
            engines_languages[name] = "google()"
        else:
            engines_languages[name] = languages(engine)


    output = base + """
        #[inline(always)]
        fn google() -> HashMap<String, String> {
            hash_map(&
        """ + str([*engines_languages["Google"].items()]).replace("'", '"') + """
        )
        }

        """

    engines_languages["Google"] = "google()"

    fmt = ",".join([f"(\"{engine}\", " + langs_codes + ")" for engine, langs_codes in zip(
        engines_languages.keys(), map(hash_map, engines_languages.values())
    )])

    output += """
    /// HashMap<Engine, HashMap<Language, Code>>
    pub type Engine = HashMap<String, HashMap<String, String>>;

    #[inline(always)]
    pub fn start() -> Engine {
    [""" + fmt + """]
        .into_iter()
        .map(|(key, value)| (key.to_string(), value))
        .collect()
    }
    """

    print(output)


if __name__ == '__main__':
    # PYTHONPATH="." python3 scripts/generate_engines.py
    main()