---
layout: plugin

id: swapxyz
title: SwapXYZ
description: Swap the X and Y axes used by the jog controls, and/or reverse the X, Y or Z axis
authors:
  - Ajimaru
license: GPLv3

date: 2026-11-07

homepage: https://github.com/Ajimaru/OctoPrint-SwapXYZ
source: https://github.com/Ajimaru/OctoPrint-SwapXYZ
archive: https://github.com/Ajimaru/OctoPrint-SwapXYZ/releases/latest/download/SwapXYZ-latest.zip

tags:
  - axis
  - jog
  - controls
  - ui

compatibility:
  octoprint:
    - 1.11.8
  python: ">=3.7,<4"
  os:
    - linux
    - macos
    - windows
---

SwapXYZ is a fork of
[SwapXY](https://plugins.octoprint.org/plugins/swapxy/) by Wolfram
Manufacturing.

While the plugin is enabled, the jog buttons for X and Y drive the other axis.
The reverse options flip the direction of the axis that is sent to the printer,
so the X, Y and Z buttons can be matched to printers whose axis orientation
differs from what OctoPrint expects.

The Z axis is never swapped, since it has no partner axis, but it can be
reversed. This helps on printers where the bed moves on Z instead of the print
head.

Swapping and reversing work on the classic serial connection. The connector
plugins introduced in OctoPrint 2.0 build their own gcode and bypass the
`octoprint.comm.protocol.gcode.queuing` hook, so the plugin has no effect there.

Options can be changed from the web UI settings window or via `config.yaml`:

```yaml
plugins:
    swapxyz:
        swap: true
        reverse:
            X: false
            Y: false
            Z: false
```
