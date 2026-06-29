from app.query.graph_query import queryclass

from .graph_db import Neo4jDB
from .mongodb import MongoDB


async def ensure_databases():
    mongo_client = MongoDB()
    graph_client = Neo4jDB()
    await mongo_client.ensure_database()
    await graph_client.ensure_graph_database(query=queryclass.ENSURE_DB_QUERY)
    return


async def close_databases():
    mongo_client = MongoDB()
    graph_client = Neo4jDB()
    await graph_client.close()
    await mongo_client.close()


__all__ = ["MongoDB", "Neo4jDB", "ensure_databases", "close_databases"]
