#!/bin/sh
rm dist/*
python setup.py sdist
python setup.py bdist_wheel
twine upload  dist/*
pip uninstall python-selve
pip install python-selve