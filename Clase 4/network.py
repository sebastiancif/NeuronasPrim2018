import layer as ly
import random
import numpy
import re
import os
# float -> float
# Derivative of sigmoid function
def transferDerivative(x):
    return x*(1.0-x)

# string -> File
# Reordena las lineas de un archivo dado
def sortFileRows(filename):
    random.seed()
    with open(filename,'r') as source:
        next(source)
        data = [(random.random(),line) for line in source]
    source.close()
    data.sort()
    with open('random'+filename,'w') as output:
        for _, line in data:
            output.write(line)
    output.close()
    return "random"+filename

class Network:

    # int, int, int, List<int> -> Network
    # Receives number of layers, number of inputs and number of neurons per layers of the network
    def __init__(self, nlayers, ninputs, nneuronslayer):
        self.mylayers = []
        self.nlastlayer = nlayers-1
        self.ninputs = ninputs
        previousneurons = ninputs
        for i in range(nlayers):
            self.mylayers.append(ly.Layer(nneuronslayer[i], previousneurons))
            previousneurons = nneuronslayer[i]

    # List<float> List<float> -> None
    # Trains the network using the given inputs and desiredoutputs
    def train(self, input, desiredoutput, learningrate = 0.2):
        lr = learningrate
        output = self.feed(input)
        self.errorBackpropagation(desiredoutput)
        self.updateWeightandBias(input, lr)

    # string, string, [float] -> List<List<float>>
    # Entrena a la red con una línea de string, separada por el indicador separator
    def trainLine(self, line, separator, learningrate = 0.2):
        myline = re.sub('\n', '', line)
        wordlist = myline.split(separator)
        self.train(wordlist[:self.ninputs],[self.ninputs:], learningrate)



    def trainDataSet(self, datasetname, validationsetname, separator, nepoch, learningrate=0.2, unsortepoch = False):
        input = datasetname
        for epoch in nepoch:
            if(unsortepoch):
                input = sortFileRows(input)
            with open(input,'r') as trainingdata:
                for line in trainingdata:
                    self.trainLine(line, separator, learningrate)



        for epoch in range(nepoch):
            for line in dataset:
                train(line)
        epoch
        precision
        errorvector
        if(unsortepoch):
            os.remove(input)

    # [float ... float] -> [float ... float]
    # Receives a Python list as input, returns the valuation of the network
    def feed(self, input):
        nextinput = input
        for layer in self.mylayers:
            nextinput = layer.feed(nextinput)
        return nextinput

    # [float ... float] -> None
    # Updates delta in every neuron using the expected value
    def errorBackpropagation(self, expected):
        current  = self.nlastlayer
        while(current >= 0):
            if(current == self.nlastlayer): #output layer
                    output = numpy.asarray(self.mylayers[current].getOutputs())
                    errorvector = expected - output
                    deltalist = (errorvector * transferDerivative(output)).tolist()
                    self.mylayers[current].updateDeltas(deltalist)
                    current-=1
            else: #hidden and input layers
                output = numpy.asarray(self.mylayers[current].getOutputs())
                weightmatrix = numpy.asmatrix(self.mylayers[current+1].getWeights())
                deltamatrix = numpy.asmatrix(self.mylayers[current+1].getDeltas())
                errorvector = numpy.asarray(deltamatrix*weightmatrix)[0]
                deltalist = (errorvector * transferDerivative(output)).tolist()
                self.mylayers[current].updateDeltas(deltalist)
                current-=1

    # [float ... float ] -> None
    # Updates the weights and bias of the network
    def updateWeightandBias(self, input, lr):
        current = 0
        for layer in self.mylayers:
            if(current == 0): #input layer
                layer.updateWeightandBiasusingLR(input, lr)
                current+=1
            else: #current > 0
                previousoutput = self.mylayers[current-1].getOutputs()
                layer.updateWeightandBiasusingLR(previousoutput, lr)
                current+=1
