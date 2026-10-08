# SwapXYZ

An OctoPrint plugin to swap the X and Y axes used by the jog controls.

## Setup

Install manually via OctoPrint's plugin manager using this URL:

```
https://github.com/Ajimaru/OctoPrint-SwapXYZ/archive/refs/heads/main.zip
```

This plugin is a fork of [SwapXY](https://plugins.octoprint.org/plugins/swapxy/) by Wolfram Manufacturing.

As long as the plugin is enabled, the jog buttons for X and Y will
drive the other axis instead.

To drive one or both of these axes in the opposite direction (negative/positive), enable the reverse option for that axis.

## Config

These options can also be changed from the web UI settings window.

Default config:

```yaml
plugins:
    swapxyz:
        reverse:
            X: false
            Y: false
```

# Advanced

Archive URL: https://github.com/Ajimaru/OctoPrint-SwapXYZ/archive/refs/heads/main.zip

Upstream project: https://gitlab.com/wolframmfg/octoprint-swapxy

---

Developed by

[![Wolfram Manufacturing](https://github.com/Ajimaru/OctoPrint-SwapXYZ/raw/main/wolframmfg.png)](https://wolframmfg.com/)
