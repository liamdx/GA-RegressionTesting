import string
import random
from collections import Counter

crossoverRate = 0.75
mutationRate = 0.05
faults = 38


def convertTestToInt(test):
     c = list(test)
     c.pop(0)
     final = ''.join(c)
     final = int(final)
     return final

def convertFaultsToInt(faults = {}):
     for i in range(len(faults)):
         faults[i] = int(faults[i])
         
def parseFile(runningLength, raw_test_data):
    new = []
    for i in range(runningLength - 1):
        currentString = raw_test_data[i]
        s = currentString.split(',')
        key = s.pop(0)
        key = convertTestToInt(key)
        convertFaultsToInt(s)
        new.append((key,s)) 

    return new

def APFD(testSuite, testSuiteSize, numberOfFaults):
    # APFD Calculation = 1 - (TF1 + TF2.... / nm) + 1 / 2n
    # denominator
    denominator = testSuiteSize * numberOfFaults
    # 1 / 2n
    end = 1.0 / (2.0 * testSuiteSize)
    # array to store test indices of faults (TF1, TF2...)
    arr = [] 
    # for each test in test suite
    for i in range(testSuiteSize):
        #for each fault in test
        for j in range(numberOfFaults):
            # note which test error first occurs
            if(testSuite[i][1][j] == 1):
                arr.insert(j, i + 1)
            # if error does not occur, add total number of tests + 0.5
            # report explains maths behind this - x = n + 1/2
            elif(j == (numberOfFaults - 1) & testSuite[i][1][j] == 0):
                arr.insert(j, testSuiteSize + 0.5) 
    #sum all elements of holding array to get numerator
    numerator = sum(arr[0:numberOfFaults])
    #return APFD
    return 1.0 - numerator / denominator + end

def randomGenerate(testSuiteSize, populationSize, tests = {}):
    print("Generating Population")
    pop = []
    for i in range (populationSize):
        currentTestSuite = []
        # for each fault in test
        for j in range (testSuiteSize):
            x = random.choice(tests)
            currentTestSuite.append(x)

        pop.append(currentTestSuite)
    return pop

def fitness(testSuiteSize, numberOfFaults, populationSize, pop = []):
    print("Fitness Calculating")
    fitness = {}
    # For each member of the population
    for i in range(len(pop)):    
        currentAPFD = APFD(pop[i], testSuiteSize, numberOfFaults)
        fitness[i] = currentAPFD

    # sort the populationFitness to front load fittest
    s = [(k,fitness[k]) for k in sorted(fitness, key = fitness.get, reverse = True)]
    if(len(s) > populationSize): 
        print("Too many fitness values!")
    elif(len(s) < populationSize):
        print("Too few fitness values")

    return s

def sortPopulation(pop = [] , fitness = []):
    # sorts population by fitness, based on return of calcFitness
    print("Sorting Population")
    newPop = []
    i = 0
    maxValue = 0
    for key, val in fitness:
        if(val > maxValue):
            maxValue = val
        newPop.insert(i, pop[key])
  
        i += 1
    print("Max APFD this sort = %f" % maxValue)
    return newPop

def mutate(testSuiteSize, tests = {}, pop = []):
    for i in range(len(pop)):
        if(random.random() < mutationRate):
            # print("Mutating")
            slot = random.randrange(0, testSuiteSize)
            pop[i][slot] = (random.choice(tests))

def crossover(parent1, parent2, testData, testSuiteSize):
    slot = random.randrange(0, testSuiteSize)
    return1 = parent1[:slot] + parent2[slot:]
    slot = random.randrange(0, testSuiteSize)
    return2 = parent2[:slot] + parent1[slot:]
    return1 = checkForDuplicates(return1, testData, testSuiteSize)
    return2 = checkForDuplicates(return2, testData, testSuiteSize)
    return (return1, return2)

def checkForDuplicates(input, tests, testSuiteSize):
    checkDict = {}
    duplicatesIndex = []
    final = []
    i = 0

    if(len(input) < testSuiteSize):
       print("Input too short before dupe check! ")

    for key, value in input:
        if key not in (checkDict.keys()):
            checkDict[key] = value
            i += 1
        else:
            duplicatesIndex.append(i)
            i += 1
    
    for key, val in checkDict.items():
        final.append((key, val))

    if(len(final) < testSuiteSize):
        # print("length of suite too short!!!")
        for i in range(len(duplicatesIndex)): 

            newTest = random.choice(tests)
            while newTest[0] not in checkDict.keys():
                    newTest = random.choice(tests)
            final.insert(duplicatesIndex[i], newTest)

    if(len(input) < testSuiteSize):
       print("Input too short after dupe check!")

    if(len(final) < testSuiteSize):
       print("Final return too short after duplication check!")
    return final


def selection(testSuiteSize, numberOfFaults, populationSize, testData, pop = [], fitness = []):
    newPop = []
    selection = (int)(populationSize / 5)

    while(len(newPop) < populationSize):
        if(random.random() < 0.9):
            #Keep a not of the selection for APFD efficiency
            fitnessSelection1 = random.randrange(0, selection)
            fitnessSelection2 = random.randrange(0, selection)
            #index in population
            parent1index = fitness[fitnessSelection1][0]
            parent2index = fitness[fitnessSelection2][0]
            #reference to the test suite
            parent1 = pop[parent1index]
            parent2 = pop[parent2index]

            #if we should crossover
            if(random.random() < crossoverRate):
                #tournament selection
                child1, child2 = crossover(parent1, parent2, testData, testSuiteSize)

                apfd1 = APFD(child1, testSuiteSize, numberOfFaults)
                apfd2 = APFD(child2, testSuiteSize, numberOfFaults)

                #append whichever child has a higher APFD
                if(apfd1 > apfd2):
                    newPop.append(child1)
                else:
                    newPop.append(child2)
            #should not crossover
            else:
                #same thing but for original parents
                apfd1 = fitness[fitnessSelection1][1]
                apfd2 = fitness[fitnessSelection2][1]

                if(apfd1 > apfd2):
                    newPop.append(parent1)
                else:
                    newPop.append(parent2)
        #randomnly allow some of the greater population in 
        else:
            # Tournament selection
            fitnessSelection1 = random.randrange(0, populationSize)
            fitnessSelection2 = random.randrange(0, populationSize)

            parent1index = fitness[fitnessSelection1][0]
            parent2index = fitness[fitnessSelection2][0]
            parent1 = pop[parent1index]
            parent2 = pop[parent2index]

            #if we should crossover
            if(random.random() < crossoverRate):
                #tournament selection
                child1, child2 = crossover(parent1, parent2, testData, testSuiteSize)

                apfd1 = APFD(child1, testSuiteSize, numberOfFaults)
                apfd2 = APFD(child2, testSuiteSize, numberOfFaults)

                #append whichever child has a higher APFD
                if(apfd1 > apfd2):
                    newPop.append(child1)
                else:
                    newPop.append(child2)
            #should not crossover
            else:
                #same thing but for original parents
                apfd1 = fitness[fitnessSelection1][1]
                apfd2 = fitness[fitnessSelection2][1]

                if(apfd1 > apfd2):
                    newPop.append(parent1)
                else:
                    newPop.append(parent2)
    
    return newPop

def GAMainLoop(faults, numberOfTests, popSize, txtFile, generations):

    test_file = open(txtFile, "r")
    raw_test_data = test_file.read()
    raw_test_data = raw_test_data.split('\n')
    test_file.close()
    runningLength = len(raw_test_data)
    data = parseFile(runningLength, raw_test_data)
    numberOfFaults = faults
    testSuiteSize = numberOfTests
    populationSize = popSize
    population = randomGenerate(testSuiteSize , populationSize,  data)
    populationFitness = fitness(testSuiteSize, numberOfFaults, populationSize, population)
    population = sortPopulation(population, populationFitness)
    gen = 0

    print("Best APFD for Generation %d = " % gen)
    print(populationFitness[0][1])
    gen += 1
    bestAPFD = []

    while(gen < generations):
        print("GEN %d : Starting Selection" % gen)
        population = selection(testSuiteSize, numberOfFaults, populationSize, data, population, populationFitness)
        mutate(testSuiteSize, data, population)
        populationFitness = fitness(testSuiteSize, numberOfFaults, populationSize, population)
        population = sortPopulation(population, populationFitness)
        print("Fittests individual for Generation %d " % gen)
        print(populationFitness[0])
        print("Best APFD for Generation %d = Candidate %d" % (gen, populationFitness[0][0]))
        bestAPFD.append(populationFitness[0][1])
        print(populationFitness[0][1])

        gen += 1

    return bestAPFD

