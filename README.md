# 🔎 Elasticsearch Search API

**A Flask REST API for Elasticsearch Data Extraction and Search**

ElasticsearchSearchAPI is a Python-based REST API designed to retrieve relevant information from multiple Elasticsearch indices through a single HTTP endpoint.

Built with Flask and the Elasticsearch Python client, the API accepts JSON search requests, executes field-based queries, and returns matching records in a structured JSON response. It supports searches across vehicle, missing-vehicle, and challan-related datasets.

## ✨ Features

- 🌐 **REST API** — Expose Elasticsearch search functionality through an HTTP endpoint.
- 🔍 **Multi-Index Search** — Search across multiple configured Elasticsearch indices.
- 🚗 **Vehicle Lookup** — Search using vehicle registration numbers, vehicle types, and models.
- 📱 **Phone Number Search** — Support phone-related search parameters.
- 👤 **Name-Based Search** — Search supported name fields.
- 📍 **Address Search** — Search supported address and location fields.
- 🎯 **Field-Based Queries** — Map incoming JSON parameters to searchable Elasticsearch fields.
- 🔐 **Basic Authentication** — Protect the API endpoint using HTTP Basic Authentication.
- 📦 **Source Filtering** — Return selected fields from Elasticsearch documents.
- ⚡ **Response Compression** — Compress HTTP responses using Flask-Compress.
- 🧾 **JSON Responses** — Return results in a structured JSON format.

## 📂 Project Structure

```text
ElasticsearchSearchAPI/
│
├── appAPIData.py       # Flask API and Elasticsearch search logic
└── README.md           # Project documentation
```

*Note: `appAPIData.py` is the suggested filename. Replace it with the actual script filename if different.*

## 🧰 Technology Stack

- **Python** — Application programming language.
- **Flask** — REST API framework.
- **Elasticsearch** — Search and data retrieval engine.
- **Flask-BasicAuth** — HTTP Basic Authentication.
- **Flask-Compress** — HTTP response compression.
- **Requests** — HTTP client library, if required by the application or its dependencies.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hemantkarne70-tech/ElasticsearchSearchAPI.git
cd ElasticsearchSearchAPI
```

### 2. Create a Virtual Environment

**Windows — Git Bash**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

**Linux / Ubuntu**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```text
Flask
elasticsearch
Flask-BasicAuth
Flask-Compress
requests
```

For production deployments, pin compatible dependency versions, especially the Elasticsearch Python client version supported by your Elasticsearch server.

### 4. Configure Elasticsearch

Configure the following settings before running the application:

- Elasticsearch server URL.
- Authentication credentials, if required.
- Flask application secret.
- API Basic Authentication username and password.
- Host and port for the Flask application.
- Index names and searchable fields.

### 5. Run the API

If the script is named `appAPIData.py`:

```bash
python appAPIData.py
```

The application exposes the following endpoint:

```text
POST /getData/
```

For production deployments, use a production-ready WSGI server and disable Flask debug mode.

## 📡 API Documentation

### Endpoint

```http
POST /getData/
```

### Authentication

The endpoint uses HTTP Basic Authentication.

Provide the configured username and password through your HTTP client's authentication settings. Use HTTPS when transmitting credentials over a network.

### Request Format

The API accepts a JSON payload containing supported search parameters.

Example:

```json
{
  "vehicle_registry_no": "KA52AB1234",
  "phone_no": "9876543210",
  "name": "Example Name",
  "vehicle_type": "Car",
  "vehicle_model": "Example Model",
  "address": "Nelamangala"
}
```

Each parameter is optional. You can submit one or more supported parameters in a request.

The API searches the mapped fields across the configured indices and combines matching records in the response. Actual matches depend on the available documents and the Elasticsearch query behavior.

### Example Request Using cURL

```bash
curl -X POST "http://localhost:5000/getData/" \
  -u "YOUR_USERNAME:YOUR_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_registry_no": "KA52AB1234",
    "name": "Example Name"
  }'
```

### Example Response

```json
{
  "Result": {
    "vehicle_missing_data": [],
    "vehicleRegistry": [],
    "challan_data": []
  }
}
```

The response contains the matching records for each configured index. The `vehicle_data` index is exposed under the display name `vehicleRegistry`.

The arrays above are illustrative; actual results depend on the query and the indexed data.

## 🔄 How It Works

1. **Receive Request** — Accept a POST request containing JSON search parameters.
2. **Authenticate** — Validate the request using HTTP Basic Authentication.
3. **Map Search Fields** — Translate incoming parameters into supported Elasticsearch fields.
4. **Build Queries** — Construct match and wildcard queries for applicable fields.
5. **Search Indices** — Execute Elasticsearch searches against the configured indices.
6. **Collect Results** — Combine matching records under their corresponding response keys.
7. **Return JSON** — Send the collected results to the API consumer.

## ⚠️ Important Considerations

- Ensure the Elasticsearch service is accessible from the application server.
- Validate incoming request payloads and search values.
- Avoid exposing stack traces or internal exception details to external API consumers in production.
- Review wildcard queries carefully, as leading-wildcard searches can be expensive.
- Configure appropriate request limits and Elasticsearch timeouts.
- The current search implementation limits each individual search to 1,000 hits; additional pagination may be required for larger result sets.
- Confirm that all fields in the search mappings are included in the corresponding index's configured searchable-field list.
- Use HTTPS and a production WSGI server when deploying the API.

## 👨‍💻 Author

**Hemant Karne**

Software Engineer | Python | Flask | REST APIs | Elasticsearch | Data Engineering

GitHub: [@hemantkarne70-tech](https://github.com/hemantkarne70-tech)

---

*Search and retrieve Elasticsearch data through a lightweight, Python-powered REST API.*
