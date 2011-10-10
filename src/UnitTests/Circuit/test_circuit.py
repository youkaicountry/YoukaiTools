import YoukaiTools.Circuit as Circuit
import unittest

class TestKeyManager(unittest.TestCase):
    def test_basicoverride(self):
        inv = Circuit.Chips.Math.InvertNeuron(3)
        inv.setInput("in0", 1.2)
        inv.setInput("in1", -2.56)
        inv.setInput("in2", 0)
        inv.calculate()
        self.assertAlmostEqual(inv.getOutput("out0"), -1.2)
        self.assertAlmostEqual(inv.getOutput("out1"), 2.56)
        self.assertEqual(inv.getOutput("out2"), 0)
        return

class TestBreadBoard(unittest.TestCase):
    def test_breadboard(self):
        print("bread")
        inv1 = Circuit.Chips.Math.InvertNeuron(2)
        inv2 = Circuit.Chips.Math.InvertNeuron(3)
        
        bbchips = {"inv1":inv1, "inv2":inv2}
        bbinputs = {"inv1.in0":"in0", "inv1.in1":"in1", "inv2.in2":"in2"}
        bboutputs = {"inv2.out0":"out0", "inv2.out1":"out1", "inv2.out2":"out2"}
        bbconstants = {}
        bbwires=[("inv1.out0", "inv2.in0"), ("inv1.out1", "inv2.in1")]
        bb = Circuit.Chips.Cases.BreadBoard(bbchips, bbinputs, bboutputs, bbconstants, bbwires)
        
        bb.setInput('in0', 100)
        bb.setInput('in1', 200)
        bb.setInput('in2', 300)
        bb.calculate()
        print(bb.getOutput('out0'))
        print(bb.getOutput('out1'))
        print(bb.getOutput('out2'))
        return
    
if __name__ == '__main__':
    unittest.main()
    