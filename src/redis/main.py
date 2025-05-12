import argparse

import redis.exceptions
import redisearch as rs

from src.redis import config


def search_redis(query_string: str):
    """Searches Redis using the given query string."""
    client = rs.Client(config.INDEX_NAME, host=config.REDIS_HOST, port=config.REDIS_PORT)

    # Create a query object
    query = rs.Query(query_string)
    print(f"query_string: {query_string}")

    try:
        # Execute the search query
        result = client.search(query)

        print(f"Found {result.total} results for '{query_string}':")
        for doc in result.docs:
            print(f"Document ID: {doc.id} - TH Name: {doc.TH_Name} - EN Name: {doc.EN_Name}")

    except redis.exceptions.ResponseError as e:
        print(f"Error executing search: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for animals in Redis.")
    parser.add_argument("query", type=str, help="The search query string.")

    args = parser.parse_args()

    search_redis(args.query)
