import os


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379
INDEX_NAME = "animal_index"
DOCUMENT_PREFIX = "animal:"