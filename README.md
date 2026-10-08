# SwapXYZ

An OctoPrint plugin to swap the X and Y axes used by the jog controls, and to reverse the direction of the X, Y or Z axis.

## Setup

Install manually via OctoPrint's plugin manager using this URL:

```
https://github.com/Ajimaru/OctoPrint-SwapXYZ/archive/refs/heads/main.zip
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

# Advanced

Archive URL: https://github.com/Ajimaru/OctoPrint-SwapXYZ/archive/refs/heads/main.zip

Upstream project: https://gitlab.com/wolframmfg/octoprint-swapxy

---

Developed by

[![Wolfram Manufacturing](https://github.com/Ajimaru/OctoPrint-SwapXYZ/raw/main/wolframmfg.png)](https://wolframmfg.com/)
