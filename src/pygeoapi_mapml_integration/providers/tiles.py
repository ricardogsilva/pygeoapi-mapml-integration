import logging
from typing import Optional

import pyproj

from pygeoapi.provider.wmts_facade import WMTSFacadeProvider
from pygeoapi.util import render_j2_template

from .. import (
    config,
    constants,
    utils,
)

_MAPML = "mapml"
logger = logging.getLogger(__name__)


class MapMlBaseTileProvider(WMTSFacadeProvider):

    def get_metadata(
        self,
        dataset: str,
        server_url: str,
        layer=None,
        tileset: Optional[str] = None,
        metadata_format: Optional[str] = _MAPML,
        title: Optional[str] = None,
        description: Optional[str] = None,
        keywords=None,
        **kwargs
    ) -> dict:
        """Provide data/file metadata"""

        if (metadata_format or _MAPML).lower() == _MAPML:
            metadata = self.get_mapml_metadata(
                dataset, server_url, layer, tileset, title, description, keywords,
                **kwargs
            )
            jinja_env = config.get_jinja_environment()
            template = jinja_env.get_template("collections/tiles/metadata.mapml")
            result = template.render(data=metadata)
        else:
            result = super().get_metadata(
                dataset, server_url, layer, tileset, title, description, keywords,
                **kwargs
            )
        return result

    def get_mapml_metadata(
        self,
        dataset,
        server_url,
        layer,
        tileset,
        title,
        description,
        keywords,
        **kwargs
    ):
        """Gets tile metadata as a mapml layer"""
        default_metadata = self.get_default_metadata(
            dataset, server_url, layer, tileset, title, description,
            keywords, **kwargs
        )
        pygeoapi_config = config.get_pygeoapi_config()
        extent = utils.get_mapml_extent(
            collection_config=pygeoapi_config["resources"][dataset],
            output_crs_uri=default_metadata["crs"]
        )
        return {
            **default_metadata,
            "extent": extent,
            "tiled_crs": utils.get_tiled_crs(default_metadata["crs"]) or "OSMTILE",
        }


class MapMlRasterTileProvider(MapMlBaseTileProvider):
    ...