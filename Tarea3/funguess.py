import funtree
import random
import math

def floatrange(init, stop, step):
    inter = []
    c = init
    while c <= stop:
        inter.append(c)
        c+=step
    return inter
class FunGuesser:
    #param operations: the set of operations valid for the trees
    #type operations: list<string>
    #param terminals: the set of terminals valid for the trees
    #type terminals: list<int|float|string>
    #param function: the function that we are approximating
    #type function: function
    #param interval: the interval in which the function will be evaluated
    #type interval: list<int|float>
    #param lenpopulation: how many individuals are going to be used per generation
    #param lenpopulation: int
    #param maxgen: max number of generations that we will wait
    #type maxgen: int
    #param maxdeep: max deep of the trees
    #type maxdeep: int
    def __init__(self, operations, terminals, function, interval, lenpopulation, maxgen, maxdeep):
        self.fun = function
        self.interval = interval
        self.pop = []
        self.npop = lenpopulation
        self.fitpop = []
        self.mating = []
        self.numparents = math.ceil((1+math.sqrt(1+8*self.npop))/2)
        self.maxgen = maxgen
        self.generator = funtree.FunTreeGenerator(operations, terminals)
        self.maxdeep = maxdeep
        self.best = None
        self.bestind = -1

    def initPopulation(self):
        for i in range(self.npop):
            self.pop.append(self.generator.makeTree(self.maxdeep))

    def fitPopulation(self):
        fits = []
        for tree in self.pop:
            #Calculamos el error del arbol con la funcion
            error = 0
            for num in self.interval:
                error+= abs(self.fun(num)-self.generator.evalTree(tree,num))
            fits.append(error)
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
                p1 = funtree.copyTree(random.choice(parents))
                crossover = funtree.randomNode(p1)
                p2 = random.choice(parents)
                #Copia de un subarbol del segundo padre
                subtree = funtree.copyTree(funtree.randomNode(p2))
                funtree.moveNode(crossover, subtree)
                crossover = subtree = None
                newgen.append(p1)
            elif chance > 0.9 and chance <= 0.99:
                #Reproduction
                newgen.append(funtree.copyTree(random.choice(parents)))
            else:
                #Mutation
                p = funtree.copyTree(random.choice(parents))
                mutationpoint = funtree.randomNode(p)
                newtree = self.generator.makeTree(self.maxdeep)
                funtree.moveNode(mutationpoint, newtree)
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
        print(f"Pasaron {gen} generaciones para buscar la funcion, mejor valor:")
        print(f"Fitness: {self.fitpop[self.bestind]}")
        print("------------------------")
        funtree.print2D(self.best)


def main():
    ops = ['*','+','-']
    terms = random.sample(range(101), 10)
    for i in range(10):
        terms.append('x')
    fun = lambda x: x**3+2*x+10
    interval = floatrange(-10,10,0.1)
    #operations, terminals, function, interval, lenpopulation, maxgen, maxdeep
    fg = FunGuesser(ops, terms, fun, interval, 500, 50, 4)
    print("Probando para f(x) = x³+2x+10")
    print(f"Intervalo: [{interval[0]}, {interval[-1]}]")
    print(f"Operaciones: {ops}")
    print(f"Terminales: {terms}")
    fg.run()
    ops2 = ['*','+','-','%']
    terms2 = random.sample(range(-5,5), 10)
    for i in range(10):
        terms2.append('x')
    fun2 = lambda x: x**2+x+1
    interval2 = floatrange(-1,1,0.1)
    fg2 = FunGuesser(ops2, terms2, fun2, interval2, 500, 50, 4)
    print("Probando para f(x) = x²+x+1")
    print(f"Intervalo: [{interval2[0]}, {interval2[-1]}]")
    print(f"Operaciones: {ops2}")
    print(f"Terminales: {terms2}")
    fg2.run()
    ops3 = ['*','+','-']
    terms3 = random.sample(range(-5,5), 10)
    for i in range(10):
        terms3.append('x')
    fun3 = lambda x: 3*x+7
    interval3 = floatrange(-1,1,0.1)
    fg3 = FunGuesser(ops3, terms3, fun3, interval3, 500, 50, 4)
    print("Probando para f(x) = 3x+7")
    print(f"Intervalo: [{interval3[0]}, {interval3[-1]}]")
    print(f"Operaciones: {ops3}")
    print(f"Terminales: {terms3}")
    fg3.run()


if __name__ == '__main__':
    main()
