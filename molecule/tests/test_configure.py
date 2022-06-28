"""Module containing the tests for the configure scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")

host_all_vars = host.ansible.get_variables()

file_paths = {
    'debian': {
        'freshclam': '/etc/clamav/freshclam.conf',
        'clamd': '/etc/clamav/clamd.conf'
        },
    'redhat': {
        'freshclam': '/etc/freshclam.conf',
        'clamd': '/etc/clam.d/scan.conf'
    }
}


def read_configuration_file(host, software_name):
    """Test distribution and read file content for further tests."""
    file_content = []

    if host.system_info.distribution in ["debian", "kali", "ubuntu"]:
        file_path = file_paths['debian'][software_name]
    elif host.system_info.distribution in ["fedora", "redhat"]:
        file_path = file_paths['redhat'][software_name]
    else:
        # We don't support this distribution
        assert False

    with open(host.file(file_path), 'r') as fh:
        file_content = fh.readlines()

    return file_content

def test_freshclam_conf(host):
    """Test freshclam configuration content."""
    databaseMirror_list_assertion = ['db.local.clamav.net', 'database.clamav.net', 'dummy.localhost']

    freshclam_conf_content = read_configuration_file(host, 'freshclam')

    for lines in freshclam_conf_content:
        words = lines.split(" ")
        if words[0] == "DatabaseMirror":
            assert words[1] in databaseMirror_list_assertion
            databaseMirror_list_assertion.remove(words[1])

        elif words[0] == 'Bytecode':
            # Should not be there
            assert False

def test_clamd_conf(host):
    """Test clamd configuration content."""
    clamd_conf_content = read_configuration_file(host, 'clamd')

    for lines in clamd_conf_content:
        words = lines.split(" ")
        if words[0] == 'LogFile':
            assert words[1] == '/var/log/clamav/clamav.log'
        elif words[0] == 'StreamMaxLength':
            assert words[1] == '22M'