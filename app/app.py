# # app.py
# import streamlit as st
# import json
# from PIL import Image
# import base64
# import requests
# from bounding_box_shower import draw_boxes_on_image

# st.title("RoadEye Object Detection Demo")

# # Upload image
# uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     # Save uploaded image temporarily
#     image = Image.open(uploaded_file)
#     temp_image_path = "temp_image.jpg"
#     image.save(temp_image_path)

#     # Send image to your inference API
#     files = {"file": open(temp_image_path, "rb")}
#     response = requests.post("http://127.0.0.1:8000/predict", files=files)

#     if response.status_code == 200:
#         data = response.json()

#         # Save API JSON to a temporary file
#         temp_json_path = "temp_prediction.json"
#         with open(temp_json_path, "w") as f:
#             json.dump(data, f)

#         # Draw bounding boxes using the function
#         img_with_boxes = draw_boxes_on_image(temp_json_path)

#         # Show result in Streamlit
#         st.image(img_with_boxes, caption="Prediction with Bounding Boxes", use_column_width=True)

#     else:
#         st.error(f"Inference failed: {response.status_code}")
import streamlit as st
from PIL import Image
import base64
import requests
from bounding_box_shower import draw_boxes_on_image

# Class mapping
class_id = {
    0: "auto_rickshaw", 1: "bicycle", 2: "bus", 3: "car",
    4: "cart_vehicle", 5: "construction_vehicle", 6: "motorbike",
    7: "person", 8: "priority_vehicle", 9: "three_wheeler",
    10: "train", 11: "truck", 12: "wheelchair"
}

st.title("RoadEye Object Detection Demo")

# Tabs
tab1, tab2 = st.tabs(["Detection", "Class Mapping"])

with tab1:
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Save temporarily
        image = Image.open(uploaded_file)
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path)

        # Call your inference API
        files = {"file": open(temp_image_path, "rb")}
        response = requests.post("http://127.0.0.1:8000/predict", files=files)

        if response.status_code == 200:
            data = response.json()

            # Draw bounding boxes with IDs
            img_with_boxes = draw_boxes_on_image(data)

            # Show result
            st.image(img_with_boxes, caption="Prediction with Bounding Boxes", use_column_width=True)

            # Optionally, show detected IDs
            st.write("Detected IDs:")
            detected_ids = [det["id"] for det in data.get("detections", [])]
            st.write(detected_ids)

        else:
            st.error(f"Inference failed: {response.status_code}")

with tab2:
    st.subheader("Class ID Mapping")
    st.write(class_id)
