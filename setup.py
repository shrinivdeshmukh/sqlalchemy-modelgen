from setuptools import setup, find_packages

setup(
    name = 'alchemy-modelgen',
    url = 'https://github.com/shree14/sqlalchemy-modelgen',
    author = 'Shrinivas Deshmukh',
    author_email = 'shrinivas.deshmukh11@gmail.com',
    version = '0.0.2',
    packages = ['modelgen', 'modelgen.templates', 'modelgen.alembic'],
    install_requires=[
          'alembic>=1.5.8',
          'Jinja2>=2.11.3',
          'mysql-connector-python>=8.0.23',
          'psycopg2-binary>=2.8.6',
          'python-dotenv>=0.17.0',
          'PyYAML>=5.4.1',
          'snowflake-sqlalchemy>=1.2.4',
          'SQLAlchemy>=1.4.4',
          'sqlalchemy-redshift>=0.8.2'
      ],
    setup_requires = [
          'alembic>=1.5.8',
          'Jinja2>=2.11.3',
          'mysql-connector-python>=8.0.23',
          'psycopg2-binary>=2.8.6',
          'python-dotenv>=0.17.0',
          'PyYAML>=5.4.1',
          'snowflake-sqlalchemy>=1.2.4',
          'SQLAlchemy>=1.4.4',
          'sqlalchemy-redshift>=0.8.2'
      ],
    package_data={'modelgen': ['alembic.ini','templates/*', 'alembic/*']},
    entry_points = {
        'console_scripts': [
            'modelgen = modelgen.__main__:main'
        ]
    }
)