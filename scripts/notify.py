import json
import os
import sys
import time

import boto3
import click
from geopy.geocoders import Nominatim

# Create SQS client
sqs = boto3.client('sqs')

BASEDIR = os.path.dirname(os.path.abspath(__file__).replace('scripts/', ''))

TYPE = {
    'opensource': 'OpensourceItem',
    'companies': 'CompanyItem'
}


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
        QueueUrl=os.getenv('SQS_URL_DATA_INGESTION'),
        MessageAttributes={},
        MessageBody=json.dumps(message)
    )


def changed_files_send(changed: str, files: dict):
    for file in files:
        filepath = abspath(BASEDIR, 'awesome', file).strip()

        if os.path.isfile(filepath):
            filename = os.path.basename(filepath)
            type_key = os.path.dirname(filepath).split('/')[-2]
            type = TYPE[type_key]

            notify(
                changed=changed,
                type=type,
                filename=filename,
                data=json_validate(filepath)
            )
            time.sleep(5)


@click.command()
@click.option('--massive', default=False, is_flag=True, help='Massive load')
@click.option('--changed-files', default='{}', help='JSON of tj-actions/changed-files action output')
def main(massive, changed_files):
    if massive:
        changed_files_send(changed='added', files=[
                           f'opensource/data/{i}' for i in os.listdir('awesome/opensource/data')])
        changed_files_send(changed='added', files=[
                           f'companies/data/{i}' for i in os.listdir('awesome/companies/data')])
        return

    changed_files = json.loads(changed_files)
    print(f'Changed files raw data: \n{changed_files}')

    added_files = changed_files.get('added_files', '').split('awesome/')
    changed_files_send(changed='added', files=added_files)
    print(f'Added: \n{added_files}')

    deleted_files = changed_files.get('deleted_files', '').split('awesome/')
    changed_files_send(changed='deleted', files=deleted_files)
    print(f'Deleted: \n{deleted_files}')

    modified_files = changed_files.get('modified_files', '').split('awesome/')
    changed_files_send(changed='modified', files=modified_files)
    print(f'Modified: \n{modified_files}')


if __name__ == '__main__':
    sys.exit(main())
