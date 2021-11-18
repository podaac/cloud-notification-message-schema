import click
from typing import DefaultDict, Dict, List
import os
import sys
import logging
import json
import re
import sys


@click.command()
@click.option('-f', '--file-name',
              help='file containing version', required=True, type=str)
@click.option('-v', '--version', 
              help='new version', required=True)

def update_version(file_name, version:str):
    with open(file_name) as f:
        json_schema:Dict = json.load(f)

    versions:List = json_schema['properties']['version']['enum']
    release_version:str = versions[len(versions) -1]
    versions[len(versions) -1] = version
    print(versions)

    with open(file_name, 'w') as f:
        json.dump(json_schema, f, indent=2)

if __name__ == '__main__':
    update_version()