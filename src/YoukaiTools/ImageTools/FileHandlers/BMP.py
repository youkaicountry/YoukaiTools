#Copyright (c) <2011> <Nathaniel Caldwell>

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from .. import Create
from .. import SubImage
from .. import __utils__
from . import __uh__ as UHEAD
import struct

#TO SAVE 24 BIT BMP:
#bits_per_pixel = 24
#data_pad_bits = 0 or a multiple of 8
#IMAGE FORMAT:
#3 channels, RGB

def getBasicUnifiedHeader(image=None, f=None):
    uh = UHEAD.getBlankUnifiedHeader()
    if image is None:
        uh["bits_per_pixel"] = 24
        uh["data_pad_bits"] = 0
        uh["dpi_x"] = 300
        uh["dpi_y"] = 300
        uh["number_of_channels"] = 3
    else:
        #do image specific stuff here
        uh["width"] = image[0]
        uh["height"] = image[1]
        uh["number_of_channels"] = image[2]
        uh["bits_per_pixel"] = 24
        uh["data_pad_bits"] = 0
        uh["dpi_x"] = 300
        uh["dpi_y"] = 300
    return uh

def getFormattedUnifiedHeader(bpp, datapad):
    uh = UHEAD.getBlankUnifiedHeader()
    uh["bits_per_pixel"] = bpp
    uh["data_pad_bits"] = datapad
    return uh

def getBasicFormatHeader(image=None, f=None):
    return

#only loads 24 bit uncompressed bmp
def load(f):
    #get file header
    s = f.read(14)
    file_header = struct.unpack_from("=HIHHI", s)
    #print(file_header)
    
    #get info header
    s = f.read(40)
    info_header = struct.unpack_from("=IIIHHIIIIII", s)
    #print(info_header)
    
    uh = UHEAD.getBlankUnifiedHeader()
    uh["width"] = info_header[1]
    uh["height"] = info_header[2]
    uh["bits_per_pixel"] = info_header[4]
    uh["dpi_x"] = info_header[7]*0.0254
    uh["dpi_y"] = info_header[8]*0.0254
    
    fh = {}
    fh["data_size_bytes"] = info_header[6]
    
    row_padding = __getRowPadding(uh["width"], uh["bits_per_pixel"])
    
    uh["data_pad_bits"] = (int(((fh["data_size_bytes"]/(((uh["width"]*uh["height"])*3) + (row_padding*uh["height"])) )) ))
    
    return (bmp_load_dispatch[uh["bits_per_pixel"]](f, uh, fh), uh, fh)

def loadFile(filename):
    f = open(filename, "rb")
    o = load(f)
    f.close()
    return o
    
def saveFile(filename, image, uh=None):
    f = open(filename, "wb")
    save(f, image, uh)
    f.close()
    return

#requires a unified header but not format header
#uh should have bitsperpixel=24, data_pad_bits (should be 0 or a multiple of 8)
#the image should have at least 3 channels, RGB
def save(f, image, uh=None):
    if uh is None: uh = getBasicUnifiedHeader(image)
    width = image[0] if uh["width"] is None else uh["width"]
    height = image[1] if uh["height"] is None else uh["height"]
    dpi_x = uh["dpi_x"] if uh["dpi_x"] is not None else 300
    dpi_y = uh["dpi_y"] if uh["dpi_y"] is not None else 300
    row_padding = __getRowPadding(width)
    data_size = int((((width * height)*(uh["bits_per_pixel"]+uh["data_pad_bits"])) / 8) + (height*row_padding))
    header_size = 54
    #print("SIZE: " + str(data_size))
    file_header = struct.pack("=HIHHI", 19778, header_size+data_size, 0, 0, 54)
    info_header = struct.pack("=IIIHHIIIIII", 40, width, height, 1, uh["bits_per_pixel"], 0, data_size, int(dpi_x*39.3701), int(dpi_y*39.3701), 0, 0)
    f.write(file_header)
    f.write(info_header)
    bmp_save_dispatch[uh["bits_per_pixel"]](f, image, uh)
    return

def __save_bmp24(f, image, uh):
    flipped = SubImage.verticalFlip(image)
    width = image[0] if uh["width"] is None else uh["width"]
    height = image[1] if uh["height"] is None else uh["height"]
    row_padding = __getRowPadding(width)
    #print(width, height)
    row_padding = __getRowPadding(width)
    padding = int(uh["data_pad_bits"] / 8)
    pixel_struct = struct.Struct("="+"BBB"+("x"*padding))
    padval = [0]*padding
    padval = list(padval)
    
    row_padding_struct = struct.Struct("="+("B"*row_padding))
    rowpadval = [0]*row_padding
    i = 3
    
    for row in range(height):
        for col in range(width):
            if uh["number_of_channels"] == 1:
                s = pixel_struct.pack(int(flipped[i][0]*255), int(flipped[i][0]*255), int(flipped[i][0]*255), *padval)
            else:
                s = pixel_struct.pack(int(flipped[i][2]*255), int(flipped[i][1]*255), int(flipped[i][0]*255), *padval)
            f.write(s)
            i+=1
        s = row_padding_struct.pack(*rowpadval)
        f.write(s)
    #for pixel in image[3:]:
    #    s = pixel_struct.pack(int(pixel[2]*255), int(pixel[1]*255), int(pixel[0]*255), *padval)
    #    f.write(s)
    return

def __getRowPadding(width, bpp=24):
    padding = 0
    pos = width*int(bpp/8)
    while True:
        if pos % 4 == 0:
            break
        pos+=1
        padding+=1
    #print("PADDING: " + str(padding))
    return padding

#3 or 4 bytes per pixel?
def __load_bmp24(f, uh, th):
    width = uh["width"]
    height = uh["height"]
    #print(width, height)
    data = []
    data_size = th["data_size_bytes"]
    
    padding = int(uh["data_pad_bits"] / 8)
    #padding = 0
    
    #print("THE PAD: "+str(padding))
    pixel_struct = struct.Struct("="+"BBB"+("x"*padding))
    row_padding = __getRowPadding(width)
    #row_padding_struct = struct.Struct("=" + ("x"*row_padding))
        
    #print(padding)
    for row in range(height):
        for col in range(width):
            p = f.read(3+padding)
            pd = list(pixel_struct.unpack_from(p))
            if uh["number_of_channels"] == 1:
                data.append([__utils__.f2b[int(pd[0])]])
            else:
                data.append([__utils__.f2b[int(pd[2])], __utils__.f2b[int(pd[1])], __utils__.f2b[int(pd[0])]])
        f.read(row_padding)
        
    #for i in range(width*height):
    #    p = f.read(3+padding)
    #    #pd = pixel_struct.unpack_from(p)[:3].reverse()
    #    pd = list(pixel_struct.unpack_from(p))
    #    #pd.reverse()
    #    #print(pd)
    #    data.append([__utils__.f2b[int(pd[2])], __utils__.f2b[int(pd[1])], __utils__.f2b[int(pd[0])]])
    image = Create.newImage(width, height, indata=data)
    return SubImage.verticalFlip(image)

#chooses proper loading function for BMP based upon the bpp
bmp_load_dispatch = {}
bmp_load_dispatch[24] = __load_bmp24

bmp_save_dispatch = {}
bmp_save_dispatch[24] = __save_bmp24
