import requests

base_image_path = "cat.jpg"
superimpose_image_path = "cage.jpg"

# Upload base image
with open(base_image_path, "rb") as file:
    response = requests.post("http://localhost:8000/upload_base_image/", files={"file": file})
    print(response.content)
    base_image_id = response.json()["image_id"]

# Upload superimpose image
with open(superimpose_image_path, "rb") as file:
    response = requests.post("http://localhost:8000/upload_superimpose_image/", files={"file": file})
    superimpose_image_id = response.json()["image_id"]

# Process image without specifying class name
response = requests.post("http://localhost:8000/process_image/", json={
    "base_image_id": base_image_id,
    "superimpose_image_id": superimpose_image_id
})
result_image_id = response.json()["result_image_id"]
print(f"Result image without class name: {result_image_id}.jpg")

# Process image with a specific class name
class_name = "cat"
response = requests.post("http://localhost:8000/process_image/", json={
    "base_image_id": base_image_id,
    "superimpose_image_id": superimpose_image_id,
    "class_name": class_name
})

response = requests.get(f"http://localhost:8000/download_result_image/{result_image_id}")
if response.status_code == 200:
    with open(f"{result_image_id}.jpg", "wb") as file:
        file.write(response.content)
    print(f"Downloaded result image without class name: {result_image_id}.jpg")
else:
    print("Failed to download result image without class name")

# Download result image with a specific class name
response = requests.get(f"http://localhost:8000/download_result_image/{result_image_id}")
if response.status_code == 200:
    with open(f"{result_image_id}_class_{class_name}.jpg", "wb") as file:
        file.write(response.content)
    print(f"Downloaded result image with class name '{class_name}': {result_image_id}_class_{class_name}.jpg")
else:
    print(f"Failed to download result image with class name '{class_name}'")

result_image_id = response.json()["result_image_id"]
print(f"Result image with class name '{class_name}': {result_image_id}.jpg")
