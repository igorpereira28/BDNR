from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def query(self, query, parameters=None, fetch_one=False):
        with self._driver.session() as session:
            if fetch_one:
                result = session.run(query, parameters)
                return result.single()
            else:
                return session.run(query, parameters).data()
