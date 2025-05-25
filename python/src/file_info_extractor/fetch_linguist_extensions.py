"""
This module fetches the latest programming language extension mappings from the GitHub Linguist project.
It downloads the 'languages.yml' file, extracts all programming language extensions, and creates a mapping
from file extensions to language names. The resulting mapping is saved as a JSON file named 'ext_to_lang.json'.

Dependencies:
    - requests
    - PyYAML

Usage:
    Run this script to update the 'BasicFileInfoExtractor.EXT_TO_LANG' with the latest extension-to-language mapping.
"""

import json
import typing

import requests
import yaml

URL = "https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml"
response = requests.get(URL)
languages_data = yaml.safe_load(response.text)

ext_to_lang: typing.Dict[str, str] = {}
for lang, data in languages_data.items():
    if data.get("type") == "programming":
        for ext in data.get("extensions", []):
            ext_to_lang[ext.lower()] = lang


with open("ext_to_lang.json", encoding="utf-8", mode="w") as fout:
    json.dump(ext_to_lang, fout, indent=4, sort_keys=True)
