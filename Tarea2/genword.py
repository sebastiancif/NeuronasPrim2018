import string
import random
from time import sleep
from sys import maxsize
from math import ceil, sqrt
from itertools import permutations

# int -> (None -> list<string>)
# Returns a function that produces a list of length len cotaining random lowercase characters
def genRanWord(len):
    def funRanWord():
        return random.choices(string.ascii_lowercase, k = len)
    return funRanWord

# string -> (List<string> -> int)
# Returns a function that calculate the similarity between thegoal and theword
def fitnessGoal(goal):
    def fitnessWord(theword):
        thegoal = list(goal)
        count = len(thegoal)
        if(len(theword)!=len(thegoal)):
            return count
        else:
            for i in range(len(theword)):
                if(theword[i]==thegoal[i]):
                    count-=1
            return count
    return fitnessWord

# int -> int
# Calculates the mininum number of parents to make a population of children
def numParents(children):
    return ceil((1+sqrt(1+8*children))/2)

# list<string>, list<string> -> list<string>
# Makes a newborn from parent1 and parent2 considering crossover and mutation
def makeChild(parent1, parent2, mutationRate = 0.1):
    mixingpt = random.randrange(len(parent1)+1)
    child = parent1[0:mixingpt]+parent2[mixingpt:]
    for i in range(len(child)):
        chance = random.random()
        if chance <= mutationRate:
            child[i] = random.choice(string.ascii_lowercase)
    return child

class GeneticAlgorithm:

    def __init__(self, npop, genfunc, fitfunc):
        self.pop = [] #Poblacion
        self.npop = npop #Cantidad de poblacion
        self.nparents = numParents(npop) #Cantidad de padres necesarios para generar npop
        self.ktour = int(3*npop/4) #Cantidad de competidores en un tournament
        self.fitpop = [] #Indice de fitness de cada miembro de la poblacion
        self.matingpool = [] #Arreglo para padres de siguientes generaciones
        self.genfun = genfunc #Funcion generadora de elementos
        self.fitfun = fitfunc #Funcion de fitness
        self.minima = maxsize

    def setKTour(self, k):
        self.ktour = k

    def initPop(self):
        self.pop = []
        for i in range(self.npop):
            self.pop.append(self.genfun())

    def fitPopulation(self):
        if(len(self.pop) != self.npop):
            print("Error in population!")
            return
        self.fitpop = []
        for ind in self.pop:
            self.fitpop.append(self.fitfun(ind))
        self.minima = min(self.fitpop)

    def kTournament(self, k):
        best = None
        for i in range(k):
            parent = random.randint(0,self.npop-1)
            while(parent in self.matingpool):
                parent = random.randint(0,self.npop-1)
            if(best == None or self.fitpop[parent]<self.fitpop[best]):
                best = parent
        return best


    def makeNewGen(self):
        if not self.pop:
            print("Error: No population!")
            return
        self.matingpool = []
        while(len(self.matingpool)<self.nparents):
            self.matingpool.append(self.kTournament(self.ktour))
        perms = list(permutations(self.matingpool, 2))
        newgen = []
        while(len(newgen)<self.npop):
            p1, p2 = perms.pop(random.randrange(len(perms)))
            newborn = makeChild(self.pop[p1],self.pop[p2])
            newgen.append(newborn)
        self.pop = newgen

    # None -> boolean, int
    # Checks if the algorithm has finished the task
    def goalReached(self):
        ind = self.fitpop.index(self.minima)
        if self.minima == 0:
            return True, ind
        else:
            return False, ind

    def run(self):
        print("Iniciando algoritmo!")
        print(f"Poblacion de {self.npop} individuos")
        self.pop = self.fitpop = self.matinpool = []
        self.initPop()
        generation = 0
        while(generation < 2000):
            self.fitPopulation()
            print(self.pop)
            b, index = self.goalReached()
            if b:
                print(f"Terminado en generacion {generation}, elemento")
                print(''.join(self.pop[index]))
                return
            self.makeNewGen()
            generation+=1
        print(f"Pasaron {generation} generaciones, mejor valor")
        print(self.pop[index])

def main():

    ga = GeneticAlgorithm(100, genRanWord(22), fitnessGoal("sandritatieneojoscafes"))
    ga.run()

if __name__ == '__main__':
    main()
