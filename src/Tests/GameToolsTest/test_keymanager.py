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
