from typing import LiteralString
from neo4j import AsyncGraphDatabase
from app.core.config import settings

graph_client = AsyncGraphDatabase.driver(
    uri= settings.NEO4J_URI,
    auth=(settings.NEO4J_USERNAME,settings.NEO4J_PASSWORD)
)

class Neo4jDB:
    def __init__(
            self,
            user_details:dict,
            query:LiteralString,
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