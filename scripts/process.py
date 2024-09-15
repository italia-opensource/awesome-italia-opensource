import argparse
import json
import os
import sys
from datetime import datetime, timezone
from random import randint
from time import sleep

import urllib3

# Set the base directory to the root of the project
_BASEDIR = os.path.dirname(os.path.abspath(__file__))
if _BASEDIR.endswith("scripts"):
    _BASEDIR = _BASEDIR.split("/scripts")[0]
sys.path.insert(1, _BASEDIR)  # noqa

_TIMESTAMP_OBJ = datetime.now(timezone.utc)
_TIMESTAMP = str(_TIMESTAMP_OBJ.isoformat()[:-13] + "Z")
_ANALYTICS_DIR = f"{_BASEDIR}/analytics"
_TYPE = ["opensource", "digital-nomads", "communities", "startups"]


def get_database_analytitcs(filename: str, with_error: bool = False):
    filename = f"{_ANALYTICS_DIR}/{filename}.json"

    if with_error is True and not os.path.isfile(filename):
        raise FileNotFoundError(f"File {filename} not found")

    return filename


def get_awesome_list_filepath(list_name: str):
    filepath = f"{_BASEDIR}/awesome/{list_name}/data/"
    if not os.path.dirname(filepath):
        raise Exception(f"Directory {filepath} does not exist")
    return filepath


def github_convert_to_percentage(dictionary):
    total_sum = sum(dictionary.values())

    if total_sum == 0:
        # Avoid division by zero
        return {key: 0 for key in dictionary}

    percentage_dict = {
        key: round((value / total_sum) * 100, 2) for key, value in dictionary.items()
    }
    return percentage_dict


def github_split_repo_url(repository_url):
    repo = repository_url.split("/")
    owner = repo[-2]
    name = repo[-1]
    return owner, name


def github_get_repo_languages(owner: str, repo: str, token: str):
    """Get the languages for a repository
    :param owner: The owner of the repository
    :param repo: The name of the repository
    :param token: The GitHub token to use for authentication
    :param languages_all_projects: A dictionary with the languages of all the projects

    :return: A dictionary of languages and bytes of code
    """

    print(f"Getting repo languages for {owner}/{repo}")

    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Mozilla/5.0",
        "Authorization": f"Bearer {token}",
    }
    languages = {}
    response = urllib3.request("GET", url, headers=headers)
    try:
        data = response.data.decode("utf-8")
        try:
            languages = json.loads(data)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON: {e}")
    except urllib3.exceptions.HTTPError as e:
        raise urllib3.exceptions.HTTPError(f"Error fetching data: {e}")

    return languages


def github_get_repo_metadata(owner: str, repo: str, token: str, languages: dict):
    """Get the metadata for a repository

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

    print(f"Getting metadata for {owner}/{repo}")
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Mozilla/5.0",
        "Authorization": f"Bearer {token}",
    }

    reqsponse = urllib3.request("GET", url, headers=headers)
    try:
        try:
            metadata = json.loads(reqsponse.data)
            return {
                "meta": {
                    "name": metadata["name"],
                    "full_name": metadata["full_name"],
                    "html_url": metadata["html_url"],
                    "created_at": metadata["created_at"],
                    "updated_at": metadata["updated_at"],
                    "pushed_at": metadata["pushed_at"],
                    "archived": metadata["archived"],
                    "disabled": metadata["disabled"],
                    "owner": metadata["owner"]["login"],
                    "owner_type": metadata["owner"]["type"],
                    "topics": metadata["topics"] if metadata["topics"] else [],
                    "license": metadata["license"]["name"]
                    if metadata["license"]
                    else "",
                },
                "analytics": {
                    "language": metadata["language"],
                    "languages": github_convert_to_percentage(languages),
                    "languages_byte": languages,
                    "stargazers_count": metadata["stargazers_count"],
                    "forks_count": metadata["forks_count"],
                    "open_issues_count": metadata["open_issues_count"],
                    "forks": metadata["forks"],
                    "open_issues": metadata["open_issues"],
                    "watchers": metadata["watchers"],
                    "updated_at": _TIMESTAMP,
                },
            }
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON: {e}")
    except urllib3.exceptions.HTTPError as e:
        raise urllib3.exceptions.HTTPError(f"Error fetching data: {e}")


def render_db_languages():
    try:
        with open(get_database_analytitcs("languages", True), "r") as f:
            return json.load(f)
    except FileNotFoundError:  # noqa
        return {
            "data": {"bytes": {}, "percentage": {}, "history": {}},
            "metadata": {"total": 0, "update_at": _TIMESTAMP},
        }


def render_db_awesome_list(path: str):
    def _render_data(data: list):
        sorted_list_key = sorted(data.keys())
        sorted_list = {}

        for key in sorted_list_key:
            sorted_list[key] = data[key]

        return {
            "data": [item for _, item in sorted_list.items()],
            "metadata": {"total": len(data), "update_at": _TIMESTAMP},
        }

    data = {}
    if not os.path.isdir(path):
        raise Exception(f"{path} is not a directory")

    for file in os.listdir(path):
        if file.endswith(".json"):
            file_path = os.path.join(path, file)

            with open(file_path, "r") as f:
                el = json.load(f)
                el["autogenerated"] = {
                    **el.get("autogenerated", {}),
                    "filename": file,
                    "timestamp": _TIMESTAMP,
                }
                data[el["name"]] = el

    return _render_data(data)


def process_analytics_github(idx, repo_object):
    owner, name = github_split_repo_url(repo_object["repository_url"])
    print(f"# {idx + 1} - Getting languages for {owner}/{name}")

    languages = github_get_repo_languages(
        owner, name, os.environ["TOKEN_GITHUB_PUBLIC_API"]
    )

    metadata = github_get_repo_metadata(
        owner, name, os.environ["TOKEN_GITHUB_PUBLIC_API"], languages
    )

    autogenerated = repo_object.get("autogenerated", {})
    autogenerated["meta"] = metadata.get("meta", {})
    autogenerated["analytics"] = metadata.get("analytics", {})

    analytics_history = autogenerated.get("analytics_history", {})
    analytics_year = analytics_history.get(str(_TIMESTAMP_OBJ.year), {})
    analytics_year[str(_TIMESTAMP_OBJ.month)] = autogenerated["analytics"]
    analytics_history[str(_TIMESTAMP_OBJ.year)] = analytics_year
    autogenerated["analytics_history"] = analytics_history

    rand_delay = randint(1, 5)
    print(f"Sleeping for {rand_delay} seconds")
    sleep(rand_delay)


def process_analytics_gitlab(idx, repo_object):
    print(f"# {idx + 1} - Skipping {repo_object['name']}")


def process_analytics_languages(db_opensources):
    db_languages = render_db_languages()
    _tmp = {"bytes": {}, "percentage": {}}

    for project in db_opensources["data"]:
        db_languages_history = db_languages.get("history", {})

        analytics_year = db_languages_history.get(str(_TIMESTAMP_OBJ.year), {})
        analytics_year[str(_TIMESTAMP_OBJ.month)] = {
            "bytes": db_languages["data"]["bytes"],
            "percentage": db_languages["data"]["percentage"],
        }

        db_languages_history[str(_TIMESTAMP_OBJ.year)] = analytics_year

        if (
            project_languages := project["autogenerated"]
            .get("analytics", {})
            .get("languages_byte")
        ):
            for language_name, language_bytes in project_languages.items():
                if language_name in _tmp["bytes"]:
                    _tmp["bytes"][language_name] += language_bytes
                else:
                    _tmp["bytes"][language_name] = language_bytes

        db_languages["data"]["percentage"] = (_tmp["bytes"],)
        db_languages["data"]["percentage"] = (
            github_convert_to_percentage(_tmp["bytes"]),
        )

        db_languages["metadata"]["update_at"] = _TIMESTAMP
        db_languages["metadata"]["total"] = len(db_languages["data"]["bytes"])

    with open(get_database_analytitcs("languages"), "w") as f:
        json.dump(db_languages, f, indent=2)


def process_analytics_opensource(
    db_opensources, only_name: list = [], only_filename: list = []
):
    for idx, repo_object in enumerate(db_opensources["data"]):
        if only_name and repo_object["name"] not in only_name:
            continue
        if (
            only_filename
            and repo_object["autogenerated"]["filename"] not in only_filename
        ):
            continue

        if repo_object["repository_platform"] == "gitlab":
            process_analytics_gitlab(idx, repo_object)

        if repo_object["repository_platform"] == "github":
            process_analytics_github(idx, repo_object)

        with open(
            f'{get_awesome_list_filepath("opensource")}/{repo_object["autogenerated"]["filename"]}',
            "w",
        ) as f:
            json.dump(repo_object, f, indent=2)

    process_analytics_languages(db_opensources)


def process_analytics_communities(db_communities):
    with open(get_database_analytitcs("partnership")) as f:
        partnerships = json.load(f)

    print("Processing communities")
    for idx, community in enumerate(db_communities["data"]):
        print(f"# {idx + 1} - Processing {community['name']}")

        if community["autogenerated"]["filename"] in partnerships["communities"]:
            community["autogenerated"]["partnership"] = True
        else:
            community["autogenerated"]["partnership"] = False


def process_db(
    list_name: str,
    without_analytics: bool,
    only_name: list = [],
    only_filename: list = [],
):
    print(f"Processing: {list_name.title()} awesome list")
    db = render_db_awesome_list(get_awesome_list_filepath(list_name))

    if not without_analytics:
        if not os.getenv("TOKEN_GITHUB_PUBLIC_API"):
            raise ValueError(
                "GitHub API token not found. Please set the environment variable TOKEN_GITHUB_PUBLIC_API in your shell."
            )

        if list_name == "opensource":
            process_analytics_opensource(db, only_name, only_filename)

    if list_name == "communities":
        process_analytics_communities(db)

    with open(get_database_analytitcs(list_name), "w") as f:
        json.dump(db, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Process awesome data")
    parser.add_argument(
        "--only-filename",
        default=[],
        nargs="+",
        help="Process only selected filenames",
        type=str,
    )
    parser.add_argument(
        "--only-name",
        default=[],
        nargs="+",
        help="Process only selected names",
        type=str,
    )
    parser.add_argument(
        "--only-type",
        "-o",
        default=[],
        choices=_TYPE,
        nargs="+",
        help="Only some awesome lists",
        type=str,
    )
    parser.add_argument(
        "--exclude-type",
        "-e",
        default=[],
        choices=_TYPE,
        nargs="+",
        help="Exclude some awesome lists",
        type=str,
    )
    parser.add_argument(
        "--without-analytics",
        "-a",
        default=False,
        action="store_true",
        help="Add analytics to opensource projects",
    )
    args = parser.parse_args()

    _type = [list_name for list_name in _TYPE if list_name not in args.exclude_type]
    _type = (
        [list_name for list_name in _type if list_name in args.only_type]
        if args.only_type
        else _type
    )
    for list_name in _type:
        process_db(
            list_name, args.without_analytics, args.only_name, args.only_filename
        )


if __name__ == "__main__":
    sys.exit(main())
