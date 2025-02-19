import pytest
from flexmock import flexmock

from cnegng.ACME.spatial2d.grid.object_container import ObjectContainer


class TestObjectContainer:
    @pytest.fixture
    def mock_object(self):
        """
        Creates a mock object with the necessary attributes for owner tracking.
        """
        return flexmock(owner=None)

    @pytest.fixture
    def mock_object2(self):
        """
        Creates a mock object with the necessary attributes for owner tracking.
        """
        return flexmock(owner=None)

    @pytest.fixture
    def owner(self):
        """
        Creates a mock owner.
        """
        return flexmock()

    @pytest.fixture
    def container(self, owner):
        """
        Creates an ObjectContainer instance.
        """
        return ObjectContainer(owner=owner, owner_attr_name="owner")

    def test_add_object_to_layer(self, container, mock_object):
        container.add(mock_object, layer=1)
        assert container.contains(mock_object, layer=1)
        assert container.size(layer=1) == 1

    def test_add_object_with_existing_owner_raises(self, container, mock_object):
        mock_object.owner = flexmock()  # Set non-None owner

        with pytest.raises(ValueError):
            container.add(mock_object, layer=0)

    def test_remove_object_from_layer(self, container, mock_object):
        container.add(mock_object, layer=2)
        container.remove(mock_object, layer=2)
        assert not container.contains(mock_object, layer=2)
        assert mock_object.owner is None

    def test_clear_layer(self, container, mock_object):
        container.add(mock_object, layer=3)
        container.clear(layer=3)
        assert not container.contains(mock_object, layer=3)

    def test_clear_all_layers(self, container, mock_object, mock_object2):
        container.add(mock_object, layer=1)
        container.add(mock_object2, layer=2)
        container.clear()
        assert container.size() == 0

    def test_get_all_objects_in_layer(self, container, mock_object):
        container.add(mock_object, layer=4)
        all_objects = container.get_all(layer=4)
        assert mock_object in all_objects
