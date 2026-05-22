"""Module containing the tests for the additional_flags scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_services(host):
    """Test that the expected services were enabled or running as intended."""
    distribution = host.system_info.distribution
    if distribution in ["debian", "kali", "ubuntu"]:
        services = [
            {
                "name": "clamav-daemon",
                "is_enabled": False,
                "is_running": False,
            },
            {
                "name": "clamav-freshclam",
                "is_enabled": True,
                "is_running": False,
            },
            {
                "name": "run-virus-scan.service",
                "is_enabled": True,
                "is_running": False,
            },
            {
                "name": "run-virus-scan.timer",
                "is_enabled": True,
                "is_running": True,  # default value has been overridden by role variable configuration
            },
        ]
    elif distribution in ["amzn", "fedora"]:
        services = [
            {
                "name": "clamav-clamonacc",
                "is_enabled": False,
                "is_running": False,
            },
            {
                "name": "clamav-freshclam",
                "is_enabled": True,
                "is_running": False,
            },
            {
                "name": "run-virus-scan.service",
                "is_enabled": True,
                "is_running": False,
            },
            {
                "name": "run-virus-scan.timer",
                "is_enabled": True,
                "is_running": True,  # default value has been overridden by role variable configuration
            },
        ]
    else:
        # We don't support this distribution
        assert False

    for service in services:
        svc = host.service(service["name"])
        assert svc.is_enabled == service["is_enabled"]
        assert svc.is_running == service["is_running"]
