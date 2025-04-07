from typing import LiteralString
from neo4j import AsyncGraphDatabase
from settings.config import NEO4J_USER, NEO4J_PASSWORD, NEO4J_URI

graph_client = AsyncGraphDatabase().driver(
    uri= NEO4J_URI,
    auth=(NEO4J_USER,NEO4J_PASSWORD)
)

class Neo4jDB:
    def __init__(
            self,
            user_details:dict,
            query:LiteralString
    ):
        self.user_details = user_details
        self.query = query

    async def db_action(self):
        async with graph_client.session() as session:
            result = await session.run(
                query=self.query,
                parameters=self.user_details
            )
            record = await result.single()
        return record