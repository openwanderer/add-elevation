import math
from tiling.tile import Tile

class GoogleProjection:

    def project (self, lonlat):
        return (self.lonToGoogle(lonlat[0]), self.latToGoogle(lonlat[1]))

    def unproject (self, projected):
        return (self.googleToLon(projected[0]), self.googleToLat(projected[1]))

    def lonToGoogle (self, lon):
        return  (lon/180) * Tile.HALF_EARTH

    def latToGoogle(self, lat):
        y = math.log(math.tan((90+lat)*math.pi/360)) / (math.pi/180)
        return y * Tile.HALF_EARTH / 180.0

    def googleToLon(self, x):
        return (x / Tile.HALF_EARTH) * 180.0

    def googleToLat(self, y):
        lat = (y / Tile.HALF_EARTH) * 180.0
        return  180/math.pi * (2 * math.atan(math.exp(lat*math.pi/180)) - math.pi/2)

    def getTile(self, p, z):
        tile = Tile(-1, -1, z)
        metres_in_tile = tile.getMetresInTile()
        tile.x = math.floor((Tile.HALF_EARTH+p[0]) / metres_in_tile)
        tile.y = math.floor((Tile.HALF_EARTH-p[1]) / metres_in_tile)
        return tile

    def getTileFromLonLat(self, lonlat, z):
        return self.getTile((self.lonToGoogle(lonlat[0]), self.latToGoogle(lonlat[1])), z)
