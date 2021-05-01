import argparse
from pathlib import Path
from os import path, getcwd, environ
from shutil import copyfile, copytree

import io
import sys
import pkg_resources

from alembic.config import main as alembic_main, CommandLine, Config
from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData
from modelgen import __file__
from modelgen import ModelGenerator
from sqlacodegen.codegen import CodeGenerator

def main():
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers(dest='command')
    init_parser = subparsers.add_parser('init', help='initialize')
    init_parser.add_argument('-d','--dir', nargs=1, required=True, 
                             help='Directory where modelgen needs to be initialized')

    createmodel_parser = subparsers.add_parser('createmodel', help='create model')
    createmodel_parser.add_argument('-s','--source', choices=['yaml', 'database'], 
                                    required=True, 
                                    help='Specify data source to create sqlalchemy model \
                                        code from. If `yaml` is specified,\
                                        sqlalchemy code is generated from yaml file.\
                                        If `database` is specified, sqlalchemy is generated \
                                        from database url specified.')
    createmodel_parser.add_argument('-p','--path',nargs=1, 
                                    help='yaml filepath if data source is `yaml`,\
                                        or sqlalchemy url if data source is `database`')
    createmodel_parser.add_argument('--version', action='store_true')
    createmodel_parser.add_argument('--schema', help='load tables from an alternate schema')
    createmodel_parser.add_argument('--tables', help='tables to process (comma-separated, default: all)')
    createmodel_parser.add_argument('--noviews', action='store_true', 
                                    help='ignore views')
    createmodel_parser.add_argument('--noindexes', action='store_true', 
                                    help='ignore indexes')
    createmodel_parser.add_argument('--noconstraints', action='store_true', 
                                    help='ignore constraints')
    createmodel_parser.add_argument('--nojoined', action='store_true', 
                                    help='don\'t autodetect joined table inheritance')
    createmodel_parser.add_argument('--noinflect', action='store_true', 
                                    help='don\'t try to convert tables names to singular form')
    createmodel_parser.add_argument('--noclasses', action='store_true', 
                                    help='don\'t generate classes, only tables')
    createmodel_parser.add_argument('--nocomments', action='store_true', 
                                    help='don\'t render column comments')
    createmodel_parser.add_argument('--outfile', help='file to write output to')
    createmodel_parser.add_argument('-a',"--alembic", action="store_true", default=False, 
                                    help='If specified, alembic support will be \
                                        set to True (default: False)')

    alembic_parser = subparsers.add_parser('migrate')
    alembic_parser.add_argument('-p','--path',nargs=1, 
                                    help='sqlalchemy url of the database')

    args, unknown = parser.parse_known_args()
    
    if args.command == 'init':
        ModelGenerator(init=args.dir[0])
    elif args.command == 'createmodel':
        if args.source == 'yaml':
            ModelGenerator(createmodel=True, file=args.path[0], alembic=args.alembic)
        elif args.source == 'database':
            if args.version:
                version = pkg_resources.get_distribution('sqlacodegen').parsed_version
                return
            if not args.outfile:
                print('You must supply a outfile path\n', file=sys.stderr)
                parser.print_help()
                return
            db_uri = environ.get('DATABASE_URI') or args.path[0]
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
            if args.alembic:
                modelgenrtr = ModelGenerator(alembic=args.alembic)._create_alembic_meta()

    elif args.command == 'migrate':
        db_uri = environ.get('DATABASE_URI') or args.path[0]
        environ['DATABASE_URI'] = db_uri
        alembic_main(unknown)
    else:
        print('You must supply a source\n', file=sys.stderr)
        parser.print_help()
        return

if __name__ == "__main__":
    main()