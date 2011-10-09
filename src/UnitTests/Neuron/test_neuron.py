import YoukaiTools.Neuron as Neuron
import unittest

class TestKeyManager(unittest.TestCase):
    def test_basicoverride(self):
        inv = Neuron.Neurons.Math.InvertNeuron(3)
        inv.setInput("0", 1.2)
        inv.setInput("1", -2.56)
        inv.setInput("2", 0)
        inv.calculate()
        self.assertAlmostEqual(inv.getOutput("0"), -1.2)
        self.assertAlmostEqual(inv.getOutput("1"), 2.56)
        self.assertEqual(inv.getOutput("2"), 0)
        return

class TestBreadBoard(unittest.TestCase):
    def test_breadboard(self):
        print("bread")
        inv1 = Neuron.Neurons.Math.InvertNeuron(2)
        inv2 = Neuron.Neurons.Math.InvertNeuron(3)
        
        bbneurons = {"inv1":inv1, "inv2":inv2}
        bbinputs = {"inv1.0":"0", "inv1.1":"1", "inv2.2":"2"}
        bboutputs = {"inv2.0":"0", "inv2.1":"1", "inv2.2":"2"}
        bbconstants = {}
        bbwires=[("inv1.0", "inv2.0"), ("inv1.0", "inv2.1")]
        bb = Neuron.Neurons.Cases.BreadBoard(bbneurons, bbinputs, bboutputs, bbconstants, bbwires)
        return
    
if __name__ == '__main__':
    unittest.main()
    