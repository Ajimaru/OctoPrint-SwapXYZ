<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <img
    src="https://github.com/Ajimaru/OctoPrint-SwapXYZ/raw/main/assets/img/swapxyz.svg"
    alt="SwapXYZ Logo"
    width="64"
    height="64"
  />
</p>
<h1 align="center">SwapXYZ</h1>
<!-- markdownlint-enable MD033 MD041 -->

[![Latest release][badge-release]](https://github.com/Ajimaru/OctoPrint-SwapXYZ/releases/latest)
[![Downloads][badge-downloads]](https://github.com/Ajimaru/OctoPrint-SwapXYZ/releases)
[![CI][badge-ci]](https://github.com/Ajimaru/OctoPrint-SwapXYZ/actions/workflows/ci.yml?query=branch%3Amain)
[![CodeQL][badge-codeql]](https://github.com/Ajimaru/OctoPrint-SwapXYZ/actions/workflows/codeql.yml?query=branch%3Amain)
[![Last commit][badge-last-commit]](https://github.com/Ajimaru/OctoPrint-SwapXYZ/commits/main)
[![License][badge-license]](https://github.com/Ajimaru/OctoPrint-SwapXYZ/blob/main/LICENSE)

[![OctoPrint][badge-octoprint]](https://octoprint.org)
[![Python][badge-python]](https://python.org)
[![PRs welcome][badge-prs]](https://github.com/Ajimaru/OctoPrint-SwapXYZ/pulls)

An OctoPrint plugin to swap the X and Y axes used by the jog controls, and to reverse the direction of the X, Y or Z axis.

## Setup

Install via OctoPrint's plugin manager using this URL:

```url
https://github.com/Ajimaru/OctoPrint-SwapXYZ/releases/latest/download/SwapXYZ-latest.zip
```

This plugin is a fork of [SwapXY](https://plugins.octoprint.org/plugins/swapxy/) by Wolfram Manufacturing.

As long as the plugin is enabled, the jog buttons for X and Y will
drive the other axis instead.

To drive one or both of these axes in the opposite direction (negative/positive), enable the reverse option for that axis.

The Z axis is never swapped, since it has no partner axis to swap with, but it
can be reversed. This is useful on printers where the bed moves on Z instead of
the print head, so that the Z buttons in OctoPrint match what you see happening
to the print.

## Compatibility

Requires OctoPrint 1.11.8 or newer with Python 3.7 or newer.

This plugin rewrites jog commands through OctoPrint's
`octoprint.comm.protocol.gcode.queuing` hook. It therefore only works for
printers whose commands pass through that hook.

| Connection | Works | Notes |
| --- | --- | --- |
| Serial / USB (Marlin, RepRapFirmware, …) | yes | the classic gcode path, via the bundled Serial Connector |
| Moonraker Connector (Klipper) | no | sends gcode straight to Moonraker, bypassing the hook |
| Bambu Connector | no | sends gcode straight to the printer's API, bypassing the hook |

The connector plugins introduced in OctoPrint 2.0 build their own gcode and
hand it to the printer directly, without dispatching OctoPrint's gcode hooks.
Swapping and reversing have no effect there, and the settings are simply
ignored. This affects any plugin that rewrites gcode via those hooks, not just
this one.

## Config

These options can also be changed from the web UI settings window.

Default config:

```yaml
plugins:
    swapxyz:
        reverse:
            X: false
            Y: false
            Z: false
```

## Advanced

Archive URL: https://github.com/Ajimaru/OctoPrint-SwapXYZ/archive/refs/heads/main.zip

Upstream project: https://gitlab.com/wolframmfg/octoprint-swapxy

## Development

```bash
python -m pip install "OctoPrint==1.11.8"
python -m pip install -r requirements-dev.txt
python -m pip install --no-build-isolation -e .
python -m pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

Developed by

[![Wolfram Manufacturing](https://github.com/Ajimaru/OctoPrint-SwapXYZ/raw/main/wolframmfg.png)](https://wolframmfg.com/)

[badge-release]: https://img.shields.io/github/v/release/Ajimaru/OctoPrint-SwapXYZ?sort=semver&style=flat-square&logo=github&logoColor=white
[badge-downloads]: https://img.shields.io/github/downloads/Ajimaru/OctoPrint-SwapXYZ/total?style=flat-square&logo=github&logoColor=white&label=downloads
[badge-ci]: https://img.shields.io/github/actions/workflow/status/Ajimaru/OctoPrint-SwapXYZ/ci.yml?branch=main&style=flat-square&logo=githubactions&logoColor=white&label=CI
[badge-codeql]: https://img.shields.io/github/actions/workflow/status/Ajimaru/OctoPrint-SwapXYZ/codeql.yml?branch=main&style=flat-square&logo=githubactions&logoColor=white&label=CodeQL
[badge-last-commit]: https://img.shields.io/github/last-commit/Ajimaru/OctoPrint-SwapXYZ?style=flat-square&logo=github&logoColor=white
[badge-license]: https://img.shields.io/github/license/Ajimaru/OctoPrint-SwapXYZ?style=flat-square&logo=gnu&logoColor=white
[badge-octoprint]: https://img.shields.io/badge/OctoPrint-1.11.8%2B-1a9f29?style=flat-square&logo=octoprint&logoColor=white
[badge-python]: https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square&logo=python&logoColor=white
[badge-prs]: https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square
