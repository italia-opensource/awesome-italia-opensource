import json
import os
import sys

import boto3
import click
from geopy.geocoders import Nominatim

# Create SQS client
sqs = boto3.client('sqs')

BASEDIR = os.path.dirname(os.path.abspath(__file__).replace('scripts/', ''))


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
        return json.load(fh)


def notify(changed: str, type: str, filename: str, data: dict):
    def _process_address(address: str):
        location = Nominatim(user_agent='myGeocoder').geocode(address)
        return {
            'type': 'Point',
            'coordinates': [location.latitude, location.longitude]
        }

    if address := data.get('address'):
        data['geometry'] = _process_address(address)

    message = {
        'filename': filename,
        'changed': changed,
        'type': type,
        'payload': data
    }

    print(message)

    sqs.send_message(
        QueueUrl=os.getenv('SQS_URL_DATA_INGESTION',
                           'https://sqs.eu-central-1.amazonaws.com/772883009446/data-ingestion-772883009446'),
        MessageAttributes={},
        MessageBody=json.dumps(message)
    )


def changed_files_send(changed: str, files: dict):
    for file in files:
        filename = abspath(BASEDIR, 'awesome', file).strip()
        type = os.path.dirname(filename).split('/')[-1]

        if os.path.isfile(filename):
            notify(
                changed=changed,
                type=type,
                filename=filename,
                data=json_validate(filename)
            )


@click.command()
@click.option('--changed-files', default='', help='JSON of tj-actions/changed-files action output')
def main(changed_files):
    changed_files = json.loads(changed_files)

    added_files = changed_files['added_files'].split('awesome/')
    changed_files_send(changed='added', files=added_files)

    deleted_files = changed_files['deleted_files'].split('awesome/')
    changed_files_send(changed='deleted', files=deleted_files)

    modified_files = changed_files['modified_files'].split('awesome/')
    changed_files_send(changed='modified', files=modified_files)

    renamed_files = changed_files['renamed_files'].split('awesome/')
    changed_files_send(changed='renamed', files=renamed_files)


if __name__ == '__main__':
    sys.exit(main())
