import YoukaiTools.Neuron as Neuron
import unittest


class InvertNeuron(Neuron.BaseNeuron):
    def __init__(self, numinputs):
        self.setup([str(x) for x in range(numinputs)], [str(x) for x in range(numinputs)])
        return
    
    def doCalculation(self):
        for k in self.inputs.keys():
            self.outputs[k] = -self.inputs[k]
        return

class TestKeyManager(unittest.TestCase):
    def test_basicoverride(self):
        inv = InvertNeuron(3)
        inv.setInput("0", 1.2)
        inv.setInput("1", -2.56)
        inv.setInput("2", 0)
        inv.calculate()
        self.assertAlmostEqual(inv.getOutput("0"), -1.2)
        self.assertAlmostEqual(inv.getOutput("1"), 2.56)
        self.assertEqual(inv.getOutput("2"), 0)
        print(inv.outputs)
        return
    
if __name__ == '__main__':
    unittest.main()
    