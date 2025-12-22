import streamlit as st
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Color Space Conversions")
st.title("Color Space Conversions & Thresholding")

uploaded_file = st.file_uploader("Upload an image (jpg, png, tif)", type=["jpg", "jpeg", "png", "tif", "tiff"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
else:
    default_path = "images/mandril_color.tif"  # Change to your local image path
    if os.path.exists(default_path):
        img_bgr = cv2.imread(default_path)
        st.info("Using default demo image. You can also upload your own image.")
    else:
        st.error("No image uploaded and default image not found.")
        st.stop()

if img_bgr is None:
    st.error("Invalid image file.")
    st.stop()

img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# =========================
# Display Original Image with Axes
# =========================
st.subheader("Original Image (RGB)")

fig, ax = plt.subplots()
ax.imshow(img_rgb)
ax.set_title("Original Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)
st.markdown("---")

# =========================
# Select Operation
# =========================
operation = st.selectbox(
    "Select Operation",
    (
        "RGB → Grayscale",
        "BGR → RGB",
        "RGB → BGR",
        "RGB → Binary (Manual Threshold)",
        "RGB → Binary (Otsu)"
    )
)

# =========================
# Processing
# =========================
result = None

if operation == "RGB → Grayscale":
    result = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

elif operation == "BGR → RGB":
    result = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

elif operation == "RGB → BGR":
    result = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

elif operation == "RGB → Binary (Manual Threshold)":
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    thresh = st.slider("Threshold Value", 0, 255, 128)
    _, result = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)

elif operation == "RGB → Binary (Otsu)":
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    _, result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# =========================
# Display Result with Axes
# =========================
st.subheader("Processed Image")

fig2, ax2 = plt.subplots(figsize=(6, 6))
if len(result.shape) == 2:
    ax2.imshow(result, cmap='gray', vmin=0, vmax=255)
else:
    ax2.imshow(result)
ax2.set_title("Processed Image")
ax2.axis("on")
st.pyplot(fig2, width=400)

# =========================
# Download Section
# =========================

_, buffer = cv2.imencode('.png', result)
st.download_button(f"Download Image", buffer.tobytes(), file_name=f"image.png")
# =========================
