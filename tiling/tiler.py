from tiling.tile import Tile
from tiling.sphmerc import GoogleProjection
from tiling.dem import DEM
import urllib
from PIL import Image
import io
import os
import requests

class Tiler:
    def __init__(self, url, z=13):
        self.tile = Tile(-1, -1, z)
        self.url = url
        self.sphMerc = GoogleProjection()
        self.indexedTiles = { }

    def setZoom(self, z):
        self.tile.z = z

    def lonLatToSphMerc(self, lonlat):
        return self.sphMerc.project(lonlat)

    def getTile(self, sphMercPos, z):
        return self.sphMerc.getTile(sphMercPos, z)

    def update(self, pos):
        loaded_data = { }
        t = self.needNewData(pos)
        if t is not None:
            tiles_x = range(t.x-1, t.x+2)
            tiles_y = range(t.y-1, t.y+2)
            for tx in tiles_x:
                for ty in tiles_y:
                    this_tile = Tile(tx, ty, t.z)
                    data = self.loadTile(this_tile)
                    if data is not None:
                        loaded_data["{this_tile.z}/{this_tile.x}/{this_tile.y}"] = data


        return loaded_data

    
    def needNewData(self, pos):
        if self.tile is not None:
            new_tile = self.sphMerc.getTile(pos, self.tile.z)
            need_update = new_tile.x != self.tile.x or new_tile.y != self.tile.y
            self.tile = new_tile
            return new_tile if need_update else None
                
        return None 
            
    
    def loadTile(self, tile):
        tile_index = f"{tile.z}/{tile.x}/{tile.y}"
        tile_dir = f"{os.environ.get('CACHEDIR')}/{tile.z}/{tile.x}"
        cache_file = f"{tile_dir}/{tile.y}.png"
        if not os.path.exists(tile_dir):
            os.makedirs(tile_dir)
        if self.indexedTiles.get(tile_index) is None:
            if os.path.isfile(cache_file):
                tdata = self.readTile(cache_file) 
            else:
                tdata = self.readTile(cache_file, self.url.replace("{x}", str(tile.x)).replace("{y}", str(tile.y)).replace("{z}", str(tile.z)))
            if tdata is not None:
                self.indexedTiles[tile_index] = self.rawTileToStoredTile(tile, tdata[0], tdata[1], tdata[2])
                return self.indexedTiles[tile_index]
        return None

    def readTile(self, cache_file, url=None):
        if url is not None:
            response = requests.get(url) 
            with open(cache_file, "wb") as fp:
                fp.write(response.content)
            if response.status_code == 200:
                im = Image.open(io.BytesIO(response.content))
        else:
            im = Image.open(cache_file)
        data = im.getdata()
        elevs = [int(value[0] * 256 + value[1] + value[2] / 256) - 32768 for value in data]

        w = im.size[0] 
        h = im.size[1] 
        
        return (elevs, w, h)
 
    def getData(self, sphMercPos):
        self.update(sphMercPos)
        this_tile = self.sphMerc.getTile(sphMercPos, self.tile.z)
        return self.indexedTiles[f"{self.tile.z}/{this_tile.x}/{this_tile.y}"]

    def rawTileToStoredTile(self, tile, data, w, h):
        top_right = tile.getTopRight()
        bottom_left = tile.getBottomLeft()
        x_spacing = (top_right[0] - bottom_left[0]) / (w - 1)
        y_spacing = (top_right[1] - bottom_left[1]) / (h - 1)
        return DEM (data, bottom_left, w, h, x_spacing, y_spacing)
