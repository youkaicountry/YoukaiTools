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

"""
Utilities for dealing with latitude and longitude values.
This module deals with 3 core types of objects:
1. Position is a basic lat or lon position. It is a tuple of length 4, with (degrees, minutes, seconds, direction).
   Direction is given as a string of a single letter "N", "S", "E", or "W".
2. Global Position is a numerically corrected position that has no direction string, It is a tuple
   of length 3, with (degrees, minutes, seconds). The function globalLatLon can produce these.
3. Radial Position is a given position in polar coordinates. It is simply a float. toRadians can produce these.
"""

from math import pi
from math import acos, sin, cos

#give as tuple (degrees, minutes, seconds)
def toDecimal(pos):
    newmin = __t60(pos[1], pos[2])
    newdeg = __t60(pos[0], newmin)
    return newdeg

def toRadians(pos):
    dec = toDecimal(toGlobal(pos))
    return dec * pi / 180.0

def dist(latlon1, latlon2, radius):
    """
    Returns the distance between 2 latitude and longitudes on a sphere with a given radius.
    Latitude and longitude pairs should be given in tuples like: ((latdegree, latminute, latsecond), (londegree, lonminute, lonsecond))
    @param latlon1: The first latitude longitude pair.
    @type latlon1: C{Iterable}
    @param latlon2: The second latitude longitude pair.
    @type latlon2: C{Iterable}
    @param radius: The radius of the sphere.  The earth is 6378.1 km, or 3963.14 miles.
    @rtype: C{float}
    """
    r1 = (toRadians(toGlobal(latlon1[0])), toRadians(toGlobal(latlon1[1])))
    r2 = (toRadians(toGlobal(latlon2[0])), toRadians(toGlobal(latlon2[1])))
    return radDist(r1, r2, radius)

def toGlobal(pos):
    """
    Takes a position (degrees, minutes, seconds) or (degrees, minutes, seconds, direction)
    Direction is a string with a letter "E", "W", "N" or "S".
    This function then converts it to a single global position without the direction.
    """
    if len(pos) == 3:
        return pos
    direction = pos[3].lower()
    if direction == 'w' or direction == 's':
        return (180.0-pos[0], 60.0-pos[1], 60.0-pos[2])
    return (pos[0]+180.0, pos[1], pos[2])

def radDist(rpos1, rpos2, radius):
    return radius * acos(sin(rpos1[0]) * sin(rpos2[0]) + cos(rpos1[0]) * cos(rpos2[0]) * cos(rpos2[1] - rpos1[1]))

def __t60(base, val):
    return base + (val / 60.0)
