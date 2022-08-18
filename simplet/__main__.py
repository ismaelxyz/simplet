#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Command line for SimpleT control
# Copyright © 2022 @asraelxyz, All Rights Reserved.

import click
from . import __version__, main as start
from json import dumps as json_dumps
from deep_translator.engines import __engines__ as engines

# Click settings
CONTEXT_SETTINGS = { 'help_option_names': ['-h', '--help'] }

def validate_text(ctx: dict, param: str, text: str):
    return text

def print_translators(ctx, _0, value):
    if not value or ctx.resilient_parsing:
        return

    click.echo(json_dumps([x.title() for x in engines.keys()]))

    ctx.exit()

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("text", metavar="<text>", required=True, callback=validate_text)
@click.option(
    "--trs",
    default=False,
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=print_translators,
    help="Print all translators availables and exit.",
)
@click.option(
    "-tr",
    "--translator",
    metavar="<translator>",
    default="google",
    show_default=True,
    # callback=validate_lang,
    help="Target Language",
)
@click.option(
    "-s",
    "--source",
    metavar="<source>",
    default='es',
    show_default=True,
    # callback=validate_lang,
    help="Source Language",
)
@click.option(
    "-t",
    "--target",
    metavar="<target>",
    default="en",
    show_default=True,
    # callback=validate_lang,
    help="Target Language",
)
@click.version_option(version=__version__)
def main(text: str, translator: str, source: str, target: str):
    """
        Displays by standard output in "json" format the original and the translated
        text, and the folder where the audios of the texts were saved.
    """
    click.echo(json_dumps(start(text, translator, source, target)))

if __name__ == '__main__':
    main()
