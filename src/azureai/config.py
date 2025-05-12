import os

# Azure AI Search configuration
AZURE_AI_SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
AZURE_AI_SEARCH_API_KEY = os.getenv("AZURE_AI_SEARCH_API_KEY")

INDEX_NAME = "animal"
DOCUMENT_PREFIX = "animal:"
