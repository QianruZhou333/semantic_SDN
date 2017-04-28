from neo4j.v1 import GraphDatabase, basic_auth

class findPath(object):
    def __init__(self, **kwargs):
        self.driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("your neo4j username", "your password"))
        self.session = self.driver.session()
        self.path = []
        self.from_node = kwargs["start"]
        self.to_node = kwargs["end"]

    def __del__(self):
        self.session.close()

    def findShortestPath(self):
        queryStr = "MATCH (start:Node {name:'"+ self.from_node +"'}), (end:Node {name:'"+ self.to_node +"'}), p = shortestPath((start)-[:CONNECT*]-(end)) RETURN p"
        result = self.session.run(queryStr)
        for p in result:
            count = 0
            for i in p["p"]:
                start = self.findNodeById(i.start)
                end = self.findNodeById(i.end)
                if count == 0:
                    if start == self.from_node:
                        self.path.append(end)
                    else:
                        self.path.append(start)
                count += 1
        print self.path

    def findNodeById(self, node_id):
        n = self.session.run("MATCH (n:Node) WHERE id(n) = "+ str(node_id) +" RETURN n.name, n.isSwitch")
        for i in n:
            print i["n.name"], i["n.isSwitch"]
            name = i["n.name"]
        return name

    def dumpAllLink(self):
        result = self.session.run("MATCH (n)-[c]-() RETURN n.name AS name,ID(n) AS id, c, ID(c) AS c_id")
        for r in result:
            print r["name"], r["id"], r["c"], r["c_id"]

    def dumpAllNode(self):
        result = self.session.run("MATCH (n) RETURN n.name AS name, ID(n) AS id, n")
        for r in result:
            print r["name"], r["id"], r["n"]

#p1 = findPath(start ='h1', end ='h5')
#p1.findShortestPath()
