import unittest
import numpy

class Perceptron:
    #Recibe como peso un arreglo y como bias un double
    def __init__(self,weight,bias):
        self.w = weight
        self.b = bias

    #Recibe como input un arreglo con los inputs binarios
    def feed(self, input):
        a = numpy.asarray(self.w)
        b = numpy.asmatrix(input).transpose()
        sum = a.dot(b)[0,0]
        if(sum + self.b<=0):
            return 0
        else:
            return 1

class SumGate:

    def __init__(self):
        self.p1 = Perceptron([-2,-2],3)

    #Recibe los dos elementos de la suma.
    #Retorna un array con la respuesta y el carry asociado [respuesta, carry].
    def binSum(self,x1,x2):
        res1 = self.p1.feed([x1,x2])
        res2 = self.p1.feed([x1,res1])
        res3 = self.p1.feed([res1,x2])
        carry = self.p1.feed([res1,res1])
        resres = self.p1.feed([res2,res3])
        return [resres,carry]


#Cosas globales para testing de perceptrones

pand = Perceptron([2,2],-3)
por = Perceptron([2,2],-1)
pnand = Perceptron([-2,-2],3)
cerocero = [0,0]
cerouno = [0,1]
unouno = [1,1]
unocero = [1,0]

pnot = Perceptron([-2],1)



class TestingPerceptrons(unittest.TestCase):

    def testing_and(self):
        self.assertEqual(pand.feed(cerocero),0)
        self.assertEqual(pand.feed(cerouno),0)
        self.assertEqual(pand.feed(unouno),1)
        self.assertEqual(pand.feed(unocero),0)

    def testing_or(self):
        self.assertEqual(por.feed(cerocero),0)
        self.assertEqual(por.feed(cerouno),1)
        self.assertEqual(por.feed(unouno),1)
        self.assertEqual(por.feed(unocero),1)

    def testing_nand(self):
        self.assertEqual(pnand.feed(cerocero),1)
        self.assertEqual(pnand.feed(cerouno),1)
        self.assertEqual(pnand.feed(unouno),0)
        self.assertEqual(pnand.feed(unocero),1)

    def testing_not(self):
        self.assertEqual(pnot.feed([0]),1)
        self.assertEqual(pnot.feed([1]),0)

#Sumador para testing

sumador = SumGate()

class TestingSumGate(unittest.TestCase):

    def testing_sum(self):
        self.assertEqual(sumador.binSum(0,0),[0,0])
        self.assertEqual(sumador.binSum(0,1),[1,0])
        self.assertEqual(sumador.binSum(1,0),[1,0])
        self.assertEqual(sumador.binSum(1,1),[0,1])


if __name__ == '__main__':
    unittest.main()
