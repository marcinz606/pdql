from typing import Any, List
from pdql.expressions import SQLFunction


def st_area(geog: Any) -> SQLFunction:
    """Gets the area covered by the polygons in a GEOGRAPHY value."""
    return SQLFunction("ST_AREA", geog)


def st_astext(geog: Any) -> SQLFunction:
    """Converts a GEOGRAPHY value to a STRING WKT geography value."""
    return SQLFunction("ST_ASTEXT", geog)


def st_centroid(geog: Any) -> SQLFunction:
    """Gets the centroid of a GEOGRAPHY value."""
    return SQLFunction("ST_CENTROID", geog)


def st_contains(geog1: Any, geog2: Any) -> SQLFunction:
    """Checks if one GEOGRAPHY value contains another GEOGRAPHY value."""
    return SQLFunction("ST_CONTAINS", [geog1, geog2])


def st_distance(geog1: Any, geog2: Any) -> SQLFunction:
    """Gets the shortest distance in meters between two GEOGRAPHY values."""
    return SQLFunction("ST_DISTANCE", [geog1, geog2])


def st_geogpoint(longitude: Any, latitude: Any) -> SQLFunction:
    """Creates a point GEOGRAPHY value for a given longitude and latitude."""
    return SQLFunction("ST_GEOGPOINT", [longitude, latitude])


def st_intersects(geog1: Any, geog2: Any) -> SQLFunction:
    """Checks if at least one point appears in two GEOGRAPHY values."""
    return SQLFunction("ST_INTERSECTS", [geog1, geog2])


def st_length(geog: Any) -> SQLFunction:
    """Gets the total length of lines in a GEOGRAPHY value."""
    return SQLFunction("ST_LENGTH", geog)


def st_union(*args: Any) -> SQLFunction:
    """Gets the point set union of multiple GEOGRAPHY values."""
    return SQLFunction("ST_UNION", list(args))
