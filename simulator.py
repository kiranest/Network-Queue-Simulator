import random
import math
import statistics
import heapq
from enum import Enum
import matplotlib.pyplot as plt

# Enum class for Events
class Event(Enum):
    ARRIVAL = 0
    DEPARTURE = 1
    OBSERVER = 2

# Exponential random variable with rate parameter input
    # Input:
        # rate  :   parameter of distribution
    # Output:
        # random number within distribution
def time_interval(rate):
    return -math.log(1- random.random())/rate

# Generation of arrival and departure events for the simulation of an infinite buffer
    # Input:
        # time          :   Total simulation time
        # packet_rate   :   Packet arrival rate
        # length        :   Size of a packet in bits
        # transmission  :   Transmission rate of output link in bits per second
        # queue         :   Event queue
def generate_arrivals_departures(time, packet_rate, length, transmission, queue):
    total_time = time_interval(packet_rate)
    prev_dep_time = -1
    while total_time < time:
        service_time = time_interval(transmission/length)
        dep_time = service_time
        if total_time > prev_dep_time:
            dep_time += total_time
        else:
            dep_time += prev_dep_time
        heapq.heappush(queue, (total_time, Event.ARRIVAL))
        heapq.heappush(queue, (dep_time, Event.DEPARTURE))
        prev_dep_time = dep_time
        total_time += time_interval(packet_rate)

# Generation of arrival events for simulation of finite buffer
    # Input:
        # time          :   Total simulation time
        # packet_rate   :   Average packet arrival rate
        # queue         :   Event queue
def generate_arrivals(time, packet_rate, queue):
    total_time = time_interval(packet_rate)
    while total_time < time:
        heapq.heappush(queue, (total_time, Event.ARRIVAL))
        total_time += time_interval(packet_rate)

# Generation of observer events for both infinite and finite buffer simulations
    # Input:
        # time          :   Total simulation time
        # observer_rate :   Average observer event rate
        # queue         :   Event queue
def generate_observers(time, observer_rate, queue):
    total_time = time_interval(observer_rate)
    while total_time < time:
        heapq.heappush(queue, (total_time, Event.OBSERVER))
        total_time += time_interval(observer_rate)

# Simulation of infinite buffer system
    # Input:
        # queue     :   list of arrival, departure, and observer events
    # Output:
        # E_N       :   average number of packets in the buffer
        # P_IDLE    :   proportion of time system is idle
def simulate_infinite(queue):
    N_a = 0                     # number of packet arrivals
    N_d = 0                     # number of packet departures
    N_o = 0                     # number of observations
    queue_packets = 0           # running total of packets observed in buffer
    idle_counter = 0            # running total of instances where buffer is observed to be empty

    while queue:
        item = heapq.heappop(queue)
        event = item[1]
        if event == Event.ARRIVAL:
            N_a += 1
        elif event == Event.DEPARTURE:
            N_d += 1
        else:
            N_o += 1
            queue_packets += N_a - N_d
            if N_a - N_d == 0:
                idle_counter += 1
    E_N = queue_packets/N_o
    P_IDLE = idle_counter/N_o

    return (E_N, P_IDLE)

# Simulation of a finite buffer system
    # Input:
        # queue         :   list of arrival and observer events
        # buffer_size   :   number of packets allowed in buffer
        # length        :   length of a packet in bits
        # transmission  :   transmission rate of output link in bits per second
    # Output:
        # E_N           :   average number of packets in the buffer
        # P_IDLE        :   proportion of time system is idle
        # P_LOSS        :   packet loss probability
def simulate_finite(queue, buffer_size, length, transmission):
    N_a = 0                     # number of packet arrivals
    N_d = 0                     # number of packet departures
    N_o = 0                     # number of observations
    queue_packets = 0           # running total of packets observed in buffer
    idle_counter = 0            # running total of instances where buffer is observed to be empty
    packets_generated = 0       # running total of packets generated
    packets_lost = 0            # running total of packets dropped
    prev_dep_time = 0           # variable to keep track of latest departure time
    while queue:
        time, event = heapq.heappop(queue)
        if event == Event.ARRIVAL:
            packets_generated += 1
            if N_a - N_d >= buffer_size:
                packets_lost += 1
            else:
                N_a += 1
                service_time = time_interval(transmission/length)
                dep_time = service_time
                if time > prev_dep_time:
                    dep_time += time
                else:
                    dep_time += prev_dep_time
                heapq.heappush(queue, (dep_time, Event.DEPARTURE))
                prev_dep_time = dep_time
        elif event == Event.DEPARTURE:
            N_d += 1
        else:
            N_o += 1
            queue_packets += N_a - N_d
            if N_a - N_d == 0:
                idle_counter += 1
    
    E_N = queue_packets / N_o
    P_IDLE = idle_counter / N_o
    P_LOSS = packets_lost / packets_generated

    return (E_N, P_IDLE, P_LOSS)

# Q1
"""
packet_rate = 75

def generate_numbers(iterations):
    nums = []
    for _ in range(iterations):
        nums.append(time_interval(packet_rate))
    return nums

num_set = generate_numbers(1000)
print("Expected mean: ", 1/packet_rate)
print("Actual mean: ", statistics.mean(num_set))
print("Expected variance: ", 1/math.pow(packet_rate, 2))
print("Actual variance: ", statistics.variance(num_set))
"""

# Q3
"""
packet_len = 2000
transmission_rate = 1000000

avg_packets_list = []
idle_prop_time = []
utilization_list = []
for packet_rate in range(125,500,50):
    event_queue = []
    observer_rate = packet_rate * 5

    generate_arrivals_departures(1000, packet_rate, packet_len, transmission_rate, event_queue)
    generate_observers(1000, observer_rate, event_queue)
    E_N, P_IDLE = simulate_infinite(event_queue)
    
    utilization_list.append(packet_len*packet_rate/transmission_rate)
    avg_packets_list.append(E_N)
    idle_prop_time.append(P_IDLE)

plt.plot(utilization_list, avg_packets_list)
plt.xlabel('Utilization of the queue, ⍴')
plt.ylabel('Average number of packets in the buffer, E[n]')
plt.suptitle('The average number of packets in the queue as a function of queue utilization')
plt.savefig('inf_avg_packets.png', bbox_inches='tight')

plt.clf()
plt.cla()

plt.plot(utilization_list, idle_prop_time)
plt.xlabel('Utilization of the queue, ⍴')
plt.ylabel('Proportion of time the system is idle, P_IDLE')
plt.suptitle('The proportion of time the system is idle as a function of queue utilization')
plt.savefig('inf_idle_system.png', bbox_inches='tight')
"""

# Q4
"""
packet_len = 2000
transmission_rate = 1000000
event_queue = []
packet_rate = 600
observer_rate = packet_rate * 5

generate_arrivals_departures(1000, packet_rate, packet_len, transmission_rate, event_queue)
generate_observers(1000, observer_rate, event_queue)
E_N, P_IDLE = simulate_infinite(event_queue)

print("Utilization of queue: ", packet_len*packet_rate/transmission_rate)
print("Average number of packets in buffer: ", E_N)
print("Proportion of time server is idle: ", P_IDLE)
"""

# Q6
"""
packet_len = 2000
transmission_rate = 1000000

avg_packets_list = []
packet_loss_list = []
for K in [10,25,50]:
    avg_packets_list_K = []
    packet_loss_list_K = []
    for packet_rate in range(250,800,50):
        event_queue = []
        observer_rate = packet_rate * 5

        generate_arrivals(1000, packet_rate, event_queue)
        generate_observers(1000, observer_rate, event_queue)
        E_N, P_IDLE, P_LOSS = simulate_finite(event_queue, K, packet_len, transmission_rate)
        
        avg_packets_list_K.append(E_N)
        packet_loss_list_K.append(P_LOSS)
    
    avg_packets_list.append(avg_packets_list_K)
    packet_loss_list.append(packet_loss_list_K)

utilization_list = []
for packet_rate in range(250,800,50):
    utilization_list.append(packet_len*packet_rate/transmission_rate)

plt.plot(utilization_list, avg_packets_list[0])
plt.plot(utilization_list, avg_packets_list[1])
plt.plot(utilization_list, avg_packets_list[2])
plt.legend(['K = 10', 'K = 25', 'K = 50'], loc='upper left')

plt.xlabel('Utilization of the queue, ⍴')
plt.ylabel('Average number of packets in the buffer, E[n]')
plt.suptitle('Average number of packets in the buffer as a function of queue utilization for K size buffer')
plt.savefig('fin_avg_packets.png', bbox_inches='tight')

plt.clf()
plt.cla()

plt.plot(utilization_list, packet_loss_list[0])
plt.plot(utilization_list, packet_loss_list[1])
plt.plot(utilization_list, packet_loss_list[2])
plt.legend(['K = 10', 'K = 25', 'K = 50'], loc='lower right')

plt.xlabel('Utilization of the queue, ⍴')
plt.ylabel('Packet loss probability, P_LOSS')
plt.suptitle('Packet loss probability as a function of queue utilization for K size buffer')
plt.savefig('fin_packet_loss.png', bbox_inches='tight')
"""