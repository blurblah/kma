
from setuptools import setup, find_packages

setup(
    name = 'kma',
    version = '0.1.3',
    description = 'Current weather and forecast information library for kma.go.kr',
    url = 'https://github.com/blurblah/kma',
    license='MIT',
    author = 'blurblah',
    author_email = 'blurblah@blurblah.net',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords = 'weather current forecast korea temperature humidity rain kma',
    packages = find_packages(exclude=['tests', 'docs']),
    install_requires = ['urllib3', 'certifi', 'pytz'],
    python_requires = '>=3',
)
