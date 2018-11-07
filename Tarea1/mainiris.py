from network import *
from time import sleep

def maincapas():
    print("")
    print("TEST DE CAPAS")
    print("Se prueban 5 casos 2, 3, 4, 5 y 10 capas")
    sleep(1)
    print("Red Neuronal de 2 capas")
    nw1 = Network(2,4,[4,3])
    nw1.dataClasification("iris.csv",20, learningrate = 0.5, randshuffle = True)
    print("Red Neuronal de 3 capas")
    nw2 = Network(3,4,[4,16,3])
    nw2.dataClasification("iris.csv",20, learningrate = 0.5, randshuffle = True)
    print("Red Neuronal de 4 capas")
    nw3 = Network(4,4,[4,16,16,3])
    nw3.dataClasification("iris.csv",20, learningrate = 0.5, randshuffle = True)
    print("Red Neuronal de 5 capas")
    nw4 = Network(5,4,[4,16,16,16,3])
    nw4.dataClasification("iris.csv",20, learningrate = 0.5, randshuffle = True)
    print("Caso extremo: Red Neuronal de 10 capas")
    nw5 = Network(10,4,[4,16,16,16,16,16,16,16,16,3])
    nw5.dataClasification("iris.csv",20, learningrate = 0.5, randshuffle = True)

def mainspeed():
    print("")
    print("TEST DE VELOCIDAD")
    print("Se prueban 3 casos, red optima, red 10 capas y red optima con 5 veces la cantidad de neuronas")
    sleep(1)
    print("Red optima:")
    nw2 = Network(3,4,[4,16,3])
    nw2.dataClasification("iris.csv",20, learningrate = 0.5, randshuffle = True, timer = True)
    sleep(2)
    print("Red 10 capas")
    nw5 = Network(10,4,[4,16,16,16,16,16,16,16,16,3])
    nw5.dataClasification("iris.csv",20, learningrate = 0.5, randshuffle = True, timer = True)
    sleep(2)
    print("Red optima con 5 veces la cantidad de neuronas por capa")
    nw6 = Network(5,4,[4,80,3])
    nw6.dataClasification("iris.csv",20, learningrate = 0.5, randshuffle = True, timer = True)
    sleep(2)
    return

def mainlearningrate():
    print("")
    print("TEST DE LEARNING RATE")
    print("Testeamos con 3 learnings rates: 0.2 0.5 y 1.0 sobre una red de 4 capas")
    sleep(1)
    nw1 = Network(4,4,[4,16,16,3])
    nw1.dataClasification("iris.csv",20, learningrate = 0.2, randshuffle = True)
    nw2 = Network(4,4,[4,16,16,3])
    nw2.dataClasification("iris.csv",20, learningrate = 0.5, randshuffle = True)
    nw3 = Network(4,4,[4,16,16,3])
    nw3.dataClasification("iris.csv",20, learningrate = 1.0, randshuffle = True)
    return

def mainorder():
    print("")
    print("TEST DE ORDEN DE DATOS")
    print("Testeamos con la red óptima cambiando entre reordenamiento y no reordenamiento de filas en el training")
    sleep(1)
    nw3 = Network(3,4,[4,16,3])
    nw3.dataClasification("iris.csv",20, learningrate = 1.0, randshuffle = True)
    nw4 = Network(3,4,[4,16,3])
    nw4.dataClasification("iris.csv",20, learningrate = 1.0, randshuffle = False)
    return

if __name__ == '__main__':
    runoptions = {'1': maincapas,
                    '2': mainspeed,
                    '3': mainlearningrate,
                    '4': mainorder,
                    }
    try:
        while(True):
            num = input("Ingrese el numero de la pregunta a responder (1 a 4), o cualquier cosa para terminar: ")
            runoptions[num]()
    except:
        print("Programa terminado")
