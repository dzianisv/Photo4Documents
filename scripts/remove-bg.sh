#!/bin/bash

set -eu
input=${1:?set input photo}
output=${2:?set output photo}

exec python3.9 -m carvekit  --post fba --net tracer_b7 -i "$input" -o "$output"
