#!/bin/bash

set -o nounset
set -o pipefail

LAST_SCAN_LOG_FILENAME='/var/log/clamav/lastscan.log'
LAST_DETECTION_FILENAME='/var/log/clamav/last_detection'

# scan the entire system and write to the log
clamdscan --infected --fdpass / &> ${LAST_SCAN_LOG_FILENAME}

# if any infections are found, touch the detection file
grep -q "Infected files: 0" ${LAST_SCAN_LOG_FILENAME}

if [ $? -ne 0 ]
then
    touch ${LAST_DETECTION_FILENAME}
fi
