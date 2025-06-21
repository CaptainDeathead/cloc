#!/bin/sh
python -m build
twine check dist/*
pip install dist/plazma_cloc-1.2.1-py3-none-any.whl --force-reinstall