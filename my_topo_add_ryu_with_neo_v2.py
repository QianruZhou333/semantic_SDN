################################
# @author: Qianru Zhou
# @email: chowqianru@gmail.com
# All rights reserved
#################################

# runs with ofctl_rest.py

from rdflib import Graph, plugin, Namespace, Literal
import json, rdflib_jsonld
from rdflib.plugin import register, Serializer
#from neo4j.v1 import GraphDatabase, basic_auth
from rdflib.namespace import RDF
import requests
import time

# rdf graph initiation
n = Namespace('http://home.eps.hw.ac.uk/~qz1/')
file_abs = '../my_buff_switchStatus.rdf'
g = Graph()
# neo4j graph initiation
#driver = GraphDatabase.driver("bolt://localhost")
#session = driver.session()

def getAllSwitches():
	allSwitches = requests.get('http://localhost:8080/v1.0/topology/switches').json()
	
	switchCount = 1 
	portCount = 1

	for item in allSwitches:
		s = 's' + str(item['dpid']).lstrip("0")
		g.add( (n[s], RDF.type, n['Switch']) )
		g.add( (n[s], n.hasName, Literal(s) ) )
		g.add( (n[s], n.hasID, Literal(str(item['dpid']).lstrip("0"))) )

#		session.run("CREATE (" + s + ":Node {name:" + s +", isSwitch:1})")
	
		for item_1 in item['ports']:
			for item_2 in item_1:
				p = s + '_port' + str(item_1['port_no']).lstrip("0")
				g.add( (n[s], n.hasPort, n[p]) ) 	
				g.add( (n[p], RDF.type, n['Port']) )
				g.add( (n[p], n.hasName, Literal(item_1['name'])) )
				g.add( (n[p], n.hasHWAddr, Literal(item_1['hw_addr'])) )
				g.add( (n[p], n.port_no, Literal(str(item_1['port_no']).lstrip("0"))) )
				g.add( (n[p], n.inSwitchID, Literal(str(item_1['dpid']).lstrip("0"))) )	
			portCount = portCount + 1
		switchCount = switchCount + 1
	
		getHosts(item['dpid'])
		getAllFlowStatus(item['dpid'])
	
	with open(file_abs, 'a') as f:
		f.write(g.serialize(format = 'turtle'))


def getAllFlowStatus(switchID):
	print str(switchID).lstrip('0')
	allFlows = requests.get('http://localhost:8080/stats/flow/' + str(switchID).lstrip('0') )
	if not allFlows: 
		print 'there is not any flows currently.'
	else:
		allFlows = allFlows.json()	
		flow_count = 0

		for flow in allFlows[str(switchID).lstrip('0')]:
			g.add( (n['s' + str(switchID).lstrip('0')], n.hasFlow, n['s'+ str(switchID).lstrip('0') +'_flow' + str(flow_count)]) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], RDF.type, n['Flow']) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.priority, Literal(flow['priority'])) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.hard_timeout, Literal(flow['hard_timeout'])) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.byte_count, Literal(flow['byte_count'])) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.duration_sec, Literal(flow['duration_sec'])) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.length, Literal(flow['length'])) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.flags, Literal(flow['flags'])) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.table_id, Literal(flow['table_id'])) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.cookie, Literal(flow['cookie'])) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.packet_count, Literal(flow['packet_count'])) )
			g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.idle_timeout, Literal(flow['idle_timeout'])) )
			
			if flow['match']:
				g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.hasInPort, Literal(flow['match']['in_port']) ) )
				g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.hasDstAddr, Literal( str(flow['match']['dl_dst'])) ) )

			if flow['actions']:
				action_count = 1
				for action in flow['actions']:
					g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count)], n.hasAction, n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count) + '_action' + str(action_count)]) )
					g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count) + '_action' + str(action_count)], RDF.type, n['Action']) )
					g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count) + '_action' + str(action_count)], n.hasType, Literal(action[0:6]) ) )
					g.add( (n['s' + str(switchID).lstrip('0') + '_flow' + str(flow_count) + '_action' + str(action_count)], n.toPort, Literal(action[7:])  ) )

					action_count += 1
										
			flow_count = flow_count + 1


def getHosts(switchID):
	hosts = requests.get('http://localhost:8080/v1.0/topology/hosts/' + str(switchID))
	if not hosts:
		print 'there is currently no hosts.'
	else:
		print 'there is at least one host'
		hosts = hosts.json()
		hostCount = 0

		for item in hosts:
			g.add( (n['s' + str(switchID).lstrip("0")], n.hasHost, n['s' + str(switchID).lstrip("0") + '_host' + str(hostCount)] ))
			g.add( (n['s' + str(switchID).lstrip("0") + '_host' + str(hostCount)], RDF.type, n['Host'] ) )
			g.add( (n['s' + str(switchID).lstrip("0") + '_host' + str(hostCount)], n.connectToPort, Literal(str(item['port']['port_no']).lstrip("0")) ) )
			g.add( (n['s' + str(switchID).lstrip("0") + '_host' + str(hostCount)], n.hasIPv4, Literal(item['ipv4'][0]) ) )
			g.add( (n['s' + str(switchID).lstrip("0") + '_host' + str(hostCount)], n.hasMAC, Literal(item['mac'])) )
			if item['ipv6']:
				g.add( (n['s' + str(switchID).lstrip("0") + '_host' + str(hostCount)], n.hasIPv6, Literal(item['ipv6'])) )

#			session.run(" CREATE (h" + str(hostCount) + ":Node {name:'h" + str(hostCount) + "', isSwitch:0})" )

			hostCount = hostCount + 1			

def clearFile(fname):
	with open(fname, 'w') as f:
		f.write('')

start = time.clock()
clearFile(file_abs)
getAllSwitches()
end = time.clock()
print end - start
