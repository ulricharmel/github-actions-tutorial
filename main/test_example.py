import numpy as np
import pytest


def test_check_kalcal_import():
    """Test if you can import kalcal."""

    # TODO - Import the module kalcal
    pass


def test_jones_correct_dimensions():
    """Test if dimensions of jones is correct."""

    # Open datafile and extract jones
    with open("normal.npy", "rb") as data:
        jones = np.load(data)

    # TODO - Check the dimensions of jones matrix
    pass