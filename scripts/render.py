import json
import os
import sys
import unicodedata

from snakemd import Document, Inline

BASEDIR = os.path.dirname(os.path.abspath(__file__).replace("scripts/", ""))
AWESOME_TYPE = ["opensource", "startups", "communities", "digital-nomads"]


def get_url_name(category, name):
    return (
        f"https://italiaopensource.com/{category}/"
        + "".join(
            c
            for c in unicodedata.normalize("NFD", name)
            if unicodedata.category(c) != "Mn"
        )
        .replace(" ", "-")
        .lower()
    )


def abspath(*args, os_path=True, separator="/"):
    path = separator.join(args)
    if os_path is True:
        from pathlib import Path

        return str(Path(path))
    return path


class Readme:
    organization_name = "italia-opensource"
    repository_name = "awesome-italia-opensource"

    def __init__(self, name, data, output_path, icon=None, title_h1=None) -> None:
        self.name = name
        self.data = data
        self.output_path = f"{output_path}/"
        self.icon = icon
        self.title_h1 = title_h1
        self.doc = Document()

    @property
    def repository_fullname(self):
        return f"{self.organization_name}/{self.repository_name}"

    @property
    def repository_url(self):
        return f"https://github.com/{self.organization_name}/{self.repository_name}"

    def component_website(self, path: str = ""):
        self.doc.add_heading("Website view", level=4)
        self.doc.add_paragraph("italiaopensource.com").insert_link(
            "italiaopensource.com", f"https://italiaopensource.com/{path}"
        )

    def component_maneiner(self):
        self.doc.add_heading(
            "Support us",
            level=3,
        )
        self.doc.add_paragraph(
            """<a href="https://opencollective.com/italia-open-source/donate" target="_blank"><img src="https://opencollective.com/italia-open-source/donate/button@2x.png?color=blue" width=200 /></a>"""
        )

    def component_contributors(self):
        self.doc.add_paragraph(
            "Feel free to make your contribution. If you want to add a new item to one or more lists please read the contribution guidelines before opening a pull request or contributing to this repository"
        ).insert_link(
            "contribution guidelines",
            f"{self.repository_url}/blob/main/CONTRIBUTING.md",
        )

    def output(self):
        self.doc.dump("README", self.output_path)

    def build(self):
        self.title(
            self.title_h1 if self.title_h1 else self.name, len(self.data), self.icon
        )
        self.header()
        self.content(self.data)
        self.footer()

    def title(self, title: str, number_of_list_element: int, icon="🇮🇹"):
        self.doc.add_heading(f"{icon} Awesome {title.title()} | Italia Open-Source")

        self.doc.add_paragraph(
            f"""
            <img src='https://img.shields.io/badge/list-{number_of_list_element}-green'>
            <img src='https://img.shields.io/github/last-commit/{self.repository_fullname}/main'>
        """
        )

    def header(self):
        raise NotImplementedError("header not implemented")

    def content(self):
        raise NotImplementedError("header not content")

    def footer(self):
        # self.doc.add_heading("Contributors", level=3)
        # self.doc.add_paragraph(
        #     f"""
        #     <a href="{self.repository_url}/graphs/contributors">
        #         <img src="https://contrib.rocks/image?repo={self.repository_fullname}" />
        #     </a>
        #     """
        # )
        self.doc.add_heading("License", level=3)
        self.doc.add_paragraph(
            "The project is made available under the GPL-3.0 license. See the `LICENSE` file for more information."
        )


class StartupsReadme(Readme):
    def __init__(self, name, data, output_path) -> None:
        super().__init__(
            name, data, output_path, icon="🏡", title_h1="Tech Startups in Italy"
        )

    def header(self):
        self.doc.add_paragraph(
            f"Awesome {self.name.title()} is a list of italian tech startups."
        )
        self.doc.add_paragraph(
            "The repository intends to give visibility to startups and stimulate the community to contribute to growing the ecosystem."
        )
        self.doc.add_paragraph(
            "Feel free to make your contribution. If you want to add a new item to one or more lists please read the contribution guidelines before opening a pull request or contributing to this repository"
        ).insert_link(
            "contribution guidelines",
            f"{self.repository_url}/blob/main/CONTRIBUTING.md",
        )

        self.component_maneiner()

    def content(self, data):
        self.doc.add_heading(self.name.title(), level=3)

        self.component_website(path="startups")

        self.doc.add_heading("List", level=4)
        table_content = []
        startups_name = []

        for item in data:
            name = item.get("name")
            if name in startups_name:
                raise Exception(f"Company {name} already exist")

            description = item.get("description", "")
            if len(description) > 59:
                description = description[0:60] + " [..]"

            table_content.append(
                [
                    Inline(name, link=get_url_name("startups", name)),
                    item.get("type"),
                    item.get("market"),
                    ", ".join(item["tags"]),
                    description,
                ]
            )

            startups_name.append(name)

        self.doc.add_table(
            ["Name", "Type", "Market", "Tags", "Description"], table_content
        )


class OpensourceReadme(Readme):
    def __init__(self, name, data, output_path) -> None:
        super().__init__(
            name, data, output_path, icon="💻", title_h1="Open Source Projects in Italy"
        )

    def header(self):
        self.doc.add_paragraph(
            f"Awesome Italia {self.name.title()} is a list of open-source projects created by italian startups or developers."
        )
        self.doc.add_paragraph(
            "The repository intends to give visibility to open source projects and stimulate the community to contribute to growing the ecosystem."
        )
        self.component_contributors()

        self.component_maneiner()

    def content(self, data):
        def _repository(repository_platform, repositories_url, license):
            license = f'<img align="right" src="https://img.shields.io/static/v1?label=license&message={license}&color=orange" alt="License">'
            if repository_platform == "github":
                repositories_url = "/".join(
                    repository_url.replace("https://github.com/", "").split("/")[0:2]
                )
                stars = f'<img align="right" src="https://img.shields.io/github/stars/{repositories_url}?label=%E2%AD%90%EF%B8%8F&logo=github" alt="Stars">'
                issues = f'<img align="right" src="https://img.shields.io/github/issues-raw/{repositories_url}" alt="Issues">'
                return f"{stars}<br>{issues}<br>{license}"

            if repository_platform == "bitbucket":
                repositories_url = "/".join(
                    repository_url.replace("https://bitbucket.org/", "").split("/")[0:2]
                )
                issues = f'<img align="right" src="https://img.shields.io/bitbucket/issues-raw/{repositories_url}" alt="Issues">'
                return f"{issues}<br>{license}"

            if repository_platform == "gitlab":
                repositories_url = "/".join(
                    repository_url.replace("https://gitlab.com", "").split("/")[0:2]
                )
                stars = f'<img align="right" src="https://img.shields.io/gitlab/stars/{repositories_url}?label=%E2%AD%90%EF%B8%8F&logo=gitlab" alt="Stars">'
                issues = f'<img align="right" src="https://img.shields.io/gitlab/issues/open-raw/{repositories_url}" alt="Issues">'
                return f"{stars}<br>{issues}<br>{license}"

        self.doc.add_heading(self.name.title(), level=3)

        self.component_website(path="opensources")

        self.doc.add_heading("List", level=4)
        table_content = []

        repositories_url = []

        for item in data:
            if item["autogenerated"].get("meta", {}).get("archived", False) is True:
                print(f"(WAR)\t{item['name']}\t[Archived]")
            else:
                print(f"\t{item['name']}")

            repository_url = item["repository_url"]

            if item.get("repository_url") in repositories_url:
                raise Exception(
                    f"Project {item['name']} ({repository_url}) already exist"
                )

            name = item["name"].title() + (
                item["autogenerated"].get("meta", {}).get("archived", False) is True
                and " [Archived]"
                or ""
            )
            repository = _repository(
                item["repository_platform"], item["repository_url"], item["license"]
            )
            tags = ", ".join(item["tags"])
            description = item.get("description", "")
            if description and len(description) > 59:
                description = description[0:60] + " [..]"

            table_content.append(
                [
                    Inline(name, link=get_url_name("opensources", name)),
                    Inline(repository, link=repository_url),
                    tags,
                    description,
                ]
            )
            repositories_url.append(repository_url)

        self.doc.add_table(
            ["Name", "Repository", "Stack", "Description"], table_content
        )


class CommunitiesReadme(Readme):
    def __init__(self, name, data, output_path) -> None:
        super().__init__(
            name, data, output_path, icon="👥", title_h1="Tech Communities in Italy"
        )

    def header(self):
        self.doc.add_paragraph(
            f"Awesome Italia {self.name.title()} is a list of italian tech {self.name}."
        )
        self.doc.add_paragraph(
            f"The repository intends to give visibility to {self.name} and stimulate the community to contribute to growing the ecosystem."
        )
        self.component_contributors()

        self.component_maneiner()

    def content(self, data):
        self.doc.add_heading(self.name.title(), level=3)

        self.component_website(path="communities")

        self.doc.add_heading("List", level=4)

        table_content = []
        communities_name = []

        for item in data:
            name = item.get("name")
            if name in communities_name:
                raise Exception(f"Community {name} already exist")

            description = item.get("description", "")
            if len(description) > 59:
                description = description[0:60] + " [..]"

            table_content.append(
                [
                    Inline(name, link=get_url_name("communities", name)),
                    item.get("type"),
                    item.get("platform"),
                    ", ".join(item["tags"]),
                    description,
                ]
            )

            communities_name.append(name)

        self.doc.add_table(
            ["Name", "Type", "Platform", "Tags", "Description"], table_content
        )


class DigitalNomadsReadme(Readme):
    def __init__(self, name, data, output_path) -> None:
        super().__init__(
            name, data, output_path, icon="🌍", title_h1="Digital Nomads Destinations"
        )

    def header(self):
        self.doc.add_paragraph(
            f"Awesome Italia {self.name.title()} is a list of best places for remote working."
        )
        self.doc.add_paragraph(
            f"The repository intends to give visibility to {self.name} and stimulate the people to share and contribute to growing the remote working ecosystem."
        )
        self.component_contributors()

        self.component_maneiner()

    def content(self, data):
        self.doc.add_heading(self.name.title(), level=3)

        self.component_website(path="digital-nomads")

        self.doc.add_heading("List", level=4)

        table_content = []
        digital_nomads_name = []

        for item in data:
            name = item.get("name")
            if name in digital_nomads_name:
                raise Exception(f"Place {name} already exist")

            table_content.append(
                [
                    Inline(name, link=get_url_name("digital-nomads", name)),
                    item.get("state_name").upper(),
                    ", ".join(item["how_to_move"]),
                    ", ".join(item["required_documents"]),
                    ", ".join(item["tags"]),
                ]
            )

            digital_nomads_name.append(name)

        self.doc.add_table(
            ["Name", "State", "How to move", "Required Documents", "Tags"],
            table_content,
        )


def render(type: str):
    if type not in AWESOME_TYPE:
        raise Exception(f'Error type "{type}" not in {AWESOME_TYPE}')

    filename = abspath(BASEDIR, "analytics", f"{type}.json")

    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    with open(filename) as fh:
        content = json.load(fh)

    print(f"Render: {type} (loaded {content['metadata']['total']} files)")

    return content["data"]


def main():
    def opensource():
        data = render(type="opensource")
        builder = OpensourceReadme(
            "open-source", data, abspath(BASEDIR, "awesome", "opensource")
        )
        builder.build()
        builder.output()

    def startups():
        data = render(type="startups")
        builder = StartupsReadme(
            "startups", data, abspath(BASEDIR, "awesome", "startups")
        )
        builder.build()
        builder.output()

    def communities():
        data = render(type="communities")
        builder = CommunitiesReadme(
            "communities", data, abspath(BASEDIR, "awesome", "communities")
        )
        builder.build()
        builder.output()

    def digital_nomads():
        data = render(type="digital-nomads")
        builder = DigitalNomadsReadme(
            "digital nomads", data, abspath(BASEDIR, "awesome", "digital-nomads")
        )
        builder.build()
        builder.output()

    opensource()
    startups()
    communities()
    digital_nomads()


if __name__ == "__main__":
    sys.exit(main())
