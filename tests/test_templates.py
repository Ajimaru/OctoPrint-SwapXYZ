import os

import flask
import jinja2
import pytest

import octoprint.plugin
import octoprint_swapxyz
from octoprint_swapxyz import SwapXYZPlugin

PLUGIN_ID = "swapxyz"
PACKAGE_DIR = os.path.dirname(os.path.abspath(octoprint_swapxyz.__file__))


def make_plugin():
    plugin = SwapXYZPlugin.__new__(SwapXYZPlugin)
    # Normally set by OctoPrint's plugin manager; the default asset and
    # template folders are derived from it.
    plugin._basefolder = PACKAGE_DIR
    plugin._identifier = PLUGIN_ID
    return plugin


def make_app(plugin):
    """
    A Flask app that serves the plugin's static folder the way OctoPrint does.

    OctoPrint only registers a static route for plugins that implement
    AssetPlugin (or BlueprintPlugin), as blueprint "<id>" under the name
    prefix "plugin" - so the endpoint is "plugin.<id>.static". 0.4.1 called
    url_for("plugin_swapxyz.static") on a plugin without AssetPlugin, which
    raised a BuildError and replaced the whole settings pane with an error.
    """
    app = flask.Flask(__name__)
    if isinstance(plugin, octoprint.plugin.AssetPlugin):
        blueprint = flask.Blueprint(
            PLUGIN_ID, PLUGIN_ID, static_folder=plugin.get_asset_folder()
        )
        app.register_blueprint(
            blueprint, url_prefix=f"/plugin/{PLUGIN_ID}", name_prefix="plugin"
        )

    def gettext(text, **kwargs):
        return text % kwargs if kwargs else text

    app.jinja_env.globals["_"] = gettext
    app.jinja_loader = jinja2.FileSystemLoader(
        plugin.get_template_folder()
    )
    return app


def test_plugin_serves_its_static_folder():
    assert isinstance(make_plugin(), octoprint.plugin.AssetPlugin)


@pytest.mark.parametrize("template", ["swapxyz_settings.jinja2"])
def test_template_renders(template):
    plugin = make_plugin()
    app = make_app(plugin)
    with app.test_request_context():
        html = flask.render_template(template)
    assert "SwapXYZ" in html


def test_settings_icon_url_points_at_an_existing_file():
    plugin = make_plugin()
    app = make_app(plugin)
    with app.test_request_context():
        html = flask.render_template("swapxyz_settings.jinja2")
    url = f"/plugin/{PLUGIN_ID}/static/img/swapxyz.svg"
    assert f'src="{url}"' in html
    response = app.test_client().get(url)
    assert response.status_code == 200
    assert b"<svg" in response.data
