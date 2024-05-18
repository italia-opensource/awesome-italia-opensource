import argparse
import json
import os
import sys
import urllib
from datetime import datetime
from random import randint
from time import sleep

# Set the base directory to the root of the project
_BASEDIR = os.path.dirname(os.path.abspath(__file__))
if _BASEDIR.endswith('scripts'):
    _BASEDIR = _BASEDIR.split('/scripts')[0]
sys.path.insert(1, _BASEDIR)  # noqa

_TIMESTAMP_OBJ = datetime.now()
_TIMESTAMP = str(_TIMESTAMP_OBJ.strftime('%Y/%m/%d %H:%M'))
_ANALYTICS_DIR = f'{_BASEDIR}/analytics'


def get_database_analytitcs_filename():
    return f'{_ANALYTICS_DIR}/database.json'


def get_languages_analytics_filename():
    return f'{_ANALYTICS_DIR}/languages.json'


def get_analytics_mounth_filepath():
    analytics_mounth_basepath = f'{
        _ANALYTICS_DIR}/{_TIMESTAMP_OBJ.year}/{_TIMESTAMP_OBJ.month}'
    if not os.path.exists(analytics_mounth_basepath):
        os.makedirs(analytics_mounth_basepath)
    return analytics_mounth_basepath


def get_awesomelist_database_filename(list_name: str):
    filepath = f'{_BASEDIR}/awesome/{list_name}/'
    if not os.path.dirname(filepath):
        raise Exception(f"Directory {filepath} does not exist")

    return f'{filepath}/database.json'


def get_raw_data_filepath(list_name: str):
    filepath = f'{_BASEDIR}/awesome/{list_name}/data/'
    if not os.path.dirname(filepath):
        raise Exception(f"Directory {filepath} does not exist")
    return filepath


def github_convert_to_percentage(dictionary):
    print('Converting languages to distribution percentage')
    total_sum = sum(dictionary.values())

    if total_sum == 0:
        # Avoid division by zero
        return {key: 0 for key in dictionary}

    percentage_dict = {
        key: round((value / total_sum) * 100, 2)
        for key, value in dictionary.items()
    }
    return percentage_dict


def github_split_repo_url(repository_url):
    repo = repository_url.split('/')
    owner = repo[-2]
    name = repo[-1]
    return owner, name


def github_get_repo_languages(owner: str, repo: str, token: str):
    """ Get the languages for a repository
    :param owner: The owner of the repository
    :param repo: The name of the repository
    :param token: The GitHub token to use for authentication
    :param languages_all_projects: A dictionary with the languages of all the projects

    :return: A dictionary of languages and bytes of code
    """

    print(f'Getting repo languages for {owner}/{repo}')

    url = f'https://api.github.com/repos/{owner}/{repo}/languages'
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'Mozilla/5.0',
        'Authorization': f'Bearer {token}'
    }
    languages = {}
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            data = response.read().decode('utf-8')
            try:
                languages = json.loads(data)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f'Error decoding JSON: {e}')
    except urllib.error.HTTPError as e:
        raise urllib.error.HTTPError(f'Error fetching data: {e}')

    return languages


def github_get_repo_metadata(owner: str, repo: str, token: str, languages: dict):
    """ Get the metadata for a repository

    example:
    {
        "id": 41881900,
        "node_id": "MDEwOlJlcG9zaXRvcnk0MTg4MTkwMA==",
        "name": "vscode",
        "full_name": "microsoft/vscode",
        "private": false,
        "owner": {
            "login": "microsoft",
            "id": 6154722,
            "node_id": "MDEyOk9yZ2FuaXphdGlvbjYxNTQ3MjI=",
            "avatar_url": "https://avatars.githubusercontent.com/u/6154722?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/microsoft",
            "html_url": "https://github.com/microsoft",
            "followers_url": "https://api.github.com/users/microsoft/followers",
            "following_url": "https://api.github.com/users/microsoft/following{/other_user}",
            "gists_url": "https://api.github.com/users/microsoft/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/microsoft/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/microsoft/subscriptions",
            "organizations_url": "https://api.github.com/users/microsoft/orgs",
            "repos_url": "https://api.github.com/users/microsoft/repos",
            "events_url": "https://api.github.com/users/microsoft/events{/privacy}",
            "received_events_url": "https://api.github.com/users/microsoft/received_events",
            "type": "Organization",
            "site_admin": false
        },
        "html_url": "https://github.com/microsoft/vscode",
        "description": "Visual Studio Code",
        "fork": false,
        "url": "https://api.github.com/repos/microsoft/vscode",
        "forks_url": "https://api.github.com/repos/microsoft/vscode/forks",
        "keys_url": "https://api.github.com/repos/microsoft/vscode/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/microsoft/vscode/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/microsoft/vscode/teams",
        "hooks_url": "https://api.github.com/repos/microsoft/vscode/hooks",
        "issue_events_url": "https://api.github.com/repos/microsoft/vscode/issues/events{/number}",
        "events_url": "https://api.github.com/repos/microsoft/vscode/events",
        "assignees_url": "https://api.github.com/repos/microsoft/vscode/assignees{/user}",
        "branches_url": "https://api.github.com/repos/microsoft/vscode/branches{/branch}",
        "tags_url": "https://api.github.com/repos/microsoft/vscode/tags",
        "blobs_url": "https://api.github.com/repos/microsoft/vscode/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/microsoft/vscode/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/microsoft/vscode/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/microsoft/vscode/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/microsoft/vscode/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/microsoft/vscode/languages",
        "stargazers_url": "https://api.github.com/repos/microsoft/vscode/stargazers",
        "contributors_url": "https://api.github.com/repos/microsoft/vscode/contributors",
        "subscribers_url": "https://api.github.com/repos/microsoft/vscode/subscribers",
        "subscription_url": "https://api.github.com/repos/microsoft/vscode/subscription",
        "commits_url": "https://api.github.com/repos/microsoft/vscode/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/microsoft/vscode/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/microsoft/vscode/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/microsoft/vscode/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/microsoft/vscode/contents/{+path}",
        "compare_url": "https://api.github.com/repos/microsoft/vscode/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/microsoft/vscode/merges",
        "archive_url": "https://api.github.com/repos/microsoft/vscode/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/microsoft/vscode/downloads",
        "issues_url": "https://api.github.com/repos/microsoft/vscode/issues{/number}",
        "pulls_url": "https://api.github.com/repos/microsoft/vscode/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/microsoft/vscode/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/microsoft/vscode/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/microsoft/vscode/labels{/name}",
        "releases_url": "https://api.github.com/repos/microsoft/vscode/releases{/id}",
        "deployments_url": "https://api.github.com/repos/microsoft/vscode/deployments",
        "created_at": "2015-09-03T20:23:38Z",
        "updated_at": "2023-12-11T17:06:56Z",
        "pushed_at": "2023-12-11T17:28:06Z",
        "git_url": "git://github.com/microsoft/vscode.git",
        "ssh_url": "git@github.com:microsoft/vscode.git",
        "clone_url": "https://github.com/microsoft/vscode.git",
        "svn_url": "https://github.com/microsoft/vscode",
        "homepage": "https://code.visualstudio.com",
        "size": 880829,
        "stargazers_count": 153870,
        "watchers_count": 153870,
        "language": "TypeScript",
        "has_issues": true,
        "has_projects": true,
        "has_downloads": true,
        "has_wiki": true,
        "has_pages": false,
        "has_discussions": false,
        "forks_count": 27699,
        "mirror_url": null,
        "archived": false,
        "disabled": false,
        "open_issues_count": 8231,
        "license": {
            "key": "mit",
            "name": "MIT License",
            "spdx_id": "MIT",
            "url": "https://api.github.com/licenses/mit",
            "node_id": "MDc6TGljZW5zZTEz"
        },
        "allow_forking": true,
        "is_template": false,
        "web_commit_signoff_required": false,
        "topics": [
            "editor",
            "electron",
            "microsoft",
            "typescript",
            "visual-studio-code"
        ],
        "visibility": "public",
        "forks": 27699,
        "open_issues": 8231,
        "watchers": 153870,
        "default_branch": "main",
        "temp_clone_token": null,
        "organization": {
            "login": "microsoft",
            "id": 6154722,
            "node_id": "MDEyOk9yZ2FuaXphdGlvbjYxNTQ3MjI=",
            "avatar_url": "https://avatars.githubusercontent.com/u/6154722?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/microsoft",
            "html_url": "https://github.com/microsoft",
            "followers_url": "https://api.github.com/users/microsoft/followers",
            "following_url": "https://api.github.com/users/microsoft/following{/other_user}",
            "gists_url": "https://api.github.com/users/microsoft/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/microsoft/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/microsoft/subscriptions",
            "organizations_url": "https://api.github.com/users/microsoft/orgs",
            "repos_url": "https://api.github.com/users/microsoft/repos",
            "events_url": "https://api.github.com/users/microsoft/events{/privacy}",
            "received_events_url": "https://api.github.com/users/microsoft/received_events",
            "type": "Organization",
            "site_admin": false
        },
        "network_count": 27699,
        "subscribers_count": 3286
    }
    """

    print(f'Getting metadata for {owner}/{repo}')
    url = f'https://api.github.com/repos/{owner}/{repo}'
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'Mozilla/5.0',
        'Authorization': f'Bearer {token}'
    }

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            data = response.read().decode('utf-8')
            try:
                metadata = json.loads(data)
                return {
                    'meta': {
                        'name': metadata['name'],
                        'full_name': metadata['full_name'],
                        'html_url': metadata['html_url'],
                        'created_at': metadata['created_at'],
                        'updated_at': metadata['updated_at'],
                        'pushed_at': metadata['pushed_at'],
                        'archived': metadata['archived'],
                        'disabled': metadata['disabled'],
                        'owner': metadata['owner']['login'],
                        'owner_type': metadata['owner']['type'],
                        'topics': metadata['topics'] if metadata['topics'] else [],
                        'license': metadata['license']['name'] if metadata['license'] else '',
                    },
                    'analytics': {
                        'language': metadata['language'],
                        'languages': github_convert_to_percentage(languages),
                        'languages_byte': languages,
                        'stargazers_count': metadata['stargazers_count'],
                        'forks_count': metadata['forks_count'],
                        'open_issues_count': metadata['open_issues_count'],
                        'forks': metadata['forks'],
                        'open_issues': metadata['open_issues'],
                        'watchers': metadata['watchers'],
                        'updated_at': _TIMESTAMP
                    }
                }
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f'Error decoding JSON: {e}')
    except urllib.error.HTTPError as e:
        raise urllib.error.HTTPError(f'Error fetching data: {e}')


def prepare_data_for_database(data: list):
    sorted_list_key = sorted(data.keys())
    sorted_list = {}

    for key in sorted_list_key:
        sorted_list[key] = data[key]

    return {
        'data': [item for _, item in sorted_list.items()],
        'metadata': {
            'total': len(data),
            'update_at': _TIMESTAMP
        }
    }


def prepare_data_for_database_analytics(data: dict):
    return {
        'data': data,
        'metadata': {
            'total': len(data),
            'update_at': _TIMESTAMP
        }
    }


def render_db(path: str):
    data = {}
    if not os.path.isdir(path):
        raise Exception(f"{path} is not a directory")

    for file in os.listdir(path):
        if file.endswith('.json'):
            file_path = os.path.join(path, file)

            with open(file_path, 'r') as f:
                el = json.load(f)
                el['filename'] = file
                el['timestamp'] = _TIMESTAMP
                data[el['name']] = el

    return prepare_data_for_database(data)


def process_opensource(with_analytics: bool = False):
    def update_languages(db_languages: dict, languages: dict):
        for language in languages:
            if language in db_languages['bytes']:
                db_languages['bytes'][language] += languages[language]
            else:
                db_languages['bytes'][language] = languages[language]

        db_languages['percentage'] = github_convert_to_percentage(
            db_languages['bytes']),

        return prepare_data_for_database_analytics(db_languages)

    def _delay():
        rand_delay = randint(1, 5)
        print(f"Sleeping for {rand_delay} seconds")
        sleep(rand_delay)

    db_languages = {
        'data': {
            'bytes': {},
            'percentage': {}
        },
        'metadata': {
            'total': 0,
            'update_at': _TIMESTAMP
        }
    }

    db_opensources = render_db(get_raw_data_filepath('opensource'))

    if with_analytics:
        for idx, repo_object in enumerate(db_opensources['data']):
            if repo_object['repository_url'] == 'gitlab':
                print(f"# {idx + 1} - Skipping {repo_object['name']}")
                continue
            owner, name = github_split_repo_url(repo_object['repository_url'])
            print(f"# {idx + 1} - Getting languages for {owner}/{name}")

            try:
                languages = github_get_repo_languages(
                    owner, name, os.environ['CALL_GH_API'])
                db_languages = update_languages(
                    db_languages['data'], languages)
            except:  # noqa
                languages = {}

            try:
                metadata = github_get_repo_metadata(
                    owner, name, os.environ['CALL_GH_API'], languages)
            except:  # noqa
                metadata = {}

            repo_object['meta'] = metadata.get('meta', {})
            repo_object['analytics'] = metadata.get('analytics', {})

            analytics = repo_object.get('analytics_history', {})
            analytics_year = analytics.get(str(_TIMESTAMP_OBJ.year), {})
            analytics_year[str(_TIMESTAMP_OBJ.month)
                           ] = repo_object['analytics']
            analytics[str(_TIMESTAMP_OBJ.year)] = analytics_year
            repo_object['analytics_history'] = analytics

            with open(f'{get_raw_data_filepath('opensource')}/{repo_object['filename']}', 'w') as f:
                json.dump(repo_object, f, indent=2)

            _delay()

        with open(get_languages_analytics_filename(), 'w') as f:
            json.dump(db_languages, f, indent=2)

        with open(f'{get_analytics_mounth_filepath()}/languages.json', 'w') as f:
            json.dump(db_languages, f, indent=2)

    with open(get_awesomelist_database_filename('opensource'), 'w') as f:
        json.dump(db_opensources, f, indent=2)


def process_db(list_name: str):
    db = render_db(get_raw_data_filepath(list_name))
    with open(get_awesomelist_database_filename(list_name), 'w') as f:
        json.dump(db, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Process awesome data')
    parser.add_argument('--exclude', '-e', default=[], nargs='+',
                        help='Exclude some awesome lists', type=list[str])
    parser.add_argument('--with-analytics', '-a', default=False,
                        action='store_true', help='Add analytics to opensource projects')
    args = parser.parse_args()

    process_opensource(with_analytics=args.with_analytics)
    process_db('digital-nomads')
    process_db('communities')
    process_db('companies')


if __name__ == '__main__':
    sys.exit(main())
