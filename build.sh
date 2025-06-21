#!/bin/sh
python -m build
twine check dist/*
pip install dist/plazma_cloc-1.2.2-py3-none-any.whl --force-reinstall