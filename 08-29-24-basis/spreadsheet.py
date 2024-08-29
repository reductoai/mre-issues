import requests
import os


api_key = os.environ["REDUCTO_API_KEY"]

upload_form = requests.post("https://v1.api.reducto.ai/upload?extension=.xlsx",
                            headers={"Authorization": f"Bearer {api_key}"}).json()

requests.put(upload_form["presigned_url"], data=open("./sample.xlsx", "rb"))

response = requests.post("https://v1.api.reducto.ai/parse",
                         json={"document_url": upload_form["file_id"]},
                         headers={"Authorization": f"Bearer {api_key}"})

print(response.json())
