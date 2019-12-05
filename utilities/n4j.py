from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, NodeMatch, RelationshipMatcher
from mysql import connector
from neo4j import GraphDatabase




class FindExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def apply_filter(self, message):
        message  = self.parse_filter(message)
        with self._driver.session() as session:
            filter_result = session.write_transaction(self._filter_result, message)
            for room in filter_result:
                print(room)
    def parse_filter(self, message):
        if not message:
            return ["(r:Room)"]
        output = []
        example = "(f2:Feature12)<-[f10:f]-(r:Room)"
        for index, condition in enumerate(message):
            c = "(feature" + str(index) + ":Feature" + str(condition) + ")<-[f" + str(index) + ":f]-(r:Room)"
            output.append(c)
        return output

    def apply_recon(self, message):
        with self._driver.session() as session:
            recon = session.write_transaction(self._recon_result, str(message))
            for g in recon:
                print(g[0], g[1])
    @staticmethod
    def _filter_result(tx, message):

        condition = ""
        for i in range(len(message) - 1):
            condition += message[i] + ","
        condition += message[len(message) - 1]
        # print(condition)
        command = "MATCH " + condition + " \nRETURN DISTINCT r.apart_key, r.type"
        result = tx.run(command)
        return result

    @staticmethod
    def _recon_result(tx, message):
        command = "MATCH (n:Room)-[f]->()-[r]->(n2:Room)\n WHERE n.room_key = " + message + " AND n2.room_key <> " + message  + " \nRETURN n2.room_key, count(n2.room_key) as Freq\n ORDER BY Freq DESC\n LIMIT 6"
        result = tx.run(command)
        return result

class NeoConnection(object):


    def __init__(self, uri, user, password):
        self.graph = Graph(uri, username=username, password=password)
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self.dictionary = {}
        match = NodeMatch(self.graph)
        for item in match:
            if item['type'] == 'room':
                self.dictionary[item['label']] = item
            else:
                self.dictionary[item['label']] = item


    def close(self):
        self._driver.close()


    def create_room_key_node(self, room_key, size, apart_key):
        """
        Create a new node in neo4j database
        @param room_key - a room_key of the room, int. eg: 123456
        @param type: Type the type of the room, string.  eg: "4b4b"
        """
        if room_key in self.dictionary:
            return self.dictionary[room_key]
        temp_node = Node("Room", room_key=room_key, type='room', size=size, apart_key=apart_key)
        self.graph.create(temp_node)
        self.dictionary[room_key] = temp_node
        return temp_node


    def create_feature_node(self, feature):
        """
        Create a new node in neo4j database
        @param room_key - a room_key of the room, int. eg: 123456
        @param type: Type the type of the room, string.  eg: "4b4b"
        """
        if feature in self.dictionary:
            return self.dictionary[feature]
        temp_node = Node(feature, label=feature, type='feature')
        self.graph.create(temp_node)
        self.dictionary[feature] = temp_node
        return temp_node

    def connect_room_and_feature(self, room, features):
        """
        Connect room and features together.
        @param room - room node, node object.
        @param features - a list of feature, list of strings.
        """
        for f in features:
            f_node = self.create_feature_node(f)
            room_feature_to = Relationship(room,'f',f_node)
            room_feature_ba = Relationship(f_node,'r',room)
            self.graph.create(room_feature_to)
            self.graph.create(room_feature_ba)
    def Transform(self):
        sql_connector = connector.connect(host='18.217.253.58',database='demo',user='admin',password='matcha')
        cursor = sql_connector.cursor()
        cursor.execute("SELECT * FROM demosite_keytable AS k JOIN demosite_apartmentfeature AS a ON k.apart_key_id = a.apart_key JOIN demosite_roomfeature AS r ON r.room_key_id = k.room_key")
        entry = cursor.fetchall()
        for e in entry:
            node = self.create_room_key_node(e[1], e[-2], e[3])
            self.connect_room_and_feature(node, ["Feature" + str(e[13]*10)+"bed"])
            self.connect_room_and_feature(node, ["Feature" + str(e[14]*10)+"bath"])
            index = 1
            for i in range(4, len(e)):
                if i == 9:
                    continue
                if e[i] == 1 or e[i] == 0:
                    if e[i] == 1:
                        self.connect_room_and_feature(node, ["Feature" + str(index)])
                    index += 1
            print(e[-2])
    def Delete_All(self):
        self.graph.delete_all()



username = 'neo4j'
password = 'Matcha411'
uri = 'bolt://18.217.253.58:7687'


test = NeoConnection(uri, username, password)
test.Transform()
test.Delete_All()



ex = FindExample(uri, username, password)
ex.apply_recon(3)
ex.close()
