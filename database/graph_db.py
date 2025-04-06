from neo4j import AsyncGraphDatabase

user="neo4j"
password="ping12345"

graph_client = AsyncGraphDatabase().driver(
    uri="bolt://localhost:7687",
    auth=(user,password)
)

