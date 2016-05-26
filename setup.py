from setuptools import setup, find_packages

config = {
    'description': 'DDB Fields',
    'author': 'Bethany Morin, U.S. News & World Report',
    'url': '',
    'download_url': '',
    'author_email': 'bmorin@usnews.com',
    'version': '1.0.0',
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