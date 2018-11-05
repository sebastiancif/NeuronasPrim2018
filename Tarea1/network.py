import layer as ly
import numpy
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale
import matplotlib
import matplotlib.pyplot as plt
from time import sleep


#--------------------#


# float -> float
# Derivative of sigmoid function
def transferDerivative(x):
    return x*(1.0-x)

# List<int>, int -> List<int>
# Given a cardinal number and the number of classes, returns a binary classification vector
# e.g classVector(1,3) = [0 1 0], classVector(1,2) = [0 1], classVector(0,1) = [0]
def classVector(vector, classes):
    num = vector[0]
    if(not type(num)==int):
        num = int(num)
    vec = [0]*classes
    vec[num%classes] = 1
    return vec

# List<float> -> List<int>
# Given a vector of real numbers between 0 and 1, returns an array with 0s and 1s
def toBin(vector):
    bin = []
    for num in vector:
        if(num < 0.5):
            bin.append(0)
        else:
            bin.append(1)
    return bin

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


    # List<float> -> List<float>
    # Receives a Python list as input, returns the valuation of the network
    def feed(self, input):
        nextinput = input
        for layer in self.mylayers:
            nextinput = layer.feed(nextinput)
        return nextinput


    # List<float> List<float> [float]-> None
    # Trains the network using the given inputs and desiredoutputs
    def train(self, input, desiredoutput, learningrate = 0.2):
        lr = learningrate
        output = self.feed(input)
        self.errorBackpropagation(desiredoutput)
        self.updateWeightandBias(input, lr)

    # None -> List<float>
    # Get the last output of the network
    def getLastOutput(self):
        return self.mylayers[self.nlastlayer].getOutputs()

    # List<float> -> None
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


    # List<float> -> None
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


#------------ Inserción de datos ----------------------- #
    # string, int, [float], [boolean] -> None
    # Given a csv file name (e.g: "data.csv"), trains a classificator network by nepoch epochs
    # plotting the cuadratic error and precison obtained.
    def dataClasification(self, dtname, nepoch, learningrate = 0.2, randshuffle = False):
        try:
            dt = numpy.loadtxt(dtname,delimiter = ",") #Cargamos el dataset csv
        except:
            print("No se encuentra el archivo "+dtname)
            return
        rows, cols = dt.shape
        X = dt[:,0:cols-1] #split en datos y clases
        X_norm = minmax_scale(X) #Normalizamos los datos con el criterio visto en clases
        y = dt[:,cols-1:]
        numofclasses = len(numpy.unique(y)) #calculamos el numero total de clases
        X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size = 0.33, random_state = 27) #Separamos los datos en train/test
        error = []
        precision = []
        epochs = list(range(nepoch))
        print("Trabajando con un dataset de "+str(rows)+" observaciones, con "+str(cols)+" atributos cada una")
        print("Número de épocas: "+str(nepoch))
        print("¿Se reordena el training set en cada epoch?: "+str(randshuffle))
        print("Learning rate de la red: "+str(learningrate))
        print("Cantidad de clases del dataset: "+str(numofclasses))
        sleep(2)
        print("Inicio de computo por epochs, esto toma tiempo...")
        for epoch in epochs:
            if(randshuffle): #Mezclamos el orden de las tuplas en caso de quererlo
                X_train, y_train = shuffle(X_train, y_train)
            if(epoch == 0): #Anotamos valores sin training alguno de la red
                totalerror = 0
                for i in range(len(X_train)):
                    expected = classVector(y_train[i],numofclasses) #Generamos el vector de clase deseado
                    raw_output = self.feed(X_train[i]) #Output sin entrenar
                    errorvector = numpy.asarray(expected) - numpy.asarray(raw_output) #Comparamos output y expected
                    squarevector = errorvector**2
                    totalerror += squarevector.sum() #Guardamos el error cuadrático
                meanerror = (totalerror*1.0)/len(X_train) #Sacamos la media de los errores
                error.append(meanerror)
                #Fin de check de errores sin training
                #Calculo de precision sin training
                hits = 0
                for j in range(len(X_test)):
                    output = self.feed(X_test[j])
                    binOutput = toBin(output) #Discretizamos el vector de salida
                    expected = classVector(y_test[j],numofclasses)
                    if(expected == binOutput):
                        hits += 1 #Si son iguales, entonces es un acierto
                epochprec = hits*1.0/len(X_test)
                precision.append(epochprec)
                print("Fin epoch "+str(epoch)+"!")
                #Fin de testing, se acumula la precision en el vector correspondiente
            else:
                #Inicio de training
                totalerror = 0
                for i in range(len(X_train)):
                    expected = classVector(y_train[i],numofclasses) #Generamos el vector de clase deseado
                    self.train(X_train[i], expected, learningrate) #Entrenamos a la red
                    errorvector = numpy.asarray(expected) - numpy.asarray(self.getLastOutput()) #Comparamos output y expected
                    squarevector = errorvector**2
                    totalerror += squarevector.sum() #Guardamos el error cuadrático
                meanerror = (totalerror*1.0)/len(X_train) #Sacamos la media de los errores
                error.append(meanerror)
                #Fin de training, se acumula error en el vector correspondiente
                #Inicio de testing
                hits = 0
                for j in range(len(X_test)):
                    output = self.feed(X_test[j])
                    binOutput = toBin(output) #Discretizamos el vector de salida
                    expected = classVector(y_test[j],numofclasses)
                    if(expected == binOutput):
                        hits += 1 #Si son iguales, entonces es un acierto
                epochprec = hits*1.0/len(X_test)
                precision.append(epochprec)
                print("Fin epoch "+str(epoch)+"!")
                #Fin de testing, se acumula la precision en el vector correspondiente
        plotcond = "Learning rate ="+str(learningrate)+", Row Shuffle="+str(randshuffle)
        plt.subplot(2, 1, 1)
        plt.plot(epochs,error, '.-')
        plt.title(plotcond)
        plt.ylabel("Error cuadratico")

        plt.subplot(2, 1, 2)
        plt.plot(epochs,precision, '.-')
        plt.xlabel("Epoch")
        plt.ylabel("Precision")
        plt.show()
