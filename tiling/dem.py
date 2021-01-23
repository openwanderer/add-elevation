# Direct conversion of freemaplib's DEM class to JavaScript and then Python. 
# from jsfreemaplib 0.3.x version 

import math
import sys

class DEM:
    def __init__ (self, elevs, bottomLeft, ptWidth, ptHeight, xSpacing, ySpacing):
        self.bottomLeft = bottomLeft
        self.ptWidth = ptWidth
        self.ptHeight = ptHeight
        self.elevs = elevs
        self.xSpacing = xSpacing
        self.ySpacing = ySpacing

    def getHeight (self, p):
        x_idx = math.floor((p[0] - self.bottomLeft[0]) / self.xSpacing)
        y_idx = self.ptHeight - math.ceil((p[1] - self.bottomLeft[1]) / self.ySpacing)
        h = sys.float_info.min
        
        if x_idx in range(self.ptWidth-1) and y_idx in range(self.ptHeight-1):
            h1 = self.elevs[y_idx*self.ptWidth+x_idx] 
            h2 = self.elevs[y_idx*self.ptWidth+x_idx+1] 
            h3 = self.elevs[y_idx*self.ptWidth+x_idx+self.ptWidth]
            h4 = self.elevs[y_idx*self.ptWidth+x_idx+self.ptWidth+1]

            x1 = self.bottomLeft[0] + x_idx * self.xSpacing
            x2 = x1 + self.xSpacing
            y1 = self.bottomLeft[1] + (self.ptHeight-1-y_idx) * self.ySpacing
            y2 = y1 - self.ySpacing

            prop_x = (p[0] - x1) / self.xSpacing
            htop = h1 * (1 - prop_x) + h2 * prop_x
            hbottom = h3 * (1 - prop_x) + h4 * prop_x

            prop_y = (p[1] - y2) / self.ySpacing
            h = hbottom * (1 - prop_y) + htop * prop_y


        return h
