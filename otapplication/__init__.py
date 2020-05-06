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

import os
import sys
from types import ModuleType


__version__ = '1.0'
def init_app(pkgname, exportdefs, name=None, attr=dict(), eager=False,
             version=None, author=None, author_email=None, description=None,
             branch=None, _license=None, repository=None, _copyright=None,
             commit=None):
    """ initialize given package from the export definitions. """
    
    oldmod = sys.modules[pkgname]
    name = name or oldmod.__name__
    d = {}
    d['__file__'] = os.path.abspath(getattr(oldmod, '__file__', None))
    
    lis = ['__author__', '__author_email__', '__description__', '__branch__',
           '_license', '__repository__', '_copyright', '__commit__']

    for num, value in enumerate([author, author_email, description, branch,
                              _license, repository, _copyright, commit]):
        if value:
            d[lis[num]] = value

    if hasattr(oldmod, '__version__'):
        d['__version__'] = oldmod.__version__
    elif version:
         d['__version__'] = version

    if hasattr(oldmod, '__name__'):
        d['__name__'] = name
    
    if hasattr(oldmod, '__loader__'):
        d['__loader__'] = oldmod.__loader__
        
    d['__path__'] = os.path.dirname(d['__file__'])
    
    if '__doc__' not in exportdefs and getattr(oldmod, '__doc__', None):
        d['__doc__'] = oldmod.__doc__
    
    d['__package__'] = oldmod.__package__ = name
    d.update(attr)
    
    if hasattr(oldmod, "__dict__"):
        oldmod.__dict__.update(d)
    
    mod = Application(name, exportdefs, pkgname, d, version)
    sys.modules[pkgname] = mod
    # eagerload in bypthon to avoid their monkeypatching breaking packages
    if 'bpython' in sys.modules or eager:
        for module in sys.modules.values():
            if isinstance(module, Application):
                module.__dict__


def importobj(modpath, attrname):
    module = __import__(modpath, None, None, ['__doc__'])
    if not attrname:
        return module

    retval = module
    names = attrname.split(".")
    
    for x in names:
        retval = getattr(retval, x)
    return retval


class Application(ModuleType):
    def __docget(self):
        try:
            return self.__doc
        
        except AttributeError:
        
            if '__doc__' in self.__map__:
                return self.__makeattr('__doc__')

    def __docset(self, value):
        self.__doc = value
    __doc__ = property(__docget, __docset)

    def __init__(self, name, importspec, implprefix=None, attr=None, version=None):
        self.__version = version
        
        self.__name__ = name
        self.__all__ = [x for x in importspec if x != '__onfirstaccess__']
        self.__map__ = {}
        self.__implprefix__ = implprefix or name
        if attr:
        
            for name, val in attr.items():
                # print "setting", self.__name__, name, val
                setattr(self, name, val)
        
        for name, importspec in importspec.items():
        
            if isinstance(importspec, dict):
                subname = '%s.%s' % (self.__name__, name)
                apimod = Application(subname, importspec, implprefix)
                sys.modules[subname] = apimod
                setattr(self, name, apimod)
        
            else:
                parts = importspec.split(':')
                modpath = parts.pop(0)
                attrname = parts and parts[0] or ""
        
                if modpath[0] == '.':
                    modpath = implprefix + modpath

                if not attrname:
                    subname = '%s.%s' % (self.__name__, name)
                    apimod = AppModule(subname, modpath)
                    sys.modules[subname] = apimod
                    if '.' not in name:
                        setattr(self, name, apimod)
                else:
                    self.__map__[name] = (modpath, attrname)

    def __repr__(self):
        l = []

        if hasattr(self, '__version__'):
            l.append("version=" + repr(self.__version__))
        elif self.__version:
            l.append("version=" + self.__version)

        if hasattr(self, '__file__'):
            l.append('from ' + repr(self.__file__))
        
        if l:
            return '<Application %r %s>' % (self.__name__, " ".join(l))
        return '<Application %r>' % (self.__name__,)

    def __makeattr(self, name):
        """lazily compute value for name or raise AttributeError if unknown."""
        # print "makeattr", self.__name__, name
        target = None
        if '__onfirstaccess__' in self.__map__:
            target = self.__map__.pop('__onfirstaccess__')
            importobj(*target)()
        try:
            modpath, attrname = self.__map__[name]
        except KeyError:
            if target is not None and name != '__onfirstaccess__':
                # retry, onfirstaccess might have set attrs
                return getattr(self, name)
            raise AttributeError(name)
        else:
            result = importobj(modpath, attrname)
            setattr(self, name, result)
            try:
                del self.__map__[name]
            except KeyError:
                pass  # in a recursive-import situation a double-del can happen
            return result

    __getattr__ = __makeattr

    @property
    def __dict__(self):
        # force all the content of the module
        # to be loaded when __dict__ is read
        dictdescr = ModuleType.__dict__['__dict__']
        dict = dictdescr.__get__(self)
        if dict is not None:
            hasattr(self, 'some')
            for name in self.__all__:
                try:
                    self.__makeattr(name)
                except AttributeError:
                    pass
        return dict


def AppModule(modname, modpath, attrname=None):
    mod = []

    def getmod():
        if not mod:
            x = importobj(modpath, None)
            if attrname is not None:
                x = getattr(x, attrname)
            mod.append(x)
        return mod[0]

    class AppModule(ModuleType):

        def __repr__(self):
            x = modpath
            if attrname:
                x += "." + attrname
            return '<AppModule %r for %r>' % (modname, x)

        def __getattribute__(self, name):
            try:
                return getattr(getmod(), name)
            except ImportError:
                return None

        def __setattr__(self, name, value):
            setattr(getmod(), name, value)

        def __delattr__(self, name):
            delattr(getmod(), name)

    return AppModule(str(modname))