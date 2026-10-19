#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:?Usage: prepare-release.sh <version>}"

# Standalone CLI bundle (jafax.zip): jar + launch scripts.
mkdir -p jafax/results
cp README.md jafax/README.md
cp target/jafax.jar jafax/jafax.jar
cp bin/jafax.sh jafax/jafax.sh
cp bin/jafax.bat jafax/jafax.bat
chmod +x jafax/jafax.sh

zip -r jafax.zip jafax
