"""Jog rewrite regressions; no OctoPrint server or printer is required."""
import itertools
from pathlib import Path
import runpy
import sys
import types
import unittest
from unittest.mock import patch


# Only the mixins are stubbed. Tests exercise the actual plugin implementation.
octoprint = types.ModuleType("octoprint")
octoprint.plugin = types.ModuleType("octoprint.plugin")
octoprint.plugin.SettingsPlugin = type("SettingsPlugin", (), {})
octoprint.plugin.TemplatePlugin = type("TemplatePlugin", (), {})
with patch.dict(sys.modules, {"octoprint": octoprint, "octoprint.plugin": octoprint.plugin}):
    SwapXYZPlugin = runpy.run_path(
        str(Path(__file__).resolve().parents[1] / "octoprint_swapxyz" / "__init__.py")
    )["SwapXYZPlugin"]


class Settings:
    def __init__(self, swap, reverse):
        self.values = {"swap": swap, "reverse": reverse}

    def get_boolean(self, path):
        value = self.values
        for key in path:
            value = value[key]
        return value


class JogTests(unittest.TestCase):
    def make_plugin(self, swap=True, reverse=()):
        plugin = SwapXYZPlugin()
        plugin._settings = Settings(swap, {axis: axis in reverse for axis in "XYZ"})
        plugin._printer_profile_manager = types.SimpleNamespace(
            get_current_or_default=lambda: {
                "axes": {"x": {"speed": 6000}, "y": {"speed": 300}, "z": {"speed": 200}}
            }
        )
        return plugin

    def rewrite(self, cmd, swap=True, reverse=()):
        result = self.make_plugin(swap, reverse).rewrite_jog(
            None, "queuing", cmd, None, cmd.split()[0], tags={"trigger:printer.jog"}
        )
        return result[0]

    def test_swap_both_axes_simultaneously(self):
        self.assertEqual(self.rewrite("G0 X10 Y20 F300"), "G0 Y10 X20 F300")
        self.assertEqual(self.rewrite("G0 Y20 X10 F300"), "G0 X20 Y10 F300")

    def test_reverse_all_axes_without_swap(self):
        self.assertEqual(
            self.rewrite("G0 X10 Y-20 Z5 F200", swap=False, reverse="XYZ"),
            "G0 X-10 Y20 Z-5 F200",
        )

    def test_reverse_destination_axes_with_swap(self):
        self.assertEqual(
            self.rewrite("G0 X10 Y-20 Z5 F200", reverse="YZ"),
            "G0 Y-10 X-20 Z-5 F200",
        )

    def test_single_axis_settings_matrix(self):
        for swap in (False, True):
            for bits in itertools.product((False, True), repeat=3):
                reverse = {axis for axis, enabled in zip("XYZ", bits) if enabled}
                for axis in "XYZ":
                    for value in (-10, 10):
                        with self.subTest(swap=swap, reverse=reverse, axis=axis, value=value):
                            target = {"X": "Y", "Y": "X", "Z": "Z"}[axis] if swap else axis
                            expected = -value if target in reverse else value
                            self.assertEqual(
                                self.rewrite("G0 {}{} F100".format(axis, value), swap, reverse),
                                "G0 {}{} F100".format(target, expected),
                            )

    def test_cap_speed_to_destination_profile(self):
        self.assertEqual(self.rewrite("G0 X10 F6000"), "G0 Y10 F300")

    def test_preserve_slower_requested_speed(self):
        self.assertEqual(self.rewrite("G0 X10 F100.5"), "G0 Y10 F100.5")
        self.assertEqual(self.rewrite("G0 Y10 F300"), "G0 X10 F300")

    def test_cap_to_slowest_destination_including_z(self):
        self.assertEqual(self.rewrite("G0 X10 Y20 Z5 F6000"), "G0 Y10 X20 Z5 F200")

    def test_do_not_cap_unswapped_moves(self):
        self.assertEqual(self.rewrite("G0 X10 F8000", swap=False), "G0 X10 F8000")
        self.assertEqual(self.rewrite("G0 Z5 F8000", reverse="Z"), "G0 Z-5 F8000")

    def test_decimal_signed_and_exponent_words(self):
        self.assertEqual(
            self.rewrite("G0X+.5Y-2.5Z1e-05F6e3", reverse="XYZ"),
            "G0Y-.5X2.5Z-1e-05F200",
        )

    def test_no_feedrate_or_mode_commands(self):
        self.assertEqual(self.rewrite("G0 X10 Y20 Z5"), "G0 Y10 X20 Z5")
        for command in ("G90", "G91"):
            self.assertEqual(self.rewrite(command), command)

    def test_ignore_non_jog_commands_and_missing_tags(self):
        for tags in (None, set(), {"source:file"}, {"trigger:printer.home"}):
            with self.subTest(tags=tags):
                self.assertIsNone(self.make_plugin().rewrite_jog(
                    None, "queuing", "G1 X10 Y20 Z5 F6000", None, "G1", tags=tags
                ))


if __name__ == "__main__":
    unittest.main()
