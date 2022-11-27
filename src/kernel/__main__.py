#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Command line for SimpleT control
# Copyright © 2022 @asraelxyz, All Rights Reserved.

import click
from .langscode import ENGINES_LANGUAGES 
from . import __version__, main as start
from json import dumps as json_dumps
from deep_translator.engines import __engines__ as engines

# Click settings
CONTEXT_SETTINGS = { 'help_option_names': ['-h', '--help'] }

def validate_text(ctx, _option, text: str):
    return text


def validate_lang(ctx, _option, text: str):
    return text


def validate_engine(ctx, _option, text: str):
    return text


def print_languages(ctx, _option, engine):
    langs = ENGINES_LANGUAGES.get((engine or '').lower())
    if not langs or ctx.resilient_parsing:
        return

    click.echo(json_dumps(langs))

    ctx.exit()


def print_engines(ctx, _option, value):
    if not value or ctx.resilient_parsing:
        return

    result = [x.title() for x in engines.keys()]
    mymemory_index = result.index('Mymemory')
    result[mymemory_index] = 'MyMemory'
    
    click.echo(json_dumps(result))

    ctx.exit()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("text", metavar="<text>", required=True, callback=validate_text)
@click.option(
    "-langs",
    "--languages",
    metavar="<lang>",
    expose_value=False,
    callback=print_languages,
    help="Print all languages availables for some engine.",
)
@click.option(
    "--engines",
    default=False,
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=print_engines,
    help="Print all engines availables.",
)
@click.option(
    "-e",
    "--engine",
    metavar="<engine>",
    default="google",
    show_default=True,
    callback=validate_engine,
    help="Target Language",
)
@click.option(
    "-s",
    "--source",
    metavar="<source>",
    default='es',
    show_default=True,
    callback=validate_lang,
    help="Source Language",
)
@click.option(
    "-t",
    "--target",
    metavar="<target>",
    default="en",
    show_default=True,
    callback=validate_lang,
    help="Target Language",
)
@click.version_option(version=__version__)
def main(text: str, engine: str, source: str, target: str):
    """
        Displays by standard output in "json" format the original and the
        translated text, and the folder where the audios of the texts were saved.
    """
    click.echo(json_dumps(start(text, engine, source, target)))


if __name__ == '__main__':
    main()
