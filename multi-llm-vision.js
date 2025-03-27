const fs = require('fs');
const axios = require('axios');
const FormData = require('form-data');

// Supported model Ids: gemini | openai | claude

function postImageWithParams(imagePath, token, textPrompt, mode) {
  const url = "<Request url from team APEX:E3>";

  // Prepare payload
  const form = new FormData();
  form.append("prompt", textPrompt);
  form.append("mode", mode);

  try {
    const imageStream = fs.createReadStream(imagePath);
    form.append("file", imageStream);

    // Make the POST request
    axios.post(url, form, {
      headers: {
        ...form.getHeaders(),
        Authorization: token
      }
    })
    .then(response => {
      if (response.status === 200) {
        console.log("Response:", response.data);
      } else {
        console.log(`Failed with status code ${response.status}:`, response.data);
      }
    })
    .catch(error => {
      if (error.response) {
        console.error(`Request failed with status ${error.response.status}:`, error.response.data);
      } else {
        console.error("Error:", error.message);
      }
    });

  } catch (err) {
    console.error(`Error: Could not open image file '${imagePath}'.`);
  }
}

// === CLI handling ===

if (process.argv.length < 5) {
  console.log("Usage: node multi-llm-vision.js <image_path> <text_prompt> <model>");
  process.exit(1);
}

const imagePath = process.argv[2];
const textPrompt = process.argv[3];
const model = process.argv[4];

// Load token from file
fs.readFile('./test-token.json', 'utf8', (err, data) => {
  if (err) {
    console.error("Error reading token file:", err);
    return;
  }

  try {
    const tokenData = JSON.parse(data);
    const token = tokenData.key;

    postImageWithParams(imagePath, token, textPrompt, model);
  } catch (parseErr) {
    console.error("Error parsing token file:", parseErr);
  }
});
