from flake8_quotes import QuoteChecker
import os
from unittest import TestCase


class TestChecks(TestCase):
    def test_get_noqa_lines(self):
        checker = QuoteChecker(None, filename=get_absolute_path('data/no_qa.py'))
        self.assertEqual(checker.get_noqa_lines(checker.get_file_contents()), [2])


class DoublesTestChecks(TestCase):
    def setUp(self):
        class DoublesOptions():
            quotes = '\''
        QuoteChecker.parse_options(DoublesOptions)

    def test_multiline_string(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_multiline_string.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [])

    def test_wrapped(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_wrapped.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [])

    def test_doubles(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [
            {'col': 24, 'line': 1, 'message': 'Q000 Remove bad quotes.'}
        ])

    def test_noqa_doubles(self):
        checker = QuoteChecker(None, get_absolute_path('data/doubles_noqa.py'))
        self.assertEqual(list(checker.run()), [])


class DoublesMixedTestChecks(TestCase):
    def setUp(self):
        class DoublesMixedOptions():
            quotes = '\''
            multiline_quotes = '"'
        QuoteChecker.parse_options(DoublesMixedOptions)

    def test_mixed(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_mixed.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [])


class SinglesTestChecks(TestCase):
    def setUp(self):
        class SinglesOptions():
            quotes = '"'
        QuoteChecker.parse_options(SinglesOptions)

    def test_multiline_string(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles_multiline_string.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [])

    def test_wrapped(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles_wrapped.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [])

    def test_singles(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [
            {'col': 24, 'line': 1, 'message': 'Q000 Remove bad quotes.'}
        ])

    def test_noqa_singles(self):
        checker = QuoteChecker(None, get_absolute_path('data/singles_noqa.py'))
        self.assertEqual(list(checker.run()), [])


class SinglesMixedTestChecks(TestCase):
    def setUp(self):
        class SinglesMixedOptions():
            quotes = '"'
            multiline_quotes = '\''
        QuoteChecker.parse_options(SinglesMixedOptions)

    def test_mixed(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles_mixed.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [])


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
