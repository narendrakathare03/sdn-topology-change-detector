# SDN Mininet Project — Topology Change Detector

## Problem Statement
Detect changes in network topology dynamically
using Mininet and POX controller by monitoring
switch/link events, updating topology map,
displaying changes and logging updates.

## Topology
- 3 Switches (s1, s2, s3) in linear topology
- 3 Hosts (h1, h2, h3)
- Remote POX Controller on port 6633

## Setup & Execution

### Terminal 1 — Start POX controller
cd ~/pox
python3 pox.py forwarding.topo_change

### Terminal 2 — Start Mininet
sudo mn --topo linear,3 \
--controller remote,ip=127.0.0.1,port=6633

## Test Scenarios

### Scenario 1 — Normal forwarding
mininet> pingall

### Scenario 2 — Link failure
mininet> link s1 s2 down
mininet> pingall

### Scenario 3 — Link restored
mininet> link s1 s2 up
mininet> pingall

## Expected Output
- Scenario 1: 0% packet loss
- Scenario 2: packets dropped, topology change logged
- Scenario 3: 0% packet loss restored

## Results
- Latency: ~0.1ms
- Throughput: 27.3 Gbits/sec
- Topology changes detected and logged in real time

## References
1. https://mininet.org/overview/
2. https://noxrepo.github.io/pox-doc/html/
3. https://github.com/noxrepo/pox
