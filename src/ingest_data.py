import csv

import redis.exceptions
import redisearch as rs

# Redis connection details
REDIS_HOST = "localhost"
REDIS_PORT = 6379
INDEX_NAME = "fund_index"
DOCUMENT_PREFIX = "fund:"


def create_index(client: rs.Client):
    """Creates the search index."""
    try:
        client.info()
        print("Index already exists.")
    except redis.exceptions.ResponseError:
        schema = (rs.TextField("name", weight=5.0, sortable=True), rs.TextField("details"))
        definition = rs.IndexDefinition(prefix=[DOCUMENT_PREFIX])
        client.create_index(fields=schema, definition=definition)
        print("Index created successfully.")


def ingest_data(client: rs.Client, csv_file_path: str ="data.csv"):
    """Ingests data from a CSV file into Redis."""
    with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header row
        print(f"CSV Header: {header}")

        count = 0
        for i, row in enumerate(reader):
            if len(row) == 2:
                doc_id = f"{DOCUMENT_PREFIX}{i}"
                name_thai = row[0]
                details = row[1]

                # Add document to Redis
                client.add_document(doc_id, name=name_thai, details=details)
                count += 1
            else:
                print(f"Skipping row {i+1} due to incorrect number of columns: {row}")
        print(f"Successfully ingested {count} documents into Redis.")


if __name__ == "__main__":
    # Initialize Redis client for RediSearch
    search_client = rs.Client(INDEX_NAME, host=REDIS_HOST, port=REDIS_PORT)

    create_index(search_client)
    ingest_data(search_client)
    print("Data ingestion complete.")

    # try:
    #     query = Query("กองทุนเปิด")
    #     result = search_client.search(query)
    #     print(f"Found {result.total} results for 'กองทุนเปิด':")
    #     for doc in result.docs:
    #         print(f"  ID: {doc.id}, Name: {doc.name}, Details: {doc.details}")
    # except Exception as e:
    #     print(f"Error during example search: {e}")
