#!/bin/sh

pyinstaller --onefile --name cloc --add-data "cloc/languages.json:cloc" cloc/__main__.py
