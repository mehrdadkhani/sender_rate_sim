import numpy as np
import random

f = open('report1.txt', 'w')
TRACE = './traces/Verizon-LTE-short.up'

RLAGENT_UPDATE_INTERVAL = 10

time = 0
dt = 1 # simluation time step is set to 1ms
PACKET_SIZE = 1504
HALF_WAY_DELAY_TO_BTS = 10
BACKBONE_RESPONSE_TIME = 20
trace_ptr = 0
next_analyse_idx = 0
SIZE = 1000000
q_arr = np.zeros(SIZE)
q_dep = np.zeros(SIZE)
sender_dep = np.zeros(SIZE)
sender_arr = np.zeros(SIZE)
q_arr_ptr = 0
q_dep_ptr = 0
sender_dep_ptr = 0
sender_arr_ptr = 0

end_flag = False


class InformationState:
    def __init__(self):
        self.info_update_ptr = 0
        self.avg_qdelays = 0.0
        self.rate = 0
    def information_update(self, time):
        qdelays = np.array(q_dep[0:q_dep_ptr]) - np.array(q_arr[0:q_dep_ptr])
        while sender_arr[self.info_update_ptr] <= time and len(qdelays) > 0 and self.info_update_ptr < len(qdelays) :
            self.avg_qdelays = 0.5 * self.avg_qdelays + 0.5 * qdelays[self.info_update_ptr]
            self.info_update_ptr += 1

        return self.avg_qdelays


    def sender_rate(self, time):
        avg_qdelay = self.information_update(time)
        target = time + HALF_WAY_DELAY_TO_BTS + BACKBONE_RESPONSE_TIME
        # if target < len(bw_bottle) :
        #     return 0.9 * np.mean(bw_bottle[target:target + RLAGENT_UPDATE_INTERVAL])
        # else:
        #     return 0
        print avg_qdelay
        if avg_qdelay < 100.0:
            self.rate += 1
            print self.rate
            return self.rate
        else:
            self.rate -= 1
            if self.rate < 0:
                self.rate = 0
            if self.rate == 0:
                print "zero"
                if random.random() < 0.01:
                    return 0.1
                else:
                    return 0
            print self.rate
            return self.rate






def bw_builder(trace):
    # we are assuming uplink has unlimited capacity
    bottle_link = np.loadtxt(trace,dtype=int)
    #bottle_link -= bottle_link[0]
    bw_bottle = np.histogram(bottle_link,bins = range(0,bottle_link[-1],dt))[0] / dt
    return bottle_link, bw_bottle

bottle_link, bw_bottle = bw_builder(TRACE)
IS = InformationState()


while time < bottle_link[-1]:
    # updating the sending rate for the whole interval
    if time % RLAGENT_UPDATE_INTERVAL == 0 :
        PKTS = int(IS.sender_rate(time) * RLAGENT_UPDATE_INTERVAL)
        N_PKTS = np.zeros(RLAGENT_UPDATE_INTERVAL,dtype=int)
        for i in xrange(0, PKTS, dt):
            N_PKTS[i % RLAGENT_UPDATE_INTERVAL ] += 1

    n_pkts = N_PKTS[time % RLAGENT_UPDATE_INTERVAL]
    if n_pkts >= 1:
        for i in xrange(0, n_pkts):
            sender_dep[sender_dep_ptr] = time
            sender_dep_ptr += 1
            q_arr[q_arr_ptr] = (time + HALF_WAY_DELAY_TO_BTS + BACKBONE_RESPONSE_TIME)
            q_arr_ptr += 1

        for i in xrange(next_analyse_idx,q_arr_ptr):
            # sometimes queue has been empty
            while trace_ptr < len(bottle_link) and bottle_link[trace_ptr] < time + HALF_WAY_DELAY_TO_BTS + BACKBONE_RESPONSE_TIME:
                trace_ptr += 1

            if trace_ptr == len(bottle_link):
                end_flag = True
                break
            q_dep[q_dep_ptr] = ( bottle_link[trace_ptr] )
            q_dep_ptr += 1
            sender_arr[sender_arr_ptr] = ( bottle_link[trace_ptr] + HALF_WAY_DELAY_TO_BTS )
            sender_arr_ptr += 1
            trace_ptr += 1
            if trace_ptr == len(bottle_link):
                end_flag = True
                break
        next_analyse_idx = q_arr_ptr

    if end_flag == True:
        break
    time += dt

qdelays = (np.array(q_dep[0:q_dep_ptr]) - np.array(q_arr[0:q_dep_ptr]))
avg_qdelays = np.average( qdelays )
qpctile = np.sort(qdelays)[int(0.95 * len(qdelays))]
print "95th percentile qdelay: ", qpctile ,"#pkts delivered: ",sender_arr_ptr ,"#total chances: ", np.sum(bw_bottle)
f.write(str(qpctile)+", " +str(sender_arr_ptr) +", "+ str(np.sum(bw_bottle)) + "\n")

f.close()
