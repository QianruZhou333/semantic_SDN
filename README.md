# semantic_SDN
## Description
An light-weight, plug-and-go programe to enable semantic-intelligent autonomic network management system for software-defined network. 
Semantic SDN consists of three main components:
1. A knowledge base generator
2. A technology-independent API for network management tasks, e.g., learning switch, build firewall.
3. A SPARQL Engine.

# Document
## my_api_*.py 
methods provided in the open API
## my_app_*.py
demonstration of the applications developed based on the API provided. 
## my_topo_add_*_with_neo.py
the knowledge base generator 
* = mn: adopts the Mininet API to extract the information.
* = ryu: adopts the Ryu API to extract the information.
