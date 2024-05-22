import json
import os
import sys

import fastjsonschema

BASEDIR = os.path.dirname(os.path.abspath(__file__).replace("scripts/", ""))


def get_jsonschema(awesome_type: str):
    with open(f"scheme/{awesome_type}.json") as fh:
        return json.load(fh)


def abspath(*args, os_path=True, separator="/"):
    path = separator.join(args)
    if os_path is True:
        from pathlib import Path

        return str(Path(path))
    return path


class Checker:
    def __init__(self) -> None:
        self.jsonschema = self.define_jsonschema()

    def json_validate(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(filename=filename)

        with open(filename) as fh:
            content = json.load(fh)

        return self.jsonschema(content)

    def validate(self, dirpath: str):
        print(f"Check: {dirpath.split('/')[-2].title()}")
        loaded = []
        for project in os.listdir(dirpath):
            filename = abspath(dirpath, project)

            if not os.path.isfile(filename):
                print(f"Skip render '{filename}'")
                continue

            if not project.endswith(".json"):
                raise Exception(f"File {project} is not json")

            item = (project.replace(".json", ""), filename)

            loaded.append(item)

        loaded = sorted(loaded, key=lambda tup: tup[0])

        values = []
        for name, filename in loaded:
            print(f"\tFile: {name}.json")
            values.append(self.json_validate(filename))

        return values

    def jsonschema(self):
        raise NotImplementedError("jsonschema not implemented")


class OpensourceChecker(Checker):
    ALLOWED_TYPE = []

    ALLOWED_REPOSITORY_PLATFORM = []

    # List from https://opensource.org/licenses/alphabetical
    ALLOWED_LICENSES = []

    def __init__(self) -> None:
        super().__init__()

    def define_jsonschema(self):
        schema = get_jsonschema("opensources")
        self.ALLOWED_TYPE = schema["properties"]["type"]["enum"]
        self.ALLOWED_REPOSITORY_PLATFORM = schema["properties"]["repository_platform"][
            "enum"
        ]
        self.ALLOWED_LICENSES = schema["properties"]["license"]["enum"]

        return fastjsonschema.compile(definition=schema)


class CompaniesChecker(Checker):
    ALLOWED_TYPE = []

    ALLOWED_MARKET = []

    def __init__(self) -> None:
        super().__init__()

    def define_jsonschema(self):
        scheme = get_jsonschema("companies")
        self.ALLOWED_TYPE = scheme["properties"]["type"]["enum"]
        self.ALLOWED_MARKET = scheme["properties"]["market"]["enum"]

        return fastjsonschema.compile(definition=scheme)


class CommunitiesChecker(Checker):
    ALLOWED_TYPE = []

    ALLOWED_PLATFORM = []

    ALLOWED_EVENTS_TYPE = []

    def __init__(self) -> None:
        super().__init__()

    def define_jsonschema(self):
        schema = get_jsonschema("communities")
        self.ALLOWED_PLATFORM = schema["properties"]["platform"]["enum"]
        self.ALLOWED_EVENTS_TYPE = schema["properties"]["events_type"]["items"]["enum"]
        self.ALLOWED_TYPE = schema["properties"]["type"]["enum"]

        return fastjsonschema.compile(definition=schema)


class DigitalNomadsChecker(Checker):
    ALLOWED_MOVE = []

    ALLOWED_DOCUMENTS = []

    ALLOWED_INTERNET_ROAMING = []

    def __init__(self) -> None:
        super().__init__()

    def define_jsonschema(self):
        schema = get_jsonschema("digital-nomads")
        self.ALLOWED_MOVE = schema["properties"]["how_to_move"]["items"]["enum"]
        self.ALLOWED_DOCUMENTS = schema["properties"]["required_documents"]["items"][
            "enum"
        ]
        self.ALLOWED_INTERNET_ROAMING = schema["properties"]["internet_roaming"]["enum"]

        return fastjsonschema.compile(definition=schema)


def main():
    OpensourceChecker().validate(abspath(BASEDIR, "awesome", "opensource", "data"))
    CompaniesChecker().validate(abspath(BASEDIR, "awesome", "companies", "data"))
    CommunitiesChecker().validate(abspath(BASEDIR, "awesome", "communities", "data"))
    DigitalNomadsChecker().validate(
        abspath(BASEDIR, "awesome", "digital-nomads", "data")
    )


if __name__ == "__main__":
    sys.exit(main())
