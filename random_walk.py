from matplotlib import pyplot
from random import randrange
from random import random

# random
series = [randrange(10) for i in range(1000)]
pyplot.plot(series)
pyplot.show()

# random walk
random_walk = []
random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
	movement = -1 if random() < 0.5 else 1
	value = random_walk[i-1] + movement
	random_walk.append(value)
pyplot.plot(random_walk)
pyplot.show()
