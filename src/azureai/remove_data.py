from src.azureai import ingest_data
from src.azureai import config


def delete_and_recreate_index(index_name: str = config.INDEX_NAME):
    """
    Deletes the entire Azure AI Search index and then recreates it.
    Assumes ingest_data module provides INDEX_NAME, get_search_index_client().
    """
    search_index_client = ingest_data.get_search_index_client()

    try:
        print(f"Attempting to delete index '{index_name}'...")
        search_index_client.delete_index(index_name)
        print(f"Index '{index_name}' deleted successfully.")
    except Exception as e:
        print(f"An unexpected error occurred during index deletion: {e}")
        raise

    try:
        print(f"Attempting to create index '{index_name}'...")
        search_index_client.create_index(index=index_name)
        ingest_data.create_or_update_index(index_name)
        print(f"Index '{index_name}' created successfully with the new schema.")
    except Exception as e:
        print(f"Error creating index '{index_name}': {e}")
        raise


if __name__ == "__main__":
    print("Attempting to delete and recreate the search index.")
    try:
        delete_and_recreate_index()
        print("Index deletion and recreation process completed.")
    except Exception as e:
        print(f"Failed to delete and recreate index: {e}")
