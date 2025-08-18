# CouchDB Integration for LNG Bunkering API

This document explains how to use the new CouchDB integration features in your LNG Bunkering API.

## 🚀 Features

- **Automatic Storage**: Bunkering calculations are automatically saved to CouchDB
- **Manual Storage**: Save bunkering data manually to CouchDB
- **Data Retrieval**: Query bunkering data from CouchDB
- **Ship Filtering**: Filter data by specific ship
- **Document Management**: Retrieve specific documents by ID

## 📋 Prerequisites

1. **CouchDB Server**: Ensure CouchDB is running and accessible
2. **Python Dependencies**: Install required packages
3. **Environment Variables**: Configure CouchDB connection settings

## 🔧 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure CouchDB Connection

Set environment variables or modify `couchdb_config.py`:

```bash
# Environment variables
export COUCHDB_URL="http://localhost:5984"
export COUCHDB_USERNAME="admin"
export COUCHDB_PASSWORD="password"

# Or create a .env file
COUCHDB_URL=http://localhost:5984
COUCHDB_USERNAME=admin
COUCHDB_PASSWORD=password
```

### 3. Start the API Server

```bash
python api.py
```

## 📡 API Endpoints

### 1. Calculate Bunkering (Auto-save to CouchDB)

**Endpoint**: `POST /bunkering/calculate`

**Description**: Calculates bunkering operations and automatically saves results to CouchDB

**Request Body**: `BunkeringRequest` model

**Response**: `BunkeringResponse` model + automatic CouchDB storage

**Example**:
```bash
curl -X POST "http://localhost:8000/bunkering/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "ship_id": "CMA CGM MONACO",
    "opening_tank1": {"level": 1000, "vapor_temp": -150, "liquid_temp": -160, "pressure": 0.20},
    "opening_tank2": {"level": 980, "vapor_temp": -151, "liquid_temp": -158, "pressure": 0.22},
    "closing_tank1": {"level": 1100, "vapor_temp": -149, "liquid_temp": -156, "pressure": 0.23},
    "closing_tank2": {"level": 1085, "vapor_temp": -148, "liquid_temp": -155, "pressure": 0.24},
    "opening_trim": 0.0,
    "opening_list": 0.0,
    "closing_trim": 0.0,
    "closing_list": 0.0,
    "opening_time": "07/10/2025 10:00",
    "closing_time": "07/10/2025 16:00",
    "density": 0.45,
    "bdn_quantity": 1000,
    "bog": 300,
    "gross_energy": 10000,
    "unreckoned_qty": 0,
    "net_energy": 9800
  }'
```

### 2. Manual Save to CouchDB

**Endpoint**: `POST /bunkering/save-to-couchdb`

**Description**: Manually save bunkering response data to CouchDB

**Request Body**: `BunkeringResponse` model

**Response**: Success message with document ID and revision

**Example**:
```bash
curl -X POST "http://localhost:8000/bunkering/save-to-couchdb" \
  -H "Content-Type: application/json" \
  -d '{
    "ship_id": "MOUNT TOURMALINE",
    "tank1_volume_opening": 850.5,
    "tank2_volume_opening": 820.3,
    "tank1_volume_closing": 950.2,
    "tank2_volume_closing": 920.1,
    "opening_quantity": 1670.8,
    "closing_quantity": 1870.3,
    "volume_difference": 199.5,
    "bog_consumption": 15.2,
    "loaded_quantity": 214.7,
    "net_quantity": 210.0,
    "difference": 4.7,
    "calculation_time": "2025-07-10T16:00:00"
  }'
```

### 3. Retrieve All Bunkering Documents

**Endpoint**: `GET /bunkering/get-from-couchdb`

**Description**: Retrieve all bunkering documents from CouchDB

**Query Parameters**:
- `ship_id` (optional): Filter by specific ship
- `limit` (optional): Maximum number of documents to return (default: 100)

**Response**: List of bunkering documents with metadata

**Example**:
```bash
# Get all documents
curl "http://localhost:8000/bunkering/get-from-couchdb"

# Get documents for specific ship
curl "http://localhost:8000/bunkering/get-from-couchdb?ship_id=CMA%20CGM%20MONACO"

# Get limited number of documents
curl "http://localhost:8000/bunkering/get-from-couchdb?limit=50"
```

### 4. Retrieve Specific Document

**Endpoint**: `GET /bunkering/get-from-couchdb/{doc_id}`

**Description**: Retrieve a specific bunkering document by ID

**Path Parameter**: `doc_id` - CouchDB document ID

**Response**: Single bunkering document

**Example**:
```bash
curl "http://localhost:8000/bunkering/get-from-couchdb/bunkering_20250710_160000_CMA%20CGM%20MONACO"
```

## 🗄️ CouchDB Document Structure

Each bunkering document in CouchDB has the following structure:

```json
{
  "_id": "bunkering_20250710_160000_CMA CGM MONACO",
  "_rev": "1-abc123def456",
  "type": "bunkering_operation",
  "timestamp": "2025-07-10T16:00:00.123456",
  "data": {
    "ship_id": "CMA CGM MONACO",
    "tank1_volume_opening": 1000.0,
    "tank2_volume_opening": 980.0,
    "tank1_volume_closing": 1100.0,
    "tank2_volume_closing": 1085.0,
    "opening_quantity": 1980.0,
    "closing_quantity": 2185.0,
    "volume_difference": 205.0,
    "bog_consumption": 15.2,
    "loaded_quantity": 220.2,
    "net_quantity": 210.0,
    "difference": 10.2,
    "calculation_time": "2025-07-10T16:00:00"
  }
}
```

## 📊 Data Fields

### Core Bunkering Data
- **ship_id**: Ship identifier
- **tank1_volume_opening**: Opening volume for tank 1 (m³)
- **tank2_volume_opening**: Opening volume for tank 2 (m³) - optional
- **tank1_volume_closing**: Closing volume for tank 1 (m³)
- **tank2_volume_closing**: Closing volume for tank 2 (m³) - optional
- **opening_quantity**: Total opening quantity (m³)
- **closing_quantity**: Total closing quantity (m³)
- **volume_difference**: Volume difference (m³)
- **bog_consumption**: BOG consumption (m³)
- **loaded_quantity**: Total loaded quantity (m³)
- **net_quantity**: Net quantity (m³)
- **difference**: Final difference (m³)
- **calculation_time**: Calculation timestamp

### Metadata
- **_id**: Unique document identifier
- **_rev**: CouchDB revision number
- **type**: Document type identifier
- **timestamp**: Storage timestamp

## 🧪 Testing

### Run Examples

```bash
python couchdb_examples.py
```

### Test Individual Endpoints

```bash
# Test bunkering calculation
python -c "
import requests
response = requests.post('http://localhost:8000/bunkering/calculate', json={
    'ship_id': 'CMA CGM MONACO',
    'opening_tank1': {'level': 1000, 'vapor_temp': -150, 'liquid_temp': -160, 'pressure': 0.20},
    'closing_tank1': {'level': 1100, 'vapor_temp': -149, 'liquid_temp': -156, 'pressure': 0.23},
    'opening_trim': 0.0, 'opening_list': 0.0, 'closing_trim': 0.0, 'closing_list': 0.0,
    'opening_time': '07/10/2025 10:00', 'closing_time': '07/10/2025 16:00',
    'density': 0.45, 'bdn_quantity': 1000, 'bog': 300,
    'gross_energy': 10000, 'unreckoned_qty': 0, 'net_energy': 9800
})
print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')
"
```

## 🔍 CouchDB Management

### View Documents in CouchDB

1. **Web Interface**: Navigate to `http://localhost:5984/_utils/`
2. **Database**: Select `lng_bunkering` database
3. **Documents**: View all bunkering documents

### CouchDB Queries

```bash
# Get all bunkering documents
curl "http://localhost:5984/lng_bunkering/_all_docs"

# Get specific document
curl "http://localhost:5984/lng_bunkering/bunkering_20250710_160000_CMA%20CGM%20MONACO"

# Get documents by ship (using Mango queries)
curl -X POST "http://localhost:5984/lng_bunkering/_find" \
  -H "Content-Type: application/json" \
  -d '{"selector": {"data.ship_id": "CMA CGM MONACO"}}'
```

## 🚨 Error Handling

### Common Issues

1. **Connection Failed**: Check CouchDB server status and credentials
2. **Database Not Found**: Database will be created automatically
3. **Authentication Failed**: Verify username/password
4. **Document Save Failed**: Check document structure and validation

### Debug Mode

Enable debug logging by setting environment variable:

```bash
export DEBUG_COUCHDB=1
```

## 📈 Performance Considerations

- **Batch Operations**: For large datasets, consider batch document operations
- **Indexing**: Create indexes for frequently queried fields
- **Caching**: Implement application-level caching for frequently accessed data
- **Connection Pooling**: Reuse CouchDB connections when possible

## 🔐 Security

- **Authentication**: Use strong passwords for CouchDB
- **Network Security**: Restrict CouchDB access to trusted networks
- **Data Encryption**: Consider encrypting sensitive bunkering data
- **Access Control**: Implement proper CouchDB user roles and permissions

## 📚 Additional Resources

- [CouchDB Python Client Documentation](https://couchdb-python.readthedocs.io/)
- [CouchDB HTTP API Reference](https://docs.couchdb.org/en/stable/api/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LNG Bunkering Standards](https://www.sigto.org/)

## 🤝 Support

For issues or questions:
1. Check the API logs for error messages
2. Verify CouchDB connection settings
3. Test with the provided examples
4. Review the API documentation

---

**Note**: This integration automatically saves all bunkering calculations to CouchDB. Ensure your CouchDB server has sufficient storage capacity for your expected data volume.
