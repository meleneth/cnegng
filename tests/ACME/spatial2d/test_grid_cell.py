import pytest
from flexmock import flexmock
from collections import defaultdict

from cnegng.ACME.spatial2d import GridCell, GridCoord
from cnegng.ACME.spatial2d import Grid, Area

class DemoItem:
    def __init__(self):
        self.current_cell = None

@pytest.fixture
def sample_area():
    """Provide a sample Area instance."""
    return Area(top=0, left=0, bottom=10, right=10)

@pytest.fixture
def grid_cell(sample_area):
    """Provide a GridCell instance."""
    return GridCell(sample_area, grid_coord=GridCoord(1, 1))

def test_gridcell_add_default_layer(grid_cell):
    obj = DemoItem()
    
    # Add an object to the default layer
    grid_cell.add(obj)
    
    # Assert the object was added to the default layer
    assert grid_cell.is_in_layer(obj, 'default')

def test_gridcell_add_custom_layer(grid_cell):
    obj = DemoItem()
    
    # Add an object to a custom layer
    grid_cell.add(obj, layer='custom_layer')
    
    # Assert the object was added to the custom layer
    assert grid_cell.is_in_layer(obj, 'custom_layer')

def test_gridcell_remove_object(grid_cell):
    obj = DemoItem()
    
    # Add and remove the object
    grid_cell.add(obj)
    grid_cell.remove(obj)
    
    # Assert the object was removed from the default layer
    assert not grid_cell.is_in_layer(obj, 'default')

def test_gridcell_remove_from_custom_layer(grid_cell):
    obj = DemoItem()
    
    # Add and remove the object from a custom layer
    grid_cell.add(obj, layer='custom_layer')
    grid_cell.remove(obj, layer='custom_layer')
    
    # Assert the object was removed from the custom layer
    assert not grid_cell.is_in_layer(obj, 'custom_layer')

def test_gridcell_contents_cleanup(grid_cell):
    obj = DemoItem()
    
    # Add and remove the object, then ensure the layer is cleaned up
    grid_cell.add(obj, layer='custom_layer')
    grid_cell.remove(obj, layer='custom_layer')
    
    # Assert that the custom layer is removed after the object is deleted
    assert 'custom_layer' not in grid_cell.contents

def test_gridcell_mock_add():
    obj = DemoItem()

    # Flexmock for add method
    mock_cell = flexmock(GridCell(Area(0, 0, 10, 10), cell_index=1))
    
    # Expecting add method to be called with a specific object
    mock_cell.should_receive('add').with_args(obj, layer='default').once()
    
    # Triggering the call
    mock_cell.add(obj, layer='default')

def test_gridcell_mock_remove():
    obj = DemoItem()

    # Flexmock for remove method
    mock_cell = flexmock(GridCell(Area(0, 0, 10, 10), cell_index=1))
    
    # Expecting remove method to be called with a specific object
    mock_cell.should_receive('remove').with_args(obj, layer='default').once()
    
    # Triggering the call
    mock_cell.remove(obj, layer='default')
