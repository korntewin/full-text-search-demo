import csv

import redis.exceptions
import redisearch as rs

from src.redis import config


def create_index(client: rs.Client):
    """Creates the search index."""
    try:
        client.info()
        print("Index already exists.")
    except redis.exceptions.ResponseError:
        schema = (rs.TextField("TH_Name", weight=5.0, sortable=True), rs.TextField("EN_Name"))
        definition = rs.IndexDefinition(prefix=[config.DOCUMENT_PREFIX])
        client.create_index(fields=schema, definition=definition)
        print("Index created successfully.")


def ingest_data(client: rs.Client, csv_file_path: str ="data/data.csv"):
    """Ingests data from a CSV file into Redis."""
    with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        header = next(reader)  # Skip header row
        print(f"CSV Header: {header}")

        count = 0
        for i, row in enumerate(reader):
            if len(row) == 2:
                doc_id = f"{config.DOCUMENT_PREFIX}{i}"
                name_thai = row["TH_Name"]
                details = row["EN_Name"]

                # Add document to Redis
                client.add_document(doc_id, TH_Name=name_thai, EN_Name=details)
                count += 1
            else:
                print(f"Skipping row {i+1} due to incorrect number of columns: {row}")
        print(f"Successfully ingested {count} documents into Redis.")


if __name__ == "__main__":
    # Initialize Redis client for RediSearch
    search_client = rs.Client(config.INDEX_NAME, host=config.REDIS_HOST, port=config.REDIS_PORT)

    create_index(search_client)
    ingest_data(search_client)
    print("Data ingestion complete.")

    # try:
    #     query = Query("แมว")
    #     result = search_client.search(query)
    #     print(f"Found {result.total} results for 'animal':")
    #     for doc in result.docs:
    #         print(f"  ID: {doc.id}, Name: {doc.name}, Details: {doc.details}")
    # except Exception as e:
    #     print(f"Error during example search: {e}")
