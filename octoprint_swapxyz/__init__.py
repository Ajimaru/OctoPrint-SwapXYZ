# coding=utf-8
from __future__ import absolute_import

import re

import octoprint.plugin

class SwapXYZPlugin(octoprint.plugin.SettingsPlugin, octoprint.plugin.TemplatePlugin):
	config_version_key = "0.3.0"

	other = dict(X="Y", Y="X")
	number_pattern = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
	axis_pattern = re.compile(r"([XYZ])(" + number_pattern + r")")
	feedrate_pattern = re.compile(r"F(" + number_pattern + r")")

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
		if not tags or "trigger:printer.jog" not in tags:
			# Ignore normal gcode commands, only affect control buttons
			return

		swap = self._settings.get_boolean(["swap"])
		target_axes = set()

		def rewrite_axis(match):
			axis, value = match.groups()
			new_axis = self.other.get(axis, axis) if swap else axis
			target_axes.add(new_axis)
			return self.reverse_axis(new_axis + value, new_axis)

		# Rewrite each original word once, so X and Y cannot overwrite each other.
		cmd = self.axis_pattern.sub(rewrite_axis, cmd)

		if swap and target_axes.intersection(self.other):
			# OctoPrint chose F for the original axes. Respect the destination
			# profile speeds as well, while preserving slower requested speeds.
			profile = self._printer_profile_manager.get_current_or_default()
			max_speed = min(profile["axes"][axis.lower()]["speed"] for axis in target_axes)

			def limit_feedrate(match):
				if float(match.group(1)) > max_speed:
					return "F{}".format(max_speed)
				return match.group(0)

			cmd = self.feedrate_pattern.sub(limit_feedrate, cmd)

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
		elif axis + "+" in cmd:
			cmd = cmd.replace(axis + "+", negative)
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
