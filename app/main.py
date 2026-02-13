from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os, uuid, shutil, base64
from PIL import Image, ImageDraw
from io import BytesIO
from .inference import run_inference

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile):
    # Temp directory to save uploaded images
    temp_dir = os.path.join(os.getcwd(), "temp_images")
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}.jpg")

    try:
        # Save uploaded file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Run inference
    try:
        boxes, scores, classes = run_inference(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")

    # Open image to draw bounding boxes
    img = Image.open(temp_path)
    draw = ImageDraw.Draw(img)

    detections = []
    for i, (box, score) in enumerate(zip(boxes, scores)):
        # Convert normalized box to image coordinates
        x1, y1, x2, y2 = box
        x1 = int(x1 * img.width)
        y1 = int(y1 * img.height)
        x2 = int(x2 * img.width)
        y2 = int(y2 * img.height)

        # Draw rectangle
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

        # Append detection with only ID, confidence, and box
        detections.append({
            "id": i,
            "confidence": float(score),
            "box": [float(x1), float(y1), float(x2), float(y2)]
        })

    # Convert image to base64
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Delete temp image
    if os.path.exists(temp_path):
        os.remove(temp_path)

    return JSONResponse({
        "detections": detections,
        "image_base64": img_str
    })
