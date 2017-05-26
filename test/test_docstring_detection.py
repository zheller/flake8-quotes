import tokenize
from unittest import TestCase

from flake8_quotes import Token, get_docstring_tokens
from test.test_checks import get_absolute_path


class GetDocstringTokensTests(TestCase):
    def _get_docstring_tokens(self, filename):
        with open(get_absolute_path(filename), 'r') as f:
            tokens = [Token(t) for t in tokenize.generate_tokens(f.readline)]
        return get_docstring_tokens(tokens)

    def test_get_docstring_tokens_absent(self):
        self.assertEqual(self._get_docstring_tokens('data/doubles.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/doubles_multiline_string.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/doubles_noqa.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/doubles_wrapped.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/multiline_string.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/no_qa.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/singles.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/singles_multiline_string.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/singles_noqa.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/singles_wrapped.py'), set())

    def test_get_docstring_tokens(self):
        with open(get_absolute_path('data/docstring_doubles.py'), 'r') as f:
            tokens = [Token(t) for t in tokenize.generate_tokens(f.readline)]
        docstring_tokens = get_docstring_tokens(tokens)
        self.assertEqual(docstring_tokens, {tokens[1], tokens[18], tokens[45]})
