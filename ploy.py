import numpy as np
import matplotlib.pyplot as plt

x = []
y = []
with open('report.txt') as file:
    for line in file:
        y.append( float(line.split(', ')[2]) / float(line.split(', ')[3]))
        #y.append( float(line.split(', ')[1]))
        x.append( float(line.split(', ')[0]))

plt.plot(x,y,'ro')
plt.xlabel('decision interval(ms)')
#plt.ylabel('95th percentile queueu delay')
plt.ylabel('utilization')
plt.show()
