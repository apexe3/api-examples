import requests
import sys
import json

# Supported model Ids: gemini | openai | claude

def post_image_with_params(image_path, token, text_prompt, mode):
   url = "<Request url from team APEX:E3>"


   # Prepare headers
   headers = {
       "Authorization": token,
   }


   # Prepare payload
   payload = {
       "prompt": text_prompt,
       "mode": mode,
   }


   # Open the image file
   try:
       with open(image_path, "rb") as image_file:
           files = {
               "file": image_file,
   }


           # Make the POST request
           response = requests.post(url, data=payload, headers=headers, files=files)


           # Check for success
           if response.status_code == 200:
               print("Response:", response.json())
           else:
               print(f"Failed with status code {response.status_code}: {response.text}")


   except FileNotFoundError:
       print(f"Error: The file '{image_path}' was not found.")
   except Exception as e:
       print(f"An error occurred: {e}")


if __name__ == "__main__":
  
   print(sys.argv[1])
   print(sys.argv[2])
   print(sys.argv[3])

   with open("./test-token.json", "r") as f:
    token_data = json.load(f)
    token = token_data["key"]
    if len(sys.argv) < 3:
        print("Usage: python script.py <image_path> <text_prompt> <model>")
    else:
        image_path = sys.argv[1]
        text_prompt = sys.argv[2]
        model = sys.argv[3]
        token = token
        post_image_with_params(image_path, token, text_prompt, model)