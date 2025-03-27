const url = "<Request url from team APEX:E3>";

// Supported model ids
// gemini-1.5-flash // gemini-2.0-flash // gpt-4o-turbo // o1-mini // o3-mini // o1
// claude-sonnet-3.5 // mistral-large-latest // grok2 // deepseek // nemotron

const body = {
  "prompt": `<your prompt>`,
  "model": "<moodel id>", 
  "systemPrompt": "Your job is to summarise earnings transcripts",
  "maxOutputTokens": 1000,
  "userId": "<your-email>"
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(body)
})
.then(response => {
  if (response.ok) {
    if (response.status === 201) {
      return response.text().then(text => console.log("Response:", text));
    } else {
      console.log("Unexpected success status code:", response.status);
    }
  } else {
    console.log("Failed to get a response. Status code:", response.status);
  }
})
.catch(error => console.error('Fetch error:', error));