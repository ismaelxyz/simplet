#include <Python.h>

#define MODULE_DOC "Módulo con operaciones aritméticas básicas."
static PyObject *
chars_add(PyObject *self, PyObject *args){
    long a, b, ret;
    if (!PyArg_ParseTuple(args, "ll", &a, &b))
        return NULL;
    ret = a + b;
    return PyLong_FromLong(ret);
}

static PyMethodDef CharsMethods[] = {
    {"add", chars_add, METH_VARARGS,
     "Suma los argumentos y retorna el resultado."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef CharsModule = {
   PyModuleDef_HEAD_INIT,
   "chars",
   MODULE_DOC,
   -1,
   CharsMethods
};

PyMODINIT_FUNC
PyInit_chars(void){
    return PyModule_Create(&CharsModule);
}