"""Module containing the tests for the default scenario."""

import os

# import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_pip(host):
    """Test that the appropriate packages were installed."""
    if host.system_info.distribution == "fedora":
        pkgs = ["clamd", "clamav-update"]
    else:
        pkgs = ["clamav-daemon"]
    packages = [host.package(pkg) for pkg in pkgs]
    installed = [package.is_installed for package in packages]
    assert len(pkgs) != 0
    assert all(installed)


# @pytest.mark.parametrize("x", [True])
# def test_packages(host, x):
#     """Run a dummy test, just to show what one would look like."""
#     assert x
