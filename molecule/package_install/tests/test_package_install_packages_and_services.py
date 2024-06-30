"""Module containing the tests for the package_install scenario."""

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
    pkgs = ["clamav"]
    packages = [host.package(pkg) for pkg in pkgs]
    installed = [package.is_installed for package in packages]
    assert len(pkgs) != 0
    assert all(installed)


def test_clamscan_executable_present(host):
    """Test that the clamscan executable is present.

    This test is added in response to issue #49.
    """
    assert host.exists("clamscan")


@pytest.mark.parametrize("service,is_enabled", [("clamav-freshclam", True)])
def test_services_debian(host, service, is_enabled):
    """Test that the expected services were enabled or disabled as intended."""
    if host.system_info.distribution in ["debian", "kali", "ubuntu"]:
        svc = host.service(service)
        assert svc.is_enabled == is_enabled


@pytest.mark.parametrize("service,is_enabled", [("clamav-freshclam", True)])
def test_services_fedora(host, service, is_enabled):
    """Test that the expected services were enabled or disabled as intended."""
    if host.system_info.distribution in ["fedora"]:
        svc = host.service(service)
        assert svc.is_enabled == is_enabled
