from datasette import hookimpl
from datasette.utils.asgi import Response
import os
import textwrap


async def env(request, datasette):
    expose = datasette.plugin_config("datasette-expose-env") or []
    if not expose:
        return Response.text(
            textwrap.dedent(
                """
                No environment variables exposed. Add this to your configuration:
                
                {
                    "plugins": {
                        "datasette-expose-env": [
                            "ENV_VAR_1",
                            "ENV_VAR_2",
                            "ENV_VAR_3",
                        ]
                    }
                }
                """
            ).strip()
        )
    output = []
    for key in expose:
        output.append("{}={}".format(key, os.environ.get(key, "<not set>")))
    return Response.text("\n".join(output))


@hookimpl
def register_routes():
    return [(r"^/-/env$", env)]
