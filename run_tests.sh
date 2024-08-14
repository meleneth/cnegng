#!/bin/bash
set -euo pipefail

pytest --cov=src tests --cov-report html
