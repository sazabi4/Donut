
#
# Utility methods for DESI
#
import numpy
from collections import OrderedDict

class desiinfo(object):
    """ desiinfo is a class used to contain DESI FGA geometry information and various utility routines

    """

    def info(self):
        """info returns a dictionary chock full of info on the DESI FGA geometry
        keyed by the CCD name
        """

        infoDict = OrderedDict()

        # store a dictionary for each CCD, keyed by the CCD name
        infoDict["GFA1"] = {"xCenter": 1.318, "yCenter": 0.86, "FAflag": True, "CCDNUM": 1, "Offset": 1500,
                          "Extension": 1}

        return infoDict

    def __init__(self, **inputDict):

        self.infoDict = self.info()
        self.degperpixel = 5.97e-5 #pixel scale in deg/pixel assuming pixel size = 15 micron and focal length = 3.6 * 4 m
        self.rClear = 99999 # something for vignetting

    def __getstate__(self):
        stateDict = {}
        keysToPickle = ['infoDict', 'degperpixel', 'rClear']
        for key in keysToPickle:
            stateDict[key] = self.__dict__[key]
        return stateDict

    def __setstate__(self, state):
        for key in state:
            self.__dict__[key] = state[key]

    def getPosition(self, extname, ix, iy):
        """ return the x,y position in [mm] for a given CCD and pixel number
        note that the ix,iy are Image pixels - overscans removed - and start at zero
        """

        ccdinfo = self.infoDict[extname]

        # CCD size in pixels
        if ccdinfo["FAflag"]:
            xpixHalfSize = 512.
            ypixHalfSize = 512.
        else:
            print('WE ONLY HAVE FAflag CHIPS HERE!')

        # calculate positions
        xPos = ccdinfo["xCenter"] + (float(ix) - xpixHalfSize + 0.5) * self.degperpixel
        yPos = ccdinfo["yCenter"] + (float(iy) - ypixHalfSize + 0.5) * self.degperpixel

        return xPos, yPos

    def getPixel(self, extname, xPos, yPos):
        """ given a coordinate in [mm], return pixel number
        """

        ccdinfo = self.infoDict[extname]

        # CCD size in pixels
        if ccdinfo["FAflag"]:
            xpixHalfSize = 512.
            ypixHalfSize = 512.
        else:
            print('WE ONLY HAVE FAflag CHIPS HERE!')


        # calculate positions
        ix = (xPos - ccdinfo["xCenter"]) / self.degperpixel + xpixHalfSize - 0.5
        iy = (yPos - ccdinfo["yCenter"]) / self.degperpixel + ypixHalfSize - 0.5

        return ix, iy

    def getSensor(self, xPos, yPos):
        """ given x,y position on the focal plane, return the sensor name
        or None, if not interior to a chip
        """
        for ext in list(self.infoDict.keys()):
            ccdinfo = self.infoDict[ext]
            # is this x,y inside this chip?
            nxdif = numpy.abs((xPos - ccdinfo["xCenter"]) / self.degperpixel)
            nydif = numpy.abs((yPos - ccdinfo["yCenter"]) / self.degperpixel)

            # CCD size in pixels
            if ccdinfo["FAflag"]:
                xpixHalfSize = 512.
                ypixHalfSize = 512.
            else:
                print('WE ONLY HAVE FAflag CHIPS HERE!')

            if nxdif <= xpixHalfSize and nydif <= ypixHalfSize:
                return ext

        # get to here if we are not inside a chip
        #return None
        return ext # for test purpose, not matter where the position of the star, always return GFA1


class desiciinfo(object):
    """ desiinfo is a class used to contain DESI FGA geometry information and various utility routines

    """

    def info(self):
        """info returns a dictionary chock full of info on the DESI FGA geometry
        keyed by the CCD name
        """

        infoDict = OrderedDict()

        # store a dictionary for each CCD, keyed by the CCD name
        # NSWE is the sky postion.
        # Rotation here is defined as the rotation angle from chip frame to fiducial global frame, counter-clock wise is positive
        infoDict["CIW"] = {"xCenter": 1.57, "yCenter": 0., "FAflag": True, "CCDNUM": 5, "Offset": 1500,
                          "Extension": 1, "Rotation": -90}
        infoDict["CIS"] = {"xCenter": 0, "yCenter": -1.57, "FAflag": True, "CCDNUM": 4, "Offset": 1500,
                          "Extension": 2, "Rotation": 0}
        infoDict["CIC"] = {"xCenter": 0, "yCenter": 0., "FAflag": True, "CCDNUM": 3, "Offset": 1500,
                          "Extension": 3, "Rotation": 180}
        infoDict["CIN"] = {"xCenter": 0, "yCenter": 1.57, "FAflag": True, "CCDNUM": 2, "Offset": 1500,
                          "Extension": 4, "Rotation": 180}
        infoDict["CIE"] = {"xCenter": -1.57, "yCenter": 0., "FAflag": True, "CCDNUM": 1, "Offset": 1500,
                          "Extension": 5, "Rotation": 90}

        return infoDict

    def __init__(self, **inputDict):

        self.infoDict = self.info()
        self.degperpixel_c = 3.7025e-05 #14.81 / 1000. * 9. /3600 #pixel scale at center chip in deg/pixel
        self.degperpixel_t = 3.5550e-05 #14.22 / 1000. * 9. /3600 #tangential pixel scale at edge chips in deg/pixel
        self.degperpixel_r = 3.2775e-05 #13.11 / 1000. * 9. /3600 #radial pixel scale at edge chips in deg/pixel

        self.rClear = 99999 # something for vignetting, what should this be?

    def __getstate__(self):
        stateDict = {}
        keysToPickle = ['infoDict', 'degperpixel', 'rClear']
        for key in keysToPickle:
            stateDict[key] = self.__dict__[key]
        return stateDict

    def __setstate__(self, state):
        for key in state:
            self.__dict__[key] = state[key]

    def getPosition(self, extname, ix, iy):
        """ return the x,y position in deg on the sky (east is positive) for a given CCD and pixel number
        note that the ix,iy are Image pixels - overscans removed - and start at zero
        """

        ccdinfo = self.infoDict[extname]

        # CCD size in pixels
        if ccdinfo["FAflag"]:
            xpixHalfSize = 1536.
            ypixHalfSize = 1024.
        else:
            print('WE ONLY HAVE FAflag CHIPS HERE!')

        # calculate positions
        #xPos = ccdinfo["xCenter"] + (float(ix) - xpixHalfSize + 0.5) * self.degperpixel
        #yPos = ccdinfo["yCenter"] + (float(iy) - ypixHalfSize + 0.5) * self.degperpixel
        # Ting: not sure about this 0.5 pixel thing
        #CD1_1 = CDELT1 * cos (CROTA2)
        #CD1_2 = -CDELT2 * sin (CROTA2)
        #CD2_1 = CDELT1 * sin (CROTA2)
        #CD2_2 = CDELT2 * cos (CROTA2)

        # rotation matrix:
        #  XPos - XCen = CD1_1 * (ix - xpixHalfSize + 0.5) + CD1_2 * (iy - ypixHalfSize + 0.5)
        #  YPos - YCen = CD2_1 * (ix - xpixHalfSize + 0.5) + CD2_2 * (iy - ypixHalfSize + 0.5)
        # but XPos should be -Xpos # updated on Aug 30

        if extname == 'CIC':
            xPos = ccdinfo["xCenter"] + (float(ix) - xpixHalfSize + 0.5) * self.degperpixel_c * -1
            yPos = ccdinfo["yCenter"] + (float(iy) - ypixHalfSize + 0.5) * self.degperpixel_c * -1

        if extname == 'CIS':
            xPos = ccdinfo["xCenter"] + (float(ix) - xpixHalfSize + 0.5) * self.degperpixel_t * 1
            yPos = ccdinfo["yCenter"] + (float(iy) - ypixHalfSize + 0.5) * self.degperpixel_r * 1

        if extname == 'CIE':
            xPos = ccdinfo["xCenter"] + (float(iy) - ypixHalfSize + 0.5) * self.degperpixel_r * 1
            yPos = ccdinfo["yCenter"] + (float(ix) - xpixHalfSize + 0.5) * self.degperpixel_t * -1

        if extname == 'CIN':
            xPos = ccdinfo["xCenter"] + (float(ix) - xpixHalfSize + 0.5) * self.degperpixel_t * -1
            yPos = ccdinfo["yCenter"] + (float(iy) - ypixHalfSize + 0.5) * self.degperpixel_r * -1

        if extname == 'CIW':
            xPos = ccdinfo["xCenter"] + (float(iy) - ypixHalfSize + 0.5) * self.degperpixel_r * -1
            yPos = ccdinfo["yCenter"] + (float(ix) - xpixHalfSize + 0.5) * self.degperpixel_t * 1

        return xPos, yPos

    def getPixel(self, extname, xPos, yPos):
        """ given a coordinate in deg on the sky (east is positive), return pixel number
        """

        ccdinfo = self.infoDict[extname]

        # CCD size in pixels
        if ccdinfo["FAflag"]:
            xpixHalfSize = 3072./2
            ypixHalfSize = 2048./2
        else:
            print('WE ONLY HAVE FAflag CHIPS HERE!')


        # calculate positions
        #ix = (xPos - ccdinfo["xCenter"]) / self.degperpixel + xpixHalfSize - 0.5
        #iy = (yPos - ccdinfo["yCenter"]) / self.degperpixel + ypixHalfSize - 0.5


        if extname == 'CIC':
            ix = (xPos - ccdinfo["xCenter"]) / self.degperpixel_c * (-1) + xpixHalfSize - 0.5
            iy = (yPos - ccdinfo["yCenter"]) / self.degperpixel_c * (-1) + ypixHalfSize - 0.5

        if extname == 'CIS':
            ix = (xPos - ccdinfo["xCenter"]) / self.degperpixel_t * 1 + xpixHalfSize - 0.5
            iy = (yPos - ccdinfo["yCenter"]) / self.degperpixel_r * 1 + ypixHalfSize - 0.5

        if extname == 'CIE':
            iy = (xPos - ccdinfo["xCenter"]) / self.degperpixel_r * 1 + ypixHalfSize - 0.5
            ix = (yPos - ccdinfo["yCenter"]) / self.degperpixel_t * (-1) + xpixHalfSize - 0.5

        if extname == 'CIN':
            ix = (xPos - ccdinfo["xCenter"]) / self.degperpixel_t * (-1) + xpixHalfSize - 0.5
            iy = (yPos - ccdinfo["yCenter"]) / self.degperpixel_r * (-1) + ypixHalfSize - 0.5

        if extname == 'CIW':
            iy = (xPos - ccdinfo["xCenter"]) / self.degperpixel_r * (-1) + ypixHalfSize - 0.5
            ix = (yPos - ccdinfo["yCenter"]) / self.degperpixel_t * 1 + xpixHalfSize - 0.5

        return ix, iy

    def getSensor(self, xPos, yPos):
        """ given x,y position on the focal plane, return the sensor name
        or None, if not interior to a chip
        """
        for ext in list(self.infoDict.keys()):
            ccdinfo = self.infoDict[ext]
            # is this x,y inside this chip?
            nxdif = numpy.abs((xPos - ccdinfo["xCenter"]) / self.degperpixel_c)
            nydif = numpy.abs((yPos - ccdinfo["yCenter"]) / self.degperpixel_c)
            print('ext, nxdif, nydif', ext, nxdif, nydif)
            # CCD size in pixels
            if ccdinfo["FAflag"]:
                xpixHalfSize = 4000./2 #This is just assuming a 4k box for now
                ypixHalfSize = 4000./2
            else:
                print('WE ONLY HAVE FAflag CHIPS HERE!')

            if nxdif <= xpixHalfSize and nydif <= ypixHalfSize:
                print('return extname', ext)
                return ext

        # get to here if we are not inside a chip
        return None
        #return ext # for test purpose, not matter where the position of the star, always return GFA1
