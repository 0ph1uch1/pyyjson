#include "pyutils.h"

PyObject *create_py_unicode(const char *str, Py_ssize_t len, int is_ascii, int kind) {
    int max_char = 128;
    if (!is_ascii) {
        switch (kind) {
            case 1:
                max_char = 0xff;
                break;
            case 2:
                max_char = 0xffff;
                break;
            case 4:
                max_char = 0x10ffff;
                break;
        }
    }
    PyObject *unicode = PyUnicode_New(len, max_char);
    if (!unicode) goto alc_fail;
    memcpy(PyUnicode_DATA(unicode), str, len * kind);
    return unicode;
alc_fail:
    PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory for PyUnicode object");
    return NULL;
}
