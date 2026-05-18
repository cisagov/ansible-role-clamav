"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "path",
    [
        # The virus scan systemd service unit
        "/etc/systemd/system/run-virus-scan.service",
        # The virus scan systemd timer unit
        "/etc/systemd/system/run-virus-scan.timer",
        # The virus scan shell script
        "/usr/local/sbin/virus_scan.sh",
    ],
)
def test_files_and_dirs(host, path):
    """Test that the expected files and directories were created."""
    assert host.file(path).exists
