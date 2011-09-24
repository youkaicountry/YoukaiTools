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

class AnimatedObject:
    def __init__(self, animation_set):
        self.animation_set = animation_set
        self.current_state = 0
        self.current_frame = 0 #
        self.current_time = 0
        self.loop_count = 0
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
    def __init__(self):
        self.frames = {}
        self.times = {}
        self.loops = {}
        self.next = {}
        
    #name - name of animation
    #framedata - list of the sprite objects
    #timedata - length of each frame [3, 2, 5, 3], etc
    #loops - times to loop. <0 means infinite
    #next_animation - the name of the animation to go to after all loops. None means it just stops at the end         
    def addAnimation(self, name, framedata, timedata=None, loops = -1, next_animation = None):
        t = []
        timedata = timedata if timedata is not None else [1 for x in range(len(framedata))]
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
    
