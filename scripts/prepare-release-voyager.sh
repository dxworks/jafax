#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:?Usage: prepare-release-voyager.sh <version>}"

# Voyager bundle (jafax-voyager.zip): jar + instrument manifest. Voyager runs
# the tool via instrument.yml (java -jar jafax.jar), so no launch scripts.
mkdir -p jafax/results
cp README.md jafax/README.md
cp target/jafax.jar jafax/jafax.jar
cp instrument.yml jafax/instrument.yml

zip -r jafax-voyager.zip jafax
