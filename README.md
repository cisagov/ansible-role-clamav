# ansible-role-clamav 🦪 #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-clamav/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-clamav/actions)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/cisagov/ansible-role-clamav.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-clamav/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/cisagov/ansible-role-clamav.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/ansible-role-clamav/context:python)

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
| clamav_cron_frequency | The frequency of ClamAV scanning.  Must be one of: `hourly`, `daily`, `weekly`, or `monthly`. | `weekly` | No |
| clamav_freshclam_conf | A dictionary of values to set in the freshclam configuration file. | false | No |
| clamav_clamd_conf | A dictionary of values to set in the clamd configuration file. | false | No |
| clamav_configuration_backup | Whether or not to backup configuration files before changing. | false | No |

### Example ###

```yaml
clamav_freshclam_conf:
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

## Example Playbook ##

Here's how to use it in a playbook:

```yaml
- hosts: all
  become: yes
  become_method: sudo
  roles:
    - clamav
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

Mark Feldhousen, Jr. - <mark.feldhousen@trio.dhs.gov>
