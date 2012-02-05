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

import collections

class AnimatedObject:
    """
    An animated object. This should correspond to a particular actor in the game, and keeps
    track of its current state of animation.
    """
    def __init__(self, animation_set, start_animation=None, start_time=0, obj=None):
        """
        @param animation_set: An AnimationSet object containing the animations for the actor.
        @type animation_set: C{AnimationSet}
        @param start_animation: The name of the animation on which to start, If None, it won't be set.
        @param start_time: The start time of the animation.
        @param obj: The object can be attached here for convenience
        """
        self.animation_set = animation_set
        self.setAnimation(start_animation, start_time)
        self.obj = obj
        return
    
    def update(self, dt=1):
        #print("frame: " + str(self.current_frame) + " time: " + str(self.current_time)) 
        if self.current_time >= self.animation_set.times[self.current_state][self.current_frame]: 
            self.current_frame += 1
            if self.current_frame >= len(self.animation_set.frames[self.current_state]): 
                if self.loop_count >= self.animation_set.loops[self.current_state] and self.animation_set.loops[self.current_state] >= 0:
                    if self.animation_set.next[self.current_state] != None:
                        self.current_state = self.animation_set.next[self.current_state] 
                        self.loop_count = 0 
                        self.current_time = 0 
                        self.current_frame = 0 
                else: self.loop_count += 1; self.current_time = 0; self.current_frame = 0 
        self.current_time += dt 
        return self.getSprite() 

    def getSprite(self):
        return self.animation_set.frames[self.current_state][self.current_frame]
   
    #if try set is true, it will not set the animation if the object is already
    #on the animation
    def setAnimation(self, animation, start_time = 0, try_set=False):
        if try_set:
            if self.current_state == animation:
                return 
        self.current_state = animation
        self.current_frame = 0
        self.current_time = start_time
        self.loop_count = 0
        return
    
#an animated object 
class AnimationSet:
    """
    A set of animations. This represents actual animations, and can be used on multiple actors. 
    """
    def __init__(self):
        self.frames = {}
        self.times = {}
        self.loops = {}
        self.next = {}
        
    #name - name of animation
    #framedata - list of the sprite objects
    #timedata - length of each frame [3, 2, 5, 3], etc. If None, will be 1 for each frame.
    #           if a number, will be that number for each frame 
    #loops - times to loop. <0 means infinite
    #next_animation - the name of the animation to go to after all loops. None means it just stops at the end         
    def addAnimation(self, name, framedata, timedata=1, loops = -1, next_animation = None):
        """
        Adds a new animation.
        @param name: The name of the animation.
        @param framedata: A list where each element is a frame of animation. A frame can be any kind of data.
        @param timedata: The length of each frame. If a list, each element is the amount of time spent on each frame. If a single number, then each frame will be set to that length.
        @param loops: The number of times to loop the animation. If less than 1, the animation will be repeated infinitely.
        @param next_animation: The name of the animation to be played after all of the loops. If None, it will stop.
        """
        if not isinstance(timedata, collections.Iterable):
            k = timedata
            timedata = [k for x in range(len(framedata))]
        
        t = []
        adder = 0
        for x in timedata:
            adder += x
            t.append(adder)
        t = list(t)
        f = framedata[:]
        self.frames[name] = f
        self.times[name] = t
        self.loops[name] = loops
        self.next[name] = next_animation
        return
    
