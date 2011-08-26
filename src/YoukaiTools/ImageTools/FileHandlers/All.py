from . import PNG
from . import BMP

iformat = {}
iformat["png"] = PNG
iformat["bmp"] = BMP

def getFormatName(filename):
    return filename.split(".")[-1].lower()

def getFormat(filename):
    return iformat[filename.split(".")[-1].lower()]

def loadFile(filename, uh=None):
    f = open(filename, "rb")
    uformat = getFormat(filename)
    o = uformat.load(f, uh)
    f.close()
    return o

def saveFile(filename, image, uh=None):
    f = open(filename, "wb")
    uformat = getFormat(filename)
    uformat.save(f, image, uh)
    f.close()
    return

def save(f, image, format="png", uh=None):
    iformat[format].save(f, image, uh)
    return

def load(f, image, format="png", uh=None):
    iformat[format].load(f, image, uh)
    return
