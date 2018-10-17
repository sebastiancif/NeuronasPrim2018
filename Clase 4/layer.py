import sigmoid as sg
import numpy

class Layer:
    # int , int -> Layer
    # Creates a layer with nneurons that receive kinputs
    def __init__(self, nneurons, kinputs):
        self.nneurons = nneurons
        self.myneurons = []
        for n in range(nneurons):
            self.myneurons.append(sg.Sigmoid(kinputs))

    # [float ... float] -> [float ... float]
    # Receives a python vector as input, returns the outputs of every neuron as vector
    def feed(self, vectorinput):
        layeroutput = []
        for neuron in self.myneurons:
            layeroutput.append(neuron.feed(vectorinput))
        return layeroutput

    # None -> [float ... float]
    # Returns all the outputs of the layer
    def getOutputs(self):
        outputs = []
        for neuron in self.myneurons:
            outputs.append(neuron.output)
        return outputs

    # None -> [float ... float]
    # Returns all the weights of the layer
    def getWeights(self):
        weights = []
        for neuron in self.myneurons:
            weights.append(neuron.weight)
        return weights

    # None -> [float ... float]
    # Return all the deltas of the layer
    def getDeltas(self):
        deltas = []
        for neuron in self.myneurons:
            deltas.append(neuron.delta)
        return deltas

    # [float ... float] -> None
    # Updates the layer deltas
    def updateDeltas(self, deltalist):
        i = 0
        for neuron in self.myneurons:
            neuron.setDelta(deltalist[i])
            i+=1

    # [float ... float], float -> None
    # Updates the weights and bias of the layer
    def updateWeightandBiasusingLR(self, input, lr):
        for neuron in self.myneurons:
            oldweights = neuron.weight
            newweights = (oldweights + lr*neuron.delta*numpy.asarray(input)).tolist()
            newbias = neuron.bias + (lr*neuron.delta)
            neuron.setBias(newbias)
            neuron.setWeight(newweights)
