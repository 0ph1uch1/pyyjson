#include <yyjson.h>

static void test_with_flags(const uint8_t *data, size_t size) {
    PyObject *re = yyjson_read_opts((const char *)data, size, NULL, NULL);
    Py_XDECREF(re);
}

int LLVMFuzzerInitialize() {
    Py_Initialize();
    return 0;
}

int LLVMFuzzerFinalize() {
    Py_Finalize();
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    test_with_flags(data, size);
    return 0;
}
