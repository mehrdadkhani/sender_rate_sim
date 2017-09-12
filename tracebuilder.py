import numpy as np


PACKET_SIZE = 1504
time = 0
flag = False
fw = open('converted_trace','w')

with open('./Finland_Logs/bus.ljansbakken-oslo/report.2010-09-28_1407CEST.log') as file:
    for line in file:
      #  if flag == False:
       #     flag = True
        #    base_time = int(line.split(' ')[1])
        bytes_ = int(line.split(' ')[4])
        dt = int(line.split(' ')[5].rstrip('\n'))
        n_pkts = int(float(bytes_) / float(PACKET_SIZE))
        temp_time = time
        if n_pkts > 0:
            for stamp in xrange(0,n_pkts, 1):
                temp_time += int(dt/n_pkts)
                fw.write(str(temp_time)+'\n')

        time += dt

fw.close()
