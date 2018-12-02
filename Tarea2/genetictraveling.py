from route import newDM, Tour, Route
import random
from itertools import permutations
from math import ceil, sqrt
#--------------------------------------------

# Route -> float
# Given a route, calculates the fitness of it
def fitFun(route):
    return 1.0/route.getDistance()

# int -> int
# Calculates the mininum number of parents to make a population of children
def numParents(children):
    return ceil((1+sqrt(1+8*children))/2)

#Genetic algorithm for Traveling Salesman Problem
#It makes population of Route objects that consist in a path and the distance of the path
class GenAlg:
    def __init__(self, npop, ngen, tour):
        self.npop = npop
        self.ngen = ngen
        self.k = ceil(npop*3/4)
        self.tour = tour
        self.pop = []
        self.matingpool = []
        self.mutationrate = 0.1
        self.nparents = numParents(self.npop)
        self.best = None

    def setGenerations(self, newngen):
        self.ngen = newngen

    def setNPopulation(self, newnpop):
        self.npop = newnpop

    def setK(self, newk):
        self.k = newk

    def setMutRate(self, newmr):
        self.mutationrate = newmr

    def initPopulation(self):
        self.pop = []
        for i in range(self.npop):
            self.pop.append((self.tour).makeRoute())

    def kTournament(self):
        best = None
        for i in range(self.k):
            ind = random.choice(self.pop)
            while(ind in self.matingpool):
                ind = random.choice(self.pop)
            if(best == None or fitFun(best) < fitFun(ind)):
                best = ind
        return best

    def makeNewGen(self):
        if(not self.pop):
            print("Error, no population")
            return
        else:
            self.matingpool = []
            while(len(self.matingpool) < self.nparents):
                self.matingpool.append(self.kTournament())
            choices = list(permutations(range(len(self.matingpool)),2))
            newgen = []
            while(len(newgen) < self.npop):
                index1, index2 = choices.pop(random.randrange(len(choices)))
                newborn = self.tour.newIndividual(self.matingpool[index1],self.matingpool[index2],self.mutationrate)
                newgen.append(newborn)
            self.pop = newgen

    def storeBest(self):
        best = None
        for route in self.pop:
            if(best == None or fitFun(best) < fitFun(route)):
                best = route
        self.best = best

    def run(self):
        print("Iniciando algoritmo")
        print(f"Poblacion de {self.npop} individuos")
        print(f"Mutation rate igual a {self.mutationrate}")
        self.pop = self.matingpool = []
        self.best = None
        self.initPopulation()
        self.storeBest()
        generation = 0
        while(generation < self.ngen):
            self.makeNewGen()
            self.storeBest()
            generation+=1
        print(f"Mejor individuo luego de {generation} generaciones")
        print(f"Distancia del camino: {self.best.getDistance()}")
        print(f"Ruta: {self.best.getPath()}")
        return self.best.getDistance()

def main():
    matrix5 = [[0,1,6,6,5],
                [1,0,2,6,6],
                [6,2,0,3,6],
                [6,6,3,0,4],
                [5,6,6,4,0]]
    matrix10 = [[0,1,11,11,11,11,11,11,11,10],
                [1,0,2,11,11,11,11,11,11,11],
                [11,2,0,3,11,11,11,11,11,11],
                [11,11,3,0,4,11,11,11,11,11],
                [11,11,11,4,0,5,11,11,11,11],
                [11,11,11,11,5,0,6,11,11,11],
                [11,11,11,11,11,6,0,7,11,11],
                [11,11,11,11,11,11,7,0,8,11],
                [11,11,11,11,11,11,11,8,0,9],
                [10,11,11,11,11,11,11,11,9,0]]

    tour5 = Tour(matrix5)
    tour10 = Tour(newDM(10))
    gw5 = GenAlg(5, 100, tour5)
    gw10 = GenAlg(50, 100, tour10)
    print("Algoritmo para matrix de 5x5, mejor camino de largo 15")
    for i in matrix5:
        print(i)
    gw5.run()
    print("")
    print("Algoritmo para matrix de 10x10, mejor camino de largo ")
    for i in matrix10:
        print(i)
    gw10.run()

if __name__ == '__main__':
    main()
