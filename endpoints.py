from fastapi import FastAPI, File, UploadFile
from typing import Optional
from images import Image, BoxedImage
from process import detect_objects, process_detections
import uuid
import cv2

app = FastAPI()

base_images = {}
superimpose_images = {}

@app.post("/upload_base_image/")
async def upload_base_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = Image(img)
    image_id = str(uuid.uuid4())
    base_images[image_id] = image
    return {"image_id": image_id}

@app.post("/upload_superimpose_image/")
async def upload_superimpose_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image = Image(img)
    image_id = str(uuid.uuid4())
    superimpose_images[image_id] = image
    return {"image_id": image_id}

@app.post("/process_image/")
async def process_image(base_image_id: str, superimpose_image_id: str, class_name: Optional[str] = None):
    base_image = base_images.get(base_image_id)
    superimpose_image = superimpose_images.get(superimpose_image_id)
    if base_image is None or superimpose_image is None:
        return {"error": "Base image or superimpose image not found"}

    outputs = detect_objects(base_image)
    boxed_image = process_detections(outputs, base_image)

    if class_name is None:
        result_image = boxed_image.superimpose_image(superimpose_image)
    else:
        result_image = boxed_image.superimpose_image(superimpose_image, class_name=class_name)

    result_image_id = str(uuid.uuid4())
    cv2.imwrite(f"{result_image_id}.jpg", result_image.image)
    return {"result_image_id": result_image_id}

@app.get("/download_result_image/{result_image_id}")
async def download_result_image(result_image_id: str):
    result_image_path = f"{result_image_id}.jpg"
    if not os.path.exists(result_image_path):
        return {"error": "Result image not found"}

    with open(result_image_path, "rb") as file:
        image_data = file.read()

    return Response(content=image_data, media_type="image/jpeg", headers={
        "Content-Disposition": f"attachment; filename={result_image_id}.jpg"
    })
