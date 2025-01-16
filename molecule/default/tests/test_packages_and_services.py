"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    if distribution in ["fedora"]:
        pkgs = ["clamav", "clamav-freshclam"]
    elif distribution in ["debian", "kali", "ubuntu"]:
        pkgs = ["clamav-daemon"]
    else:
        # We don't support this distribution
        assert False
    packages = [host.package(pkg) for pkg in pkgs]
    installed = [package.is_installed for package in packages]
    assert len(pkgs) != 0
    assert all(installed)


def test_clamscan_executable_present(host):
    """Test that the clamscan executable is present.

    This test is added in response to issue #49.
    """
    assert host.exists("clamscan")


def test_services(host):
    """Test that the expected services were enabled or disabled as intended."""
    distribution = host.system_info.distribution
    if distribution in ["debian", "kali", "ubuntu"]:
        services = [
            {
                "is_enabled": False,
                "name": "clamav-daemon",
            },
            {
                "is_enabled": True,
                "name": "clamav-freshclam",
            },
            {
                "is_enabled": True,
                "name": "run-virus-scan.service",
            },
            {
                "is_enabled": True,
                "name": "run-virus-scan.timer",
            },
        ]
    elif distribution in ["fedora"]:
        services = [
            {
                "is_enabled": False,
                "name": "clamav-clamonacc",
            },
            {
                "is_enabled": True,
                "name": "clamav-freshclam",
            },
            {
                "is_enabled": True,
                "name": "run-virus-scan.service",
            },
            {
                "is_enabled": True,
                "name": "run-virus-scan.timer",
            },
        ]
    else:
        # We don't support this distribution
        assert False

    for service in services:
        svc = host.service(service["name"])
        assert svc.is_enabled == service["is_enabled"]
