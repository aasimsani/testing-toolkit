#!/usr/bin/env bash
# The eval runner starts this script in the empty workspace of one run. The
# script copies the fixture in, so that the agent finds a small repo to test.
# The run's shell has no network, so the script also installs the test tools
# that the fixture's README names.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -R "$here/fixture/." .
uv venv -q .venv
uv pip install -q --python .venv/bin/python pytest hypothesis
