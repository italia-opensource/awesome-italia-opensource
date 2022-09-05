import json
import os
import sys

import click
import fastjsonschema
from snakemd import Document
from snakemd.generator import InlineText

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
    'tool'
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
    'Fair',
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


def build(data):
    def _header(doc, data):
        doc.add_header('Italia Opensource')
        doc.add_paragraph(
            f"<img src='https://img.shields.io/badge/projects-{len(data)}-green'>")

        doc.add_paragraph(
            'Italia Opensource is a list of open source projects created by Italian companies or developers.')
        doc.add_paragraph(
            'The repository intends to give visibility to open source projects and stimulate the community to contribute to growing the ecosystem.')

        doc.add_paragraph(
            '[ATTENTION] Please read the contribution guidelines before opening a pull request or contributing to this repository')

    def _projects(doc, data):
        doc.add_header('Open source projects', level=3)
        table_content_project = []
        for item in data:
            description = item.get('description', '')
            if len(description) > 59:
                description = description[0:60] + ' [..]'
            table_content_project.append([
                InlineText(item['name'].title(), url=item.get('site_url')),
                InlineText(item['repository_platform'].title(),
                           url=item.get('repository_url')),
                item['license'],
                ', '.join(item['tags']),
                description
            ])

        doc.add_table(
            ['Name', 'Repository', 'License', 'Stack', 'Description'],
            table_content_project
        )

    def _contributors(doc):
        doc.add_header('Contributors', level=3)

        doc.add_paragraph("""
                <a href="https://github.com/italia-opensource/awesome-italia-opensource/graphs/contributors">
                    <img src="https://contrib.rocks/image?repo=italia-opensource/awesome-italia-opensource" />
                </a>
                Made with [contrib.rocks](https://contrib.rocks).
            """)

    doc = Document('README')

    _header(doc, data)
    _projects(doc, data)
    _contributors(doc)

    doc.output_page()


@click.command()
@click.option('--render', default=False, help='Make data render', is_flag=True)
@click.option('--output', default=False, help='Make data output', is_flag=True)
def main(render, output):
    data = os.listdir(abspath(os.path.dirname(
        os.path.abspath(__file__)), 'data'))

    loaded = []
    for project in data:
        if not project.endswith('.json'):
            raise Exception(f'File {project} is not json')
        item = (project.replace('.json', ''), abspath(
            os.path.dirname(os.path.abspath(__file__)), 'data', project))
        loaded.append(item)

    loaded = sorted(loaded, key=lambda tup: tup[0])
    parsed = check(loaded)

    if render:
        build(parsed)

    if output:
        with open('website/src/data/outputs.json', 'w+') as file_output:
            file_output.write(json.dumps({'data': parsed}))


if __name__ == '__main__':
    sys.exit(main())
