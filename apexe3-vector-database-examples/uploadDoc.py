import http.client
import mimetypes
import ssl
import json

# Get user input
file_path = input("Enter the file path: ").strip()
file_name = input("Enter the file name: ").strip()
client_id = input("Enter Client ID: ").strip()
client_secret = input("Enter Client Secret: ").strip()
index_name = input("Enter Index Name: ").strip()
document_prefix = input("Enter Document Prefix: ").strip()

# Establish HTTP connection
conn = http.client.HTTPSConnection("Ask APEXE3 team for url", context=ssl._create_unverified_context())

# --- Upload Resource ---
multipart_boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'

# Prepare multipart form-data payload
data_parts = [
    f'--{multipart_boundary}',
    f'Content-Disposition: form-data; name="file"; filename="{file_name}"',
    f'Content-Type: {mimetypes.guess_type(file_path)[0] or "application/octet-stream"}',
    ''
]

# Read file content
try:
    with open(file_path, 'rb') as file:
        file_content = file.read()
    data_parts.append(file_content)
except FileNotFoundError:
    print("Error: File not found. Please check the file path and try again.")
    exit(1)

# Add additional form fields
data_parts.extend([
    f'--{multipart_boundary}',
    'Content-Disposition: form-data; name="cleanText"',
    'Content-Type: text/plain',
    '',
    'n',
    
    f'--{multipart_boundary}',
    'Content-Disposition: form-data; name="perPage"',
    'Content-Type: text/plain',
    '',
    'y',
    
    f'--{multipart_boundary}--',
    ''
])

# Convert data to byte format
request_body = b'\r\n'.join(
    part if isinstance(part, bytes) else part.encode('utf-8') for part in data_parts
)

# Set headers
resource_headers = {
    'clientID': client_id,
    'clientSecret': client_secret,
    'Content-type': f'multipart/form-data; boundary={multipart_boundary}'
}

# Send request to upload resource
conn.request("POST", "/backend_vector_db/api/v1/vector-resources/createResourceFromFile", request_body, resource_headers)
resource_response = conn.getresponse()
resource_data = resource_response.read().decode("utf-8")

# Extract resource ID
try:
    resource_json = json.loads(resource_data)
    resource_id = resource_json.get("id", "DEFAULT-VALUE")
    print(f"Uploaded Resource ID: {resource_id}")
except json.JSONDecodeError:
    print(f"{resource_data}")
    exit(1)

# --- Create Index ---
index_payload = json.dumps({
    "modelId": "0.0.1-U-S-E",
    "name": index_name,
    "documentPrefix": document_prefix,
    "distanceMetric": "COSINE"
})

index_headers = {
    'clientID': client_id,
    'clientSecret': client_secret,
    'Content-Type': 'application/json'
}

# Send request to create an index
conn.request("POST", "/backend_vector_db/api/v1/vector-resources/createVectorIndex", index_payload, index_headers)
index_response = conn.getresponse()
index_data = index_response.read().decode("utf-8")

# Extract index ID
try:
    index_json = json.loads(index_data)

    if "id" in index_json:
        index_id = index_json["id"]
        print(f"Created Index ID: {index_id}")
    else:
        error_message = index_json.get("message", "Unknown error occurred")
        status_code = index_json.get("statusCode", "Unknown status code")

        print(f"Error creating index: {error_message} (Status Code: {status_code})")
        exit(1)

except json.JSONDecodeError:
    print(f"Invalid JSON response: {index_data}")
    exit(1)


# --- Add Resource to Index ---
add_to_index_payload = json.dumps({
    "indexId": index_id,
    "resourceId": resource_id,
    "chunkSize": 250
})

add_to_index_headers = {
    'clientID': client_id,
    'clientSecret': client_secret,
    'Content-Type': 'application/json'
}

# Send request to add resource to index
conn.request("POST", "/backend_vector_db/api/v1/vector-resources/addResourceEmbeddingsToIndex", add_to_index_payload, add_to_index_headers)
final_response = conn.getresponse()
final_data = final_response.read().decode("utf-8")

# Print final response
print("Final API Response:", final_data)
