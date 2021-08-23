from unittest import TestCase

from flake8_quotes import QuoteChecker
from test.test_checks import get_absolute_path


class DocstringTestChecks(TestCase):
    def test_require_double_docstring_double_present(self):
        class Options():
            inline_quotes = 'single'
            multiline_quotes = 'single'
            docstring_quotes = 'double'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 5, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 4, 'line': 16, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 20, 'line': 21, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 8, 'line': 30, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 12, 'line': 35, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 4, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 0, 'line': 9, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 2, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 0, 'line': 6, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 22, 'line': 5, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 4, 'line': 11, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 38, 'line': 15, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 4, 'line': 17, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
            {'col': 4, 'line': 21, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
        ])

    def test_require_single_docstring_double_present(self):
        class Options():
            inline_quotes = 'single'
            multiline_quotes = 'double'
            docstring_quotes = 'single'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': 'Q002 Double quote docstring found but single quotes preferred'},
            {'col': 4, 'line': 12, 'message': 'Q002 Double quote docstring found but single quotes preferred'},
            {'col': 8, 'line': 24, 'message': 'Q002 Double quote docstring found but single quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': 'Q002 Double quote docstring found but single quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': 'Q002 Double quote docstring found but single quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': 'Q002 Double quote docstring found but single quotes preferred'},
            {'col': 8, 'line': 6, 'message': 'Q002 Double quote docstring found but single quotes preferred'},
            {'col': 28, 'line': 9, 'message': 'Q002 Double quote docstring found but single quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': 'Q002 Double quote docstring found but single quotes preferred'},
            {'col': 4, 'line': 8, 'message': 'Q002 Double quote docstring found but single quotes preferred'},
        ])

    def test_require_double_docstring_single_present(self):
        class Options():
            inline_quotes = 'single'
            multiline_quotes = 'single'
            docstring_quotes = 'double'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': 'Q002 Single quote docstring found but double quotes preferred'},
            {'col': 4, 'line': 14, 'message': 'Q002 Single quote docstring found but double quotes preferred'},
            {'col': 8, 'line': 26, 'message': 'Q002 Single quote docstring found but double quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': 'Q002 Single quote docstring found but double quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': 'Q002 Single quote docstring found but double quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': 'Q002 Single quote docstring found but double quotes preferred'},
            {'col': 8, 'line': 6, 'message': 'Q002 Single quote docstring found but double quotes preferred'},
            {'col': 28, 'line': 9, 'message': 'Q002 Single quote docstring found but double quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': 'Q002 Single quote docstring found but double quotes preferred'},
            {'col': 4, 'line': 8, 'message': 'Q002 Single quote docstring found but double quotes preferred'},
        ])

    def test_require_single_docstring_single_present(self):
        class Options():
            inline_quotes = 'single'
            multiline_quotes = 'double'
            docstring_quotes = 'single'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/docstring_singles.py'))
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 5, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 20, 'line': 11, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 4, 'line': 18, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 20, 'line': 23, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 8, 'line': 32, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 12, 'line': 37, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 4, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 0, 'line': 9, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 2, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 0, 'line': 6, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 22, 'line': 5, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 4, 'line': 11, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 38, 'line': 15, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 4, 'line': 17, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
            {'col': 4, 'line': 21, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
        ])
