import numpy as np

def sender_rate(time):
    info = information_update()
    return 1    


def information_update(time):
    ptr = 0
    while sender.arr[ptr] <= time:
        ptr += 1
    
    info = np.concatenate([sender_dep[0:ptr], q_arr[0:ptr], q_dep[0:ptr], sender_arr[0:ptr]], axis = 1)
    print info
    return info
        
      
def bw_builder(trace):
    # we are assuming uplink has unlimited capacity 
    bottle_link = np.loadtxt(trace,dtype=int)
    bw_bottle = np.histogram(bottle_link,bins = range(0,bottle_link[-1],dt))[0] / dt
    return bottle_link, bw_bottle

