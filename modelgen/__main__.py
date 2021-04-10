import argparse
from pathlib import Path
from os import path, getcwd
from shutil import copyfile, copytree
from modelgen import __file__, create_model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--init", type=str, help="Initialize sqlalchemygen project")
    parser.add_argument("-c","--create_model", type=str, help="Create sqlalchemy model")
    parser.add_argument("-a", "--alembic", action="store_true", help="If specified, alembic support will be set to True")
    parser.add_argument("-f", "--file", help="path/to/the/template_file.yaml")

    args = parser.parse_args()
    # if args.init and not args.file:
    #     raise TypeError('Please specify folder path. Ex: modelgen init -f ./example')
    # if args.create_model and not args.file:
    #     raise TypeError('Please specify YAML file path. Ex: modelgen create_model -f ./example.yaml')
    try:
        if args.init:
            if path.isabs(args.init):
                f_path = path.join(args.init)
            else:
                f_path = path.join(getcwd(), args.init)
            alembic_path = path.join('/',*(__file__.split('/')[:-1]),'alembic')
            module_src_path = alembic_path
            ini_src_path = path.join('/',*(__file__.split('/')[:-1]),'alembic.ini')
            templates_src_path = path.join('/',*(__file__.split('/')[:-1]),'templates')
            
            templates_dst_path = path.join(args.init, 'templates')
            Path(templates_dst_path).mkdir(parents=True, exist_ok=False)
            Path(path.join(alembic_path,'versions')).mkdir(parents=True, exist_ok=False)

            copytree(module_src_path, path.join(f_path, 'alembic'))
            copyfile(ini_src_path, path.join(f_path, 'alembic.ini'))
            copyfile((path.join(templates_src_path, 'example.yaml')), path.join(templates_dst_path, 'example.yaml'))
        
        elif args.create_model:
            filepath = path.join(args.create_model)
            datasource = filepath.split('.yaml')[0].split('/')[-1]
            create_model(datasource=datasource, filepath=filepath)
            if args.alembic:
                create_model(datasource=datasource, alembic=True, filepath=filepath)
    except FileExistsError as e:
        raise FileExistsError("Folder exists. Please specify a new folder name") from FileExistsError
    

if __name__ == "__main__":
    main()