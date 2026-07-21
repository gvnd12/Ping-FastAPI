import logging

from app.core.config import settings
from app.query.graph_query import queryclass

from .graph_db import Neo4jDB
from .minio_storage import MinIO
from .mongodb import MongoDB, close_mongo_client, init_mongo_client

logger = logging.getLogger(settings.APP_NAME)


async def ensure_databases():
    mongo_client = MongoDB()
    graph_client = Neo4jDB()
    mongo_database = await mongo_client.ensure_database()
    logger.info(f"Mongo database '{mongo_database.name}' initialized successfully!")
    await graph_client.ensure_graph_database(query=queryclass.ENSURE_DB_QUERY)
    logger.info("Neo4j database initialized successfully!")
    return


async def close_databases():
    graph_client = Neo4jDB()
    await graph_client.close()
    await close_mongo_client()


__all__ = [
    "MongoDB",
    "Neo4jDB",
    "ensure_databases",
    "close_databases",
    "MinIO",
    "init_mongo_client",
    "close_mongo_client",
]
