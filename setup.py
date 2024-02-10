import io
import os
from setuptools import setup

__dir__ = os.path.dirname(__file__)


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


LONG_DESCRIPTION = read(os.path.join(__dir__, 'README.rst'))

about = {}
with open(os.path.join(__dir__, 'flake8_quotes', '__about__.py')) as file:
    exec(file.read(), about)


setup(
    name='flake8-quotes',
    author='Zachary Wright Heller',
    author_email='zheller@gmail.com',
    version=about['__version__'],
    install_requires=[
        'flake8',
        'setuptools',
    ],
    url='http://github.com/zheller/flake8-quotes/',
    long_description=LONG_DESCRIPTION,
    description='Flake8 lint for quotes.',
    packages=['flake8_quotes'],
    test_suite='test',
    include_package_data=True,
    entry_points={
        'flake8.extension': [
            'Q0 = flake8_quotes:QuoteChecker',
        ],
    },
    license='MIT',
    zip_safe=True,
    keywords='flake8 lint quotes',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ]
)
