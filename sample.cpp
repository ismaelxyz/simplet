/*
 Copyright © 2020 Ismael Belisario

 This file is part of Open Translation.

 Open Translation is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Open Translation is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Open Translation. If not, see <https://www.gnu.org/licenses/>.
*/

#include "Python.h"

// using namespace std;


int main(int argc, char *argv[]) {
    
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);

    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]/n");
        exit(1);
    }

    Py_SetProgramName(program);
    Py_Initialize();
    PyObject *args;

    if (argc == 1) {
        args = Py_None;
    
    } else {    
        args = PyList_New(0);
        for (int i=1; i<argc; i++) {
            PyList_Append(args, PyUnicode_FromString(argv[i]));
        }
    }
    
    PyObject *PySys, *PySySPath, *OpenTranslation, *MainFunc, *pArgs;

    PySys = PyImport_Import(PyUnicode_FromString("sys"));
    PySySPath = PyObject_GetAttrString(PySys, "path");
    
    
    PyList_Append(PySySPath, 
    PyUnicode_FromString(/* "Path_to/OpenTranslation" */));
    
    OpenTranslation = PyImport_Import(PyUnicode_FromString("OpenTranslation"));
    MainFunc = PyObject_GetAttrString(OpenTranslation, "main");

    // Params for call func of python.
    pArgs = PyTuple_New(1);
    PyTuple_SetItem(pArgs, 0, args);
    
    if (MainFunc && PyCallable_Check(MainFunc)) {
        PyObject_CallObject(MainFunc, pArgs);
        PyErr_Print();
    
    } else {
        PyErr_Print();
        fprintf(stderr, "Error: Not Open Translation\n");
        return 1;   
    }

    PyMem_RawFree(program);
    return 0;
}