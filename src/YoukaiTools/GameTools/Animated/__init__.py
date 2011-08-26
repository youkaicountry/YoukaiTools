#an animated object
class Animated:
   def __init__(self):
      self.frames = {}
      self.times = {}
      self.loops = {}
      self.next = {}
      
      self.current_state = 0
      self.current_frame = 0 #
      self.current_time = 0
      self.loop_count = 0
      
   def update(self, dt=1):
      #print("frame: " + str(self.current_frame) + " time: " + str(self.current_time))
      if self.current_time >= self.times[self.current_state][self.current_frame]:
         self.current_frame += 1
         if self.current_frame >= len(self.frames[self.current_state]):
            if self.loop_count >= self.loops[self.current_state] and self.loops[self.current_state] >= 0:
               if self.next[self.current_state] != None:
                  self.current_state = self.next[self.current_state]
                  self.loop_count = 0
                  self.current_time = 0
                  self.current_frame = 0
            else: self.loop_count += 1; self.current_time = 0; self.current_frame = 0
      self.current_time += dt
      return self.getSprite()
            
      
   
   #name - name of animation
   #framedata - list of the sprite objects
   #timedata - length of each frame [3, 2, 5, 3], etc
   #loops - times to loop. <0 means infinite
   #next_animation - the name of the animation to go to after all loops. None means it just stops at the end         
   def addAnimation(self, name, framedata, timedata, loops = -1, next_animation = None):
      t = []
      adder = 0
      for x in timedata:
         adder += x
         t.append(adder)
      f = framedata[:]
      self.frames[name] = f
      self.times[name] = t
      self.loops[name] = loops
      self.next[name] = next_animation
      return
      
   def setAnimation(self, animation, start_time = 0):
      self.current_state = animation
      self.current_frame = 0
      self.current_time = start_time
      self.loop_count = 0
      return
   
   def getSprite(self):
      return self.frames[self.current_state][self.current_frame]
      
