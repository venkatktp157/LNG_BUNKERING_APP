FROM python:3.9.23-slim

# Set working directory to match project folder
WORKDIR /lng_bunker_api

# Copy requirements and install dependencies
COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

# Copy source files
COPY api.py couchdb_config.py ./

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
