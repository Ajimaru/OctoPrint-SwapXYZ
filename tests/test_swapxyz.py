import pytest

from octoprint_swapxyz import SwapXYZPlugin


class FakeSettings:
    def __init__(self, values):
        self.values = values

    def get_boolean(self, path):
        node = self.values
        for key in path:
            node = node[key]
        return bool(node)


def make_plugin(swap=True, reverse=None):
    plugin = SwapXYZPlugin.__new__(SwapXYZPlugin)
    plugin._settings = FakeSettings(
        {
            "swap": swap,
            "reverse": {"X": False, "Y": False, "Z": False, **(reverse or {})},
        }
    )
    return plugin


JOG_TAGS = {"trigger:printer.jog", "source:api"}


def jog(plugin, cmd, tags=JOG_TAGS):
    return plugin.rewrite_jog(
        None, "queuing", cmd, None, cmd.split()[0], tags=tags
    )


@pytest.mark.parametrize(
    ("swap", "reverse", "command", "expected"),
    [
        (True, None, "G1 X10", "G1 Y10"),
        (True, None, "G1 Y10", "G1 X10"),
        (False, None, "G1 X10", "G1 X10"),
        (False, None, "G1 Y10", "G1 Y10"),
        # The reverse option follows the axis sent to the printer, not the
        # axis of the button that was pressed.
        (True, {"Y": True}, "G1 X10", "G1 Y-10"),
        (True, {"Y": True}, "G1 X-10", "G1 Y10"),
        (True, {"X": True}, "G1 Y10", "G1 X-10"),
        (False, {"Y": True}, "G1 Y10", "G1 Y-10"),
        (False, {"Y": True}, "G1 Y-10", "G1 Y10"),
        (True, {"Z": True}, "G1 Z10", "G1 Z-10"),
        (False, {"Z": True}, "G1 Z-10", "G1 Z10"),
        (True, {"Z": True}, "G1 Z10 F600", "G1 Z-10 F600"),
    ],
)
def test_rewrite_jog(swap, reverse, command, expected):
    plugin = make_plugin(swap=swap, reverse=reverse)
    assert jog(plugin, command) == (expected,)


def test_z_is_never_swapped():
    plugin = make_plugin(swap=True)
    assert jog(plugin, "G1 Z5") == ("G1 Z5",)


def test_reverse_of_original_axis_is_ignored_while_swapping():
    plugin = make_plugin(swap=True, reverse={"X": True})
    assert jog(plugin, "G1 X10") == ("G1 Y10",)


def test_non_jog_commands_are_ignored():
    plugin = make_plugin(swap=True)
    assert jog(plugin, "G1 X10", tags={"trigger:printer.commands"}) is None


def test_missing_tags_are_ignored():
    plugin = make_plugin(swap=True)
    assert jog(plugin, "G1 X10", tags=None) is None


def test_reverse_axis_without_configuration_keeps_command():
    plugin = make_plugin(swap=True)
    assert plugin.reverse_axis("G1 Y10", "Y") == "G1 Y10"


def test_reverse_axis_flips_both_directions():
    plugin = make_plugin(swap=True, reverse={"Y": True})
    assert plugin.reverse_axis("G1 Y10", "Y") == "G1 Y-10"
    assert plugin.reverse_axis("G1 Y-10", "Y") == "G1 Y10"
