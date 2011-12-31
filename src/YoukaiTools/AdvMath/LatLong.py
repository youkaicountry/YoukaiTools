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

from math import pi
from math import acos, sin, cos

#give as tuple (degrees, minutes, seconds)
def toDecimal(pos):
    newmin = __t60(pos[1], pos[2])
    newdeg = __t60(pos[0], newmin)
    return newdeg

def toRadians(pos):
    dec = toDecimal(*pos)
    return dec * pi / 180.0

def dist(latlon1, latlon2, radius):
    """
    Returns the distance between 2 latitude and longitudes on a sphere with radius radius.
    Latitude and longitude pairs should be given in tuples like: ((latdegree, latminute, latsecond), (londegree, lonminute, lonsecond))
    @param latlon1: The first latitude longitude pair.
    @type latlon1: C{Iterable}
    @param latlon2: The second latitude longitude pair.
    @type latlon2: C{Iterable}
    @param radius: The radius of the sphere.  The earth is 6378.1 km, or 3961.3 miles.
    @rtype: C{float}
    """
    r1 = (toRadians(latlon1[0]), toRadians(latlon1[1]))
    r2 = (toRadians(latlon2[0]), toRadians(latlon2[1]))
    return radDist(r1, r2, radius)

def radDist(rpos1, rpos2, radius):
    return radius * acos[sin(rpos1[0]) * sin(rpos2[0]) + cos(rpos1[0]) * cos(rpos2[0]) * cos(rpos2[1] - rpos1[1])]

def __t60(base, val):
    return base + (val / 60.0)
