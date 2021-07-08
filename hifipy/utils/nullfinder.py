import numpy as np
from scipy.optimize import brentq
from scipy.interpolate import interp1d


def roots_of_1d_array(x: np.ndarray, y: np.ndarray, kind: str = 'cubic', ytol=1e-15) -> np.array:
    roots = np.array([])

    if not len(x) == len(y):
        raise ValueError("x and y must contain the same number of elements")
    else:
        n = len(x)

    f = interp1d(x, y, kind=kind)

    for ix in range(0, n):
        if np.isclose(y[ix], 0, atol=ytol):
            roots = np.append(roots, x[ix])
        elif np.isclose(y[ix + 1], 0, atol=ytol) and ix + 1 == n:
            roots = np.append(roots, x[ix + 1])
        elif y[ix] * y[ix + 1] < 0:
            roots = np.append(roots, brentq(f, x[ix], x[ix + 1]))

    return (roots)

