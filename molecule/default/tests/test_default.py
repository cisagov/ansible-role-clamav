"""Module containing the tests for the default scenario."""

import os

import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Test that the appropriate packages were installed."""
    if host.system_info.distribution == "fedora":
        pkgs = ["clamav", "clamav-update"]
    else:
        pkgs = ["clamav-daemon"]
    packages = [host.package(pkg) for pkg in pkgs]
    installed = [package.is_installed for package in packages]
    assert len(pkgs) != 0
    assert all(installed)


@pytest.mark.parametrize(
    "path",
    [
        # The virus scan cron job
        "/etc/cron.weekly/virus_scan",
        # The clamav log directory (created for Fedora)
        "/var/log/clamav",
        # freshclam virus signatures
        "/var/lib/clamav/bytecode.cvd",
    ],
)
def test_files_and_dirs(host, path):
    """Test that the expected files and directories were created."""
    assert host.file(path).exists
