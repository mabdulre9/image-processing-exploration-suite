import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Geometric Transformations")
st.title("Geometric Transformations")

# =========================
# Load Default Image
# =========================
default_img_path = "images/Fig0222(b)(cameraman).tif"  # Replace with your default image path

uploaded_file = st.file_uploader(
    "Upload an image (jpg, png, tif) or use default",
    type=["jpg", "jpeg", "png", "tif", "tiff"]
)

if uploaded_file:
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
else:
    img = cv2.imread(default_img_path)
    if img is None:
        st.error("Default image not found. Please upload an image.")
        st.stop()

# Check image size limits
if img.shape[1] > 4096 or img.shape[0] > 4096:
    st.error("Image width and height must not exceed 4096 pixels.")
    st.stop()

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Display original image with axes
fig, ax = plt.subplots()
ax.imshow(img_rgb)
ax.set_title("Original Image")
ax.axis("on")
st.pyplot(fig, width=400)

st.markdown("---")

# =========================
# Scaling
# =========================
st.subheader("1. Scaling")
scale_x = st.slider("Scale X", 0.1, 10.0, 1.0)
scale_y = st.slider("Scale Y", 0.1, 10.0, 1.0)

M_scale = np.array([[scale_x, 0, 0],
                    [0, scale_y, 0]], dtype=np.float32)
scaled_img = cv2.warpAffine(img_rgb, M_scale, (int(img.shape[1]*scale_x), int(img.shape[0]*scale_y)))

fig, ax = plt.subplots()
ax.imshow(scaled_img)
ax.set_title("Scaled Image")
ax.axis("on")
st.pyplot(fig, width=400)
# Download scaled image
_, buffer = cv2.imencode('.png', cv2.cvtColor(scaled_img, cv2.COLOR_RGB2BGR))
st.download_button("Download Image", buffer.tobytes(), file_name="image.png", key="scaled_download")
st.markdown("---")

# =========================
# Translation
# =========================
st.subheader("2. Translation")
tx = st.slider("Translate X (pixels)", -img.shape[1], img.shape[1], 0)
ty = st.slider("Translate Y (pixels)", -img.shape[0], img.shape[0], 0)

M_translate = np.array([[1, 0, tx],
                        [0, 1, ty]], dtype=np.float32)
translated_img = cv2.warpAffine(img_rgb, M_translate, (img.shape[1], img.shape[0]))

fig, ax = plt.subplots()
ax.imshow(translated_img)
ax.set_title("Translated Image")
ax.axis("on")
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', cv2.cvtColor(translated_img, cv2.COLOR_RGB2BGR))
st.download_button("Download Image", buffer.tobytes(), file_name="image.png", key="translated_download")
st.markdown("---")

# =========================
# Shearing
# =========================
st.subheader("3. Shearing")
shear_x = st.slider("Shear X", -1.0, 1.0, 0.0)
shear_y = st.slider("Shear Y", -1.0, 1.0, 0.0)

M_shear = np.array([[1, shear_x, 0],
                    [shear_y, 1, 0]], dtype=np.float32)
sheared_img = cv2.warpAffine(img_rgb, M_shear, (img.shape[1], img.shape[0]))

fig, ax = plt.subplots()
ax.imshow(sheared_img)
ax.set_title("Sheared Image")
ax.axis("on")
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', cv2.cvtColor(sheared_img, cv2.COLOR_RGB2BGR))
st.download_button("Download Image", buffer.tobytes(), file_name="image.png", key="sheared_download")
st.markdown("---")

# =========================
# Rotation
# =========================
st.subheader("4. Rotation")
angle = st.slider("Rotation Angle (degrees)", -180, 180, 0)
center = (img.shape[1]//2, img.shape[0]//2)
M_rot = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated_img = cv2.warpAffine(img_rgb, M_rot, (img.shape[1], img.shape[0]))

fig, ax = plt.subplots()
ax.imshow(rotated_img)
ax.set_title("Rotated Image")
ax.axis("on")
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', cv2.cvtColor(rotated_img, cv2.COLOR_RGB2BGR))
st.download_button("Download Image", buffer.tobytes(), file_name="image.png", key="rotated_download")
