import os
import re
import subprocess
from unittest import TestCase

OUTPUT_REGEX = re.compile(r'.*?:([\d]+):([\d]+): (.*)')


def run_flake8(path, options):
    p = subprocess.Popen(['flake8', '--select=Q', path] + options,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if (stderr):
        return [{'col': 0, 'line': 0, 'message': stderr.decode('ascii')}]
    stdout_lines = stdout.splitlines()
    result = []
    for line in stdout_lines:
        match = OUTPUT_REGEX.match(line.decode('ascii'))
        if (match):
            result.append({'line': int(match.group(1)), 'col': int(match.group(2)), 'message': match.group(3)})
    return result


class TestFlake8Stdin(TestCase):
    def test_stdin(self):
        """Test using stdin."""
        filepath = get_absolute_path('data/doubles.py')
        with open(filepath, 'rb') as f:
            p = subprocess.Popen(['flake8', '--select=Q', '-'], stdin=f,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

        stdout_lines = stdout.splitlines()
        self.assertEqual(stderr, b'')
        self.assertEqual(len(stdout_lines), 3)
        self.assertRegex(stdout_lines[0], b'stdin:1:(24|25): Q000 Remove bad quotes')
        self.assertRegex(stdout_lines[1], b'stdin:2:(24|25): Q000 Remove bad quotes')
        self.assertRegex(stdout_lines[2], b'stdin:3:(24|25): Q000 Remove bad quotes')


class DoublesTestChecks(TestCase):
    options = ["--inline-quotes='", "--multiline-quotes='"]

    def test_multiline_string(self):
        result = run_flake8(get_absolute_path('data/doubles_multiline_string.py'), self.options)
        self.assertEqual(result, [
            {'col': 5, 'line': 1, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

    def test_wrapped(self):
        result = run_flake8(get_absolute_path('data/doubles_wrapped.py'), self.options)
        self.assertEqual(result, [])

    def test_doubles(self):
        result = run_flake8(get_absolute_path('data/doubles.py'), self.options)
        self.assertEqual(result, [
            {'col': 25, 'line': 1, 'message': 'Q000 Remove bad quotes'},
            {'col': 25, 'line': 2, 'message': 'Q000 Remove bad quotes'},
            {'col': 25, 'line': 3, 'message': 'Q000 Remove bad quotes'},
        ])

    def test_noqa_doubles(self):
        result = run_flake8(get_absolute_path('data/doubles_noqa.py'), self.options)
        self.assertEqual(result, [])

    def test_escapes(self):
        result = run_flake8(get_absolute_path('data/doubles_escaped.py'), self.options)
        self.assertEqual(result, [
            {'col': 26, 'line': 1, 'message': 'Q003 Change outer quotes to avoid escaping inner quotes'},
        ])

    def test_escapes_allowed(self):
        options = ["--inline-quotes='", '--no-avoid-escape']
        result = run_flake8(get_absolute_path('data/doubles_escaped.py'), options)
        self.assertEqual(result, [])


class DoublesAliasTestChecks(TestCase):
    options = ['--inline-quotes=single', '--multiline-quotes=single']

    def test_doubles(self):
        result = run_flake8(get_absolute_path('data/doubles_wrapped.py'), self.options)
        self.assertEqual(result, [])

        result = run_flake8(get_absolute_path('data/doubles.py'), self.options)
        self.assertEqual(result, [
            {'col': 25, 'line': 1, 'message': 'Q000 Remove bad quotes'},
            {'col': 25, 'line': 2, 'message': 'Q000 Remove bad quotes'},
            {'col': 25, 'line': 3, 'message': 'Q000 Remove bad quotes'},
        ])


class SinglesTestChecks(TestCase):
    options = ['--inline-quotes="', '--multiline-quotes="']

    def test_multiline_string(self):
        result = run_flake8(get_absolute_path('data/singles_multiline_string.py'), self.options)
        self.assertEqual(result, [
            {'col': 5, 'line': 1, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

    def test_wrapped(self):
        result = run_flake8(get_absolute_path('data/singles_wrapped.py'), self.options)
        self.assertEqual(result, [])

    def test_singles(self):
        result = run_flake8(get_absolute_path('data/singles.py'), self.options)
        self.assertEqual(result, [
            {'col': 25, 'line': 1, 'message': 'Q000 Remove bad quotes'},
            {'col': 25, 'line': 2, 'message': 'Q000 Remove bad quotes'},
            {'col': 25, 'line': 3, 'message': 'Q000 Remove bad quotes'},
        ])

    def test_noqa_singles(self):
        result = run_flake8(get_absolute_path('data/singles_noqa.py'), self.options)
        self.assertEqual(result, [])

    def test_escapes(self):
        result = run_flake8(get_absolute_path('data/singles_escaped.py'), self.options)
        self.assertEqual(result, [
            {'col': 26, 'line': 1, 'message': 'Q003 Change outer quotes to avoid escaping inner quotes'},
        ])

    def test_escapes_allowed(self):
        options = ['--inline-quotes="', '--no-avoid-escape']

        result = run_flake8(get_absolute_path('data/singles_escaped.py'), options)
        self.assertEqual(result, [])


class SinglesAliasTestChecks(TestCase):
    options = ['--inline-quotes=double', '--multiline-quotes=double']

    def test_singles(self):
        result = run_flake8(get_absolute_path('data/singles_wrapped.py'), self.options)
        self.assertEqual(result, [])

        result = run_flake8(get_absolute_path('data/singles.py'), self.options)
        self.assertEqual(result, [
            {'col': 25, 'line': 1, 'message': 'Q000 Remove bad quotes'},
            {'col': 25, 'line': 2, 'message': 'Q000 Remove bad quotes'},
            {'col': 25, 'line': 3, 'message': 'Q000 Remove bad quotes'},
        ])


class MultilineTestChecks(TestCase):
    def test_singles(self):
        options = ["--inline-quotes='", '--multiline-quotes="']

        result = run_flake8(get_absolute_path('data/multiline_string.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 10, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

    def test_singles_alias(self):
        options = ['--inline-quotes=single', '--multiline-quotes=double']

        result = run_flake8(get_absolute_path('data/multiline_string.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 10, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

    def test_doubles(self):
        options = ['--inline-quotes="', "--multiline-quotes='"]

        result = run_flake8(get_absolute_path('data/multiline_string.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 1, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])

    def test_doubles_alias(self):
        options = ['--inline-quotes=double', '--multiline-quotes=single']

        result = run_flake8(get_absolute_path('data/multiline_string.py'), options)
        self.assertEqual(result, [
            {'col': 5, 'line': 1, 'message': 'Q001 Remove bad quotes from multiline string'},
        ])


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
