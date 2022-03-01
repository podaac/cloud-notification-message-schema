"""
Validate all CNM Sample messages in samples/ against the CNM JSON Schema

Note: date-time format won't be validated unless the following dependency is installed: strict-rfc3339
"""

import os
import json

import jsonschema

from cloudnotificationmessage import CloudNotificationMessage

schema_file_name = 'cumulus_sns_schema.json'
sample_files_dir = 'samples'

schema = open(schema_file_name, 'r').read()
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

# tests for cloud_notification_message.py using OISSS L4 values
cnm_test_provider = "NASA/JPL/PO.DAAC"
cnm_test_dataset = "OISSS_L4_multimission_monthly_v1"
cnm_test_data_version = "1.0"
cnm_test_files = list()
cnm_test_granule_data = dict(
    type="data",
    uri="s3://podaac-dev-cumulus-test-input-v2/OISSS_L4_multimission_monthly_v1/OISSS_L4_multimission_global_monthly_v1.0_2013-08.nc",
    size=16603204,
    checksum='md5'
)
cnm_test_granule_checksum = dict(
    type="metadata",
    uri="s3://podaac-dev-cumulus-test-input-v2/OISSS_L4_multimission_monthly_v1/OISSS_L4_multimission_global_monthly_v1.0_2013-08.nc.md5",
    size=86
)
cnm_test_files.append(cnm_test_granule_data)
cnm_test_files.append(cnm_test_granule_checksum)
test_cnm = CloudNotificationMessage(cnm_test_dataset, cnm_test_files, cnm_test_data_version, cnm_test_provider)

try:
    data = json.loads(test_cnm.get_json())
    jsonschema.validate(data, schema, format_checker=jsonschema.FormatChecker())
    print(f'Validated {cnm_test_dataset}')
except jsonschema.exceptions.ValidationError as error:
    print(f'Failed to validate {cnm_test_dataset}. Error: {error.message}')