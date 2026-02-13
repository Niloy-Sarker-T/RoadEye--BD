# # bounding_box_shower.py
# import json
# import base64
# from PIL import Image, ImageDraw
# from io import BytesIO

# def draw_boxes_on_image(json_file_path):
#     """
#     Load a prediction JSON file containing base64 image and detections,
#     draw bounding boxes on the image, and return a PIL image.
    
#     Args:
#         json_file_path (str): Path to the JSON file

#     Returns:
#         PIL.Image: Image with drawn bounding boxes
#     """
#     # Load JSON
#     with open(json_file_path, "r") as f:
#         response = json.load(f)

#     # Decode base64 image
#     img_data = base64.b64decode(response.get("image_base64", ""))
#     img = Image.open(BytesIO(img_data)).convert("RGB")

#     # Draw bounding boxes
#     draw = ImageDraw.Draw(img)
#     for det in response.get("detections", []):
#         box = det["box"]  # [x1, y1, x2, y2]
#         draw.rectangle(box, outline="red", width=2)
#         draw.text((box[0], box[1]-10), f"ID: {det['id']}", fill="red")

#     return img
import json
import base64
from PIL import Image, ImageDraw
from io import BytesIO

def draw_boxes_on_image(json_data):
    """
    Draw bounding boxes with IDs on the image from JSON data.

    Args:
        json_data (dict): JSON response from your API

    Returns:
        PIL.Image: Image with drawn bounding boxes and IDs
    """
    # Decode base64 image
    img_data = base64.b64decode(json_data.get("image_base64", ""))
    img = Image.open(BytesIO(img_data)).convert("RGB")

    # Draw bounding boxes
    draw = ImageDraw.Draw(img)
    for det in json_data.get("detections", []):
        box = det["box"]  # [x1, y1, x2, y2]
        obj_id = det["id"]
        draw.rectangle(box, outline="red", width=2)
        draw.text((box[0], box[1]-10), f"ID: {obj_id}", fill="red")

    return img
