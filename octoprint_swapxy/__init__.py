# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class SwapXYPlugin(octoprint.plugin.OctoPrintPlugin):
	def on_plugin_enabled(self):
		pass

	def on_plugin_disabled(self):
		pass

	def get_update_information(self):
		return dict(
			swapxy=dict(
				displayName="SwapXY",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="klikini",
				repo="OctoPrint-SwapXY",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/klikini/OctoPrint-SwapXY/archive/{target_version}.zip"
			)
		)

	def rewrite_jog(self, comm_instance, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
		"""
		Replace X with Y or Y with X in gcode initiated by jog commands.
		"""
		if "trigger:printer.jog" not in tags:
			return

		if "X" in cmd:
			cmd = cmd.replace("X", "Y")
		elif "Y" in cmd:
			cmd = cmd.replace("Y", "X")

		return cmd,

__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = SwapXYPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.rewrite_jog,
	}
