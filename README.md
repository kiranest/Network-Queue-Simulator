# M/M/1 Queue Simulation

The arrival, departure, and observer events were generated before the simulation. These events were put into a priority queue because the events would be sorted upon an O(log n) insertion.

The arrival and departure events were generated in the same function: first an arrival event was generated, then the departure event was generated using the time of the packet arrival, service time, and previous departure time. Observer events were generated in its own function since its rate needed to be at least five times that of the arrival packet rate.

In the simulation function, the priority queue is continuously popped until the queue is empty. For each event, the corresponding event counter is incremented. But for the observer event, the number of packets in the buffer is observed and added to the running total. This running total is divided by the number of observer events to get the average number of packets in the buffer, which is returned by the function. An observer event also increases the total amount of empty buffer events observed, which is again divided by the number of observer events to get the proportion of time that the buffer is empty.

# M/M/1/K Queue Simulation

The arrival and observer events were generated before the simulation. The observer event generation uses the same function as the infinite buffer design.

The arrival events were generated in a similar way to the observer event generation, but with the packet arrival rate replaced with the observer rate. The departure events were not generated before the simulation since it needs to be generated during the finite buffer simulation.

In the simulation function, the priority queue is continuously popped until the queue is empty. Counters for the number of generated packets and the number of packets dropped is defined. For the arrival event, a check is made to see whether the buffer is full or not. If it’s full, the running packet loss counter is incremented. If it’s not full, the packet arrival counter is incremented. Then the service and departure time of the arrived packet is determined. This departure event is added back into the event queue. If the event popped is a departure event, its counter is simply incremented. But for the observer event, besides incrementing the observed counter, the number of packets in the buffer is observed and added to the running total. This running total is divided by the number of observer events to get the average number of packets in the buffer, which is returned by the function. An observer event also increases the total amount of empty buffer events observed, which is again divided by the number of observer events to get the proportion of time that the buffer is empty. Lastly, the ratio of the total number of packets lost to the total number of packets generated is returned.