import network as nw
import numpy
import operator
import matplotlib
import matplotlib.pyplot as plt
# int int -> List<int>
# Recibe un input binario y retorna [1 0] si la respuesta xor es 0 y [0 1] si la respuesta xor es 1
def myXor(b1,b2):
    if(operator.xor(b1,b2) == 0):
        return [1, 0]
    else:
        return [0, 1]
# List<float> -> List<int>
# Vuelve binario un array de float entre 0 y 1
def toBin(input):
    res = []
    for num in input:
        if(num < 0.5):
            res.append(0)
        else: # num >= 0.5
            res.append(1)
    return res

class XORNetwork:
    '''
    Tabla de XOR:
    0 0 0
    0 1 1
    1 0 1
    1 1 0
    '''

    def __init__(self):
        self.network = nw.Network(2,2,[3,2])

    # None -> None
    # Reinicia la red neuronal XOR
    def reset(self):
        self.network = nw.Network(2,2,[3,2])
        print("Red reseteada!")

    def feed(self, input):
        return self.network.feed(input)

    # int -> None
    # Entrena a la red XOR con ejemplos de XOR aleatorios según la cantidad especificada
    def trainNTimes(self, n, learningrate = 0.2):
        numpy.random.seed()
        trainx = numpy.random.randint(0,2,n)
        trainy = numpy.random.randint(0,2,n)
        for i in range(len(trainx)):
            self.network.train([trainx[i],trainy[i]],myXor(trainx[i],trainy[i]), learningrate)
        print("Red entrenada "+str(n)+" veces!")

    # int, int, int -> None
    # Recibe numero de entrenamientos, paso de evaluacion y cantidad de casos de test
    # Retorna la cantidad de aciertos por paso en un arreglo
    def getErrorOfTraining(self, nepoch, trainstep=100, learningrate = 0.2):
        numpy.random.seed()
        testx = numpy.random.randint(0,2,int(trainstep*.3))
        testy = numpy.random.randint(0,2,int(trainstep*.3))
        trainx = numpy.random.randint(0,2,trainstep)
        trainy = numpy.random.randint(0,2,trainstep)
        precision = []
        error = []
        epoch = 0
        epochs = list(range(nepoch))
        print('Generando información para '+str(nepoch)+" epochs...")
        for cepoch in epochs:
            #Primero entrenamos con todo el set de training
            totalerror = 0
            for i in range(trainstep):
                expected = myXor(trainx[i],trainy[i])
                self.network.train([trainx[i],trainy[i]], expected, learningrate)
                errorvector = numpy.asarray(expected) - numpy.asarray(self.network.getLastOutput())
                squarevector = errorvector**2
                totalerror += squarevector.sum()
            meanerror = (totalerror*1.0)/trainstep
            error.append(meanerror)
            #Ahora la etapa de testing
            hits = 0
            for i in range(len(testx)):
                output = self.network.feed([testx[i],testy[i]])
                idealizedoutput = toBin(output) #Discretizamos las respuestas
                expected = myXor(testx[i],testy[i])
                if(expected == idealizedoutput):
                    hits+=1
            thisprec = hits*1.0/len(testx)
            precision.append(thisprec)

        plt.figure(1)
        plt.subplot(211)
        plt.plot(epochs,error)
        plt.subplot(212)
        plt.plot(epochs,precision)
        plt.show()

def main():
    nw = XORNetwork()
    nw.getErrorOfTraining(20)
    nw.reset()
    nw.getErrorOfTraining(50)
    nw.reset()
    nw.getErrorOfTraining(100)
if __name__ == '__main__':
    main()
