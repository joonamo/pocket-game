#!/bin/bash
set -euxo pipefail

./build.sh
killall java -jar Emulicious/Emulicious.jar || true
java -jar Emulicious/Emulicious.jar bin/pocket-game.gbc &
