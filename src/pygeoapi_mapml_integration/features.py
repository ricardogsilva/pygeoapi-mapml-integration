import json
import logging

import flask

from . import (
    config,
    constants,
    schemas,
    utils,
)

logger = logging.getLogger(__name__)


def prepare_mapml_features_response(
    collection_id: str,
    pygeoapi_items_reponse: flask.Response
) -> flask.Response:
    original_response_body = json.loads(pygeoapi_items_reponse.get_data(as_text=True))
    mapml_features = [
        schemas.MapMlFeature.from_geojson_dict(f)
        for f in original_response_body.get("features", [])
    ]
    pygeoapi_config = config.get_pygeoapi_config()
    collection_config = pygeoapi_config.get("resources", {}).get(collection_id, {})
    jinja_env = config.get_jinja_environment()
    template = jinja_env.get_template("collections/items/item.mapml")
    tiled_crs = "OSMTILE"
    extent = utils.get_mapml_extent(
        collection_config,
        output_crs_uri=utils.get_crs_uri("WGS84")
    )
    context = {
        "title": collection_config.get("title", collection_id),
        "tiled_crs": tiled_crs,
        "coordinate_system": "gcrs",
        "extent": extent,
        "features": mapml_features,
    }
    logger.debug(f"{context=}")
    payload = template.render(data=context)
    pygeoapi_items_reponse.set_data(payload)
    return pygeoapi_items_reponse

