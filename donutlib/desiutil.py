
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
        # Rotation here is defined as the rotation angle from chip frame to fiducial global frame, counter-clock wise is positive
        infoDict["FOCUS1"] = {"CRVAL1": 178.7586, "CRVAL2":  9.0116, "CD1_1": -3.4778e-05, "CD1_2":  4.3981e-05, "CD2_1":  4.7668e-05, "CD2_2":  3.1954e-05, "Rotation":  -54., "FAflag": True, "Offset": 1500}
        infoDict["FOCUS4"] = {"CRVAL1": 179.4300, "CRVAL2": 11.4703, "CD1_1":  5.6263e-05, "CD1_2":  1.6797e-05, "CD2_1":  1.8281e-05, "CD2_2": -5.1696e-05, "Rotation": -162., "FAflag": True, "Offset": 1500}
        infoDict["FOCUS9"] = {"CRVAL1": 180.5650, "CRVAL2":  8.5285, "CD1_1": -5.6274e-05, "CD1_2": -1.6800e-05, "CD2_1": -1.8284e-05, "CD2_2":  5.1704e-05, "Rotation":   18., "FAflag": True, "Offset": 1500}
        infoDict["FOCUS6"] = {"CRVAL1": 181.2488, "CRVAL2": 10.9838, "CD1_1":  3.4774e-05, "CD1_2": -4.3977e-05, "CD2_1": -4.7862e-05, "CD2_2": -3.1951e-05, "Rotation":  126., "FAflag": True, "Offset": 1500}


        """This is the old version (need to read in a file)
        f = open('GFA_CDs.txt')
        tmp = f.readlines()
        infoDict = numpy.zeros(10, dtype=[('PETAL', '<i4'), ('PETALLOC', '<i4'), ('CRVAL1', '<f8'), ('CRVAL2', '<f8'), ('CRPIX1', '<f8'),
                                   ('CRPIX2', '<f8'), ('CD1_1', '<f8'), ('CD1_2', '<f8'), ('CD2_1', '<f8'),
                                   ('CD2_2', '<f8'), ('FAflag', 'bool'), ('Offset', '<f8'), ('EXTNAME', 'S6'), ('Rotation', '<f8')])
        # need to update here: the sign for offset depend on the ix pixel value
        infoDict['Offset'] = 1500.

        k = -1
        for i in tmp:
            if '=' in i:
                a = str(i.split('=')[0]).replace(' ', '')
                b = float(i.split('=')[1])
                if a == 'PETAL':
                    k += 1
                infoDict[a][k] = b

        #assign ones are Focus Alignment Chips
        for i in range(10):
            if i in [1, 4, 6, 9]:
                idx = infoDict['PETALLOC'] == i
                infoDict['FAflag'][idx] = 1
                infoDict['EXTNAME'][idx] = 'FOCUS' + str(i)
            else:
                idx = infoDict['PETALLOC'] == i
                infoDict['EXTNAME'][idx] = 'GUIDE' + str(i)
        """


        return infoDict

    def __init__(self, **inputDict):

        self.infoDict = self.info()
        self.mmperpixel = 0.015
        self.degperpixel = 5.97e-5 #pixel scale in deg/pixel assuming pixel size = 15 micron and focal length = 3.6 * 4 m
        self.rClear = 99999 # something for vignetting

    def __getstate__(self):
        stateDict = {}
        keysToPickle = ['infoDict','rClear']
        for key in keysToPickle:
            stateDict[key] = self.__dict__[key]
        return stateDict

    def __setstate__(self, state):
        for key in state:
            self.__dict__[key] = state[key]

    def getPosition(self, extname, ix, iy):
        """ return the x,y position in angle (degree) for a given petal and pixel number
        note that the ix,iy are Image pixels - overscans removed - and start at zero
        """

        #ccdinfo = self.infoDict[self.infoDict['EXTNAME'] == extname]
        ccdinfo = self.infoDict[extname]

        # CCD size in pixels
        if ccdinfo["FAflag"]:
            xpixHalfSize = 1024.
            ypixHalfSize = 516. #GFA is 1032 pixel, not 1024
        else:
            print('WRONG! WE ONLY HAVE FAflag CHIPS HERE!')

        # calculate positions based on rotation matrix, centered at RA ~ 180, dec 10.
        xPos = ccdinfo['CRVAL1'] - 180 + ccdinfo['CD1_1'] * (float(ix) - xpixHalfSize + 0.5) + ccdinfo['CD1_2'] * (float(iy) - ypixHalfSize + 0.5)
        yPos = ccdinfo['CRVAL2'] - 10  + ccdinfo['CD2_1'] * (float(ix) - xpixHalfSize + 0.5) + ccdinfo['CD2_2'] * (float(iy) - ypixHalfSize + 0.5)

        return xPos, yPos

    def getPixel(self, extname, xPos, yPos):
        """ given a coordinate in angle (degree), return pixel number
        """

        #ccdinfo = self.infoDict[self.infoDict['EXTNAME'] == extname]
        ccdinfo = self.infoDict[extname]

        # CCD size in pixels
        if ccdinfo["FAflag"]:
            xpixHalfSize = 1024.
            ypixHalfSize = 516. #GFA is 1032 pixel, not 1024
        else:
            print('WRONG! WE ONLY HAVE FAflag CHIPS HERE!')


        # calculate positions
        ix = ((xPos - ccdinfo['CRVAL1'] + 180) * ccdinfo['CD2_2'] - (yPos - ccdinfo['CRVAL2'] + 10) * ccdinfo['CD1_2']) / (ccdinfo['CD1_1'] * ccdinfo['CD2_2'] - ccdinfo['CD2_1'] * ccdinfo['CD1_2']) + xpixHalfSize - 0.5
        iy = ((xPos - ccdinfo['CRVAL1'] + 180) * ccdinfo['CD2_1'] - (yPos - ccdinfo['CRVAL2'] + 10) * ccdinfo['CD1_1']) / (ccdinfo['CD1_2'] * ccdinfo['CD2_1'] - ccdinfo['CD2_2'] * ccdinfo['CD1_1']) + ypixHalfSize - 0.5

        return ix, iy

    def getSensor(self, xPos, yPos):
        """ given x,y position on the focal plane, return the sensor name
        or None, if not interior to a chip
        """
        #for extname in list(self.infoDict['EXTNAME']):
        #    ccdinfo = self.infoDict[self.infoDict['PETAL'] == petal]
                
        for ext in list(self.infoDict.keys()):
            ccdinfo = self.infoDict[ext]
            # CCD size in pixels
            if ccdinfo["FAflag"]:
                xpixHalfSize = 1024.
                ypixHalfSize = 516. #GFA is 1032 pixel, not 1024
            else:
                print('WRONG WE ONLY HAVE FAflag CHIPS HERE!')
            # is this x,y inside this chip?
            #nxdif = numpy.abs((xPos - ccdinfo['CRVAL1'] + 180) / self.degperpixel)
            #nydif = numpy.abs((yPos - ccdinfo['CRVAL2'] + 10)  / self.degperpixel)
            #ix,iy = getPixel(ext,xPos,yPos)
            ix = ((xPos - ccdinfo['CRVAL1'] + 180) * ccdinfo['CD2_2'] - (yPos - ccdinfo['CRVAL2'] + 10) * ccdinfo['CD1_2']) / (ccdinfo['CD1_1'] * ccdinfo['CD2_2'] - ccdinfo['CD2_1'] * ccdinfo['CD1_2']) + xpixHalfSize - 0.5
            iy =  iy = ((xPos - ccdinfo['CRVAL1'] + 180) * ccdinfo['CD2_1'] - (yPos - ccdinfo['CRVAL2'] + 10) * ccdinfo['CD1_1']) / (ccdinfo['CD1_2'] * ccdinfo['CD2_1'] - ccdinfo['CD2_2'] * ccdinfo['CD1_1']) + ypixHalfSize - 0.5
           
            if ix <= 2*xpixHalfSize and iy <= 2*ypixHalfSize and ix >=0 and iy >= 0:
                return ext


        # get to here if we are not inside a chip
        print("{:4f}".format(xPos))
        print("{:4f}".format(yPos))
        return None
        


class desiciinfo(object):
    """ desiciinfo is a class used to contain DESI CI geometry information and various utility routines

    """

    def info(self):
        """info returns a dictionary chock full of info on the DESI CI geometry
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

        # offset 1500 is 1.5 mm. Does not matter for CI instrument but should be set for GFAs +/- 1500
        # FAflag should be true for all focus and alignment chip.

        return infoDict

    def __init__(self, **inputDict):

        self.infoDict = self.info()
        self.degperpixel_c = 3.7025e-05 #14.81 / 1000. * 9. /3600 #pixel scale at center chip in deg/pixel
        self.degperpixel_t = 3.5550e-05 #14.22 / 1000. * 9. /3600 #tangential pixel scale at edge chips in deg/pixel
        self.degperpixel_r = 3.2775e-05 #13.11 / 1000. * 9. /3600 #radial pixel scale at edge chips in deg/pixel

        self.rClear = 99999 # something for vignetting, what should this be?

    def __getstate__(self):
        stateDict = {}
        keysToPickle = ['infoDict', 'degperpixel_c', 'degperpixel_t', 'degperpixel_r', 'rClear']
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
