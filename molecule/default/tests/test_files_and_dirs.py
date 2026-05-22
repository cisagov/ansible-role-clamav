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
    "path, exists",
    [
        (
            # The virus scan systemd service unit
            "/etc/systemd/system/run-virus-scan.service",
            True,
        ),
        (
            # The virus scan systemd timer unit
            "/etc/systemd/system/run-virus-scan.timer",
            True,
        ),
        (
            # The virus scan shell script
            "/usr/local/sbin/virus_scan.sh",
            True,
        ),
        (
            # freshclam virus signatures
            "/var/lib/clamav/bytecode.cvd",
            False,
        ),
    ],
)
def test_files_and_dirs(host, path, exists):
    """Test that the expected files and directories were created."""
    assert exists == host.file(path).exists
