#!/bin/bash

set -e
PACKAGE_NAME=neural_semigroups
cd doc
make clean html
cd ..
pycodestyle --max-doc-length 160 --ignore E203,E501,W503 \
	    ${PACKAGE_NAME} scripts tests
pylint --rcfile=.pylintrc ${PACKAGE_NAME} scripts
mypy --config-file mypy.ini ${PACKAGE_NAME} tests
pytest --cov ${PACKAGE_NAME} --cov-report term-missing --cov-fail-under=99 \
       --junit-xml test-results/neural-semigroups.xml \
       --doctest-modules ${PACKAGE_NAME} tests/
scc -i py ${PACKAGE_NAME}
