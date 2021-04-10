from setuptools import setup

setup(
    name = 'alchemy-modelgen',
    version = '0.1.0',
    packages = ['modelgen'],
    entry_points = {
        'console_scripts': [
            'modelgen = modelgen.__main__:main'
        ]
    }
)