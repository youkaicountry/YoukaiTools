import itertools

import png

from ... import Create
from .. import __uh__ as UHEAD
from YoukaiTools.ImageTools import Metric

def encodehex(s):
    out = ""
    for x in s:
        out += str(chr(x))
    return out

def load(f):
    a = png.Reader(file=f)
    b = a.read()
    m = list(b[2])
    imagedata = []
    for row in m:
        #print(len(x))
        #print("IN ROW: ", row)
        imagedata += [[p[0]/255.0 for p in j] for i,j in itertools.groupby(zip(row, (x//b[3]["planes"] for x in itertools.count())), lambda ri:ri[1])]
        #print("OUT ROW: ", newrow)
        #print(newrow)
    #uh, fh    
    return (Create.newImage(b[0], b[1], channels=b[3]["planes"], indata=imagedata), None, None)

def loadFile(filename):
    f = open(filename, "rb")
    o = load(f)
    f.close()
    return o

def save(f, image, uh=None):
    if uh is None: uh = getBasicUnifiedHeader(image)
    width = image[0] if uh["width"] is None else uh["width"]
    height = image[1] if uh["height"] is None else uh["height"]
    dpi_x = uh["dpi_x"] if uh["dpi_x"] is not None else 300
    dpi_y = uh["dpi_y"] if uh["dpi_y"] is not None else 300
    #if 1 channel, then grayscale. if 2, grayscale with alpha
    #if 3 channels, then color. If 4 channels, then color with alpha
    if uh["number_of_channels"] == 1:
        greyscale = True
        alpha = False
    elif uh["number_of_channels"] == 2:
        greyscale = True
        alpha = True
    elif uh["number_of_channels"] == 3:
        greyscale = False
        alpha = False
    elif uh["number_of_channels"] == 4:
        greyscale = False
        alpha = True
    w = png.Writer(width=uh["width"], height=uh["height"], interlace=uh["interlace"], greyscale=greyscale, alpha=alpha, bitdepth=8)
    
    data = []
    for y in range(uh["height"]):
        row = []
        for x in range(uh["width"]):
            c = Metric.getColorAt(image, x, y)
            nc = [int(df*255) for df in c]
            row.extend(nc)
        data.append(row)
    w.write(f, data)
    
    """self, width=None, height=None,
                 size=None,
                 greyscale=False,
                 alpha=False,
                 bitdepth=8,
                 palette=None,
                 transparent=None,
                 background=None,
                 gamma=None,
                 compression=None,
                 interlace=False,
                 bytes_per_sample=None, # deprecated
                 planes=None,
                 colormap=None,
                 maxval=None,
                 chunk_limit=2**20):"""
    return

def saveFile(filename, image, uh=None):
    f = open(filename, "wb")
    save(f, image, uh)
    f.close()
    return

def getBasicUnifiedHeader(image=None, f=None):
    uh = UHEAD.getBlankUnifiedHeader()
    if image is None:
        uh["number_of_channels"] = 3
    else:
        uh["width"] = image[0]
        uh["height"] = image[1]
        uh["number_of_channels"] = image[2]
    uh["bits_per_pixel"] = 24
    uh["data_pad_bits"] = 0
    uh["dpi_x"] = 300
    uh["dpi_y"] = 300
    uh["interlace"] = True
    return uh

def getBasicFormatHeader(image=None, f=None):
    return