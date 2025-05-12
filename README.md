# Redis & Azure AI Search Full-Text Search Demo

## Overview

This project demonstrates and compares full-text search capabilities on **Thai language** using two different technologies:

1.  **Redis**: Leveraging Redis's search features (e.g., RediSearch module).
2.  **Azure AI Search**: Utilizing Microsoft Azure's dedicated search-as-a-service.

The primary goal is to showcase how to ingest data, remove data, and perform full-text search queries against datasets indexed by both systems.

## Running the Services with Docker Compose

This project uses Docker Compose to manage and run the different services.

### Prerequisites

*   Docker installed
*   Docker Compose installed
*   For Azure AI Search: Valid Azure subscription with AI Search service credentials

### Configuration

#### Redis Configuration
Redis is configured to run as a Docker container with the RediSearch module enabled. No additional configuration is needed.

#### Azure AI Search Configuration
To use Azure AI Search features:

1. Create an Azure AI Search service in your Azure portal
2. Set the following environment variables in .env file:
   ```bash
   AZURE_AI_SEARCH_ENDPOINT="your-search-service-endpoint"
   AZURE_AI_SEARCH_API_KEY="your-search-service-api-key"
   ```

### Services

The `docker-compose.yaml` file defines several services. Here's how to run the key operational services:

#### 1. Ingest Data 📥

To populate the search indexes with sample data:

*   **For Redis:**
    ```bash
    docker compose up ingest-data-redis
    ```

*   **For Azure AI Search:**
    ```bash
    docker compose up ingest-data-azureai
    ```

This command will execute the `ingest-data` service, which is responsible for loading and indexing data into both Redis and Azure AI Search.

#### 2. Remove Data 🗑️

To clear all data from the search indexes:

*   **For Redis:**
    ```bash
    docker compose up remove-data-redis
    ```

*   **For Azure AI Search:**
    ```bash
    docker compose up remove-data-azureai
    ```
This command will execute the `remove-data` service, which will delete the indexed data from both systems.

#### 3. Query Data 🔍

To perform search queries against the indexed data:

*   **For Redis:**
    ```bash
    QUERY_STRING="your search term" docker compose up query-redis
    ```

*   **For Azure AI Search:**
    ```bash
    QUERY_STRING="your search term" docker compose up query-azureai
    ```

Replace `"your search term"` with the actual query you want to execute. The services will interact with their respective search engines and return the results.

## Comparison results for Thai language

- **Redis:** Query the word `แมว` (cat in english) 
    - Redis doesn't found any documents with this word!
    - That's purely because Redis cannot tokenize Thai word and use the whole long-text as `inverted index`.

```txt
query-redis-1  | query_string: แมว
query-redis-1  | Found 0 results for 'แมว':
```

- **Azure AI Search:** Query the word `แมว`
    - Azure AI Search found 5 documents with this word.
    - Azure AI Search can tokenize Thai word, and thus `inverted index` is created properly.

```txt
query-azureai-1  | Document ID: animal_6 - TH Name: แมวศุภลักษณ์ - EN Name: SUPHALAK
query-azureai-1  | Document ID: animal_8 - TH Name: แมวเปอร์เซีย - EN Name: PERSIANCAT
query-azureai-1  | Document ID: animal_10 - TH Name: แมวสกอตติชโฟลด์ - EN Name: SCOTTISHFLD
query-azureai-1  | Document ID: animal_12 - TH Name: แมวบริติชชอร์ตแฮร์ - EN Name: BRITISHSH
query-azureai-1  | Document ID: animal_0 - TH Name: แมวขาวมณี - EN Name: KHAOMANEE
query-azureai-1  | Found 5 documents for query: 'แมว'
```

## Feature Comparison

This project demonstrates main key difference between Redis and Azure AI Search which is *Tokenization for Thai language*. Without proper tokinization, the inverted index became unusable and the **full-text search** capability should not be considered on such language.

## Data Schema

Both search engines are configured to index the following fields from the dataset:
- `id`: Unique identifier
- `TH_Name`: Name in Thai language
- `EN_Name`: Name in English language
