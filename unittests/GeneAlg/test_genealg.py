import YoukaiTools.GeneAlg as GeneAlg
import unittest

def dummy_basic():
    return "basic"

def dummy_random():
    return "random"

def dummy_fitness(obj):
    return 1

def dummy_func():
    return

class TestGeneAlg(unittest.TestCase):
    def test_community(self):
        g = GeneAlg.make_gene(dummy_fitness, dummy_func, dummy_func, dummy_random, dummy_basic, dummy_func)
        s = ["seed" for x in range(3)]
        o = GeneAlg.make_options(seeds=s)
        ga = GeneAlg.Algorithms.Community(g, o, 5)
        gal = ga.getGeneList()
        self.assertItemsEqual([(1,'basic'),(1,'basic'),(1,'seed'),(1,'seed'),(1,'seed')] , gal)
        return

    def test_pool(self):
        g = GeneAlg.make_gene(dummy_fitness, dummy_func, dummy_func, dummy_random, dummy_basic, dummy_func)
        s = ["seed" for x in range(3)]
        o = GeneAlg.make_options(seeds=s)
        ga = GeneAlg.Algorithms.Community(g, o, 5)
        gal = ga.getGeneList()
        self.assertItemsEqual([(1,'basic'),(1,'basic'),(1,'seed'),(1,'seed'),(1,'seed')] , gal)
        return

if __name__ == '__main__':
    unittest.main()
    