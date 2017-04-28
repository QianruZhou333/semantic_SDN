from my_api_sparql import run_query
import time

run = True
all_is_well = True
q_str = '''select ?link ?status ?port1 ?port2
	where {
		?l RDF:type :Link;
		   :hasStatus ?status;
		   :linkTo ?p1;
		   :linkTo ?p2.
		filter (?p1 != ?p2)
		bind(strafter(str(?l), "http://home.eps.hw.ac.uk/~qz1/") as ?link)
		bind(strafter(str(?p1), "http://home.eps.hw.ac.uk/~qz1/") as ?port1)
		bind(strafter(str(?p2), "http://home.eps.hw.ac.uk/~qz1/") as ?port2)

	}	
'''
f = open('../output_query.txt', 'a')

def detectLinks():
	while run:
		all_is_well = True
		q = run_query(q_str)
	
		for row in q.bindings:
			if row['status'].find('MISSING') > 0:
				all_is_well = False
				print >> f, 'link: ' + row['link'] + ' between ' + row['port1'] +' and '+ row['port2'] +' is missing at: ' + str(time.time())
		print >> f, '\n'
		time.sleep(0.5)
	
detectLinks() 