import unittest
import YoukaiTools.GameTools as GameTools

class TestKeyManager(unittest.TestCase):
    def setUp(self):
        self.km = GameTools.KeyManager(["a", "b", "c", "d", "e"])
        return
    
    def tearDown(self):
        return
    
class TestBasicKeys(TestKeyManager):
    def test_basic(self):
        self.assertEqual(len(self.km.update_from_keyset(keyset=set())), 0)
        self.km.update_from_keyset(keyset=set(["b", "d"])) #b_down, d_down
        self.km.update_from_keyset(keyset=set(["b", "d", "e"])) #e_down
        self.km.update_from_keyset(keyset=set(["b", "e"])) #d_up
        self.km.update_from_keyset(keyset=set(["b"])) #e_up
        self.km.update_from_keyset(keyset=set(["a"])) #a_down, b_up
        self.km.update_from_keyset(keyset=set()) #a_up

if __name__ == '__main__':
    unittest.main()
    