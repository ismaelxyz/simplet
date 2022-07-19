# Copyright © 2022 @asraelxyz, All Rights Reserved.

from hashlib import sha256 as Sha256
from gtts import gTTS
from os import path as fs
from simplet.base import DataBase
from deep_translator.engines import __engines__ as engines

# App version
__version__ = '0.0.10' 

# Translate a "text" from a "source" language into a "target" language using
# one of the available translators ("engine").
def translate(engine: str, source: str, target: str, text: str) -> str:
    translator_class = engines.get(engine, None)
    if not translator_class:
        names      = list(engines.keys())
        text_names = ", ".join(names[:-1])

        raise NameError(
            f"""Translator `{engine}` is not supported.
            \r Supported translators: {text_names} and {names[-1]}"""
        )

    translator  = translator_class(source=source, target=target)
    return translator.translate(text)

# It converts the "text" of a given "language" into audio in mp3 format and
# stores it in a "directory".
def text_to_speech(directory: str, name_file: str, lang: str, text: str):
    speech = gTTS(text=text, lang=lang, slow=False, tld='com', lang_check=True)
    speech.save(fs.join(directory, name_file + '.mp3'))

# Translates a "text" from "source" to "target", saves audios in "mp3" format
# of the original and translated text in a specific folder, also returns the
# path of the directory where the audios, the original text and the translated
# text are located.
def main(text: str, translator: str, source: str, target: str) -> dict:
    hash_registry = Sha256(text.encode('utf-8')).hexdigest()
    registry_dir = fs.join(fs.expanduser('~'), '.simplet')
    initiaize_database = False

    if not fs.isdir(registry_dir):
        initiaize_database = True
        fs.os.makedirs(registry_dir)
    
    with DataBase(fs.join(registry_dir, 'registry.db')) as registry:
        if initiaize_database:
            registry.initialize()

        directory, source_text, target_text = registry.search(
            hash_registry, source, target
        )
        sound_directory = fs.join(registry_dir, str(directory))

        if (directory, source_text, target_text) == (None,) * 3:
            translation = translate(translator, source, target, text)
            registry.add_translation(
                hash_registry, source, target, text, translation
            )

            directory, source_text, target_text = registry.search(
                hash_registry, source, target
            )

            sound_directory = fs.join(registry_dir, str(directory))

            fs.os.makedirs(sound_directory)

            text_to_speech(sound_directory, 'source', source, text)
            text_to_speech(sound_directory, 'target', target, translation)
    
    return {
        "sound_directory": sound_directory,
        "source_text": source_text,
        "target_text": target_text,
    }
    
