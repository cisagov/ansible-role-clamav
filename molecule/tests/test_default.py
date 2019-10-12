"""Module containing the tests for the default scenario."""

import json
import os

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
    elif distribution == "debian" or distribution == "ubuntu":
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
    "service,isEnabled", [("clamav-daemon", False), ("clamav-freshclam", True)]
)
def test_services(host, service, isEnabled):
    """Test that the expected services were enabled or disabled as intended."""
    if (
        host.system_info.distribution == "debian"
        or host.system_info.distribution == "ubuntu"
    ):
        svc = host.service(service)
        assert svc.is_enabled == isEnabled


@pytest.mark.parametrize("log_group_name", ["/instance-logs/freshclam"])
def test_cloudwatch_agent_config(host, log_group_name):
    """Test that the expected sections were added to the Amazon CloudWatch Agent config."""
    config_file = host.file(
        "/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json"
    )
    if config_file.exists:
        config = json.loads(config_file.content)
        log_sections = config["logs"]["logs_collected"]["files"]["collect_list"]
        assert any([x["log_group_name"] == log_group_name for x in log_sections])
