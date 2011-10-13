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
        self.assertEqual(bb.getOutput('out0'), 100)
        self.assertEqual(bb.getOutput('out1'), 200)
        self.assertEqual(bb.getOutput('out2'), -300)
        return

class TestArtificialNeuron(unittest.TestCase):
    #has only positives, meanfield, and T
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
    
    #has negatives, spin, and no T
    def test_withoutT(self):
        tcases = [[(0.089, -0.7063), (0.1653, -0.6145), (-0.041, 0.9843), (-0.9835, -0.6365), -1.0], [(0.9208, 0.1044), (0.0505, 0.9819), (0.0191, -0.9898), (0.1362, 0.2462), -1.0], [(0.9873, 0.424), (0.9531, -0.3273), (0.6517, -0.0728), (-0.8909, 0.9253), -1.0], [(0.9164, -0.5422), (0.2678, -0.7984), (0.2843, 0.4623), (-0.931, -0.3396), -1.0], [(0.5196, 0.4315), (-0.8262, -0.5443), (0.4527, -0.9646), (0.7993, -0.987), -1.0], [(0.0576, 0.5803), (-0.882, 0.2914), (0.308, -0.3341), (0.5839, 0.3249), -1.0], [(0.54, -0.8592), (0.7102, -0.2615), (0.2662, -0.153), (-0.0597, 0.8781), -1.0], [(0.2302, 0.7365), (-0.5541, -0.7312), (-0.6055, 0.3225), (-0.1408, -0.4408), -1.0], [(-0.466, -0.1326), (-0.7405, 0.0534), (0.5273, -0.0322), (0.3759, -0.1063), -1.0], [(0.1688, -0.3674), (-0.7474, -0.2167), (0.7298, -0.9801), (-0.6135, 0.8525), -1.0], [(-0.61, -0.2719), (0.1809, -0.3706), (0.7175, 0.8278), (0.2134, 0.3504), 1.0], [(-0.3115, 0.9577), (0.8449, -0.5191), (-0.7054, 0.7402), (0.4756, 0.1973), -1.0], [(0.2424, -0.6736), (-0.5308, 0.5492), (0.7721, 0.497), (-0.3798, -0.5948), -1.0], [(0.1768, -0.3122), (0.0975, 0.2031), (0.5155, -0.2339), (-0.8242, -0.7319), -1.0], [(-0.6279, -0.4887), (-0.399, -0.9639), (0.8166, -0.1852), (-0.8017, 0.9129), -1.0], [(0.0233, -0.4049), (0.0528, 0.0398), (-0.5337, 0.3784), (-0.9933, -0.697), -1.0], [(-0.496, -0.1517), (0.0798, 0.4819), (-0.8552, 0.1), (0.2776, -0.6455), -1.0], [(-0.8882, 0.3097), (0.7641, -0.393), (0.3983, -0.6928), (0.3225, -0.6684), -1.0], [(-0.8803, 0.7562), (-0.2118, -0.254), (-0.5008, -0.503), (-0.3519, 0.8691), -1.0], [(-0.8219, -0.4743), (0.9264, 0.3042), (-0.8395, -0.22), (0.2672, -0.5915), 1.0], [(-0.5801, -0.947), (0.0221, 0.1306), (0.6118, 0.3257), (0.4807, 0.8696), 1.0], [(-0.6468, -0.3523), (0.0617, 0.8705), (-0.3706, -0.2516), (-0.1695, 0.8523), -1.0], [(-0.0329, 0.3007), (-0.3537, 0.6724), (-0.6449, 0.1526), (-0.9122, 0.903), -1.0], [(-0.1412, -0.7595), (-0.6134, -0.622), (-0.8826, -0.4014), (-0.7182, -0.7776), 1.0], [(-0.6539, 0.5761), (0.6394, 0.7956), (-0.6838, 0.7267), (-0.3505, 0.623), -1.0]]
        an = Circuit.Chips.NeuralNet.ArtificalNeuron(4, .5, Circuit.Chips.NeuralNet.thresh_spin)
        self.assertTrue("T" not in an.inputs)
        self.assertEqual(len(an.inputs), 8)
        self.assertEqual(len(an.outputs), 1)
        for t in tcases:
            an.reset()
            for i, x in enumerate(t[:-1]):
                an.setInput("in"+str(i), x[0])
                an.setInput("w"+str(i), x[1])
            an.calculate()
            self.assertAlmostEqual(an.outputs["out"], t[-1])
        return

class TestLogicGates(unittest.TestCase):
    def setUp(self):
        self.and_truth = ([0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1])
        self.nand_truth = ([0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 0])
        self.or_truth = ([0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1])
        self.xor_truth = ([0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0])
        self.not_truth = [[0, 1], [1, 0]]
    
    def __tester(self, gate, truth):
        for s in truth:
            gate.setInput("a", s[0])
            gate.calculate()
            self.assertEqual(gate.getOutput("out"), s[1])
    
    def __tester2(self, gate, truth):
        for s in truth:
            gate.setInput("a", s[0])
            gate.setInput("b", s[1])
            gate.calculate()
            self.assertEqual(gate.getOutput("out"), s[2])
    
    def test_complexgate(self):
        not1 = Circuit.Chips.Logic.Not()
        nand1 = Circuit.Chips.Logic.Nand()
        not2 = Circuit.Chips.Logic.Not()
        and1 = Circuit.Chips.Logic.And()
        nand2 = Circuit.Chips.Logic.Nand()
        bbchips = {"not1":not1, "nand1":nand1, "not2":not2, "and1":and1, "nand2":nand2}
        bbinputs = {"inv1.a":"in0", "inv1.in1":"in1", "inv2.in2":"in2"}
        bboutputs = {"inv2.out0":"out0", "inv2.out1":"out1", "inv2.out2":"out2"}
        bbconstants = {}
        bbwires=[("inv1.out0", "inv2.in0"), ("inv1.out1", "inv2.in1")]
        return
    
    def test_simplegates(self):
        #nand
        nand = Circuit.Chips.Logic.Nand()
        self.__tester2(nand, self.nand_truth)
        
        #and
        andg = Circuit.Chips.Logic.And()
        self.__tester2(andg, self.and_truth)
        
        #or
        org = Circuit.Chips.Logic.Or()
        self.__tester2(org, self.or_truth)
        
        #xor
        xor = Circuit.Chips.Logic.Xor()
        self.__tester2(xor, self.xor_truth)
        
        #not
        notg = Circuit.Chips.Logic.Not()
        self.__tester(notg, self.not_truth)
        
        return
    
    def test_xbitgates(self):
        return

if __name__ == '__main__':
    unittest.main()
    