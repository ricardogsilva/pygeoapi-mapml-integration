import dataclasses


@dataclasses.dataclass(frozen=True)
class MapMlFeature:
    properties: dict
    geometry: str

    @classmethod
    def from_geojson_dict(cls, feature: dict) -> "MapMlFeature":
        geom = feature.get("geometry")
        coord_format = ".8f"
        if (type_ := geom.get("type")) == "Point":
            coords = geom.get("coordinates")
            representation = (
                f"<map-point><map-coordinates>"
                f"{' '.join(f'{{c:{coord_format}}}'.format(c=coord) for coord in coords)}"
                f"</map-coordinates></map-point>")
        elif type_ == "LineString":
            coords = geom.get("coordinates")
            representation = (
                f"<map-linestring><map-coordinates>"
                f"{' '.join(f'{{c:{coord_format}}}'.format(c=coord) for coord in coords)}"
                f"</map-coordinates></map-linestring>")
        elif type_ == "Polygon":
            representation = "<map-polygon>"
            for ring in geom.get("coordinates", []):
                representation+= (
                    f"<map-coordinates>"
                    f"{' '.join(f'{{c:{coord_format}}}'.format(c=coord) for coord in ring)}"
                    f"</map-coordinates"
                )
            representation += "</map-polygon>"
        else:
            raise NotImplementedError(f"{type_!r} is not implemented yet")
        return cls(
            properties=feature.get("properties", {}),
            geometry=representation
        )