
class Tile:
    EARTH = 40075016.68
    HALF_EARTH = 20037508.34

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getMetresInTile(self):
        return Tile.EARTH / (2**self.z)
        

    def getBottomLeft(self):
        metres_in_tile = self.getMetresInTile()
        return (self.x * metres_in_tile - Tile.HALF_EARTH, Tile.HALF_EARTH - (self.y+1)*metres_in_tile)

    def getTopRight(self):
        p = self.getBottomLeft()
        metres_in_tile = self.getMetresInTile()
        return [coord+metres_in_tile for coord in p]

    def __str__(self):
        return f"Tile: {self.x},{self.y},{self.z}"
