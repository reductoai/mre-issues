import requests
import os


api_key = os.environ["REDUCTO_API_KEY"]

upload_form = requests.post(
    "https://v1.api.reducto.ai/upload?extension=.xlsx",
    headers={"Authorization": f"Bearer {api_key}"},
).json()

requests.put(upload_form["presigned_url"], data=open("./sample.xlsx", "rb"))

response = requests.post(
    "https://v1.api.reducto.ai/extract",
    json={
        "document_url": upload_form["file_id"],
        "schema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The main content of the message.",
                }
            },
            "required": ["message"],
        },
    },
    headers={"Authorization": f"Bearer {api_key}"},
)

print(response.json())
