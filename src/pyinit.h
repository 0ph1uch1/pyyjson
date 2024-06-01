#ifndef PYINIT_H
#define PYINIT_H

#define PY_SSIZE_T_CLEAN
// must be included before Python.h
#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif

extern PyObject *JSONDecodeError;

#endif // PYINIT_H
