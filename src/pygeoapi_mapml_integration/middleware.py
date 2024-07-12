import logging
import re

import flask
from werkzeug.wrappers import (
    Request,
    Response,
)

from . import (
    config,
    constants,
    features,
    schemas,
)

logger = logging.getLogger(__name__)


def modify_content_type(response: flask.Response):
    """Modify the content_type header to text/mapml, if originally requested.

    This function should be applied to the pygeoapi flask app using it's
    ``after_request`` method:

    More info:
        https://flask.palletsprojects.com/en/3.0.x/api/#flask.Flask.after_request

    """
    logger.debug(f"f arg: {flask.request.args.get('f')}")
    wants_mapml_response = (
            flask.request.args.get("f") == constants.MAPML_FORMAT_QUERY_STRING or
            constants.MAPML_MEDIA_TYPE in flask.request.headers.get("Accept", "")
    )
    if response.status_code == 200:
        if wants_mapml_response:
            response.headers["Content-Type"] = constants.MAPML_MEDIA_TYPE
            item_id_re_obj = re.search(
                r"/collections/(?P<collection_id>.*?)/items", flask.request.path)
            if item_id_re_obj is not None:
                collection_id = item_id_re_obj.groupdict()["collection_id"]
                response = features.prepare_mapml_features_response(
                    collection_id, response)
    return response
