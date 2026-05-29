"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_services(host):
    """Test that the expected services were enabled, disabled or running as intended."""
    distribution = host.system_info.distribution
    if distribution in ["debian", "kali", "ubuntu"]:
        services = [
            {
                "is_enabled": False,
                "is_running": False,
                "name": "clamav-daemon",
            },
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
    elif distribution in ["amzn", "fedora"]:
        services = [
            {
                "is_enabled": False,
                "is_running": False,
                "name": "clamav-clamonacc",
            },
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
    else:
        # We don't support this distribution
        raise ValueError(f"Unsupported distribution {distribution}")

    for service in services:
        svc = host.service(service["name"])
        assert svc.is_enabled == service["is_enabled"]
        assert svc.is_running == service["is_running"]
