import requests
import os
from pdf2image import convert_from_path

# API endpoint URLs
UPLOAD_URL = "https://v1.api.reducto.ai/upload?extension=.pdf"
PARSE_URL = "https://v1.api.reducto.ai/parse"

# Your API key (replace with your actual key)
API_KEY = os.environ.get("REDUCTO_API_KEY")

# Headers for the API requests
headers = {"Authorization": f"Bearer {API_KEY}"}

# Upload the PDF file
with open("./researchpaper.pdf", "rb") as file:
    files = {"file": ("researchpaper.pdf", file, "application/pdf")}
    response = requests.post(UPLOAD_URL, headers=headers, files=files)

if response.status_code == 200:
    upload_data = response.json()
    file_id = upload_data.get("file_id")

    if file_id:
        payload = {"document_url": file_id}
        parse_headers = headers.copy()
        parse_headers["Content-Type"] = "application/json"
        parse_response = requests.post(PARSE_URL, headers=parse_headers, json=payload)

        parse_result = parse_response.json()

        # Create figures directory if it doesn't exist
        os.makedirs("./figures", exist_ok=True)

        # Convert PDF to images
        pages = convert_from_path("./researchpaper.pdf")

        # Extract figures from the response
        for chunk in parse_result["result"]["chunks"]:
            for block in chunk["blocks"]:
                if block["type"] == "Figure":
                    bbox = block["bbox"]
                    page_num = (
                        bbox["page"] - 1
                    )  # PDF pages are 1-indexed, list is 0-indexed

                    if page_num < len(pages):
                        page = pages[page_num]
                        width, height = page.size

                        left = int(bbox["left"] * width)
                        top = int(bbox["top"] * height)
                        right = left + int(bbox["width"] * width)
                        bottom = top + int(bbox["height"] * height)

                        figure = page.crop((left, top, right, bottom))

                        # Save the figure
                        figure_path = f"./figures/figure_{page_num+1}_{left}_{top}.png"
                        figure.save(figure_path)
                        print(f"Saved figure: {figure_path}")

    else:
        print("File ID not found in the upload response")
else:
    print(f"Upload failed. Status code: {response.status_code}")
    print("Response:", response.text)
# End of Selection
