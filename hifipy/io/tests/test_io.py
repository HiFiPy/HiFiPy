import pytest
from hifipy.io import hifi_class
import os

postpath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'sample_simulation_directory/post_out',
    )

physical_attributes = [
    'ni',
    'Az',
    'Bz',
    'Vix',
    'Viy',
    'Viz',
    'Jz',
    'pp',
    'nn',
    'Vnx',
    'Vny',
    'Vnz',
    'pn',
    'Bx',
    'By',
    ]

spatiotemporal_attributes = ['x', 'y', 'time']

metadata_attributes = ['name', 'Nx', 'Ny', 'Nt']

all_attributes = physical_attributes + spatiotemporal_attributes + metadata_attributes


def test_instantiation():
    """Check that hifi_class can be instantiated for a sample simulation."""
    try:
        instance = hifi_class(postpath)
    except Exception as exc:
        pytest.fail(f"Unable to instantiate hifi_class for {postpath}")


@pytest.fixture
def hifi_class_instance():
    try:
        return hifi_class(postpath)
    except Exception:
        return None


@pytest.mark.parametrize('var', all_attributes)
def test_attributes(hifi_class_instance, var):
    try:
        eval(f"hifi_class_instance.{var}")
    except Exception as exc:
        pytest.fail(f"Unable to evaluate hifi_class(postpath).{var} for postpath = {repr(postpath)}")


@pytest.mark.parametrize('var', physical_attributes)
def test_shape_of_physical_attributes(hifi_class_instance, var):
    Nx = hifi_class_instance.Nx
    Ny = hifi_class_instance.Ny
    Nt = hifi_class_instance.Nt
    expected_shape = (Nt, Ny, Nx)
    actual_shape = eval(f"hifi_class_instance.{var}.shape")
    if expected_shape != actual_shape:
        pytest.fail(f'Dimension mismath: {expected_shape} != {actual_shape}')

@pytest.mark.parametrize()