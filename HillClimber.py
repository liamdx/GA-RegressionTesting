import string
import random
from collections import Counter

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

def fitness(testSuite, testSuiteSize, numberOfFaults):
    nm = testSuiteSize * numberOfFaults
    # 1 / 2n
    end = 1.0 / (2.0 * testSuiteSize)
    arr = [] 
    for i in range(testSuiteSize):
        for j in range(numberOfFaults):
            if(testSuite[i][1][j] == 1):
                arr.insert(j, i + 1)
            elif(j == (numberOfFaults - 1) & testSuite[i][1][j] == 0):
                arr.insert(j, testSuiteSize + 0.5)

    numerator = sum(arr[0:numberOfFaults])
    return 1.0 - (numerator / nm) + end

def getRandomSolution(tests, testSuiteSize):
    new = []

    for i in range(testSuiteSize):
        new.append(random.choice(tests))

    return new

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

def getNewSolution(testSuite, tests, testSuiteSize):    
    new = testSuite
    #  1 change every new solution, keep changes to initial solution incremental
    numberOfChanges = 1
    for i in range(numberOfChanges):
        slot = random.randrange(0,  testSuiteSize)
        new[slot] = random.choice(tests)
    
    new = checkForDuplicates(new, tests, testSuiteSize)
    return new


def HCMainLoop(faults, numberOfTests, popSize, txtFile, generations):
    print("Hillclimber")
    testSuiteSize = numberOfTests
    numberOfFaults = faults
    maxNumberNeighbours = popSize
    maxStoredValues = int(generations / 2)

    test_file  = open(txtFile, "r")
    raw_test_data = test_file.read()
    raw_test_data = raw_test_data.split('\n')
    test_file.close()
    runningLength = len(raw_test_data)

    tests = parseFile(runningLength, raw_test_data)
    newStates = []
    newFitness = []
    currentState = getRandomSolution(tests, testSuiteSize)
    currentFitness = fitness(currentState, testSuiteSize, numberOfFaults)
    previousFitnessValues = [maxStoredValues]
    bestAPFD = []
    print("fitness for initial state = %f" % currentFitness)
    gen = 0

    while(gen < generations):
        newFitness.clear()
        newStates.clear()
        lastFitness = currentFitness

        for i in range(maxNumberNeighbours):
            newStates.append(getNewSolution(currentState, tests, testSuiteSize))
            newFitness.append(fitness(newStates[i], testSuiteSize, numberOfFaults))

        for j in range(maxNumberNeighbours):
            if(newFitness[i] > currentFitness):
                currentState = newStates[i]
                currentFitness = newFitness[i]

        previousFitnessValues.append(currentFitness)

        if(len(previousFitnessValues) > maxStoredValues):
            previousFitnessValues.pop(0)
        
        if(len(previousFitnessValues) == maxStoredValues):
            if(previousFitnessValues[maxStoredValues - 1] == previousFitnessValues[0]):
                print("getting random solution")
                currentState = getRandomSolution(tests, testSuiteSize)
                currentFitness = fitness(currentState, testSuiteSize, numberOfFaults)
                
        print("Iteration %d best fitness = %f" % (gen, currentFitness))
        bestAPFD.append(currentFitness)
        gen += 1 

    return bestAPFD