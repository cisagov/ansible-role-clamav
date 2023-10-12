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
    if distribution in ["fedora"]:
        if host.system_info.release == "38":
            pkgs = ["clamav", "clamav-freshclam"]
        else:
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
    "service,is_enabled", [("clamav-daemon", False), ("clamav-freshclam", True)]
)
def test_services_debian(host, service, is_enabled):
    """Test that the expected services were enabled or disabled as intended."""
    if host.system_info.distribution in ["debian", "kali", "ubuntu"]:
        svc = host.service(service)
        assert svc.is_enabled == is_enabled


@pytest.mark.parametrize(
    "service,is_enabled", [("clamav-clamonacc", False), ("clamav-freshclam", True)]
)
def test_services_fedora(host, service, is_enabled):
    """Test that the expected services were enabled or disabled as intended."""
    if host.system_info.distribution in ["fedora"]:
        svc = host.service(service)
        assert svc.is_enabled == is_enabled
