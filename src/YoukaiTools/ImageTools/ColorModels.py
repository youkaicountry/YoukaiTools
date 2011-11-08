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

import math

two_pi = math.pi * 2.0                 #6.283
pi_over_3 = math.pi / 3.0              #1.047
two_thirds_pi = math.pi * (2.0/3.0)    #2.094
four_thirds_pi = math.pi * (4.0 / 3.0) #4.189



def RGB2HSI(rgb):
    rmg = rgb[0]-rgb[1]
    rmb = rgb[0]-rgb[2]
    gmb = rgb[1]-rgb[2]
    rpgpb = rgb[0]+rgb[1]+rgb[2]
    p = pow(rmg**2 + rmb*gmb, .5)
    theta = math.acos(.5*(rmg+rmb)/p) if p > 0 else 0.0
    h = theta if rgb[2] <= rgb[1] else two_pi-theta
    h /= two_pi
    i = rpgpb/3.0
    #s = 1-((3/rpgpb)*min(rgb)) if rpgpb > 0 else 0.0
    s = 1 - (min(rgb)/i)
    return [h,s,i]

def HSI2RGB(hsi):
    eh = two_pi*hsi[0]
    s = hsi[1]
    i = hsi[2]
    if eh < two_thirds_pi:
        b = i*(1-s)
        r = i*(1+((s*math.cos(eh))/math.cos(pi_over_3-eh)))
        g = 3*i - (r + b)
    elif eh < four_thirds_pi:
        nh = eh - two_thirds_pi
        r = i*(1-s)
        g = i*(1+((s*math.cos(nh))/math.cos(pi_over_3-nh)))
        b = 3*i - (r + g)
    else:
        nh = eh - four_thirds_pi
        g = i*(1-s)
        b = i*(1+((s*math.cos(nh))/math.cos(pi_over_3-nh)))
        r = 3*i - (g + b)
    return [r, g, b]

def invertColor(color):
    i_color = []
    for c in color:
        i_color.append(1.0-c)
    return i_color

def complementHSI(hsi):
    h, s, i = hsi
    out_h = 0
    if h < 0.5:
        out_h = h + 0.5
    else:
        out_h = h - 0.5
    return [out_h, s, i]

def complementRGB(rgb):
    hsi = RGB2HSI(rgb)
    comp_hsi = complementHSI(hsi)
    comp_rgb = HSI2RGB(comp_hsi)
    return comp_rgb
