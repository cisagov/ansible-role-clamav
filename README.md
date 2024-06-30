# ansible-role-clamav 🦪 #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-clamav/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-clamav/actions)
[![CodeQL](https://github.com/cisagov/ansible-role-clamav/workflows/CodeQL/badge.svg)](https://github.com/cisagov/ansible-role-clamav/actions/workflows/codeql-analysis.yml)

Installs [ClamAV](https://www.clamav.net) and a related cron job.
This allows servers to be quickly queried en mass for any matched
signatures.  The
[ClamAV-Report](https://github.com/cisagov/clamav-report) tool can be
used to gather scan data from systems using this role.

## Requirements ##

None.

## Role Variables ##

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| clamav_clamd_configuration | A dictionary of values to set in the clamd configuration file. | `{}` | No |
| clamav_configuration_backup | Whether or not to backup configuration files before changing. | `false` | No |
| clamav_cron_frequency | The frequency of ClamAV scanning.  Must be `custom` or an ansible.builtin.cron [special_time](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/cron_module.html#parameter-special_time). | `weekly` | No |
| clamav_cron_custom    | If frequency is set to `custom`, a dictionary to define the timer. | `{"day": "*", "job": "/usr/local/share/virus_scan.sh", "minute": "30", "month": "*", "hour": "5", "weekday": "*"}` | No |
| clamav_freshclam_configuration | A dictionary of values to set in the freshclam configuration file. | `{}` | No |
| clamav_install_from_package_manager | A boolean value to determine if the role should install from the system package manager. | `true` | No |
| clamav_package_version | The package version to install from the URL if not installing from the system package manager. | `1.3.1` | No |
| clamav_scan_copy | Whether to copy infected files to quarantine folder. | `false` | No |
| clamav_scan_exclude_directories | A list of regexes matching directory trees that are to be excluded from scan operations. | `[^/dev, ^/proc, ^/sys, ^/var/spool/clamav]` | No |
| clamav_scan_extra_flags | Additional flags to pass to clamscan (see clamscan man page for reference).  | `[]` | No |
| clamav_scan_move | Whether to move infected files to a quarantine directory. | `false` | No |
| clamav_scan_quarantine_directory | Directory to store infected files. | `/var/spool/clamav` | No |
| clamav_scan_quarantine_group | Group owner to apply to quarantine directory. | `root` | No |
| clamav_scan_quarantine_mode | Permissions to apply to quarantine directory. | `0750` | No |
| clamav_scan_quarantine_owner | Owner to apply to quarantine directory. | `root` | No |
| clamav_seboolean_name | The name of the SELinux boolean used to configure whether or not ClamAV is allowed to scan files.  Note that this variable is only used when SELinux is enabled. | `antivirus_can_scan_system` | No |
| clamav_seboolean_state | The value to use for the SELinux boolean that configures whether or not ClamAV is allowed to scan files.  Note that this variable is only used when SELinux is enabled. | `true` | No |

### Example ###

```yaml
clamav_freshclam_configuration:
  DatabaseMirror: ['db.local.clamav.net', 'database.clamav.net']
  Bytecode: 'true'
  PrivateMirror:
```

would change:

```properties
  ...
  DatabaseMirror foo.bar.com
  DatabaseMirror bar.baz.com
  PrivateMirror private.mirror.local
  Bytecode false
  ...
```

to:

```properties
  ...
  DatabaseMirror db.local.clamav.net
  DatabaseMirror database.clamav.net
  Bytecode true
  ...
```

## Dependencies ##

None.

## Installation ##

This role can be installed via the command:

```console
ansible-galaxy install --role-file path/to/requirements.yml
```

where `requirements.yml` looks like:

```yaml
---
- name: clamav
  src: https://github.com/cisagov/ansible-role-clamav
```

and may contain other roles as well.

For more information about installing Ansible roles via a YAML file,
please see [the `ansible-galaxy`
documentation](https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-multiple-roles-from-a-file).

## Example Playbook ##

Here's how to use it in a playbook:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Install ClamAV and a cron job to run automated AV scans
      ansible.builtin.include_role:
        name: clamav
```

## Cron job output ##

The log of the last scan is accessible at: `/var/log/clamav/lastscan.log`

If a detection occurs the file `/var/log/clamav/last_detection` will be touched.
Its modification time represents the time of the last detection.

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.

## Author Information ##

Mark Feldhousen, Jr. - <mark.feldhousen@gwe.cisa.dhs.gov>
