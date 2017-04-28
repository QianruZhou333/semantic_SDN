################################
# @author: Qianru Zhou
# @email: chowqianru@gmail.com
# All rights reserved
#################################

from my_api_sparql import query_string_for_hosts, run_query
from my_api_switch_ovs import SwitchAPI as API
import eventlet

def connect_all(*switches):
	length = len(switches)
	print 'length ' + str(length)
	pool = eventlet.GreenPool()
	for s in switches:
		api = API(s)
		queryStr = query_string_for_hosts(s)
		q = run_query(queryStr)

		q1 = q
		#print q.bindings
		action_type = 'output'
		for count in range(length):
			port = 'port' + str(count+1)
			mac = 'macAddr' + str(count+1)

			for row in q.bindings:
				# e.g., from query result 's1-eth3' get '3'
				inPort = str(row[str(port)])
				inPort = inPort[inPort.index('eth')+3:len(inPort)]
				print 'inPort ' + inPort
				for row1 in q1.bindings:
					if row[port] != row1[port]:

						outPort = str(row1[port])
						outPort = outPort[outPort.index('eth')+3:len(outPort)]
						print 'outPort ' + outPort
						print 'mac '+ mac
						macAddr = str(row1[mac])
						#api.add_flow(in_port=inPort, actions=('output:'+outPort))
						pool.spawn(api.add_flow, in_port=inPort, dl_dst=macAddr, actions=('output:'+outPort))
					pool.waitall()
