import json
import os
import sys

import fastjsonschema

BASEDIR = os.path.dirname(os.path.abspath(__file__).replace('scripts/', ''))


def abspath(*args, os_path=True, separator='/'):
    path = separator.join(args)
    if os_path is True:
        from pathlib import Path

        return str(Path(path))
    return path


class Checker():
    def __init__(self) -> None:
        self.jsonschema = self.define_jsonschema()

    def json_validate(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(filename=filename)

        with open(filename) as fh:
            content = json.load(fh)

        return self.jsonschema(content)

    def validate(self, dirpath: str):
        print(f'Check: {dirpath.split("/")[-2].title()}')
        loaded = []
        for project in os.listdir(dirpath):
            filename = abspath(dirpath, project)

            if not os.path.isfile(filename):
                print(f"Skip render '{filename}'")
                continue

            if not project.endswith('.json'):
                raise Exception(f'File {project} is not json')

            item = (project.replace('.json', ''), filename)

            loaded.append(item)

        loaded = sorted(loaded, key=lambda tup: tup[0])

        values = []
        for name, filename in loaded:
            print(f'\tFile: {name}.json')
            values.append(self.json_validate(filename))

        return values

    def jsonschema(self):
        raise NotImplementedError('jsonschema not implemented')


class OpensourceChecker(Checker):
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

    def __init__(self) -> None:
        super().__init__()

    def define_jsonschema(self):
        return fastjsonschema.compile(
            definition={
                '$schema': 'https://json-schema.org/draft/2019-09/schema',
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'repository_platform': {'type': 'string', 'enum': self.ALLOWED_REPOSITORY_PLATFORM},
                    'repository_url': {'type': 'string', 'format': 'uri'},
                    'site_url': {'type': 'string', 'format': 'uri'},
                    'description': {'type': 'string', 'minLength': 5, 'maxLength': 508},
                    'type': {'type': 'string', 'enum': self.ALLOWED_TYPE},
                    'license': {'type': 'string', 'enum': self.ALLOWED_LICENSES},
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


class CompaniesChecker(Checker):
    ALLOWED_TYPE = [
        'B2B',
        'B2C',
        'C2C',
        'D2C',
        'Nonprofit',
        'Other',
    ]

    ALLOWED_MARKET = [
        'Housing',
        'Travel',
        'Aeropsace',
        'Health',
        'Food',
        'Automotive',
        'Fintech',
        'Energy',
        'AI',
        'Recruiting',
        'Blockchain',
        'Biotech',
        'Ecommerce',
        'Software',
        'Hardware',
        'Service',
        'Insurance',
        'Entertainment',
        'Education',
        'Retail',
        'Transport',
        'Security',
        'Agriculture',
        'Manufacturing',
        'Banking',
        'Gaming',
        'Sports',
        'Fashion',
        'Environment',
        'Building',
        'Other',
        # TODO: in progress (crete issues if missing your market)
    ]

    def __init__(self) -> None:
        super().__init__()

    def define_jsonschema(self):
        return fastjsonschema.compile(
            definition={
                '$schema': 'https://json-schema.org/draft/2019-09/schema',
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'repository_organization_url': {'type': 'string', 'format': 'uri'},
                    'site_url': {'type': 'string', 'format': 'uri'},
                    'description': {'type': 'string', 'minLength': 5, 'maxLength': 508},
                    'type': {'type': 'string', 'enum': self.ALLOWED_TYPE},
                    'market': {'type': 'string', 'enum': self.ALLOWED_MARKET},
                    'address': {'type': 'string'},
                    'foundation_year': {
                        'type': 'string',
                        'pattern': '^[2][0-0][1-2][0-9]$'
                    },
                    'tech_stack': {
                        'type': 'array',
                        'minItems': 1,
                        'maxItems': 20,
                        'uniqueItems': True,
                        'items': {
                            'type': 'string',
                            'maxLength': 24
                        }
                    },
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
                    'site_url',
                    'type',
                    'market',
                    'tags',
                ],
                'additionalProperties': False
            }
        )


class CommunitiesChecker(Checker):
    ALLOWED_TYPE = [
        'Blog',
        'Channel',
        'Newsletter',
        'Event',
        'Podcast',
    ]

    ALLOWED_PLATFORM = [
        'Telegram',
        'Discord',
        'Slack',
        'Reddit',
        'Website',
        'Email',
        'Location',
        'Youtube',
        'Twitch',
        'Other',
    ]

    ALLOWED_EVENTS_TYPE = [
        'Talk',
        'Meetup',
        'Webinar',
        'Conference',
        'Workshop',
        'Hackathon',
        'Chat',
        'Article',
        'Video',
        'Audio',
        'Other',
        'Coworking trips'
    ]

    def __init__(self) -> None:
        super().__init__()

    def define_jsonschema(self):
        return fastjsonschema.compile(
            definition={
                '$schema': 'https://json-schema.org/draft/2019-09/schema',
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'url': {'type': 'string', 'format': 'uri'},
                    'description': {'type': 'string', 'minLength': 5, 'maxLength': 508},
                    'type': {'type': 'string', 'enum': self.ALLOWED_TYPE},
                    'platform': {'type': 'string', 'enum': self.ALLOWED_PLATFORM},
                    'tags': {
                        'type': 'array',
                        'minItems': 1,
                        'maxItems': 20,
                        'uniqueItems': True,
                        'items': {
                            'type': 'string',
                            'maxLength': 24
                        }
                    },
                    'events_type': {
                        'type': 'array',
                        'minItems': 1,
                        'uniqueItems': True,
                        'items': {
                            'type': 'string',
                            'enum': self.ALLOWED_EVENTS_TYPE
                        }
                    },
                },
                'required': [
                    'name',
                    'url',
                    'type',
                    'platform',
                    'tags',
                    'events_type'
                ],
                'additionalProperties': False
            }
        )


class DigitalNomadsChecker(Checker):
    ALLOWED_MOVE = [
        'Airplane',
        'Ship',
        'Walk',
        'Car',
        'Bike',
        'Taxi',
        'Bus',
        'Train',
        'Tram',
        'Public transports',
        'Motorbike',
        'Ferry',
        'VAN',
        'Other',
    ]

    ALLOWED_DOCUMENTS = [
        'CI',
        'Passport',
        'Visa',
        'Other',
    ]

    ALLOWED_INTERNET_ROAMING = [
        'Available',
        'Not required',  # Just for Italy
        'Local SIM required',
        'Not yet available',  # For countries like Albania or Türkiye who requested to join EU
    ]

    def __init__(self) -> None:
        super().__init__()

    def define_jsonschema(self):
        return fastjsonschema.compile(
            definition={
                '$schema': 'https://json-schema.org/draft/2019-09/schema',
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'state_name': {'type': 'string', 'minLength': 2, 'maxLength': 40},
                    'description': {'type': 'string', 'minLength': 5, 'maxLength': 508},
                    'required_documents': {
                        'type': 'array',
                        'minItems': 1,
                        'items': {
                            'type': 'string',
                            'enum': self.ALLOWED_DOCUMENTS
                        }
                    },
                    'internet_roaming': {'type': 'string', 'enum': self.ALLOWED_INTERNET_ROAMING},
                    'daily_average_cost': {'type': 'number', 'min': 1},
                    'tags': {
                        'type': 'array',
                        'minItems': 1,
                        'maxItems': 20,
                        'uniqueItems': True,
                        'items': {
                            'type': 'string',
                            'maxLength': 24
                        }
                    },
                    'how_to_arrive': {
                        'type': 'array',
                        'minItems': 1,
                        'uniqueItems': True,
                        'items': {
                            'type': 'string',
                            'enum': self.ALLOWED_MOVE
                        }
                    },
                    'how_to_move': {
                        'type': 'array',
                        'minItems': 1,
                        'uniqueItems': True,
                        'items': {
                            'type': 'string',
                            'enum': self.ALLOWED_MOVE
                        }
                    },
                    'resources': {
                        'type': 'array',
                        'minItems': 1,
                        'uniqueItems': True,
                        'items': {
                            'type': 'string',
                            'format': 'uri'
                        }
                    },
                    'coworking': {
                        'type': 'array',
                        'minItems': 1,
                        'uniqueItems': True,
                        'items': {
                            'type': 'string',
                            'format': 'uri'
                        }
                    },
                },
                'required': [
                    'name',
                    'state_name',
                    'required_documents',
                    'tags',
                    'internet_roaming',
                    'coworking',
                    'resources',
                    'how_to_move'
                ],
                'additionalProperties': False
            }
        )


def main():
    OpensourceChecker().validate(abspath(BASEDIR, 'awesome', 'opensource', 'data'))
    CompaniesChecker().validate(abspath(BASEDIR, 'awesome', 'companies', 'data'))
    CommunitiesChecker().validate(abspath(BASEDIR, 'awesome', 'communities', 'data'))
    DigitalNomadsChecker().validate(
        abspath(BASEDIR, 'awesome', 'digital-nomads', 'data'))


if __name__ == '__main__':
    sys.exit(main())
