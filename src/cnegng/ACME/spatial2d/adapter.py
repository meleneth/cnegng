from cnegng.ACME.spatial2d.dimensions import Dimensions
from cnegng.ACME.spatial2d.area import Area
from cnegng.ACME.spatial2d.position import Position

def DimensionsToArea(dimensions: Dimensions) -> Area :
    return Area(top=0, left =0, bottom =dimensions.height, right = dimensions.width)

def AreaToPosition(area: Area) -> Position :
    return Position(x=area.width, y = area.height)
