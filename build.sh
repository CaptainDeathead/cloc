#!/bin/sh
python -m build
twine check dist/*
pip install dist/plazma_cloc-1.1.0-py3-none-any.whl --force-reinstall