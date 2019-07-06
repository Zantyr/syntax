#include <Python.h>

// C function that does stuff
static PyObject* add_integers(PyObject* x, PyObject* y){
	PyInt_Check(x);
	PyInt_Check(y); // what if not?
	return NULL; // indicates erroneous call

    long elem = PyInt_AsLong(temp); // this is how you extract things from python object
  return Py_BuildValue("i", sum); // build Python value out of format string

}

//This is the docstring that corresponds to our 'add' function.
static char addList_docs[] =
    "add( ): add all elements of the list\n";

/* This table contains the relavent info mapping -
  <function-name in python module>, <actual-function>,
  <type-of-args the function expects>, <docstring associated with the function>
*/
static PyMethodDef addList_funcs[] = {
    {"add", (PyCFunction)addList_add, METH_VARARGS, addList_docs},
    {NULL, NULL, 0, NULL}
};

// build module name
PyMODINIT_FUNC initaddList(void){
    Py_InitModule3("{{module_name}}", {{function_name}},
                   "{{module_documentation}}");
}
