import unittest

import os
from importlib._bootstrap_external import _NamespacePath

import muadib_notebook


class TestHook(unittest.TestCase):

    def setUp(self):
        pass

    def test_module_methods_and_functions(self):
        import notebooks.test_notebook as given_module
        self.assertListEqual(dir(given_module), [
            'SampleClass',
            '__builtins__',
            '__doc__',
            '__file__',
            '__loader__',
            '__name__',
            '__package__',
            '__spec__',
            'get_ipython',
            'sample_dictionary',
            'sample_float',
            'sample_instance',
            'sample_integer',
            'sample_list',
            'sample_object',
            'sample_strng',
            'sample_tuple',
        ])

        given_module.sample_instance.sample_method()
        given_module.sample_instance.sample_method_with_inoutput(param='omega', param_a='alfa', param_b='beta')

    def test_execute(self):
        print(os.path.abspath(os.path.curdir))
        with muadib_notebook.NotebookExecutor(
                path=os.path.join('..', 'notebooks'),
                fullname='test_notebook'
        ) as e:
            e()


if __name__ == '__main__':
    unittest.main()
