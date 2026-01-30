from typing import Any
from pdql.expressions import SQLFunction


def host(url: Any) -> SQLFunction:
    """Gets the hostname from a URL."""
    return SQLFunction("NET.HOST", url)


def ip_from_string(ip_string: Any) -> SQLFunction:
    """Converts an IPv4 or IPv6 address from a STRING value to a BYTES value."""
    return SQLFunction("NET.IP_FROM_STRING", ip_string)


def ip_to_string(ip_bytes: Any) -> SQLFunction:
    """Converts an IPv4 or IPv6 address from a BYTES value to a STRING value."""
    return SQLFunction("NET.IP_TO_STRING", ip_bytes)


def public_suffix(url: Any) -> SQLFunction:
    """Gets the public suffix from a URL."""
    return SQLFunction("NET.PUBLIC_SUFFIX", url)


def reg_domain(url: Any) -> SQLFunction:
    """Gets the registered or registrable domain from a URL."""
    return SQLFunction("NET.REG_DOMAIN", url)
