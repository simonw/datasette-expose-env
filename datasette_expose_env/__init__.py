from datasette import hookimpl
from datasette.utils.asgi import Response
import os
import textwrap


def get_config(datasette):
    config = datasette.plugin_config("datasette-expose-env") or {}
    if isinstance(config, list):
        config = {"variables": config}
    if "variables" not in config:
        config["variables"] = []
    config["show_all_redacted"] = bool(config.get("show_all_redacted"))
    return config


async def env(datasette):
    config = get_config(datasette)
    variables = config["variables"]
    if not variables:
        return Response.text(
            textwrap.dedent(
                """
                No environment variables exposed. Add this to your configuration:
                
                {
                    "plugins": {
                        "datasette-expose-env": {
                            "variables": [
                                "ENV_VAR_1",
                                "ENV_VAR_2",
                                "ENV_VAR_3",
                            ]
                        }
                    }
                }
                """
            ).strip()
        )
    output = []
    for key in variables:
        output.append("{}={}".format(key, os.environ.get(key, "<not set>")))
    if config["show_all_redacted"]:
        output.append("")
        for key in os.environ:
            if key not in variables:
                output.append("{}=...".format(key))
    return Response.text("\n".join(output))


@hookimpl
def register_routes():
    return [(r"^/-/env$", env)]
