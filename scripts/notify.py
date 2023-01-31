import json
import os
import sys

import boto3
import click
import fastjsonschema

# Create SQS client
sqs = boto3.client('sqs')


ALLOWED_TYPE = [
    'app',
    'community',
    'faas',
    'library',
    'learning',
    'paas',
    'package',
    'saas',
    'scripts',
    'tool',
    'language',
    'framework'
]

ALLOWED_REPOSITORY_PLATFORM = [
    'github',
    'gitlab',
    'bitbucket',
    # TODO: add other platform
]

# List from https://opensource.org/licenses/alphabetical
ALLOWED_LICENSES = [
    'Undefined',
    '0BSD',
    'BSD-1-Clause',
    'BSD-2-Clause',
    'BSD-3-Clause',
    'AFL-3.0',
    'APL-1.0',
    'Apache-1.1',
    'Apache-2.0',
    'APSL-2.0',
    'Artistic-1.0',
    'Artistic-2.0',
    'AAL',
    'BSL-1.0',
    '3-clause BSD License',
    '2-clause BSD License',
    '1-clause BSD License',
    '0-clause BSD license',
    'BSD-3-Clause-LBNL',
    'BSD-2-Clause-Patent',
    'Creative Commons',
    'CERN Open Hardware Licence Version 2 - Permissive',
    'CERN Open Hardware Licence Version 2 - Weakly Reciprocal',
    'CERN Open Hardware Licence Version 2 - Strongly Reciprocal',
    'CECILL-2.1',
    'CDDL-1.0',
    'CPAL-1.0',
    'CPL-1.0',
    'CATOSL-1.1',
    'Coopyleft',
    'CopyFair',
    'CSL',
    'CAL-1.0',
    'EPL-1.0',
    'EPL-2.0',
    'eCos-2.0',
    'ECL-1.0',
    'ECL-2.0',
    'EFL-1.0',
    'EFL-2.0',
    'Entessa',
    'EUDatagrid',
    'EUPL-1.2',
    'FairSource',
    'Frameworx-1.0',
    '0BSD',
    'AGPL-3.0',
    'GPL-2.0',
    'GPL-3.0',
    'LGPL-2.1',
    'LGPL-3.0',
    'HPND',
    'IPL-1.0',
    'IPA',
    'ISC',
    'Jam',
    'LPPL-1.3c',
    'BSD-3-Clause-LBNL',
    'LiLiQ-P',
    'LiLiQ-R',
    'LiLiQ-R+',
    'LPL-1.0',
    'LPL-1.02',
    'MS-PL',
    'MS-RL',
    'MirOS',
    'MIT',
    'MIT-0',
    'Motosoto',
    'MPL-1.0',
    'MPL-1.1',
    'MPL-2.0',
    'MulanPSL',
    'Multics',
    'NASA-1.3',
    'Naumen',
    'NGPL',
    'NPOSL-3.0',
    'NTP',
    'OCLC-2.0',
    'OGTSL',
    'OSL-1.0',
    'OSL-2.1',
    'OSL-3.0',
    'OLDAP-2.8',
    'QPL-1.0',
    'RPSL-1.0',
    'RPL-1.1',
    'RPL-1.5',
    'RSCPL',
    'OFL-1.1',
    'PPL',
    'SimPL-2.0',
    'Sleepycat',
    'SPL-1.0',
    'Watcom-1.0',
    'UPL',
    'NCSA',
    'Upstream Compatibility License v1.0',
    'Unicode Data Files and Software License',
    'Unlicense',
    'VSL-1.0',
    'W3C',
    'WXwindows',
    'Xnet',
    '0BSD',
    'ZPL-2.0',
    'ZPL-2.1',
    'Zlib'
]

JSONSCHEME_COMPILE = fastjsonschema.compile(
    definition={
        '$schema': 'https://json-schema.org/draft/2019-09/schema',
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'repository_platform': {'type': 'string', 'enum': ALLOWED_REPOSITORY_PLATFORM},
            'repository_url': {'type': 'string', 'format': 'uri'},
            'site_url': {'type': 'string', 'format': 'uri'},
            'description': {'type': 'string', 'minLength': 5, 'maxLength': 254},
            'type': {'type': 'string', 'enum': ALLOWED_TYPE},
            'license': {'type': 'string', 'enum': ALLOWED_LICENSES},
            'tags': {
                'type': 'array',
                'minItems': 1,
                'maxItems': 20,
                'uniqueItems': True,
                'items': {
                    'type': 'string',
                    'maxLength': 24
                }
            }
        },
        'required': [
            'name',
            'repository_platform',
            'repository_url',
            'type',
            'license',
            'tags',
        ],
        'additionalProperties': False
    }
)


def abspath(*args, os_path=True, separator='/'):
    path = separator.join(args)
    if os_path is True:
        from pathlib import Path

        return str(Path(path))
    return path


def json_validate(filename: str):
    if not os.path.exists(filename):
        raise FileNotFoundError(filename=filename)

    with open(filename) as fh:
        content = json.load(fh)

    return JSONSCHEME_COMPILE(content)


def check(loaded: list):
    values = []
    for name, filename in loaded:
        print(f'Check: {name}')
        values.append(json_validate(filename))

    return values


def send_sqs_message(changed: str, type: str, filename: str, data: dict):
    message = {
        'metadata': {
            'filename': filename,
            'changed': changed,
            'type': type,
        },
        'payload': data
    }
    print(message)

    sqs.send_message(
        QueueUrl=os.getenv('SQS_URL_DATA_INGESTION'),
        MessageAttributes={},
        MessageBody=json.dumps(message)
    )


def changed_files_send(changed: str, files: dict):
    for file in files:
        filename = abspath(os.path.dirname(
            os.path.abspath(__file__)), 'data', file).strip()
        type = os.path.dirname(filename).split('/')[-1]
        if os.path.isfile(filename):
            send_sqs_message(changed=changed, type=type,
                             filename=filename, data=json_validate(filename))


@click.command()
@click.option('--changed-files', default='', help='JSON of tj-actions/changed-files action output')
def main(changed_files):
    changed_files = json.loads(changed_files)

    added_files = changed_files['added_files'].split('data/')
    print(added_files)
    changed_files_send(changed='added', files=added_files)

#   deleted_files = changed_files["deleted_files"].split("data/")
#   print(deleted_files)
#   changed_files_send(changed='deleted', files=deleted_files)

#   modified_files = changed_files["modified_files"].split("data/")
#   print(modified_files)
#   changed_files_send(changed='modified', files=modified_files)

#   renamed_files = changed_files["renamed_files"].split("data/")
#   print(renamed_files)
#   changed_files_send(changed='renamed', files=renamed_files)


if __name__ == '__main__':
    sys.exit(main())
