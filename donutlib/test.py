###
### Script for very basic testing of donutengine and donutfit
###

from donutlib.makedonut import makedonut
from donutlib.donutfit import donutfit


# make donuts
z4 = -4.509
#z4 = 0
z5 = 0.
z6 = -0.1168
z7 = 0
z8 = -0.249
z9 = 0.
z10 = 0.294
z11 = -0.065

inputDict = {'writeToFits':True,
             'outputPrefix':'unittest.0001',
             'iTelescope':6,
             'nZernikeTerms':37,
             'nbin':512,
             'nPixels':64,
             'pixelOverSample':8,
             'scaleFactor':1.,
             'rzero':0.125,
             'nEle':5.0e6,
             'background':4000.,
             'randomFlag':True,
             'randomSeed':2314808,
             'ZernikeArray':[0.,0.,0.,z4,z5,z6,z7,z8,z9,z10,z11],
             'xDECam': 0,
             'yDECam': 1.57,
             #'xDECam': 1.286,
             #'yDECam': 0.806,
             #'xDECam':1.318,
             #'yDECam':0.86,
             #'xDECam':0.0,
             #'yDECam':0.0,
             "debugFlag": True,
             'printLevel': 2
             }

m = makedonut(**inputDict)
donut1 = m.make()

print('FINISH MAKING DONUTS, NOW START FITTING')

## fit them
fitinitDict = {"nZernikeTerms":15,
               "fixedParamArray1":[0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
               "fixedParamArray2":[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
               "nFits":2,
               "nPixels":64,
               "nbin":512,
               "scaleFactor":1.0,
               "pixelOverSample":8,
               "iTelescope":6,
               "inputrzero":0.15,
               #'xDECam': 1.37,
               #'yDECam': 0.862,
               "debugFlag":False}
df = donutfit(**fitinitDict)


# fit first donut
fitDict  = {}
fitDict["inputFile"] = 'unittest.0001.stamp.fits'
#import pyfits
#extname = pyfits.open(fitDict["inputFile"])[0].header['extname']
fitDict["outputPrefix"] = 'unittest.0001'
fitDict["inputrzero"] = 0.125
#fitDict["inputZernikeDict"] = {"CIC":[0.0,0.0,5.2,0.0,0.0,0.0,0.0,0.0,0.0,-0.08]}
df.setupFit(**fitDict)


