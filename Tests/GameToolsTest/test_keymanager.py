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

from YoukaiTools import GameTools

km = GameTools.KeyManager(["a", "b", "c", "d", "e"])

print("KEYSET:")
print(km.update_from_keyset(keyset=set())) #no events
print(km.update_from_keyset(keyset=set(["b", "d"]))) #b_down, d_down
print(km.update_from_keyset(keyset=set(["b", "d", "e"]))) #e_down
print(km.update_from_keyset(keyset=set(["b", "e"]))) #d_up
print(km.update_from_keyset(keyset=set(["b"]))) #e_up
print(km.update_from_keyset(keyset=set(["a"]))) #a_down, b_up
print(km.update_from_keyset(keyset=set())) #a_up

print("KEYSET, NOFETCH:")
km.update_from_keyset(set(), False) #no events
km.update_from_keyset(set(["b", "d"]), False) #b_down, d_down
km.update_from_keyset(set(["b", "d", "e"]), False) #e_down
km.update_from_keyset(set(["b", "e"]), False) #d_up
km.update_from_keyset(set(["b"]), False) #e_up
km.update_from_keyset(set(["a"]), False) #a_down, b_up
km.update_from_keyset(set(), False) #a_up
print(km.fetch_events())
print(km.fetch_events())

print("KEYSTATE:")
print(km.update_from_keystate({"a":False, "b":False, "c":False, "d":False, "e":False}))
print(km.update_from_keystate({"a":False, "b":True, "c":False, "d":True, "e":False}))
print(km.update_from_keystate({"a":False, "b":True, "c":False, "d":True, "e":True}))
print(km.update_from_keystate({"a":False, "b":True, "c":False, "d":False, "e":True}))
print(km.update_from_keystate({"a":False, "b":True, "c":False, "d":False, "e":False}))
print(km.update_from_keystate({"a":True, "b":False, "c":False, "d":False, "e":False}))
print(km.update_from_keystate({"a":False, "b":False, "c":False, "d":False, "e":False}))

print("KEYSTATE, DELTA:")
print(km.update_from_keystate({}))
print(km.update_from_keystate({"b":True, "d":True}))
print(km.update_from_keystate({"e":True}))
print(km.update_from_keystate({"d":False}))
print(km.update_from_keystate({"e":False}))
print(km.update_from_keystate({"a":True, "b":False}))
print(km.update_from_keystate({"a":False}))
