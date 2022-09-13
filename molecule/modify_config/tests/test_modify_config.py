"""Module containing the tests for the configure scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")

file_paths = {
    "debian": {
        "freshclam": "/etc/clamav/freshclam.conf",
        "clamd": "/etc/clamav/clamd.conf",
    },
    "redhat": {"freshclam": "/etc/freshclam.conf", "clamd": "/etc/clamd.d/scan.conf"},
}


def read_configuration_file(host, software_name):
    """Test distribution and read file content for further tests."""
    file_lines = []

    if host.system_info.distribution in ["debian", "kali", "ubuntu"]:
        file_path = file_paths["debian"][software_name]
    elif host.system_info.distribution in ["fedora", "redhat"]:
        file_path = file_paths["redhat"][software_name]
    else:
        # We don't support this distribution
        assert False

    file_content = host.file(file_path).content_string
    file_lines = file_content.splitlines()

    return file_lines


def test_freshclam_conf(host):
    """Test freshclam configuration content."""
    databaseMirror_list_assertion = [
        "db.local.clamav.net",
        "database.clamav.net",
        "dummy.localhost",
    ]

    freshclam_conf_content = read_configuration_file(host, "freshclam")

    for lines in freshclam_conf_content:
        words = lines.split(" ")
        if words[0] == "DatabaseMirror":
            """Test DatabaseMirror values"""
            assert words[1] in databaseMirror_list_assertion
            databaseMirror_list_assertion.remove(words[1])

        elif words[0] == "Bytecode":
            # Should not be there
            """Test Bytecode existence"""
            assert False

    assert len(databaseMirror_list_assertion) == 0


def test_clamd_conf(host):
    """Test clamd configuration content."""
    clamd_conf_content = read_configuration_file(host, "clamd")

    for lines in clamd_conf_content:
        words = lines.split(" ")
        if words[0] == "LogFile":
            assert words[1] == "/var/log/clamav/clamav.log"
        elif words[0] == "StreamMaxLength":
            assert words[1] == "22M"
