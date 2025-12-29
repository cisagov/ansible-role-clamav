"""Module containing the tests for the package_install scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_services(host):
    """Test that the expected services were enabled, disabled, or running as intended."""
    services = [
        {
            "is_enabled": True,
            "is_running": False,
            "name": "clamav-freshclam",
        },
        {
            "is_enabled": True,
            "is_running": False,
            "name": "run-virus-scan.service",
        },
        {
            "is_enabled": True,
            "is_running": False,
            "name": "run-virus-scan.timer",
        },
    ]

    for service in services:
        svc = host.service(service["name"])
        assert svc.is_enabled == service["is_enabled"]
        assert svc.is_running == service["is_running"]
