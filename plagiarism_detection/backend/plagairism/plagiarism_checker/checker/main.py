import requests

url = "https://ai-content-detector-ai-gpt.p.rapidapi.com/api/detectText/"
text = input("Enter the text to check for AI-generated content: ")
payload = { "text": text }
headers = {
	"x-rapidapi-key": "f9c6fdcf34msh47df29fc02a20bcp10e999jsnef5e5b251464",
	"x-rapidapi-host": "ai-content-detector-ai-gpt.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)


print(response.json())