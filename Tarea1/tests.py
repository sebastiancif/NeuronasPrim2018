from network import *
from sigmoid import *
from layer import *
import unittest

sig = Sigmoid(3)
lay = Layer(5,3)
nw = Network(3,5,[5,3,3])

class TestSig(unittest.TestCase):
    def testnotnull(self):
        self.assertNotEqual(None, sig)
    def testinit(self):
        self.assertEqual(0, sig.output)
    def testweight(self):
        self.assertNotEqual([], sig.weight)
    def testdelta(self):
        sig.setDelta(0.5)
        self.assertEqual(0.5,sig.delta)
    def testbias(self):
        sig.setBias(0.8)
        self.assertEqual(0.8,sig.bias)

class TestLayer(unittest.TestCase):
    def testnotnull2(self):
        self.assertNotEqual(None, lay)
    def testinit2(self):
        self.assertEqual(lay.nneurons,5)
        self.assertEqual(len(lay.myneurons),5)

class TestNetwork(unittest.TestCase):
    def testnotnull3(self):
        self.assertNotEqual(None, nw)
    def testinit(self):
        self.assertEqual(len(nw.mylayers),3)
        self.assertEqual(nw.nlastlayer,2)
        self.assertEqual(nw.ninputs,5)


if __name__ == '__main__':
    unittest.main()
