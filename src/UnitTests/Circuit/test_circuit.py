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

class TestArtificialNeuron(unittest.TestCase):
    def test_withT(self):
        tcases = [[(0.995, 0.5666), (0.2389, 0.3728), (0.7665, 0.1629), 0.8325, 0.7325295227347438], [(0.7789, 0.3576), (0.2125, 0.93), (0.8018, 0.2482), 0.0929, 0.9999990263269115], [(0.7879, 0.8048), (0.1348, 0.5842), (0.5434, 0.4019), 0.2074, 0.9997482710077739], [(0.7851, 0.8579), (0.4285, 0.4212), (0.4253, 0.6228), 0.1204, 0.9999999830534884], [(0.2926, 0.3967), (0.7139, 0.5807), (0.4658, 0.8043), 0.1096, 0.9999998661497648], [(0.4795, 0.4926), (0.4622, 0.8489), (0.2657, 0.3984), 0.8465, 0.7001495431715], [(0.9976, 0.7311), (0.5944, 0.454), (0.7098, 0.3298), 0.3184, 0.9991361511327517], [(0.1743, 0.3119), (0.0078, 0.7541), (0.4948, 0.2134), 0.8072, 0.20260403388652318], [(0.7134, 0.054), (0.5896, 0.6303), (0.3061, 0.0963), 0.5143, 0.6935710809714969], [(0.9393, 0.9897), (0.6211, 0.3894), (0.7373, 0.3279), 0.0027, 1.0], [(0.0868, 0.5725), (0.5031, 0.5647), (0.7208, 0.121), 0.868, 0.45026689092452515], [(0.2572, 0.6689), (0.8416, 0.6571), (0.0182, 0.5779), 0.9532, 0.6479106625585448], [(0.7416, 0.9401), (0.7805, 0.623), (0.0872, 0.8958), 0.8845, 0.8909014341493647], [(0.9405, 0.579), (0.0996, 0.3995), (0.1028, 0.8753), 0.8351, 0.6681937755404503], [(0.8576, 0.4964), (0.15, 0.3905), (0.3656, 0.9253), 0.0649, 0.9999999999804084], [(0.3097, 0.0906), (0.1773, 0.2144), (0.897, 0.1668), 0.636, 0.32670729960177675], [(0.5479, 0.8496), (0.0078, 0.6757), (0.6866, 0.0164), 0.2947, 0.9268622330270743], [(0.3389, 0.9862), (0.7926, 0.8631), (0.5504, 0.2075), 0.8669, 0.8633634586239414], [(0.8631, 0.2655), (0.8085, 0.3643), (0.7408, 0.7398), 0.5037, 0.9720233041004869], [(0.4408, 0.2711), (0.6085, 0.4033), (0.274, 0.8255), 0.5294, 0.8063618203133396], [(0.575, 0.1698), (0.066, 0.1193), (0.3179, 0.1677), 0.0129, 0.9999999999595197], [(0.6492, 0.0074), (0.9084, 0.7453), (0.697, 0.9614), 0.784, 0.9383907897024669], [(0.8577, 0.8531), (0.4168, 0.5745), (0.6184, 0.3495), 0.9215, 0.8587142348506789], [(0.1403, 0.9076), (0.2874, 0.5688), (0.6242, 0.841), 0.5833, 0.8850331376584316], [(0.7993, 0.9325), (0.5159, 0.6563), (0.8551, 0.6062), 0.6961, 0.9801678351252966]]
        an = Circuit.Chips.NeuralNet.ArtificalNeuron(3, None)
        self.assertTrue("T" in an.inputs)
        self.assertEqual(len(an.inputs), 7)
        self.assertEqual(len(an.outputs), 1)
        for t in tcases:
            an.reset()
            for i, x in enumerate(t[:-2]):
                an.setInput("in"+str(i), x[0])
                an.setInput("w"+str(i), x[1])
            an.setInput("T", t[-2])
            an.calculate()
            self.assertAlmostEqual(an.outputs["out"], t[-1])
        return
    
    def test_withoutT(self):
        an = Circuit.Chips.NeuralNet.ArtificalNeuron(4, .5)
        self.assertTrue("T" not in an.inputs)
        self.assertEqual(len(an.inputs), 8)
        self.assertEqual(len(an.outputs), 1)
        return

if __name__ == '__main__':
    unittest.main()
    