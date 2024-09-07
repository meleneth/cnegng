#!/bin/bash
set -euo pipefail

cd docs
# sphinx-autogen -o generated *.rst
sphinx-build -b html . build
cd -

