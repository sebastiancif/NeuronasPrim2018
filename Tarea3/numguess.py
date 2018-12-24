import optree

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
        self.maxgen = maxgen
        self.generator = optree.TreeGenerator(operations, terminals)
        self.maxdeep = maxdeep

    def initPopulation(self):
        for i in range(self.npop):
            self.pop
