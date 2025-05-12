import csv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents import indexes
from azure.search.documents.indexes import models

from src.azureai import config


def get_search_client():
    """Returns a SearchClient for interacting with Azure AI Search."""
    return SearchClient(
        endpoint=config.AZURE_AI_SEARCH_ENDPOINT,
        index_name=config.INDEX_NAME,
        credential=AzureKeyCredential(config.AZURE_AI_SEARCH_API_KEY),
    )


def get_search_index_client():
    """Returns a SearchIndexClient for managing Azure AI Search indexes."""
    return indexes.SearchIndexClient(
        endpoint=config.AZURE_AI_SEARCH_ENDPOINT,
        credential=AzureKeyCredential(config.AZURE_AI_SEARCH_API_KEY),
    )


def create_or_update_index(index_name: str):
    """Creates or updates the search index with the defined schema."""
    index_client = get_search_index_client()
    fields = [
        models.SimpleField(name="id", type=models.SearchFieldDataType.String, key=True, filterable=True),
        models.SearchableField(name="th_title", type=models.SearchFieldDataType.String, searchable=True, analyzer_name="th.microsoft", sortable=True),
        models.SearchableField(name="en_title", type=models.SearchFieldDataType.String, searchable=True, sortable=True),
    ]
    index = models.SearchIndex(name=index_name, fields=fields)
    try:
        result = index_client.create_or_update_index(index=index)
        print(f"Index '{index_name}' created/updated successfully.")
        return result
    except Exception as e:
        print(f"Error creating/updating index: {e}")
        raise


def ingest_documents(documents: list[dict]):
    """Ingests a list of documents into the Azure AI Search index."""
    search_client = get_search_client()
    try:
        result = search_client.upload_documents(documents=documents)
        print(f"Successfully uploaded {len(documents)} documents.")
        return result
    except Exception as e:
        print(f"Error ingesting documents: {e}")
        raise


if __name__ == "__main__":
    DATA_FILE_PATH = "./data/data.csv"

    print(f"Creating or updating index '{config.INDEX_NAME}'...")
    create_or_update_index(config.INDEX_NAME)

    # Load data from CSV and prepare documents for ingestion
    print(f"Loading data from '{DATA_FILE_PATH}'...")
    documents_to_ingest = []

    with open(DATA_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for _id, row in enumerate(reader):
            document = {
                "id": f"{config.DOCUMENT_PREFIX}{_id}",
                "th_title": row["th_title"],
                "en_title": row["en_title"],
            }
            documents_to_ingest.append(document)
    print(f"Loaded {len(documents_to_ingest)} documents from CSV.")

    if documents_to_ingest:
        print("Ingesting documents into Azure AI Search...")
        ingest_documents(documents_to_ingest)
    else:
        print("No documents to ingest.")

    print("Ingestion process finished.")
