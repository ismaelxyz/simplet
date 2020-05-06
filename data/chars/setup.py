#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup, Extension
# from distutils.cygwinccompiler
#from ctypes import *
#asd = LibraryLoader.LoadLibrary("") 
#cdll.LoadLibrary()
# C:\Users\juan\AppData\Local\Programs\Python\Python38-32\Lib\distutils

#{'name': 'Keywdarg', 'version': '1.0', 'description': 'Basic math functions.', 
#'ext_modules': [<distutils.extension.Extension('keywdarg') at 0x5ce5c8>]}

"""
# extend 1. Embedding Python in Another Application
PyObject *pName, *pModule, *pFunc;
PyObject *pArgs, *pValue;

Py_Initialize();
    pName = PyUnicode_DecodeFSDefault(argv[1]);
    /* Error checking of pName left out */

    pModule = PyImport_Import(pName);
    Py_DECREF(pName);
"""

#C:\Program Files\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.24.28314\bin\HostX86\x86\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MD -DMAJOR_VERSION=1 -DMINOR_VERSION=0 -IC:\Users\juan\AppData\Local\Programs\Python\Python38-32\include -IC:\Users\juan\AppData\Local\Programs\Python\Python38-32\include "-IC:\Program Files\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.24.28314\ATLMFC\include" "-IC:\Program Files\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.24.28314\include"
#"-IC:\Program Files\Windows Kits\NETFXSDK\4.8\include\um" "-IC:\Program Files\Windows Kits\10\include\10.0.18362.0\ucrt" "-IC:\Program Files\Windows Kits\10\include\10.0.18362.0\shared" "-IC:\Program Files\Windows Kits\10\include\10.0.18362.0\um" "-IC:\Program Files\Windows Kits\10\include\10.0.18362.0\winrt" "-IC:\Program Files\Windows Kits\10\include\10.0.18362.0\cppwinrt"
#/EHsc /Tpchars.cpp /Fobuild\temp.win32-3.8\Release\chars.obj

#C:\Program Files\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.24.28314\bin\HostX86\x86\link.exe /nologo /INCREMENTAL:NO /LTCG /DLL /MANIFEST:EMBED,ID=2 /MANIFESTUAC:NO /LIBPATH:C:\Users\juan\AppData\Local\Programs\Python\Python38-32\libs /LIBPATH:C:\Users\juan\AppData\Local\Programs\Python\Python38-32\PCbuild\win32 "/LIBPATH:C:\Program Files\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.24.28314\ATLMFC\lib\x86" "/LIBPATH:C:\Program Files\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.24.28314\lib\x86" "/LIBPATH:C:\Program Files\Windows Kits\NETFXSDK\4.8\lib\um\x86" "/LIBPATH:C:\Program Files\Windows Kits\10\lib\10.0.18362.0\ucrt\x86" "/LIBPATH:C:\Program Files\Windows Kits\10\lib\10.0.18362.0\um\x86" /EXPORT:PyInit_chars build\temp.win32-3.8\Release\chars.obj /OUT:build\lib.win32-3.8\chars.cp38-win32.pyd /IMPLIB:build\temp.win32-3.8\Release\chars.cp38-win32.lib

# g++ -DNDEBUG -g -O3 -Wall -fPIC -DMAJOR_VERSION=1 -DMINOR_VERSION=0 -IC:\Users\juan\AppData\Local\Programs\Python\Python38-32\include -IC:\Users\juan\AppData\Local\Programs\Python\Python38-32\include -c chars.cpp -o build/temp/chars.o
#g++ -DNDEBUG -g -O3 -Wall -fPIC -DMAJOR_VERSION=1 -DMINOR_VERSION=0 -c chars.cpp -o build/temp/chars.o

# g++ -shared build/temp/chars.o -L"C:\Program Files\Windows Kits\10\lib\10.0.18362.0\ucrt\x86" -o build/lib/chars.dll
# -ltcl83
# Nombre el módulo y archivos que contienen el código de fuente.
module = Extension("chars", sources=["chars.cpp"], define_macros=[('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')]
)
#Py_STRINGIFY(x)
#Convert x to a C string. E.g. Py_STRINGIFY(123) returns "123".
#Py_BuildValue

# Nombre del paquete, versión, descripción y una lista con las extensiones.
setup(name="chars",
      version="1.0",
      description="Basic math functions.",
      ext_modules=[module],
      license="MIT"
     )