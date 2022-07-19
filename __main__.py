#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Command line for SimpleT control
# Copyright © 2022 @asraelxyz, All Rights Reserved.

import click
from sys import stdout
import simplet.main as simplet
from json import dump as json_dump

# Click settings
CONTEXT_SETTINGS = { 'help_option_names': ['-h', '--help'] }

def validate_text(ctx: dict, param: str, text: str):
    return text

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("text", metavar="<text>", required=True, callback=validate_text)
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
@click.version_option(version=simplet.__version__)
# Displays by standard output in "json" format the original and the translated
# text, and the folder where the audios of the texts were saved.
def main(text: str, translator: str, source: str, target: str):
    json_dump(simplet.main(text, translator, source, target), stdout)

if __name__ == '__main__':
    main()
