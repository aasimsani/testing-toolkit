#!/usr/bin/env bash
# The eval runner starts this script in the empty workspace of one run. The
# script copies the fixture in, so that the agent finds a small repo to test.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -R "$here/fixture/." .
