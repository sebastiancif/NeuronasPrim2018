import learningperceptron as lp
import matplotlib.pyplot as plt
import random
import numpy
import time

class PointPlotter:
    # int -> None
    #Plotea dado el numero de entrenamientos n
    def plotUsing(self, numtrain):
        myPerc = lp.LPerceptron(2)
        #aquí se entrena al perceptron
        for i in range(numtrain):
            point = [random.random(),random.random()]
            ans = updownidentity(point)
            myPerc.train(point,ans)
        ranx = numpy.random.rand(1,100)
        rany = numpy.random.rand(1,100)
        ans = numpy.zeros(100)
        for i in range(len(ranx[0])):
            ans[i] = myPerc.feed([ranx[0][i],rany[0][i]])
        plt.scatter(ranx[0],rany[0],c=ans)
        x = [0,1]
        plt.plot(x,x, 'r')
        plt.show()

class PrecisionPlotter:

    # int -> None
    # Plotea la curva de precisión desde 0 entrenamientos hasta el limite dado, usando 100 puntos a clasificar
    def plotTo(self, trainlim):
        fullTrain = range(0,trainlim+1,100)
        prec = []
        for n in fullTrain:
            exploitedPerc = lp.LPerceptron(2)
            for i in range(n):
                point = [random.random(), random.random()]
                ans = updownidentity(point)
                exploitedPerc.train(point, ans)
            success = 0
            ranx = numpy.random.rand(1,100)
            rany = numpy.random.rand(1,100)
            for i in range(len(ranx[0])):
                if(updownidentity([ranx[0][i],rany[0][i]]) == exploitedPerc.feed([ranx[0][i],rany[0][i]])):
                    success+=1
            prec.append(float(success)/100)
        plt.plot(fullTrain, prec)
        plt.show()



# [float float] -> int (0,1)
#Funcion que clasifica un punto sobre la curva x = y. 0 si está bajo la curva, 1 si está sobre la curva
def updownidentity(point):
    if(point[0] <= point[1]):
        return 0
    else:
        return 1

def main():
    pp = PointPlotter()
    print("Resultado de un training set de tamaño 50")
    pp.plotUsing(50)
    input("Presione Enter para seguir")
    time.sleep(1)
    print("Resultado de un training set de tamaño 300")
    pp.plotUsing(300)
    input("Presione Enter para seguir")
    time.sleep(1)
    print("Resultado de un training set de tamaño 1000")
    pp.plotUsing(1000)
    input("Presione Enter para seguir")
    time.sleep(1)
    prp = PrecisionPlotter()
    print("Ploteando evolución de precisión hasta 10000")
    prp.plotTo(10000)





if __name__ == "__main__":
    main()
