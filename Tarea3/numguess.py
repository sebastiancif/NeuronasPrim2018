import optree
import random
import math



class NumGuesser:
    #param operations: the set of operations valid for the trees
    #type operations: list<string>
    #param terminals: the set of terminals valid for the trees
    #type terminals: list<int|float>
    #param answer: the number that we are looking for
    #type answer: float
    #param lenpopulation: how many individuals are going to be used per generation
    #param lenpopulation: int
    #param maxgen: max number of generations that we will wait
    #type maxgen: int
    #param maxdeep: max deep of the trees
    #type maxdeep: int
    def __init__(self, operations, terminals, answer, lenpopulation, maxgen, maxdeep):
        self.key = answer
        self.pop = []
        self.npop = lenpopulation
        self.fitpop = []
        self.mating = []
        self.numparents = math.ceil((1+math.sqrt(1+8*self.npop))/2)
        self.maxgen = maxgen
        self.generator = optree.TreeGenerator(operations, terminals)
        self.maxdeep = maxdeep
        self.best = None
        self.bestind = -1

    def initPopulation(self):
        for i in range(self.npop):
            self.pop.append(self.generator.makeTree(self.maxdeep))

    def fitPopulation(self):
        fits = []
        for tree in self.pop:
            val = self.generator.evalTree(tree)
            #aqui se hace la evaluacion de fitness
            fits.append(abs(self.key - val))
        self.fitpop = fits

    def tournamentSelectionIndex(self):
        if not self.fitpop:
            print("No hay poblacion!")
            return
        else:
            indbest = -1
            for i in range(math.ceil(self.npop*3/4)):
                ind = random.randint(0,self.npop-1)
                while ind in self.mating:
                    ind = random.randint(0,self.npop-1)
                if indbest == -1 or self.fitpop[indbest] > self.fitpop[ind]:
                    indbest = ind
            return indbest

    def makeNewGen(self):
        if not self.pop:
            print("Error: no population!")
            return
        self.mating = []
        for j in range(self.numparents):
            self.mating.append(self.tournamentSelectionIndex())
        parents = [self.pop[k] for k in self.mating]
        newgen = []
        while(len(newgen) < self.npop):
            chance = random.random()
            if chance <= 0.9:
                #Crossover
                #Copia del primer arbol
                p1 = optree.copyTree(random.choice(parents))
                crossover = optree.randomNode(p1)
                p2 = random.choice(parents)
                #Copia de un subarbol del segundo padre
                subtree = optree.copyTree(optree.randomNode(p2))
                optree.moveNode(crossover, subtree)
                crossover = subtree = None
                newgen.append(p1)
            elif chance > 0.9 and chance <= 0.99:
                #Reproduction
                newgen.append(optree.copyTree(random.choice(parents)))
            else:
                #Mutation
                p = optree.copyTree(random.choice(parents))
                mutationpoint = optree.randomNode(p)
                newtree = self.generator.makeTree(self.maxdeep)
                optree.moveNode(mutationpoint, newtree)
                newgen.append(p)
        self.pop = newgen

    def run(self):
        self.pop = self.mating = self.fitpop = []
        self.best = None
        self.initPopulation()
        gen = 0
        while(gen < self.maxgen):
            self.fitPopulation()
            if 0 in self.fitpop:
                self.bestind = self.fitpop.index(0)
                self.best = self.pop[self.bestind]
                break
            self.makeNewGen()
            gen+=1
        if self.best is None:
            self.fitPopulation()
            minima = min(self.fitpop)
            self.bestind = self.fitpop.index(minima)
            self.best = self.pop[self.bestind]
        print(f"Pasaron {gen} generaciones para buscar el numero {self.key}, mejor valor:")
        print(f"Fitness: {self.fitpop[self.bestind]}")
        print(f"Valor: {self.generator.evalTree(self.best)}")
        print("------------------------")
        optree.print2D(self.best)

def main():
    ops = ['*','+','-']
    terms = [19,7,40,3]
    #ops, terms, answer, npop, ngen, maxdeep
    ng = NumGuesser(ops, terms, 147, 500, 50,3)
    print(f"Terminales: {terms}")
    print(f"Operaciones: {ops}")
    ng.run()
    ops2 = ['*','+']
    terms2 = [10,1,25,9,3,6]
    ng2 = NumGuesser(ops2,terms2,595,500,50,3)
    print(f"Terminales: {terms2}")
    print(f"Operaciones: {ops2}")
    ng2.run()
    ops3 = ['*','+','-','/']
    terms3 = [25,7,8,100,4,2]
    ng3 = NumGuesser(ops3,terms3,459,500,50,3)
    print(f"Terminales: {terms3}")
    print(f"Operaciones: {ops3}")
    ng3.run()

if __name__ == '__main__':
    main()
