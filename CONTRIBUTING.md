# Contributing to Awesome Italia Open Source

## Code of Conduct

Please read [the full text](https://github.com/italia-opensource/awesome-italia-opensource/blob/main/CODE_OF_CONDUCT.md) so that you can understand what actions will and will not be tolerated.

### Join our Community

[![LinkedIn](https://img.shields.io/badge/Linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/italia-open-source)

## Issues

We have three type of issues:

1. Bug report
2. Feature request
3. Question

## How To Contribute with PRs

*Pull requests can be used to add/edit/delete in awesome/**/data dir.*

The new project must be added to the `awesome/{startups,opensource,communities,digital-nomads}/data` folder using a dedicated file in `kebab-case.json` format.
Subsequently, the `README.md` file is automatically generated, so you don't have to edit it manually.
Projects entered must be maintained and have guidelines and/or documentation for use

1. Open `awesome/{startups,opensource,communities,digital-nomads}/data` directory
2. Add a new JSON file for the new project (file name should be a slugified version of the project name)
3. File content should respect json rule
4. (Optional) Before commit exec

   ```bash
   make setup
   source .activate
   make lint check-data
   ```

5. if the tests are passed successfully create PR on GitHub, the title should be `feat(type): added/updated Name`
   **WARNING *type*** must be: startups, opensource, communities or digital-nomads)

**ATTENTION** do not modify any README.md file.

## Json Rules

- [Open-Source Projects](https://github.com/italia-opensource/awesome-italia-opensource/blob/main/CONTRIBUTING.md#awesomeopensource-rules)
- [Communities](https://github.com/italia-opensource/awesome-italia-opensource/blob/main/CONTRIBUTING.md#awesomecommunities-rules)
- [Digital-Nomads](https://github.com/italia-opensource/awesome-italia-opensource/blob/main/CONTRIBUTING.md#awesomedigital-nomads-rules)
- [Companies](https://github.com/italia-opensource/awesome-italia-opensource/blob/main/CONTRIBUTING.md#awesomestartups-rules)

### awesome/opensource rules

Schema reference: [opensources.json](https://github.com/italia-opensource/awesome-italia-opensource/blob/main/scheme/opensources.json)

```JSON
{
  "name": "Test",
  "repository_platform": "github",
  "repository_url": "https://www.github.com/test/name-of-repo",
  "site_url": "https://www.test.com", // no required
  "type": "tool",
  "description": "lorem ipsum", // no required
  "license": "GPL-3.0",
  "tags": [
    "python", "aws"
  ]
}
```

#### Tags

The maximum number of tags is 20. This rule is necessary to avoid format problems with the MarkDown file.

### awesome/communities rules

Schema reference: [communities.json](https://github.com/italia-opensource/awesome-italia-opensource/blob/main/scheme/communities.json)

```JSON
{
  "name": "Test",
  "url": "https://url",
  "type": "...",
  "platform": "...",
  "description": "lorem ipsum", // no required
  "tags": [
    "tech", "aws"
  ],
  "events_type": [
    "Meetup",
    "Hackathon"
  ]
}
```

### awesome/digital-nomads rules

Schema reference: [digital-nomads.json](https://github.com/italia-opensource/awesome-italia-opensource/blob/main/scheme/digital-nomads.json)

```JSON
{
  "name": "Bansko",
  "state_name": "Bulgaria",
  "required_documents": [ "Passport", "CI" ],
  "internet_roaming": "Available",
  "tags": [ "nature", "snow", "lake", "mountain"],
  "resources": [ "https://example.com/" ],
  "coworking": [ "https://exmaple.com/" ],
  "how_to_move": [ "Bike", "Walk", "Taxi" ],
  "daily_average_cost": 30, // no required
  "description": "lorem ipsum", // no required
  "how_to_arrive": [ "Airplane", "Bus", "Train" ],  // no required
}
```

### awesome/startups rules

Schema reference: [startups.json](https://github.com/italia-opensource/awesome-italia-opensource/blob/main/scheme/startups.json)

```JSON
{
  "name": "Test",
  "repository_organization_url": "https://www.github.com/test/name-of-repo", // no required
  "site_url": "https://www.test.com",
  "type": "B2B",
  "market": "Fintech",
  "description": "lorem ipsum",
  "tags": [
    "python", "aws"
  ],
  "foundation_year": "YYYY", // required data >= 2010
  "address": "Colosseum, Piazza del Colosseo, 1, 00184 Roma RM" // no required
}
```

## Development

### Online one-click setup for contributing

|Reuirements|Version|
|---|---|
|Python| >= 3.10|
|Makefile| |

**Setup local env**:

```bash
git clone https://github.com/italia-opensource/awesome-italia-opensource.git

cd awesome-italia-opensource

make setup

source .activate

make test
```

**Create Analytics**:

```bash
# Set secrets from Doppler
doppler login
make doppler
# Or set secrets manually (*)
echo "export TOKEN_GITHUB_PUBLIC_API=_YOUR_TOKEN_" > .env

source .activate

make test
make process-data
```

(*) Create GitHub PAT [here](https://github.com/settings/tokens?type=beta):

  1. Add **Repository access** > `Public Repositories (read-only)`
  2. Save and copy token
