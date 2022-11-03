"""Module containing the tests for the additional_flags scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_quarantine_folder(host):
    """Test the quarantine folder."""
    assert host.file("/var/spool/test-clamav").exists
    assert host.file("/var/spool/test-clamav").is_directory


def test_virus_scan_shell(host):
    """Test the scan shell script exists with the expected content."""
    f = host.file("/etc/cron.daily/virus_scan")
    assert f.exists
    assert f.is_file
    assert f.contains(r"--exclude-dir=^/var/spool/test-clamav")
    assert f.contains(r"--foo bar")
    assert f.contains(r"--bar foo")
