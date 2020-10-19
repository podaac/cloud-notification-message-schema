import click
from typing import Dict, List
import os
import sys
import logging
import json

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'
SHORT_TIMESTAMP_FORMAT = '%Y-%m-%d'

logger:object = logging.getLogger('Artifact Builder ===>')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
class builder:
    def __init__(self, *args, **kwargs) -> None:
        print('Builder started')

@click.command()
@click.option('-d', '--project-dir',
              help='Project working directory', required=True, type=str)
def process(project_dir:str) -> None:
    '''
        this entire process is meant to run either through command line or inside a docker container
        which contains java 8, python 3 , pipe and zip utilities.
    '''
    logger.info('project directory:{}'.format('project_dir'))
    builder_o = builder()
    os.system('pwd')
    os.chdir(project_dir)
    os.system('pwd')
    with open(os.path.join(project_dir, 'cumulus_sns_schema.json')) as f:
        json_schema:Dict = json.load(f)
    versions:List = json_schema['properties']['version']['enum']
    release_version:str = versions[len(versions) -1]


    # create version.txt
    logger.info('Opening and writing version.txt with release version: '.format(release_version))
    version_file:str = os.path.join(project_dir,'version.txt')
    f = open(version_file, "w")
    f.write(release_version)
    f.close()
    os.system('chmod 777 {}'.format(version_file))
    logger.info('Version.txt created')



if __name__ == '__main__':
    builder_obj:object = builder()
    process()
