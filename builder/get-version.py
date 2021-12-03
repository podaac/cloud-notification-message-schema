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

def get_version(file_name):
    with open(file_name) as f:
        json_schema:Dict = json.load(f)

    versions:List = json_schema['properties']['version']['enum']
    return print(versions[len(versions) -1])

if __name__ == '__main__':
    get_version()