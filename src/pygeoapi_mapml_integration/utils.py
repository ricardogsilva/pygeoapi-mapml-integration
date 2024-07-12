import logging
import pyproj
import typing

from . import constants

logger = logging.getLogger(__name__)


def get_tiled_crs(crs_uri: str) -> typing.Optional[str]:
    for known_uri, known_tiled in constants.TILED_CRS_MAP.items():
        if known_uri == crs_uri:
            return known_tiled


def get_crs_uri(tiled_crs: str) -> typing.Optional[str]:
    for known_uri, known_tiled in constants.TILED_CRS_MAP.items():
        if known_tiled == tiled_crs:
            return known_uri


def get_mapml_extent(
    collection_config: dict,
    output_crs_uri: str
) -> typing.Optional[dict[str, float]]:
    if (
            bbox := collection_config.get(
                "extents", {}).get("spatial", {}).get("bbox")
    ) is not None:
        crs_4326 = pyproj.CRS.from_epsg(4326)
        output_crs_code = output_crs_uri.rpartition("/")[-1]
        logger.debug(f"{output_crs_code}")
        if output_crs_code not in ("4326", "CRS84"):
            output_crs = pyproj.CRS.from_epsg(output_crs_code)
            transformer = pyproj.Transformer.from_crs(
                crs_4326, output_crs, always_xy=True)
            top_left = transformer.transform(bbox[0], bbox[1])
            bottom_right = transformer.transform(bbox[2], bbox[3])
            extent = {
                "top-left-easting": top_left[0],
                "top-left-northing": top_left[1],
                "bottom-right-easting": bottom_right[0],
                "bottom-right-northing": bottom_right[1],
            }
        else:
            extent = {
                "top-left-longitude": bbox[0],
                "top-left-latitude": bbox[1],
                "bottom-right-longitude": bbox[2],
                "bottom-right-latitude": bbox[3],
            }
    else:
        extent = None
    return extent
