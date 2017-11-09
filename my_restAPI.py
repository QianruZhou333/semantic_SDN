from mininet.net import Mininet
from mininet.topo import LinearTopo
from mininet.util import dumpNodeConnections
from bottle import get, route, run, template

net = Mininet( topo=LinearTopo( k = 2 ) )

@get('/nodes')
def dump( ):
	nodes = str(net.hosts + net.switches + net.controllers)
	return nodes

@get('/links')
def links():
	links = str(net.links)
	return links

@route('/stop')
def stop():
    net.stop()

net.start()
run(host='localhost', port=8080 )
