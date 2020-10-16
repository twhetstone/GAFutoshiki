# Tyler Whetstone, Riley Holzmeyer, Logan Brown
# Genetic Algorithm for solving Futoshiki Puzzle
# EGR 425

import random

class Futoshiki():
    found = False
    dimension = 0 # size of the puzzle, is changed according to length of puzzle input
    popSize = 300 # number of members in each generation
    mutationRate = .02
    crossover = .5
    
    population = []
    fitness = []
    setValues, logic = [], []
    solution = []
        
    def initializePop(self): # randomly generates the first generation and checks fitness
        gen = []
        for i in range(self.popSize):
            individual = []
            for j in range(self.dimension**2): # fill in puzzle with random values
                individual.append(random.randint(1, self.dimension))
            for j in range(len(self.setValues)): # keeps the set values equal to input
                if self.setValues[j]:
                    individual[j] = self.setValues[j]
            gen.append(individual)
        self.population = gen
        self.fitnessEval()

    def reproduction(self): # take parents from last population to generate a new one
        gen = []
        for i in range(self.popSize):
            parent1 = self.rouletteSelect()
            parent2 = self.rouletteSelect()
            child = []
            for j in range(self.dimension**2):
                if random.random() < self.crossover: # 50% chance to take square from either parent
                    child.append(parent1[j])
                else:
                    child.append(parent2[j])
            for j in range(self.dimension**2): # runs thru child w/ chance to mutate each square
                if random.random() < self.mutationRate:
                    child[j] = random.randint(1,self.dimension)
            for j in range(len(self.setValues)): # keeps the set values equal to input
                if self.setValues[j]:
                    child[j] = self.setValues[j]
            gen.append(child)
        self.population = gen
        self.fitnessEval()

    def fitnessEval(self):
        self.fitness = []
        for member in self.population: # run thru every puzzle in the population
            fit = 0
            
            # calc logic
            for i in range(0, len(self.logic)-1, 2): 
                if not member[self.logic[i]] < member[self.logic[i+1]]: # penalize for logic errors
                    fit += 7

            # calc repeating numbers in row/columns
            repetitions = [] # this keeps track of number of repetitions
            
            # check for repeats in rows
            for i in range(self.dimension):
                rowRepeats = [0]*self.dimension
                for j in range(self.dimension):
                    rowRepeats[member[i*self.dimension + j]-1] += 1
                for element in rowRepeats:
                    repetitions.append(element)

            # check for repeats in columns
            for i in range(self.dimension):
                colRepeats = [0]*self.dimension
                for j in range(self.dimension):
                    colRepeats[member[i + j*self.dimension]-1] += 1
                for element in colRepeats:
                    repetitions.append(element)

##            print(repetitions)
            for i in repetitions: # penalize for repeats in rows/columns, will penalize if > 1
                if i > 1: # if repetition, repetitions*penalty
                    fit += i*5

            if not fit: # no penalty assigned
                fit = 1
                self.checkSolution(member) # save puzzle as solution
            self.fitness.append(1/fit)

    def checkSolution(self, soln):
        self.found = True
        self.solution = soln

    def rouletteSelect(self): # roulette wheel selection
        total = sum(self.fitness)
        choice = random.uniform(0,total)
        current = 0
        j = 0
        for i in self.fitness: # run thru each fitness
            current += i
            if current > choice: # if fitness crosses threshold, choose that member of population
                return self.population[j]
            else:
                j +=1
            
##    def display(self): # displays every member, currently unused
##        for i in range(self.popSize):
##            self.printMatrix(self.population[i])
##            print()

    def displayFit(self): # displays only most fit of generation
        self.printMatrix(self.population[self.fitness.index(max(self.fitness))])
        print()

    def printMatrix(self, this): # displays the puzzle in neat matrix format
        array = [[this[j*self.dimension + i] for i in range(self.dimension)] for j in range(self.dimension)]
        print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in array]))

def puzzle(): # reads puzzle from txt, puts into appropriate format, and sends to class Futoshiki
    f = Futoshiki()
    
    # input file name, must have correct format to work
    fileName = str(input('Enter file name: '))
    nfileName = fileName + 'n.txt'
    lfileName = fileName + 'l.txt'
    
    # getting set numbers
    nums = open(nfileName, "r")
    nums = nums.read().replace(" ", "")
    nums = nums.replace("\n", "")
    nums = list(map(int, nums))
    f.dimension = int(len(nums)**(1/2)) # sets dimension of puzzle
    f.setValues = nums
    
    # getting logic
    logic = open(lfileName, "r")
    logic = logic.read().replace(" ", "")
    logic = logic.replace("\n", "")
    logic = list(map(int, logic))
    newL = []
    for i in range(0, len(logic)-1, 2): # changes coordinate-type values to index values
        newL.append(logic[i]*f.dimension + logic[i+1])
    f.logic = newL
    
    return f

def main():
    f = puzzle() # gets puzzle
    numGens = 0
    reset = int(input('Enter max number of generations: ')) # number of gens before killing pop and starting from scratch, helps if stuck in "local min"
    restart = False                                         # in general, 50 for 3x3, 300 for 4x4, 400-500 for 5x5, ??? for 6x6
    numRestarts = 0
    while not f.found:
        if not numGens:
            f.initializePop() # initialize the population
##            print('Most fit of generation', numGens)
##            f.displayFit()
            numGens += 1
        else:
            numGens += 1
            f.reproduction()
##            if numGens % 10 == 0:
##                print('Most fit of generation', numGens)
##                f.displayFit()
        if f.found: # if solution found, print and exit program
            print('The solution to the puzzle is: ')
            f.printMatrix(f.solution)
            print('Solution found in', numGens+1, 'generations after', numRestarts, 'restarts.')
        elif numGens > reset: # if max number of gens reached, start over
            print('----- RESTART -----')
            restart = False
            numGens = 0
            numRestarts += 1
            
main()
