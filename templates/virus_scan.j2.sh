#!/usr/bin/env bash
# shellcheck disable=all
# Managed by cisagov/ansible-role-clamav.
# Beware:  This script will be run by root.

# Note that we turn off all shellcheck checking for this script, since
# the shellcheck linter cannot deal with the jinja templating.  We do,
# however, validate the generated file with shfmt and shellcheck after
# the templating is applied.

set -o errexit
set -o nounset
set -o pipefail

LAST_SCAN_LOG_FILENAME=/var/log/clamav/lastscan.log
LAST_DETECTION_FILENAME=/var/log/clamav/last_detection

# Scan the entire file system (modulo excluded trees) and write to the
# log.  Use nice since clamscan can be temporarily CPU-hungry.
echo -n Running clamscan...
{% if clamav_install_from_package_manager %}
nice clamscan \
  {% else %}
nice /usr/local/bin/clamscan \
  {% endif %}
--database=/var/lib/clamav \
  {% if clamav_scan_copy %}
--copy={{ clamav_scan_quarantine_directory }} \
  {% endif %}
{% for dir in clamav_scan_exclude_directories %}
--exclude-dir={{ dir }} \
  {% endfor %}
--infected \
  --log=${LAST_SCAN_LOG_FILENAME} \
  {% if clamav_scan_move %}
--move={{ clamav_scan_quarantine_directory }} \
  {% endif %}
--recursive \
  {% for flag in clamav_scan_extra_flags %}
{{ flag }} \
  {% endfor %}
/
echo done.

# If any infections were found in the most recent run, touch the
# detection file.
prefix=${LAST_SCAN_LOG_FILENAME}-
latest_scan_log=${LAST_SCAN_LOG_FILENAME}-00

# This function cleans the individual scan logs created by the csplit
# command.
cleanup_after_csplit() {
  echo -n Cleaning up individual scan logs created by csplit...
  rm -f ${prefix}*
  echo done.
}
# Run cleanup_after_csplit when the script exits.
trap cleanup_after_csplit EXIT

# Split the scan log so that each scan is its own log file.
echo -n Splitting the scan log into separate files for each scan run...
tac "$LAST_SCAN_LOG_FILENAME" | csplit --prefix="$prefix" --quiet - \
  "/^-* SCAN SUMMARY -*$/" "{*}"
echo done.
if [ -f "$latest_scan_log" ]; then
  # Extract the number of infected files found.
  echo -n Extracting number of infected files found in latest scan run...
  num_infected_files=$(sed --quiet --regexp-extended \
    "s/^Infected files: ([[:digit:]]+)$/\1/p" \
    "$latest_scan_log")
  echo done. "$num_infected_files" infected files found.
  if [ -n "$num_infected_files" ]; then
    if [ "$num_infected_files" -ne 0 ]; then
      # An infected file was found.
      echo -n Touching $LAST_DETECTION_FILENAME...
      touch "$LAST_DETECTION_FILENAME"
      echo done.
    fi
  else
    echo Unable to parse number of infected files from file \
      $latest_scan_log. >&2
    exit 1
  fi
else
  echo Unable to split file $LAST_DETECTION_FILENAME into constituent \
    scan logs via csplit. >&2
  exit 1
fi
