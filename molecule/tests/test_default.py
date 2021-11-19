"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    if distribution == "fedora":
        pkgs = ["clamav", "clamav-update"]
    elif distribution in ["debian", "kali", "ubuntu"]:
        pkgs = ["clamav-daemon"]
    else:
        # We don't support this distribution
        assert False
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


@pytest.mark.parametrize(
    "service,is_enabled", [("clamav-daemon", False), ("clamav-freshclam", True)]
)
def test_services_debian(host, service, is_enabled):
    """Test that the expected services were enabled or disabled as intended."""
    if host.system_info.distribution in ["debian", "ubuntu"]:
        svc = host.service(service)
        assert svc.is_enabled == is_enabled


@pytest.mark.parametrize(
    "service,is_enabled", [("clamav-clamonacc", False), ("clamav-freshclam", True)]
)
def test_services_fedora(host, service, is_enabled):
    """Test that the expected services were enabled or disabled as intended."""
    if host.system_info.distribution in ["fedora"] and host.system_info.release in [
        "34"
    ]:
        svc = host.service(service)
        assert svc.is_enabled == is_enabled
