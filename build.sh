#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


function help() {
	echo "HELP"
}

function build() {
	if [ -z $BUILD_VERSION ]; then
		echo "Missing parameter: build version"
		exit 1
	fi

	echo -n "Generating.."
	python3 $DIR/setup.py sdist bdist_wheel > /dev/null 2>&1
	echo " ok"

	echo -n "Installing.."
	python3 -m pip install --force-reinstall  "$DIR/dist/starcitizen-scraper-${1}-py3-none-any.whl"
	echo " ok"
}

function dev() {
	echo "Development mode enabled"
	pip3 install -e .
	exit 0
}

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
    shift # past argument
	exit 0
    ;;
    -b|--build)
	build $2
    ;;
    -d|--dev)
	dev
    ;;
esac
done

exit 0
