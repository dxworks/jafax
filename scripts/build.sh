#!/usr/bin/env bash
set -euo pipefail

# JaFaX is compiled with Kotlin 1.6.21, whose compiler targets up to JDK 17.
# Prefer a JDK 17 when the runner provides one (GitHub runners expose
# JAVA_HOME_17_X64); otherwise fall back to the active JAVA_HOME. The produced
# jar still runs on Java 21+ at runtime (see minimumJavaVersion in lib/lib.js).
if [ -n "${JAVA_HOME_17_X64:-}" ]; then
  export JAVA_HOME="$JAVA_HOME_17_X64"
  export PATH="$JAVA_HOME/bin:$PATH"
fi

mvn -B clean package
