import network as nw
import numpy
import operator


class XORNetwork:
    '''
    Tabla de XOR:
    0 0 0
    0 1 1
    1 0 1
    1 1 0
    '''

    def __init__(self):
        self.network = nw.Network(2,2,[3,1])

    # None -> None
    # Reinicia la red neuronal XOR
    def reset(self):
        self.network = nw.Network(2,2,[3,1])
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
            self.network.train([trainx[i],trainy[i]],[operator.xor(trainx[i],trainy[i])], learningrate)
        print("Red entrenada "+str(n)+" veces!")

    # int, int, int -> [float ... float]
    # Recibe numero de entrenamientos, paso de evaluacion y cantidad de casos de test
    # Retorna la cantidad de aciertos por paso en un arreglo
    def getErrorOfTraining(self, ntrains, trainstep, ntest):
        numpy.random.seed()
        testx = numpy.random.randint(0,2,ntest)
        testy = numpy.random.randint(0,2,ntest)
        trainx = numpy.random.randint(0,2,ntrains)
        trainy = numpy.random.randint(0,2,ntrains)
        precision = []
        trainCounter = 0
        for i in range(ntrains):
            if(trainCounter < trainstep):
                self.network.train([trainx[i],trainy[i]],[operator.xor(trainx[i],trainy[i])])
                trainCounter+=1
                continue
            else:
                for j in range(ntest):
                    output = self.network.feed([testx[j],testy[j]])
                    desired = operator.xor(testx[j],testy[j])
                    algo = 0
        return
