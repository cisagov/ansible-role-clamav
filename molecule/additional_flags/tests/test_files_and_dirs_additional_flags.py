"""Module containing the tests for the additional_flags scenario."""

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
        # The virus scan cron job
        "/etc/cron.daily/virus_scan",
        # freshclam virus signatures
        "/var/lib/clamav/bytecode.cvd",
    ],
)
def test_files_and_dirs(host, path):
    """Test that the expected files and directories were created."""
    assert host.file(path).exists
