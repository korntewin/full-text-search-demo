# Redis & Azure AI Search Full-Text Search Demo

## Overview

This project demonstrates and compares full-text search capabilities using two different technologies:

1.  **Redis**: Leveraging Redis's search features (e.g., RediSearch module).
2.  [TBC] **Azure AI Search**: Utilizing Microsoft Azure's dedicated search-as-a-service.

The primary goal is to showcase how to ingest data, remove data, and perform full-text search queries against datasets indexed by both systems.

## Running the Services with Docker Compose

This project uses Docker Compose to manage and run the different services.

### Prerequisites

*   Docker installed
*   Docker Compose installed

### Services

The `docker-compose.yaml` file defines several services. Here's how to run the key operational services:

#### 1. Ingest Data 📥

To populate the search indexes with sample data:

```bash
docker compose up ingest-data
```
This command will execute the `ingest-data` service, which is responsible for loading and indexing data into both Redis and Azure AI Search (if configured).

#### 2. Remove Data 🗑️

To clear all data from the search indexes:

```bash
docker compose up remove-data
```
This command will execute the `remove-data` service, which will delete the indexed data from both systems.

#### 3. Query Data 🔍

To perform search queries against the indexed data:

*   **For Redis:**
    ```bash
    QUERY_STRING="your search term" docker compose up query
    ```

Replace `"your search term"` with the actual query you want to execute. The `query` service will then interact with the redis and return the results.
