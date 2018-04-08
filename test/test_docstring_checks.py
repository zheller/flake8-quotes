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
            {'col': 0, 'line': 5, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 4, 'line': 16, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 20, 'line': 21, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 8, 'line': 30, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 12, 'line': 35, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 4, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 0, 'line': 9, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 2, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 0, 'line': 6, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 22, 'line': 5, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 4, 'line': 11, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 38, 'line': 15, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 4, 'line': 17, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 4, 'line': 21, 'message': 'Q001 Remove bad quotes from multiline string'},
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
            {'col': 0, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 4, 'line': 12, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 8, 'line': 24, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 8, 'line': 6, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 28, 'line': 9, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 4, 'line': 8, 'message': 'Q002 Remove bad quotes from docstring'},
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
            {'col': 0, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 4, 'line': 14, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 8, 'line': 26, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 8, 'line': 6, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 28, 'line': 9, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': 'Q002 Remove bad quotes from docstring'},
            {'col': 4, 'line': 8, 'message': 'Q002 Remove bad quotes from docstring'},
        ])

    def test_require_single_docstring_single_present(self):
        class Options():
            inline_quotes = 'single'
            multiline_quotes = 'double'
            docstring_quotes = 'single'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/docstring_singles.py'))
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 5, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 20, 'line': 11, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 4, 'line': 18, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 20, 'line': 23, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 8, 'line': 32, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 12, 'line': 37, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 4, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 0, 'line': 9, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 2, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 0, 'line': 6, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 22, 'line': 5, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 4, 'line': 11, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 38, 'line': 15, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 4, 'line': 17, 'message': 'Q001 Remove bad quotes from multiline string'},
            {'col': 4, 'line': 21, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])
