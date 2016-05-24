from setuptools import setup, find_packages

config = {
    'description': 'DDB Fields',
    'author': 'US News',
    'url': '',
    'download_url': '',
    'author_email': '',
    'version': '0.0.1',
    'setup_requires': [
        'nose',
    ],
    'install_requires': [],
    'tests_require': [],
    'test_suite': None,
    'packages': find_packages(),
    'scripts': [],
    'name': 'ddb_field'
}

setup(**config)