import random
import re
from copy import deepcopy
#-----------------------------
# Referencias usadas:
# https://github.com/joowani/binarytree/
# https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
#-----------------------------

# Node -> None
# Prints a tree
def printTree(root):
    actuals = [root]
    fullprints = []
    while actuals:
        next = []
        prints = []
        for node in actuals:
            if node is None:
                prints.append("_")
                continue
            else:
                prints.append(str(node.value))
            next.append(node.left)
            next.append(node.right)
        print(' '.join(prints))
        actuals = next

# Node, int .> None
# Aux function used in print2D
# Source: https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
def print2Daux(root, space):
    count = 10
    if root is None:
        return
    space += count
    print2Daux(root.right, space)
    print("\n", end = '', flush = True)
    print(" "*(space-count), end = '', flush = True)
    print(f"{str(root.value)}\n", end = '', flush = True)
    print2Daux(root.left, space)

# Node -> None
# Prints a 2D tree.
# Source: https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
def print2D(root):
    print2Daux(root,0)

# Node -> Node
# Gives a copy of a tree
def copyTree(root):
    t = deepcopy(root)
    return t

class Node:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.parent = None
        self.value = val
    #Para setear y obtener los valores de un nodo podemos usar
    #getattr(obj,atr) y setattr(obj,atr,newatr)

class TreeGenerator:
    # param ops: Set of operations for the expression tree
    # type ops : list<string>
    # param terms: Set of terminals for the expression tree
    # type terms: list<int|float|string>
    def __init__(self, ops, terms):
        self.myops = ops
        self.myterms = terms
        self.opsdict = {
                    '+' : lambda a,b: a+b,
                    '-' : lambda a,b: a-b,
                    '*' : lambda a,b: a*b,
                    '/' : lambda a,b: a/b,
        }

    # int -> list<int|float|string>
    # Generates a list in breadth first order representing a perfect expression tree
    def makePerfectTreeList(self, height):
        maxnodes = 2**(height+1)-1
        maxleaves = 2**height
        treelist = []
        for i in range(0,maxnodes-maxleaves):
            treelist.append(random.choice(self.myops))
        for i in range(maxleaves,maxnodes+1):
            treelist.append(random.choice(self.myterms))
        return treelist


    # int -> list<int|float|string>
    # Generates a list in breadth first order representing a expression tree
    def makeTreeList(self, height):
        #Numero de nodos de un arbol perfecto
        maxnodes = 2**(height+1)-1
        #Numero de hojas de un arbol perfecto
        maxleaves = 2**height
        #Iniciamos el arbol con una operacion
        treelist = [random.choice(self.myops)]
        #Rellenamos aleatoriamente el arbol
        while(len(treelist) < maxnodes):
            treelist.append(random.choice(self.myops+self.myterms))
        #Como la lista se hizo aleatoriamente, validamos el arbol
        #Usamos la condicion de que el nodo en la posición i tiene
        #por hijos a los nodos en posicion 2i+1 y 2i+2 (izq y der)
        #Primero revisamos que los últimos nodos sean terminales, de no serlo
        #los cambiamos
        anti = -1
        while(anti >= -maxleaves):
            if treelist[anti] in self.myterms:
                anti -= 1
                continue
            else:
                treelist[anti] = random.choice(self.myterms)
                anti-=1
                continue
        #Ahora verificamos la correctitud del arbol y corregimos errores
        for i in range(maxnodes):
            if treelist[i] in self.myops:
                continue
            elif treelist[i] is None:
                izq = 2*i+1
                der = 2*i+2
                if izq < maxnodes and der < maxnodes:
                    treelist[izq] = treelist[der] = None
                    continue
                else: #Alguno de los indices se sale del rango
                    break
            elif treelist[i] in self.myterms:
                izq = 2*i+1
                der = 2*i+2
                if izq < maxnodes and der < maxnodes:
                    treelist[izq] = treelist[der] = None
                    continue
                else: #Alguno de los indices se sale del rango
                    break
        return treelist
    # int -> Node
    # param height: max height of the tree
    # Generates a random expression tree with a maximum deep
    def makeTree(self, height):
        treelist = self.makeTreeList(height)
        nodes = [None if v is None else Node(v) for v in treelist]
        for i in range(1, len(nodes)):
            node = nodes[i]
            if node is not None:
                parent = nodes[(i-1)//2]
                if parent is None:
                    print("Error: nodo vacío como padre")
                    return
                setattr(parent, 'left' if i % 2 else 'right', node)
        return nodes[0]

    # Node -> int
    # Evaluates a given expression tree
    def evalTree(self, root):
        if root.right == root.left == None:
            return root.value
        else:
            return self.opsdict[root.value](self.evalTree(root.left),self.evalTree(root.right))



def main():
    ops = ['*','+','-']
    terms = [19,7,40,3]
    tg = TreeGenerator(ops, terms)
    t1 = tg.makeTree(3)
    t2 = tg.makeTree(3)
    t3 = tg.makeTree(3)
    print2D(t1)
    print("------------------------------")
    print(tg.evalTree(t1))
    print2D(t2)
    print("------------------------------")
    print(tg.evalTree(t2))
    print2D(t3)
    print("------------------------------")
    print(tg.evalTree(t3))

def gimmeTree():
    ops = ['*','+','-']
    terms = [19,7,40,3]
    tg = TreeGenerator(ops, terms)
    t1 = tg.makeTree(3)
    return t1

if __name__ == '__main__':
    main()
