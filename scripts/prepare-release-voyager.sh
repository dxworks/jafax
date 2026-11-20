#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:?Usage: prepare-release-voyager.sh <version>}"

# Voyager bundle (jafax-voyager.zip): jar + instrument manifest. Voyager runs
# the tool via instrument.yml (java -jar jafax.jar), so no launch scripts.
# Voyager 2 reads instrument.v2.yml and runs the summary script.
mkdir -p jafax/results
mkdir -p jafax/templates
cp README.md jafax/README.md
cp target/jafax.jar jafax/jafax.jar
cp lib/jafax-summary.py jafax/jafax-summary.py
cp lib/summary_render.py jafax/summary_render.py
cp lib/templates/summary.html jafax/templates/summary.html
cp instrument.yml jafax/instrument.yml
cp instrument.v2.yml jafax/instrument.v2.yml

# The tool's version, from the release tag, in both manifests (V1 and V2)
for f in jafax/instrument.yml jafax/instrument.v2.yml; do
  awk -v v="$VERSION" '!/^version:/ {print} /^name:/ {print "version: " v}' "$f" > "$f.tmp"
  mv "$f.tmp" "$f"
done

zip -r jafax-voyager.zip jafax
