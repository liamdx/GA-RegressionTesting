from GA import GAMainLoop
from HillClimber import HCMainLoop
from RandomGenerate import RandomMainLoop
import matplotlib.pyplot as plt
import statistics
import numpy as np


def GetResults():
    generations = 100
    aggregateCount = 10

    numberOfTests = 5
    numberOfFaults = 9
    populationSize = 100
    fileToRead = "smallfaultmatrix.txt"

    GA_RESULTS = GAMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations)
    HC_RESULTS = HCMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations)
    RANDOM_RESULTS = RandomMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations)

    # small data set individual figure
    fig = plt.figure()
    plt.plot(GA_RESULTS, label='GA')
    plt.plot(HC_RESULTS, label='Hill-Climber')
    plt.plot(RANDOM_RESULTS, label='Random')
    plt.xlabel('Generations')
    plt.ylim(0.2, 0.8)
    plt.xlim(0, generations)
    plt.ylabel('Fitness Score (APFD)')
    plt.suptitle("Small Data Set Individual Run Results")
    plt.title("Population Size %d , Test Suite Size %d, Number of Faults to detect = %d" % (
    populationSize, numberOfTests, numberOfFaults))
    plt.legend()
    plt.grid()

    # Aggregates
    GA_AGG_RESULTS = []
    HC_AGG_RESULTS = []
    RA_AGG_RESULTS = []

    for i in range(aggregateCount):
        GA_AGG_RESULTS.append(GAMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations))
        HC_AGG_RESULTS.append(HCMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations))
        RA_AGG_RESULTS.append(RandomMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations))

    GA_MEAN_RESULTS = []
    HC_MEAN_RESULTS = []
    RA_MEAN_RESULTS = []
    GA_SPREAD_RESULTS = []
    HC_SPREAD_RESULTS = []
    RA_SPREAD_RESULTS = []

    for i in range(aggregateCount):
        GA_MEAN, HC_MEAN, RA_MEAN = 0, 0, 0

        for j in range(generations - 1):
            GA_MEAN += GA_AGG_RESULTS[i][j]
            HC_MEAN += HC_AGG_RESULTS[i][j]
            RA_MEAN += RA_AGG_RESULTS[i][j]

        GA_MEAN = GA_MEAN / generations
        HC_MEAN = HC_MEAN / generations
        RA_MEAN = RA_MEAN / generations

        GA_SPREAD = (max(GA_AGG_RESULTS[i]) - min(GA_AGG_RESULTS[i]))
        HC_SPREAD = (max(HC_AGG_RESULTS[i]) - min(HC_AGG_RESULTS[i]))
        RA_SPREAD = (max(RA_AGG_RESULTS[i]) - min(RA_AGG_RESULTS[i]))

        GA_MEAN_RESULTS.append(GA_MEAN)
        HC_MEAN_RESULTS.append(HC_MEAN)
        RA_MEAN_RESULTS.append(RA_MEAN)
        GA_SPREAD_RESULTS.append(GA_SPREAD)
        HC_SPREAD_RESULTS.append(HC_SPREAD)
        RA_SPREAD_RESULTS.append(RA_SPREAD)

    # SMALL DATA SET AGGREGATE RESULTS
    fig = plt.figure()
    plt.plot(GA_MEAN_RESULTS, label='GA MEAN')
    plt.plot(HC_MEAN_RESULTS, label='Hillclimbing MEAN')
    plt.plot(RA_MEAN_RESULTS, label='Random MEAN')
    plt.xlabel('Iterations')
    plt.ylim(0.2, 0.8)
    plt.xlim(0, aggregateCount)
    plt.ylabel('Fitness Score (APFD)')
    plt.suptitle("Small Data Set Aggregate Results")
    plt.title("Population Size %d , Test Suite Size %d, Number of Faults to detect = %d" % (
        populationSize, numberOfTests, numberOfFaults))
    plt.legend()
    plt.grid()

    # small data set aggregate results
    fig = plt.figure()
    limit = []
    limit.extend(range(1,11))
    GA_X = np.array(GA_MEAN_RESULTS)
    GA_E = np.array(GA_SPREAD_RESULTS)
    plt.errorbar(limit, GA_X, GA_E, linestyle='-', marker='^', label='GA Spread')
    plt.xlabel('Iterations')
    plt.ylim(0.2, 0.8)
    plt.xlim(0, aggregateCount)
    plt.ylabel('Fitness Score (APFD)')
    plt.suptitle("GA Spread Results - Small Data Set")
    plt.title("Population Size %d , Test Suite Size %d, Number of Faults to detect = %d" % (
        populationSize, numberOfTests, numberOfFaults))
    plt.legend()
    plt.grid()

    fig = plt.figure()
    HC_X = np.array(HC_MEAN_RESULTS)
    HC_E = np.array(HC_SPREAD_RESULTS)
    plt.errorbar(limit, HC_X, HC_E, linestyle='-', marker='*', label='Hillclimber Spread')
    plt.xlabel('Iterations')
    plt.ylim(0.2, 0.8)
    plt.xlim(0, aggregateCount)
    plt.ylabel('Fitness Score (APFD)')
    plt.suptitle("Hill Climber Spread Results - Small Data Set")
    plt.title("Population Size %d , Test Suite Size %d, Number of Faults to detect = %d" % (
        populationSize, numberOfTests, numberOfFaults))
    plt.legend()
    plt.grid()

    # large data set individual results
    numberOfTests = 8
    numberOfFaults = 38
    fileToRead = "bigfaultmatrix.txt"

    GA_RESULTS = GAMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations)
    HC_RESULTS = HCMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations)
    RANDOM_RESULTS = RandomMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations)

    fig = plt.figure()
    plt.plot(GA_RESULTS, label='GA')
    plt.plot(HC_RESULTS, label='Hill-Climber')
    plt.plot(RANDOM_RESULTS, label='Random')
    plt.xlabel('Generations')
    plt.ylim(0.2, 0.8)
    plt.xlim(0, generations)
    plt.ylabel('Fitness Score (APFD)')
    plt.suptitle("Large Data Set Individual Run Results")
    plt.title("Population Size %d , Test Suite Size %d, Number of Faults to detect = %d" % (
    populationSize, numberOfTests, numberOfFaults))
    plt.legend()
    plt.grid()

    # Aggregates
    GA_AGG_RESULTS.clear()
    HC_AGG_RESULTS.clear()
    RA_AGG_RESULTS.clear()

    for i in range(aggregateCount):
        GA_AGG_RESULTS.append(GAMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations))
        HC_AGG_RESULTS.append(HCMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations))
        RA_AGG_RESULTS.append(RandomMainLoop(numberOfFaults, numberOfTests, populationSize, fileToRead, generations))

    GA_MEAN_RESULTS.clear()
    HC_MEAN_RESULTS.clear()
    RA_MEAN_RESULTS.clear()
    GA_SPREAD_RESULTS.clear()
    HC_SPREAD_RESULTS.clear()
    RA_SPREAD_RESULTS.clear()

    for i in range(aggregateCount):
        GA_MEAN, HC_MEAN, RA_MEAN = 0, 0, 0

        for j in range(generations - 1):
            GA_MEAN += GA_AGG_RESULTS[i][j]
            HC_MEAN += HC_AGG_RESULTS[i][j]
            RA_MEAN += RA_AGG_RESULTS[i][j]

        GA_MEAN = GA_MEAN / generations
        HC_MEAN = HC_MEAN / generations
        RA_MEAN = RA_MEAN / generations

        GA_SPREAD = (max(GA_AGG_RESULTS[i]) - min(GA_AGG_RESULTS[i]))
        HC_SPREAD = (max(HC_AGG_RESULTS[i]) - min(HC_AGG_RESULTS[i]))
        RA_SPREAD = (max(RA_AGG_RESULTS[i]) - min(RA_AGG_RESULTS[i]))

        GA_MEAN_RESULTS.append(GA_MEAN)
        HC_MEAN_RESULTS.append(HC_MEAN)
        RA_MEAN_RESULTS.append(RA_MEAN)
        GA_SPREAD_RESULTS.append(GA_SPREAD)
        HC_SPREAD_RESULTS.append(HC_SPREAD)
        RA_SPREAD_RESULTS.append(RA_SPREAD)


    # LARGE DATA SET AGGREGATE RESULTS
    fig = plt.figure()
    plt.plot(GA_MEAN_RESULTS, label='GA MEAN')
    plt.plot(HC_MEAN_RESULTS, label='Hillclimbing MEAN')
    plt.plot(RA_MEAN_RESULTS, label='Random MEAN')
    plt.xlabel('Iterations')
    plt.ylim(0.2, 0.8)
    plt.xlim(0, aggregateCount)
    plt.ylabel('Fitness Score (APFD)')
    plt.suptitle("Large Data Set Aggregate Results")
    plt.title("Population Size %d , Test Suite Size %d, Number of Faults to detect = %d" % (
    populationSize, numberOfTests, numberOfFaults))
    plt.legend()
    plt.grid()
    plt.show()


GetResults()
