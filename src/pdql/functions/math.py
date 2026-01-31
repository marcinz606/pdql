from typing import Any, Union, Optional
from pdql.expressions import SQLFunction


def abs(x: Any) -> SQLFunction:
    """Computes the absolute value of X."""
    return SQLFunction("ABS", x)


def acos(x: Any) -> SQLFunction:
    """Computes the inverse cosine of X."""
    return SQLFunction("ACOS", x)


def acosh(x: Any) -> SQLFunction:
    """Computes the inverse hyperbolic cosine of X."""
    return SQLFunction("ACOSH", x)


def asin(x: Any) -> SQLFunction:
    """Computes the inverse sine of X."""
    return SQLFunction("ASIN", x)


def asinh(x: Any) -> SQLFunction:
    """Computes the inverse hyperbolic sine of X."""
    return SQLFunction("ASINH", x)


def atan(x: Any) -> SQLFunction:
    """Computes the inverse tangent of X."""
    return SQLFunction("ATAN", x)


def atan2(y: Any, x: Any) -> SQLFunction:
    """Computes the inverse tangent of Y/X, using the signs of Y and X to determine the quadrant."""
    return SQLFunction("ATAN2", [y, x])


def atanh(x: Any) -> SQLFunction:
    """Computes the inverse hyperbolic tangent of X."""
    return SQLFunction("ATANH", x)


def ceil(x: Any) -> SQLFunction:
    """Gets the smallest integral value that isn't less than X."""
    return SQLFunction("CEIL", x)


def ceiling(x: Any) -> SQLFunction:
    """Synonym of CEIL."""
    return SQLFunction("CEILING", x)


def cos(x: Any) -> SQLFunction:
    """Computes the cosine of X."""
    return SQLFunction("COS", x)


def cosh(x: Any) -> SQLFunction:
    """Computes the hyperbolic cosine of X."""
    return SQLFunction("COSH", x)


def cot(x: Any) -> SQLFunction:
    """Computes the cotangent of X."""
    return SQLFunction("COT", x)


def coth(x: Any) -> SQLFunction:
    """Computes the hyperbolic cotangent of X."""
    return SQLFunction("COTH", x)


def exp(x: Any) -> SQLFunction:
    """Computes e to the power of X."""
    return SQLFunction("EXP", x)


def floor(x: Any) -> SQLFunction:
    """Gets the largest integral value that isn't greater than X."""
    return SQLFunction("FLOOR", x)


def ln(x: Any) -> SQLFunction:
    """Computes the natural logarithm of X."""
    return SQLFunction("LN", x)


def log(x: Any, y: Optional[Any] = None) -> SQLFunction:
    """Computes the natural logarithm of X or the logarithm of X to base Y."""
    if y is None:
        return SQLFunction("LOG", x)
    return SQLFunction("LOG", [x, y])


def log10(x: Any) -> SQLFunction:
    """Computes the natural logarithm of X to base 10."""
    return SQLFunction("LOG10", x)


def mod(x: Any, y: Any) -> SQLFunction:
    """Gets the remainder of the division of X by Y."""
    return SQLFunction("MOD", [x, y])


def pow(x: Any, y: Any) -> SQLFunction:
    """Produces the value of X raised to the power of Y."""
    return SQLFunction("POW", [x, y])


def power(x: Any, y: Any) -> SQLFunction:
    """Synonym of POW."""
    return SQLFunction("POWER", [x, y])


def rand() -> SQLFunction:
    """Generates a pseudo-random value of type FLOAT64 in the range of [0, 1)."""
    return SQLFunction("RAND")


def round(x: Any, n: Optional[int] = None) -> SQLFunction:
    """Rounds X to the nearest integer or rounds X to N decimal places."""
    if n is None:
        return SQLFunction("ROUND", x)
    return SQLFunction("ROUND", [x, n])


def sign(x: Any) -> SQLFunction:
    """Produces -1, 0, or +1 for negative, zero, and positive arguments respectively."""
    return SQLFunction("SIGN", x)


def sin(x: Any) -> SQLFunction:
    """Computes the sine of X."""
    return SQLFunction("SIN", x)


def sinh(x: Any) -> SQLFunction:
    """Computes the hyperbolic sine of X."""
    return SQLFunction("SINH", x)


def sqrt(x: Any) -> SQLFunction:
    """Computes the square root of X."""
    return SQLFunction("SQRT", x)


def tan(x: Any) -> SQLFunction:
    """Computes the tangent of X."""
    return SQLFunction("TAN", x)


def tanh(x: Any) -> SQLFunction:
    """Computes the hyperbolic tangent of X."""
    return SQLFunction("TANH", x)


def trunc(x: Any, n: Optional[int] = None) -> SQLFunction:
    """Rounds a number towards zero."""
    if n is None:
        return SQLFunction("TRUNC", x)
    return SQLFunction("TRUNC", [x, n])
