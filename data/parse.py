#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2020 Ismael Belisario

# This file is part of Open Translation.

# Open Translation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Open Translation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Open Translation. If not, see <https://www.gnu.org/licenses/>.

"""
Script Name: parse.py
Parse for OT.
"""

from optparse import OptionParser, Option
from sys import stderr
from .constans import *
from typing import Optional
from types import FunctionType


class OTOption(Option):

    ACTIONS = ('store',
               'store_const',
               'store_true',
               'store_false',
               'append',
               'append_const',
               'count',
               'callback',
               'copyright',
               'license',
               'warranty',
               'branch',
               'help',
               'author',
               'version')
    
    def __init__(self, *k, **kw):
        super().__init__(*k, **kw)
    
    def take_action(self, action: str, dest, opt, value, values, parser):

        if action == 'copyright':
            parser.print_copyright()
            parser.exit()
        
        elif action == 'license':
            parser.print_license()
            parser.exit()
        
        elif action == 'warranty':
            parser.print_warranty()
            parser.exit()
        
        elif action == 'branch':
            parser.print_branch()
            parser.exit()
        
        elif action == 'author':
            parser.print_author()
            parser.exit()

        super().take_action(action, dest, opt, value, values, parser)

class OTOptionParser(OptionParser):
    
    def __init__(self):
        #  *args, **kwargs, # epilog="Hola"
        usage = 'usage: %prog [options] ... [-m MODE | -s FILE] [-f FILE or FILE]'
        version = f"{NAME} {VERSION}"
        # f"{NAME} (OT)"
        description = f"A Translate for all persons, in evolution."
        super().__init__(usage=usage, version=version, option_class=OTOption,
                         description=description)
    
    def print_license(self):
        from .utilities import read_file
        stderr.write(read_file('data/legal/COPYRIGHT.txt'))
    
    def format_basic(self, title, text):
        return f"{' ' * 28}{NAME}\n\n{title}\n\n{text}"

    def print_copyright(self):
        stderr.write(self.format_basic('COPYRIGHT', COPYRIGHT))
    
    def print_warranty(self):
        stderr.write(self.format_basic('WARRANTY', WARRANTY[1:]))
    
    def print_branch(self):
        stderr.write(self.format_basic('BRANCH', BRANCH))
    
    def print_author(self):
        stderr.write(self.format_basic('AUTHOR', AUTHOR))
    
    def format_help(self, formatter=None) -> str:
        if formatter is None:
            formatter = self.formatter
        #result = [f"\n{' ' * 31 }{NAME}\n", f"{' ' * 21}{COPYRIGHT}\n\n"]
        result = [f"{NOTICE}\n"]
        # [self.version, self.com
        if self.description:
            result.append(self.format_description(formatter) + "\n")

        if self.usage:
            result.append(self.get_usage() + "\n")
        result.append(self.format_option_help(formatter))
        result.append(self.format_epilog(formatter))
        return ''.join(result)
    
    def _populate_option_list(self, option: list, add_help: bool=True):
        super()._populate_option_list(option, add_help)
        self._add_copyright_option()
        self._add_license_option()
        self._add_warranty_option()
        self._add_author_option()
        self._add_branch_option()
    
    def _add_version_option(self):
        self.add_option('-v', '--version', action='version',
                        help='Show program version number and exit.')
    
    def _add_copyright_option(self):
        self.add_option('-c', '--copyright',  action='copyright', 
                        help='Show program copyright and exit.')

    def _add_license_option(self):
        self.add_option('-l', '--license', action='license', 
                        help='Show program license and exit.')

    def _add_warranty_option(self):
        self.add_option('-w', '--warranty', action='warranty', 
                        help='Show program warranty and exit.')
    
    def _add_author_option(self):
        self.add_option('-a', '--author', action='author', 
                        help='Show program author and exit.')

    def _add_branch_option(self):
        self.add_option('-b', '--branch', action='branch', 
                        help='Show program branch and exit.')
        #  -> Optional[dict, type]
    def parse_args(self, dic: bool=False):
        # Return the options and args of user.

        ## Param
        # dic: Change type opts of Values to dict.

        if dic :
            opts, args = super().parse_args()
            return opts.__dict__, args
        return super().parse_args()

def run_parser() -> type:
    parser = OTOptionParser()


    parser.add_option('-m', '--mode', default='commands', help='Interaction mod'
                      "e: graphic, console, commands [default: %default.]")

    parser.add_option('-f', '--file', metavar='FILE', help='File at Translate.')

    parser.add_option('-o', '--output', metavar='FILE', help='Save translation'
    '; If give input file save translation of these file else save translation'
    ' of the interaction.')

    parser.add_option('-n', '--notice', default='true', metavar='BOOL', help='S'
    "how notice program states: true (t) or false (f) [default: %default.]")
    
    return parser.parse_args(True)

def manager_parse():
    # Manager of parse for OT.

    opts, args = run_parser()
    if opts['notice'] in ('t', 'true'): opts['notice'] = True
    if opts['notice'] in ('f', 'false'): opts['notice'] = False
    
    if len(args) > 1 or args and opts['file'] is not None:
        stderr.write("Error: One input file must be specified.\n")
        exit(1)
    
    if opts['mode'] not in ('graphic', 'console','commands'):
        stderr.write(f"Error: Unknown mode: {opts['mode']}.\n")
        exit(1)
    
    if args:
        opts['file'] = args[0]
    
    return opts