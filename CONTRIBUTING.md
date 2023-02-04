# Contributing to Awesome Italia Open Source

## Code of Conduct

Please read [the full text](https://github.com/italia-opensource/awesome-italia-opensource/blob/main/CODE_OF_CONDUCT.md) so that you can understand what actions will and will not be tolerated.

### Join our Community

We have
- [Discord](https://discord.gg/CsPwpqTGDK)

## Issues

We have three type of issue:

1. Bug report
2. Feature reqeust
2. Question

## Development

### Online one-click setup for contributing

Reuirements:

- Python >= 3.6
- utils: make, pip3

Setup env:

- clone the awesome-italia-opensource repostory.
- run `make setup`
- run `source .activate`


## Pull Requests

*Pull requests can be used to add/edit/delete in awesome/**/data dir.*

### How To Contribute with PRs

The new project must be added to the `awesome/{companies or opensource}/data` folder using a dedicated file in `kebab-case.json` format.
Subsequently, the `README.md` file is automatically generated, so you don't have to edit it manually.
Projects entered must be maintained and have guidelines and/or documentation for use

1. Open `awesome/{companies or opensource}/data` directory
2. Add a new JSON file for the new project (file name should be a slugified version of the project name)
3. File content should respect the following format:

### awesome/companies rules

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

- *Allowed Type of companies*
  - B2B
  - B2C
  - C2C
  - D2C
  - Consulting
  - Other

- *Allowed Market of companies*
  - Food
  - Aerospace
  - Housing
  - Health
  - Automotive
  - Fintech
  - Energy
  - AI
  - Biotech
  - Ecommerce
  - Software
  - Hardware
  - Service
  - Insurance
  - Travel
  - Other

### awesome/opensource rules

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

- *Allowed Type of projects*
  - app
  - saas
  - paas
  - faas
  - framework
  - tool
  - scripts
  - package
  - library
  - community
  - learning
  - language

- *Allowed Repository Platform*
  - github
  - gitlab
  - bitbucket

- Allowed Licenses
  - Undefined
  - 0BSD
  - BSD-1-Clause
  - BSD-2-Clause
  - BSD-3-Clause
  - AFL-3.0
  - APL-1.0
  - Apache-1.1
  - Apache-2.0
  - APSL-2.0
  - Artistic-1.0
  - Artistic-2.0
  - AAL
  - BSL-1.0
  - BSD-3-Clause-LBNL
  - BSD-2-Clause-Patent
  - Creative Commons
  - CERN Open Hardware Licence Version 2 - Permissive
  - CERN Open Hardware Licence Version 2 - Weakly Reciprocal
  - CERN Open Hardware Licence Version 2 - Strongly Reciprocal
  - CECILL-2.1
  - CDDL-1.0
  - CPAL-1.0
  - CPL-1.0
  - CATOSL-1.1
  - CAL-1.0
  - Coopyleft
  - CopyFair
  - CSL
  - EPL-1.0
  - EPL-2.0
  - eCos-2.0
  - ECL-1.0
  - ECL-2.0
  - EFL-1.0
  - EFL-2.0
  - Entessa
  - EUDatagrid
  - EUPL-1.2
  - FairSource
  - Frameworx-1.0
  - 0BSD
  - AGPL-3.0
  - GPL-2.0
  - GPL-3.0
  - LGPL-2.1
  - LGPL-3.0
  - HPND
  - IPL-1.0
  - IPA
  - ISC
  - Jam
  - LPPL-1.3c
  - BSD-3-Clause-LBNL
  - LiLiQ-P
  - LiLiQ-R
  - LiLiQ-R+
  - LPL-1.0
  - LPL-1.02
  - MS-PL
  - MS-RL
  - MirOS
  - MIT
  - MIT-0
  - Motosoto
  - MPL-1.0
  - MPL-1.1
  - MPL-2.0
  - MulanPSL
  - Multics
  - NASA-1.3
  - Naumen
  - NGPL
  - NPOSL-3.0
  - NTP
  - OCLC-2.0
  - OGTSL
  - OSL-1.0
  - OSL-2.1
  - OSL-3.0
  - OLDAP-2.8
  - QPL-1.0
  - RPSL-1.0
  - RPL-1.1
  - RPL-1.5
  - RSCPL
  - OFL-1.1
  - PPL
  - SimPL-2.0
  - Sleepycat
  - SPL-1.0
  - Watcom-1.0
  - UPL
  - NCSA
  - Upstream Compatibility License v1.0
  - Unicode Data Files and Software License
  - Unlicense
  - VSL-1.0
  - W3C
  - WXwindows
  - Xnet
  - 0BSD
  - ZPL-2.0
  - ZPL-2.1
  - Zlib

#### Tags

The maximum number of tags is 20. This rule is necessary to avoid format problems with the MarkDown file.
