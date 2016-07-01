#!/bin/bash
set -o nounset  # exit if trying to use an uninitialized var
set -o errexit  # exit if any program fails
set -o pipefail # exit if any program in a pipeline fails, also
set -x          # debug mode

fonts=( bold default large )
for font in "${fonts[@]}"; do
  python png2mcm.py -i images/betaflight.png -o fonts/betaflight/${font}.mcm -x 24 -y 4 -s 160
  python copy2mcm.py -i fonts/mwosd/${font}.mcm -o fonts/betaflight/${font}.mcm -f 0 -t 0 -c 160
  # move the symbols we need into a range outside of the logo
  # throttle
  python copy2mcm.py -i fonts/mwosd/${font}.mcm -o fonts/betaflight/${font}.mcm -f 0xC8 -t 0x04 -c 2
  # rssi
  python copy2mcm.py -i fonts/mwosd/${font}.mcm -o fonts/betaflight/${font}.mcm -f 0xBA -t 0x01 -c 1
  # volt
  python copy2mcm.py -i fonts/mwosd/${font}.mcm -o fonts/betaflight/${font}.mcm -f 0xA9 -t 0x06 -c 1
  # ahi
  python copy2mcm.py -i fonts/mwosd/${font}.mcm -o fonts/betaflight/${font}.mcm -f 0xBC -t 0x27 -c 1
  # copy it into the project
  cp fonts/betaflight/${font}.mcm ~/src/rc/betaflight-configurator/resources/osd/
done
