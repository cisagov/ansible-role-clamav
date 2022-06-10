#!/bin/bash

set -o nounset
set -o pipefail

LAST_SCAN_LOG_FILENAME='/var/log/clamav/lastscan.log'
LAST_DETECTION_FILENAME='/var/log/clamav/last_detection'

# Scan the entire file system (modulo the /dev, /sys, and /proc trees)
# and write to the log
clamscan --infected --recursive \
  --log=${LAST_SCAN_LOG_FILENAME} \
  --exclude-dir=/dev \
  --exclude-dir=/sys \
  --exclude-dir=/proc \
  /

# if any infections are found, touch the detection file
if ! grep --quiet "^Infected files: 0$" ${LAST_SCAN_LOG_FILENAME}; then
  touch ${LAST_DETECTION_FILENAME}
fi
