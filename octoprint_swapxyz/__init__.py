# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class SwapXYZPlugin(octoprint.plugin.SettingsPlugin, octoprint.plugin.TemplatePlugin):
	config_version_key = "0.3.0"

	other = dict(X="Y", Y="X")

	def on_plugin_enabled(self):
		pass

	def on_plugin_disabled(self):
		pass

	def get_update_information(self):
		return dict(
			swapxyz=dict(
				displayName="SwapXYZ",
				displayVersion=self._plugin_version,

				# version check: GitHub releases
				type="github_release",
				user="Ajimaru",
				repo="OctoPrint-SwapXYZ",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/Ajimaru/OctoPrint-SwapXYZ/archive/{target_version}.zip"
			)
		)

	def get_settings_defaults(self):
		return dict(
			reverse=dict(
				X=False,
				Y=False,
				Z=False,
			),
			swap=True
		)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False),
		]

	def is_template_autoescaped(self):
		# Our template only renders translated text and static markup, so
		# autoescaping is safe. Required as of OctoPrint 2.1.0.
		return True

	def rewrite_jog(self, comm_instance, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
		"""
		Replace X with Y or Y with X in gcode initiated by jog commands, and
		reverse the direction of any axis configured for it.
		"""
		if "trigger:printer.jog" not in tags:
			# Ignore normal gcode commands, only affect control buttons
			return

		for axis in ["X", "Y"]:
			if axis in cmd:
				if self._settings.get_boolean(["swap"]):
					# Swap to other axis
					new_axis = self.other[axis]
					cmd = cmd.replace(axis, new_axis)
				else:
					# Do not swap
					new_axis = axis

				cmd = self.reverse_axis(cmd, new_axis)

				# Don't switch it back by iterating again
				break
		else:
			# Z is never swapped, it has no partner axis, so only reverse it
			if "Z" in cmd:
				cmd = self.reverse_axis(cmd, "Z")

		return cmd,

	def reverse_axis(self, cmd, axis):
		"""
		Flip the sign of the given axis in cmd, if it is configured for reversal.
		"""
		if not self._settings.get_boolean(["reverse", axis]):
			return cmd

		negative = axis + "-"

		if negative in cmd:
			cmd = cmd.replace(negative, axis)
		elif axis in cmd:
			cmd = cmd.replace(axis, negative)

		return cmd

__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = SwapXYZPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.rewrite_jog,
	}
