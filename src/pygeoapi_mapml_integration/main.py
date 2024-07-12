import os
from pathlib import Path
from typing import Annotated

import flask
import typer

from . import middleware


app = typer.Typer()


@app.command()
def serve_pygeoapi(
    pygeoapi_config: Annotated[Path, typer.Argument(envvar="PYGEOAPI_CONFIG")],
    pygeoapi_openapi: Annotated[Path, typer.Argument(envvar="PYGEOAPI_OPENAPI")],
):
    """serve pygeoapi for development with its flask app and our custom middleware."""

    # this needs to be imported here, in order to allow us to manipulate the env
    os.environ["PYGEOAPI_CONFIG"] = str(pygeoapi_config)
    os.environ["PYGEOAPI_OPENAPI"] = str(pygeoapi_openapi)
    from pygeoapi import flask_app
    flask_app.APP.after_request(middleware.modify_content_type)
    flask_app.APP.run(
        debug=True,
        host=flask_app.api_.config["server"]["bind"]["host"],
        port=flask_app.api_.config["server"]["bind"]["port"],
    )
