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
        print(inv.outputs)
        return

class TestBreadBoard(unittest.TestCase):
    def test_breadboard(self):
        return
    
if __name__ == '__main__':
    unittest.main()
    