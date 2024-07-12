import functools

import jinja2
from pygeoapi.config import get_config


@functools.lru_cache
def get_jinja_environment() -> jinja2.Environment:
    return jinja2.Environment(loader=jinja2.PackageLoader("pygeoapi_mapml_integration"))


@functools.lru_cache
def get_pygeoapi_config() -> dict:
    return get_config()