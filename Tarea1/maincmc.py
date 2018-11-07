from network import *
from time import sleep
def main():

    nw1 = Network(4,9,[9,18,18,3])
    nw1.dataClasification("cmc.csv",30, learningrate = 0.5, randshuffle = True)
    nw2 = Network(4,9,[9,18,18,3])
    nw2.dataClasification("cmc.csv",30, learningrate = 0.5, randshuffle = False)


if __name__ == '__main__':
    main()
