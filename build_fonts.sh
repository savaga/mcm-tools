#!/bin/bash
set -o nounset  # exit if trying to use an uninitialized var
set -o errexit  # exit if any program fails
set -o pipefail # exit if any program in a pipeline fails, also
set -x          # debug mode

# insert the logo
python png2mcm.py -i images/betaflight.png -o fonts/betaflight/bold.mcm -x 24 -y 4 -s 158
