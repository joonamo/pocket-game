#!/bin/bash
set -euxo pipefail

export ZGB_PATH="/Users/joonah/repos/omat-repot/pocket-game/zgb/common"
cd src
make build_gb BUILD_TYPE=ReleaseColor
cd -