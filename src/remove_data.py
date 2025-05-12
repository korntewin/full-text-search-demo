\
import redis.exceptions
import redisearch as rs

from src import ingest_data, config

def remove_all_data(client: rs.Client):
    """Removes all documents from the search index by dropping and recreating it."""
    try:
        client.drop_index()
        print(f"Index '{config.INDEX_NAME}' dropped successfully.")
        ingest_data.create_index(client)
    except redis.exceptions.ResponseError as e:
        print(f"Error dropping index '{config.INDEX_NAME}': {e}. It might not exist, attempting to create.")
        ingest_data.create_index(client)

if __name__ == "__main__":
    search_client = rs.Client(config.INDEX_NAME, host=config.REDIS_HOST, port=config.REDIS_PORT)

    print(f"Attempting to remove all data from index: {config.INDEX_NAME}")
    remove_all_data(search_client)
    print("Data removal process complete.")
