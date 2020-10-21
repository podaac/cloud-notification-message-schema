"""
Validate all CNM Sample messages in samples/ against the CNM JSON Schema

Note: date-time format won't be validated unless the following dependency is installed: strict-rfc3339
"""

import os
import json

import jsonschema

schema_file_name = 'cumulus_sns_schema.json'
sample_files_dir = 'samples'

schema = open(schema_file_name,'r').read()
schema = json.loads(schema)

sample_files = [os.path.join(sample_files_dir, file) for file in os.listdir(sample_files_dir)]

for sample_file in sample_files:
    data = open(sample_file).read()
    data = json.loads(data)
    try:
        jsonschema.validate(data, schema, format_checker=jsonschema.FormatChecker())
        print(f'Validated {sample_file}')
    except jsonschema.exceptions.ValidationError as error:
        print(f'Failed to validate {sample_file}. Error: {error.message}')
