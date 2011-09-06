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

#This class allows tracking of keyup and keydown events

class KeyManager:
    def __init__(self, keylist, initial_state=None):
        self.keylist = keylist
        self.key_events = []
        if initial_state is None:
            istate = {}
            for key in keylist:
                istate[key] = False
        else:
            istate = initial_state
        self.keysdown={}
        for key in self.keylist:
            self.keysdown[key] = istate[key]
        return
    
    #keyset should be a set of keys that are down
    def update_from_keyset(self, keyset, fetch_events=True):
        for key in self.keylist:
            kin = key in keyset
            self.__delta_key(key, kin)
        return self.fetch_events() if fetch_events else self.peek_events()
    
    #keystate should represent (in a dictionary) all keys, and be True if pressed,
    #False if not pressed. You can express delta updates this way, by
    #only having keys that have changed in the keystate, with True for keydown,
    #and False for keyup
    def update_from_keystate(self, keystate, fetch_events=True):
        for key in keystate:
            self.__delta_key(key, keystate[key])
        return self.fetch_events() if fetch_events else self.peek_events()
    
    def peek_events(self):
        return self.key_events
    
    def fetch_events(self):
        out = self.key_events
        self.key_events = []
        return out
        
    
    def __delta_key(self, key, value):
        if self.keysdown[key] != value:
            self.key_events.append(str(key)+vtable[self.keysdown[key], value])
            self.keysdown[key] = value
        return

vtable = {}
vtable[True, False] = "_up"
vtable[False, True] = "_down"
