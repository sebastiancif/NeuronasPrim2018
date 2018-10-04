import random
import numpy


class LPerceptron:

    # int -> LPerceptron
    #Recibe la cantidad de inputs que recibirá el perceptron
    def __init__(self,ninputs):
        self.weight = []
        for n in range(ninputs):
            self.weight.append(random.uniform(-2,2))
        self.bias = random.uniform(-2,2)

    # [x1 x2 ... xk] -> int (0,1)
    #Recibe un input en formato lista de python
    def feed(self, input):
        w = numpy.asarray(self.weight)
        x = numpy.asarray(input)
        sum = numpy.dot(w,x)
        if(sum + self.bias <=0):
            return 0
        else:
            return 1

    # [x1 x2 ... xk] int(0,1) -> None
    #Recibe un input para el perceptron y el output esperado
    def train(self,x,y):
        diff = y - self.feed(x)
        lr = 0.1
        for i in range(len(self.weight)):
            self.weight[i] = self.weight[i] + (lr * x[i] * diff)
        self.bias = self.bias + (lr * diff)
        return
