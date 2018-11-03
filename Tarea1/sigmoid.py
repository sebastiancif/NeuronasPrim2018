import math
import numpy
import random

class Sigmoid:

    # int -> Sigmoid
    #Receives the number of inputs of the neuron
    def __init__(self,ninputs):
        self.weight = []
        for n in range(ninputs):
            self.weight.append(random.uniform(-2,2))
        self.bias = random.uniform(-2,2)
        self.output = 0
        self.delta = 1

    # [float ... float] -> float (0,1)
    #Receives a python list with inputs
    def feed(self, input):
        w = numpy.asarray(self.weight)
        x = numpy.asarray(input)
        z = numpy.dot(w,x) + self.bias
        self.output = 1/(1+math.exp(-z))
        return self.output

    # float -> None
    # Updates the bias of a neuron
    def setBias(self, b):
        self.bias = b

    # [float ... float ] -> None
    # Updates the neuron weights
    def setWeight(self, w):
        self.weight = w

    # float -> None
    # Updates the neuron delta
    def setDelta(self, d):
        self.delta = d
