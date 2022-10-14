"""Module containing the tests for the additional flags scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")

string_template_content = """#!/bin/bash
# Managed by ansible role clamscan

set -o nounset
set -o pipefail

LAST_SCAN_LOG_FILENAME='/var/log/clamav/lastscan.log'
LAST_DETECTION_FILENAME='/var/log/clamav/last_detection'

# Scan the entire file system (modulo excluded trees)
# and write to the log
clamscan \\
  --copy=/var/spool/test-clamav \\
  --exclude-dir=^/dev/ \\
  --exclude-dir=^/proc/ \\
  --exclude-dir=^/sys/ \\
  --exclude-dir=^/var/spool/test-clamav \\
  --infected \\
  --log=${LAST_SCAN_LOG_FILENAME} \\
  --recursive \\
  --bar foo \\
  --foo bar \\
  /

# if any infections are found, touch the detection file
if ! grep -q "^Infected files: 0$" ${LAST_SCAN_LOG_FILENAME}; then
  touch ${LAST_DETECTION_FILENAME}
fi
"""

# Bytify string content
template_content = bytes(string_template_content, encoding="utf-8")


def test_quarantine_folder(host):
    """Test the quarantine folder."""
    assert host.file("/var/spool/test-clamav").exists
    assert host.file("/var/spool/test-clamav").is_directory


def test_virus_scan_shell(host):
    """Test the scan shell script existence then content."""
    assert host.file("/etc/cron.daily/virus_scan").exists
    shell_content = host.file("/etc/cron.daily/virus_scan").content
    assert template_content == shell_content
