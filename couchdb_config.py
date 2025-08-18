#!/usr/bin/env python
# coding: utf-8

"""
CouchDB Configuration for LNG Bunkering Application
"""

import os

# CouchDB Connection Settings
COUCHDB_URL = os.getenv("COUCHDB_URL", "http://app.wayship.io:5984")
COUCHDB_USERNAME = os.getenv("COUCHDB_USERNAME", "admin")
COUCHDB_PASSWORD = os.getenv("COUCHDB_PASSWORD", "WTX6N8S3")
DB_NAME = "lng_bunkering"

# CouchDB Document Settings
DOCUMENT_PREFIX = "bunkering"
MAX_DOCUMENTS_RETRIEVAL = 1000

# CouchDB Connection Timeout (seconds)
CONNECTION_TIMEOUT = 30

# CouchDB Retry Settings
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Document Metadata
DOCUMENT_TYPE = "bunkering_operation"
DOCUMENT_VERSION = "1.0"
