from typing import LiteralString

from neo4j import AsyncGraphDatabase

from app.core.config import settings


class Neo4jDB:
    def __init__(
        self,
    ):
        super().__init__()
        self.graph_client = AsyncGraphDatabase.driver(
            uri=settings.NEO4J_URI,
            auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD),
        )

    async def ensure_graph_database(
        self,
        query: LiteralString,
        parameters: dict | None = None,
    ):
        async with self.graph_client.session() as session:
            await session.run(query=query, parameters=parameters)

    async def close(self):
        await self.graph_client.close()
        return

    async def db_action(
        self,
        query: LiteralString,
        parameters: dict | None = None,
    ):
        async with self.graph_client.session(database=settings.DATABASE) as session:
            result = await session.run(query=query, parameters=parameters)
            record = await result.data()
        return record
