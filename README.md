# RSI-Scraper
[![GitHub license](https://img.shields.io/github/license/Dymerz/RSI-Scraper)](https://github.com/Dymerz/RSI-Scraper/blob/develop/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/Dymerz/RSI-Scraper)](https://github.com/Dymerz/RSI-Scraper/issues) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rsi-scraper) ![PyPI](https://img.shields.io/pypi/v/rsi-scraper?label=version)

## Overview

Web Scraper for RSI (used in [starcitizen-api.com](https://starcitizen-api.com))

This module allows you to easy retrive online information related to the RSI website.

## Requirements
- Python>=3.7
- requests>=2.25.1
- lxml>=4.6.3

## Installation
    pip install rsi-scraper

## Modules
 Module                  | Description   |
|-------------------------|---------------|
| Organization  | Find an organization by SID |
| OrganizationMembers   | List members of an organization by page of 32 |
| ProgressTracker   | Get all progress tracker teams |
| ProgressTrackerInfo   | Get progress tracker information using the slug |
| Roadmap   | List cards of the Roadmap by specified version |
| Ship  | Search ship using multiple parameters  |
| StarmapSystems    | Get systems from the starmap by name |
| StarmapTunnels    | Get tunnels from the starmap by id |
| StarmapSpecies    | Get species from the starmap by name |
| StarmapAffiliations   | Get affiliations from the starmap by name |
| StarmapStarSystems    | Get star-system from the starmap by code |
| StarmapCelestialObjects   | Get celestial objects from the starmap by name |
| StarmapSearch | Search object from the starmap by name |
| StarmapRouteSearch   | Find routes from position to destionation |
| Stats | Get general information like the numbers of citizens |
| Telemetry | Get some telemetry info |
| User  | Find information about a user by handle |
| Version   | Get a list of all versions |

## Usage
```py
  from rsi_scraper import User, Organization, Ship

  user = User('dymerz').execute()
  organization = Organization('PROTECTORA').execute()

  ship = Ship(name='Cutlass Black').execute()
```

## Optional Environment Variables
```yaml
    # Used in the HTTP header of requests
    VERSION = "DEVELOPMENT"

    # Define the HTTP proxy to use (e.g: http://127.0.0.1:8000).
    HTTP_PROXY = ""
```

# Contributing

1. Fork the repo on GitHub
2. Clone the project to your own machine
3. Commit changes to your own branch
4. Push your work back up to your fork
5. Submit a Pull request so that we can review your changes

> NOTE: Be sure to merge the latest from "upstream" before making a pull request!

See [CONTRIBUTING.md](./CONTRIBUTING.md).

***
# Rights

 This is an unofficial Star Citizen tool, not affiliated with the Cloud Imperium group of companies. All content on this site not authored by its host or users are property of their respective owners. [robertsspaceindustries.com](https://robertsspaceindustries.com/)

 This project is not endorsed by or affiliated with the Cloud Imperium or Roberts Space Industries group of companies.

 All game content and materials are copyright Cloud Imperium Rights LLC, Cloud Imperium Rights Ltd, Star Citizen®, Squadron 42®, Roberts Space Industries®, and Cloud Imperium® are registered trademarks of Cloud Imperium Rights LLC.

 All rights reserved.
