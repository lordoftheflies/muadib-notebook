import io
import os
import sys
import types

import nbformat
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat import read


def find_notebook(fullname, path=None, extension=".ipynb"):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit('.', 1)[-1]
    if not path:
        path = ['']
    for d in path:
        nb_path = os.path.join(d, name + extension)
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path


class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""

    def __init__(self, path=None):
        self.shell = InteractiveShell.instance()
        self.path = path

    def load_module(self, fullname):
        """import a notebook as a module"""
        path = find_notebook(fullname, self.path)

        print("importing Jupyter notebook from %s" % path)

        # load the notebook object
        with io.open(path, 'r', encoding='utf-8') as f:
            nb = read(f, 4)

        # create the module and add it to sys.modules
        # if name in sys.modules:
        #    return sys.modules[name]
        mod = types.ModuleType(fullname)
        mod.__file__ = path
        mod.__loader__ = self
        mod.__dict__['get_ipython'] = get_ipython
        sys.modules[fullname] = mod

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        try:
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    # transform the input to executable Python
                    code = self.shell.input_transformer_manager.transform_cell(cell.source)
                    # run the code in themodule
                    exec(code, mod.__dict__)
        finally:
            self.shell.user_ns = save_user_ns
        return mod


class NotebookFinder(object):
    """Module finder that locates Jupyter Notebooks"""

    def __init__(self):
        self.loaders = {}

    def find_module(self, fullname, path=None):
        nb_path = find_notebook(fullname, path)
        if not nb_path:
            return

        key = path
        if path:
            # lists aren't hashable
            key = os.path.sep.join(path)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)
        return self.loaders[key]


class NotebookExecutor(object):
    """Executor that execute notebooks"""

    def __init__(self, fullname, path=None, extension="ipynb", kernel_name='python3', timeout=600):
        super().__init__()
        self.fullname = fullname
        self.path = path
        self.extension = extension
        self.kernel_name = kernel_name
        self.timeout = timeout

    @property
    def notebook_path(self):
        return '%s/%s.%s' % (self.path, self.fullname, self.extension)

    def __enter__(self):
        self.nb = self.read(path=(self.notebook_path))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.write()

    def __call__(self, *args, **kwargs):
        ep = ExecutePreprocessor(timeout=self.timeout, kernel_name=self.kernel_name)
        ep.preprocess(self.nb, {'metadata': {'path': '%s/' % self.path}})

    def write(self):
        with open(self.notebook_path, 'wt') as f:
            nbformat.write(self.nb, f)

    def read(self, path):
        nb = None

        print("reading Jupyter notebook from %s" % path)
        # load the notebook object
        with io.open(path, 'r', encoding='utf-8') as f:
            nb = read(f, 4)
        return nb


sys.meta_path.append(NotebookFinder())
