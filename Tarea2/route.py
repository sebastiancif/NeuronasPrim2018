import random
#--------------------

# int -> list<list<int>>
# Generate a random distance matrix using ncities cities connected
def newDM(ncities):
    distmatrix = []
    for i in range(ncities):
        citierow = []
        for j in range(ncities):
            if(i == j):
                citierow.append(0)
            elif(i>j):
                citierow.append(distmatrix[j][i])
            else:
                citierow.append(random.randint(10,100))
        distmatrix.append(citierow)
    return distmatrix

# float, int -> list<list<int>>
# Generates a random matrix of distances using a choosen seed
def detDM(seed, ncities):
    random.seed(seed)
    return newDM(ncities)

#Class that stores a distance matrix for a group of cities
class Tour:
    # list<list<float>>, int -> Tour
    # Makes a new tour, considering by default the 0 index as the initial city
    def __init__(self, matrix, initialcity = 0):
        self.distmatrix = matrix
        self.ncities = len(matrix)
        self.initialcity = initialcity

    def pathDistance(self, path):
        dist = self.distmatrix[self.initialcity][path[0]] + self.distmatrix[path[-1]][self.initialcity] #Salida y llegada
        prev = -1
        for city in path:
            if prev == -1:
                prev = city
                continue
            else:
                dist+= self.distmatrix[prev][city]
                prev = city
        return dist

    # None -> Route
    # Make a random route crossing all cities in the Tour
    def makeRoute(self):
        path = list(range(self.ncities))
        path.remove(self.initialcity)
        random.shuffle(path) #Se reordena el arreglo aleatoriamente
        dist = self.pathDistance(path)
        return Route(path,dist)

    # Route, Route -> Route
    # Generates a new individual using two individuals for mating
    def newIndividual(self, parent1, parent2, mutationrate = 0.1):
        #Primero hacemos crossover
        p1 = parent1.getPath()
        p2 = parent2.getPath()
        mixingpt = random.randint(0,len(p1))
        newpath = p1[0:mixingpt]
        for city in p2:
            if city in newpath:
                continue
            else:
                newpath.append(city)
        #Luego mutamos al individuo con swap
        for i in range(len(newpath)):
            if (random.random()<=mutationrate):
                j = random.randint(0,len(newpath)-1)
                while(j==i):
                    j = random.randint(0,len(newpath)-1)
                newpath[i] , newpath[j] = newpath[j] , newpath[i]
        distance = self.pathDistance(newpath)
        return Route(newpath, distance)



class Route(Tour):
    def __init__(self, path, distance):
        self.path = path
        self.distance = distance

    def getDistance(self):
        return self.distance

    def getPath(self):
        return self.path
