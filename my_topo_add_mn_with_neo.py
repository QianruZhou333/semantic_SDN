#!/usr/bin/python
from functools import partial
from subprocess import check_output
from mininet.net import Mininet
from mininet.topo import LinearTopo
from mininet.node import OVSSwitch
from neo4j.v1 import GraphDatabase, basic_auth
#from grapheekdb.backends.data.localmem import LocalMemoryGraph
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF
#from api.my_switch_API import switchAPI
import time

class AddTopology():
	def __init__(self):
		# rdf initiation
		self.n = Namespace('http://home.eps.hw.ac.uk/~qz1/')
		self.g = Graph()
		self.file_abs = '../my_buff_switchStatus_mn.rdf'
		# graph database initiation
		self.driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "Sylvia2561435"))
		self.session = self.driver.session()
		# grapheekdb initiation
		# self.g2 = LocalMemoryGraph()

		self.clearFile()
		self.clearGraphDatabase()
		self.net = self.creatNetwork()
		self.getAllControllers()
		self.getAllSwitches()
		self.getAllHosts()
		self.getAllLinks()
		#self.r2 = self.session.run("MATCH (n)-[c]-() RETURN n,c")
		#for i in self.r2:
		#	print i

	def __del__(self):
		self.writeRdfToFile()	
		self.net.stop()
		self.session.close()

	def creatNetwork(self):
		switch = partial( OVSSwitch, protocols='OpenFlow13' )
		net = Mininet( topo=LinearTopo( k=5 ), switch=switch )
		net.start()
		return net

	def getAllControllers(self):
		
		for controller in self.net.controllers:
			self.g.add( ( self.n[str(controller.name)], RDF.type, self.n['Controller'] ) )

	def getAllSwitches(self):
		sCount = 0
		for switch in self.net.switches:
			self.g.add( ( self.n[str(switch.name)], RDF.type, self.n['Switch'] ) )
			for port in switch.intfList():
				self.g.add(( self.n[str(switch.name)], self.n.hasPort, self.n[str(port.name)] ))
				self.g.add(( self.n[str(port.name)], self.n.isIn, self.n[str(switch.name)] ))
				self.g.add(( self.n[str(port.name)], RDF.type, self.n['Port'] ))
				self.g.add(( self.n[str(port.name)], self.n.hasIP, Literal(str(port.ip)) ))
				self.g.add(( self.n[str(port.name)], self.n.hasMAC, Literal(str(port.mac)) ))

			self.session.run("CREATE ("+ str(switch.name) +":Node {name:'"+ str(switch.name) +"', isSwitch:1 })")

			#g2.add_node( kind = 'switch', self.n.me = str(switch.name) )

	def getAllHosts(self):
		
		for host in self.net.hosts:
			self.g.add( ( self.n[str(host.name)], RDF.type, self.n['Host'] ) )
			for intf in host.intfList():
				self.g.add( ( self.n[str(intf.name)], RDF.type, self.n['Port'] ) )
				self.g.add( ( self.n[str(host.name)], self.n.hasPort, self.n[str(intf.name)] ) )
				self.g.add( ( self.n[str(intf.name)], self.n.isIn, self.n[str(host.name)] ) )
				self.g.add( ( self.n[str(intf)], self.n.hasIP, Literal(str(intf.ip)) ) )
				self.g.add( ( self.n[str(intf)], self.n.hasMAC, Literal(str(intf.mac)) ) )
			self.session.run("CREATE ("+ str(host.name) +":Node {name:'"+ str(host.name) +"', isSwitch:0 })")
			#self.g2.add_node( kind='host', self.n.me = str(host.name) )

	def getAllLinks(self):
		link_count = 0
		for link in self.net.links:
			linkString = str(link)
			node1 = str(linkString[0:linkString.index('-')])
			node2 = str(linkString[(linkString.index('>')+1):linkString.rindex('-')])
			self.g.add( ( self.n['Link'+str(link_count)], RDF.type, self.n['Link'] ) )
			self.g.add( ( self.n['Link'+str(link_count)], self.n.linkTo, self.n[str(linkString[0:linkString.index('<')])] ) )
			self.g.add( ( self.n['Link'+str(link_count)], self.n.linkTo, self.n[str(linkString[linkString.index('>')+1:len(linkString)])] ) )
			self.g.add( ( self.n['Link'+str(link_count)], self.n.hasStatus, Literal(str(link.status())) ) )
			self.g.add( ( self.n[node1], self.n.isConnectedTo, self.n[node2] ) )
			self.g.add( ( self.n[node2], self.n.isConnectedTo, self.n[node1] ) )

			link_count += 1

			self.session.run(" MATCH (n1:Node {name:'"+ str(node1) +"'}), (n2:Node {name:'"+ str(node2) +"'}) CREATE (n1)-[:CONNECT]->(n2)" )

	def findShortestPath(self, node1, node2):
		path = self.session.run("MATCH (start:Node {name:'"+ node1 +"'}), (end:Node {name:'"+ node2 +"'}), p = shortestPath((start)-[:CONNECT*]-(end)) RETURN p")
		for p in path:
			print p["p"]

	def clearFile(self):
		with open(self.file_abs, 'w') as f:
			f.write('')

	def clearGraphDatabase(self):
		self.session.run("MATCH (n) DETACH DELETE n")

	def writeRdfToFile(self):
		with open(self.file_abs, 'a') as f:
			f.write(self.g.serialize(format = 'turtle'))



startTime = time.clock()
a1 = AddTopology()
endTime = time.clock()
print endTime - startTime
del a1 
