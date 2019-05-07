import pytest
from hifipy.io import hifi_class


postpath = './sample_simulation_directory/post_out'


def test_instantiation():
    """The most minimal test."""
    try:
        instance = hifi_class(postpath)
    except Exception as exc:
        raise IOError from exc


@pytest.fixture
def hifi_class_instance():
    return hifi_class(postpath)


#def test_something(hifi_class_instance):
    #hifi_class_instance.postpath = "sdfa"


def test_attributes(hifi_class_instance):

    for attr in ['ni', 'Az', 'Bz', 'Vix', 'Viy', 'Viz', 'pp', 'dasffa']:
        eval(f"hifi_class_instance.{attr}")