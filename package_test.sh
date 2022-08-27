#!/bin/sh
rm dist/*
python setup.py sdist
python setup.py bdist_wheel
python -m twine upload -r testpypi dist/* --verbose
pip uninstall python-selve-http
pip install --index-url https://test.pypi.org/simple/ python-selve-http