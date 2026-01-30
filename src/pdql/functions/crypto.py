from typing import Any
from pdql.expressions import SQLFunction


def md5(value: Any) -> SQLFunction:
    """Computes the hash of a STRING or BYTES value, using the MD5 algorithm."""
    return SQLFunction("MD5", value)


def sha1(value: Any) -> SQLFunction:
    """Computes the hash of a STRING or BYTES value, using the SHA-1 algorithm."""
    return SQLFunction("SHA1", value)


def sha256(value: Any) -> SQLFunction:
    """Computes the hash of a STRING or BYTES value, using the SHA-256 algorithm."""
    return SQLFunction("SHA256", value)


def sha512(value: Any) -> SQLFunction:
    """Computes the hash of a STRING or BYTES value, using the SHA-512 algorithm."""
    return SQLFunction("SHA512", value)


def farm_fingerprint(value: Any) -> SQLFunction:
    """Computes the fingerprint of a STRING or BYTES value."""
    return SQLFunction("FARM_FINGERPRINT", value)
