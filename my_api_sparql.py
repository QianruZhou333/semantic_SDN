################################################################################
# The TOUCAN Project 
# semantic SDN management                                                      #
# author: Qianru Zhou  (qz1@hw.ac.uk)                                          #
################################################################################

import urllib2
import rdflib
from rdflib import plugin
from rdflib import Namespace
from rdflib.namespace import RDF

####### for ontology v 1.0 #######
# switch and hosts must be passed as strings.
# this query get all the hosts connected to the given switches, except for the hosts given
# the return value is the name and macAddress of ports on the hosts 
def query_string_for_hosts(*switch, **host):
	qstring1 = ' select '
	qstring = ' where { '
	if switch:
		switch_count = 1
		for s in switch:
			qstring += '?p'+ str(switch_count*2-1) +' :isIn ' + ':' + str(s) + '. ?l'+ str(switch_count) +' :linkTo ?p' \
				+ str(switch_count*2-1) +'; :linkTo ?p'+ str(switch_count*2) +'. filter (?p'\
				+ str(switch_count*2-1) +' != ?p'+ str(switch_count*2) +'). ?p'+ str(switch_count*2) +' :isIn ?h' \
				+ str(switch_count) + '. ?h' + str(switch_count) + ' RDF:type :Host. ' + ' ?p'+str(switch_count*2) \
				+ ' :hasMAC ?macAddr' + str(switch_count) + '. bind(strafter(str(?p'+ str(switch_count*2-1) \
				+'), "http://home.eps.hw.ac.uk/~qz1/") as ?port'+ str(switch_count*2-1) +') ' \
				+ ' bind(strafter(str(?h'+ str(switch_count) + '), "http://home.eps.hw.ac.uk/~qz1/") as ?host' \
				+ str(switch_count) + ') '
			qstring1 += ' ?host'+ str(switch_count) + ' ?port' + str(switch_count*2-1) + ' ?macAddr' + str(switch_count)
			switch_count += 1
		switch_count -=1

	if host:
		for h in host:
			qstring += ' filter (?h' + str(switch_count) + ' != :' + str(host[h]) + '). '
			switch_count -= 1
	qstring += '}'
	qstring1 += qstring

	print qstring1
	return qstring1	


def run_query(qstring):
	# Code from Fetching Data and Parsing Data examples
	with open('../my_buff_switchStatus_mn.rdf', 'rb') as f: 
		response = str(f.read())

	graph = rdflib.Graph()
	graph.parse(data=response, format='turtle')

	netRes = Namespace("http://home.eps.hw.ac.uk/~qz1/")
	q = graph.query(qstring, initNs = {'':netRes, 'RDF':RDF})

	for item in q.bindings:
		print item

	return q

#query_string_for_hosts('s1')
#run_query(query_string_for_hosts('s1'))
