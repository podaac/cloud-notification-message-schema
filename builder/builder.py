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
        print('CMR Query object created')

    def find_executable(self, executable, path=None):
        """Tries to find 'executable' in the directories listed in 'path'.

        A string listing directories separated by 'os.pathsep'; defaults to
        os.environ['PATH'].  Returns the complete filename or None if not found.
        """
        if path is None:
            path = os.environ.get('PATH', os.defpath)

        paths = path.split(os.pathsep)
        base, ext = os.path.splitext(executable)

        if (sys.platform == 'win32' or os.name == 'os2') and (ext != '.exe'):
            executable = executable + '.exe'

        if not os.path.isfile(executable):
            for p in paths:
                f = os.path.join(p, executable)
                if os.path.isfile(f):
                    # the file exists, we have a shot at spawn working
                    return f
            return None
        else:
            return executable

    def clean_up(self, project_dir:str):
        target_dir = os.path.join(project_dir, 'target')
        build_dir = os.path.join(project_dir, 'build')
        os.system('rm -Rf {}'.format(target_dir))
        os.system('rm -Rf {}'.format(build_dir))

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
    f = open(os.path.join(project_dir,'version.txt'), "w")
    f.write(release_version)
    f.close()
    logger.info('Version.txt created')



if __name__ == '__main__':
    builder_obj:object = builder()
    process()
