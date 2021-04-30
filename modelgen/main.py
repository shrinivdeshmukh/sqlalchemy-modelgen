import argparse
from pathlib import Path
from os import path, getcwd, environ
from shutil import copyfile, copytree

import io
import sys
import pkg_resources

from sqlalchemy.engine import create_engine
# from sqlalchemy.schema import MetaData
from sqlalchemy import MetaData
from modelgen import __file__
from modelgen import ModelGenerator
from sqlacodegen.codegen import CodeGenerator

def msg(name=None):                                                            
    return '''modelgen [--source SOURCE, use yaml file or use database url to create sqlalchemy model files (yaml or database)] [OPTIONS]

    1. `modelgen --source yaml` usage:

        [--init FOLDER_PATH, Initialize sqlalchemygen project]
        [--createmodel, Create sqlalchemy model code] [-f, --file, path/to/the/schema_template_file.yaml] (OPTIONAL)[--alembic, If specified, alembic support will be set to True (default: False)]
                
        examples:
            * modelgen --source yaml --init ./example
            * modelgen --source yaml --createmodel -f example/templates/example.yaml (without alembic support)
            * modelgen --source yaml --createmodel -f example/templates/example.yaml --alembic (with alembic support)

    2. `modelgen --source database` usage:
        [-u, --url, SQLAlchemy url to the database]
        [--version, print the version number and exit]
        [--schema, load tables from an alternate schema]
        [--tables, tables to process (comma-separated, default: all)]
        [--noviews, ignore views]
        [--noindexes, ignore indexes]
        [--noconstraints, ignore constraints]
        [--nojoined, don't autodetect joined table inheritance]
        [--noinflect, don't try to convert tables names to singular form]
        [--noclasses, don't generate classes, only tables]
        [--nocomments, don't render column comments]
        [--outfile, file to write output to (default: stdout)]

        examples: 
            * modelgen --source database --url mysql+mysqlconnector://user:password@localhost/dbname --noviews
            * modelgen --source database --url postgresql+psycopg2:://user:password@localhost/dbname --tables table1,table2
            * modelgen --source database --url sqlite:///dbname.db

'''

def main():
    parser = argparse.ArgumentParser(usage=msg())
    
    parser.add_argument('--source', type=str, choices=['yaml', 'database'])
    parser.add_argument("--init", type=str)
    parser.add_argument("--createmodel", action="store_true")
    parser.add_argument("--alembic", action="store_true")
    parser.add_argument("-f", "--file")

    parser.add_argument('-u', '--url', nargs='?')
    parser.add_argument('--version', action='store_true')
    parser.add_argument('--schema')
    parser.add_argument('--tables')
    parser.add_argument('--noviews', action='store_true')
    parser.add_argument('--noindexes', action='store_true')
    parser.add_argument('--noconstraints', action='store_true')
    parser.add_argument('--nojoined', action='store_true')
    parser.add_argument('--noinflect', action='store_true')
    parser.add_argument('--noclasses', action='store_true')
    parser.add_argument('--nocomments', action='store_true')
    parser.add_argument('--outfile')
    args = parser.parse_args()

    if args.source == 'yaml':
        if args.createmodel:
            if not args.file:
                print('You must supply a file path\n', file=sys.stderr)
                parser.print_help()
                return
        ModelGenerator(args.init, args.createmodel, args.file, args.alembic)
    elif args.source == 'database':
        if args.version:
            version = pkg_resources.get_distribution('sqlacodegen').parsed_version
            print(version.public)
            return

        db_uri = environ.get('DATABASE_URI', args.url)
        if not db_uri:
            print('You must supply a url\n Either set DATABASE_URI in the environment or pass --url', file=sys.stderr)
            parser.print_help()
            return
        # Use reflection to fill in the metadata
        engine = create_engine(db_uri)
        metadata = MetaData(engine)
        tables = args.tables.split(',') if args.tables else None
        metadata.reflect(engine, args.schema, not args.noviews, tables)

        # Write the generated model code to the specified file or standard output
        outfile_path_args = args.outfile.split('/')
        outfile_path = '/'.join(outfile_path_args[:-1])
        if len(outfile_path_args) > 1 and not path.exists(outfile_path):
            Path(outfile_path).mkdir(parents=True, exist_ok=False)
        outfile = io.open(args.outfile, 'w', encoding='utf-8') if args.outfile else sys.stdout
        generator = CodeGenerator(metadata, args.noindexes, args.noconstraints, args.nojoined,
                                args.noinflect, args.noclasses, nocomments=args.nocomments)
        generator.render(outfile)
        modelgenrtr = ModelGenerator(alembic=args.alembic)._create_alembic_meta()
    else:
        print('You must supply a source\n', file=sys.stderr)
        parser.print_help()
        return
if __name__ == "__main__":
    main()