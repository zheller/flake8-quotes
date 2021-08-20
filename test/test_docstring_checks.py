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
        message = 'Q001 Double quoted multiline string literal found but single quotes are preferred'
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 5, 'message': message},
            {'col': 4, 'line': 16, 'message': message},
            {'col': 20, 'line': 21, 'message': message},
            {'col': 8, 'line': 30, 'message': message},
            {'col': 12, 'line': 35, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 4, 'message': message},
            {'col': 0, 'line': 9, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 2, 'message': message},
            {'col': 0, 'line': 6, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': message},
            {'col': 22, 'line': 5, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': message},
            {'col': 4, 'line': 11, 'message': message},
            {'col': 38, 'line': 15, 'message': message},
            {'col': 4, 'line': 17, 'message': message},
            {'col': 4, 'line': 21, 'message': message},
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
        message = 'Q002 Double quoted docstring literal found but single quotes are preferred'
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': message},
            {'col': 4, 'line': 12, 'message': message},
            {'col': 8, 'line': 24, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': message},
            {'col': 8, 'line': 6, 'message': message},
            {'col': 28, 'line': 9, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_doubles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': message},
            {'col': 4, 'line': 8, 'message': message},
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
        message = 'Q002 Double quoted docstring literal found but single quotes are preferred'
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': message},
            {'col': 4, 'line': 14, 'message': message},
            {'col': 8, 'line': 26, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 1, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': message},
            {'col': 8, 'line': 6, 'message': message},
            {'col': 28, 'line': 9, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 2, 'message': message},
            {'col': 4, 'line': 8, 'message': message},
        ])

    def test_require_single_docstring_single_present(self):
        class Options():
            inline_quotes = 'single'
            multiline_quotes = 'double'
            docstring_quotes = 'single'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/docstring_singles.py'))
        message = 'Q001 Double quoted multiline string literal found but single quotes are preferred'
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 5, 'message': message},
            {'col': 20, 'line': 11, 'message': message},
            {'col': 4, 'line': 18, 'message': message},
            {'col': 20, 'line': 23, 'message': message},
            {'col': 8, 'line': 32, 'message': message},
            {'col': 12, 'line': 37, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_multiline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 4, 'message': message},
            {'col': 0, 'line': 9, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_module_singleline.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 0, 'line': 2, 'message': message},
            {'col': 0, 'line': 6, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_class.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': message},
            {'col': 22, 'line': 5, 'message': message},
        ])

        multiline_checker = QuoteChecker(
            None,
            filename=get_absolute_path('data/docstring_singles_function.py')
        )
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 3, 'message': message},
            {'col': 4, 'line': 11, 'message': message},
            {'col': 38, 'line': 15, 'message': message},
            {'col': 4, 'line': 17, 'message': message},
            {'col': 4, 'line': 21, 'message': message},
        ])
