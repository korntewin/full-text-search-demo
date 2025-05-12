import argparse

from src.azureai.ingest_data import get_search_client  # Reusing get_search_client


def search_azureai(search_text: str, top: int = 5):
    """Performs a search query against the Azure AI Search index."""
    search_client = get_search_client()
    try:
        results = search_client.search(search_text=search_text, top=top)
        documents_found = []
        for result in results:
            documents_found.append(result)
        print(f"Found {len(documents_found)} documents for query: '{search_text}'")
        return documents_found
    except Exception as e:
        print(f"Error searching documents: {e}")
        # Consider more specific error handling
        raise


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Search for animals in Azure AI.")
    parser.add_argument("query", type=str, help="The search query string.")

    args = parser.parse_args()

    search_azureai(args.query)