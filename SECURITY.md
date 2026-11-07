# Security policy

## Supported versions

| Version | Supported |
| --- | --- |
| 0.4.x | yes |
| < 0.4 | no |

## Reporting a vulnerability

Please do not open a public issue for security problems. Use GitHub's private
vulnerability reporting instead: **Security → Advisories → Report a
vulnerability** in this repository.

Include the OctoPrint version, the SwapXYZ version, the printer connection type
and the steps to reproduce.

## Scope

SwapXYZ rewrites the gcode of jog commands inside OctoPrint. It opens no network
connections, starts no daemon and stores no credentials.

Vulnerabilities in OctoPrint itself or in a connector plugin (Serial, Moonraker,
Bambu) belong in the respective upstream project.
