from unittest import TestCase

from test.test_checks import get_absolute_path, run_flake8


class DocstringTestChecks(TestCase):
    def test_require_double_docstring_double_present(self):
        options = ['--inline-quotes=single', '--multiline-quotes=single', '--docstring-quotes=double']

        result = run_flake8(get_absolute_path('data/docstring_doubles.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 5, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 5, 'line': 16, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 21, 'line': 21, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_doubles_module_multiline.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 4, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_doubles_module_singleline.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 2, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_doubles_class.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 3, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 23, 'line': 5, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_doubles_function.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 3, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 5, 'line': 11, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 39, 'line': 15, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 5, 'line': 17, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 5, 'line': 21, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

    def test_require_single_docstring_double_present(self):
        options = ['--inline-quotes=single', '--multiline-quotes=double', '--docstring-quotes=single']

        result = run_flake8(get_absolute_path('data/docstring_doubles.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 5, 'line': 12, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 9, 'line': 24, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 9, 'line': 30, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 13, 'line': 35, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_doubles_module_multiline.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 1, 'line': 9, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_doubles_module_singleline.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 1, 'line': 6, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_doubles_class.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 2, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 9, 'line': 6, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 29, 'line': 9, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_doubles_function.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 2, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 5, 'line': 8, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

    def test_require_double_docstring_single_present(self):
        options = ['--inline-quotes=single', '--multiline-quotes=single', '--docstring-quotes=double']

        result = run_flake8(get_absolute_path('data/docstring_singles.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 5, 'line': 14, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 9, 'line': 26, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 9, 'line': 32, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 13, 'line': 37, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_singles_module_multiline.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 1, 'line': 9, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_singles_module_singleline.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 1, 'line': 6, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_singles_class.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 2, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 9, 'line': 6, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 29, 'line': 9, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_singles_function.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 2, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 5, 'line': 8, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

    def test_require_single_docstring_single_present(self):
        options = ['--inline-quotes=single', '--multiline-quotes=double', '--docstring-quotes=single']

        result = run_flake8(get_absolute_path('data/docstring_singles.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 5, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 21, 'line': 11, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 5, 'line': 18, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 21, 'line': 23, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_singles_module_multiline.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 4, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_singles_module_singleline.py'), options)
        self.assertEqual(result, [
            {'col': 1, 'line': 2, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_singles_class.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 3, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 23, 'line': 5, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        result = run_flake8(get_absolute_path('data/docstring_singles_function.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 3, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 5, 'line': 11, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 39, 'line': 15, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 5, 'line': 17, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 5, 'line': 21, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])
