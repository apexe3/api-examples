import http.client
import ssl
import json
  
conn = http.client.HTTPSConnection("Ask APEXE3 team for URL", context=ssl._create_unverified_context())
  
payload = ''
headers = {
      'clientID': 'YOUR-CLIENT-ID',
      'clientSecret': 'YOUR-CLIENT-SECRET',
      'Content-Type': 'application/json'
}
conn.request("POST", "/backend_vector_db/api/v1/vector-resources/fetchVectorResources", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))