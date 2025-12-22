import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Resizing & Interpolations")
st.title("Resizing & Interpolations")

demo_img = cv2.imread("images/Fig0222(b)(cameraman).tif",cv2.IMREAD_GRAYSCALE)

if demo_img is None:
    st.error("Demo image not found.")
    st.stop()

img_file = st.file_uploader( "Upload an image (jpg, png, tif)", type=["jpg", "png", "tif"])

if img_file:
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
else:
    img = demo_img.copy()
    st.info("Using default demo image. You can also upload your own image.")

h, w = img.shape[:2]
if h > 4096 or w > 4096:
    st.warning("Please upload an image smaller than 4096 × 4096.", icon="⚠️")
    st.stop()

st.subheader("Original Image")

fig, ax = plt.subplots()
if img.ndim == 2:
    ax.imshow(img, cmap="gray")
else:
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

ax.axis("on")
st.pyplot(fig, width=400)
st.markdown("---")

st.subheader("1. Resize Using Scale Factors")

interpolation = st.selectbox("Select Interpolation Method", ("Nearest Neighbor", "Bilinear", "Bicubic"), width = "stretch", key="interp_method")
if interpolation == "Nearest Neighbor":
    interp_method = cv2.INTER_NEAREST
elif interpolation == "Bilinear":
    interp_method = cv2.INTER_LINEAR
else:
    interp_method = cv2.INTER_CUBIC

fx = st.slider("fx (Horizontal Scale Factor)", 0.1, 10.0, 0.3)
fy = st.slider("fy (Vertical Scale Factor)", 0.1, 10.0, 0.3)

resized_scale = cv2.resize( img, None, fx=fx, fy=fy, interpolation=interp_method)

fig, ax = plt.subplots()
if resized_scale.ndim == 2:
    ax.imshow(resized_scale, cmap="gray")
else:
    ax.imshow(cv2.cvtColor(resized_scale, cv2.COLOR_BGR2RGB))

ax.set_title("Resized Image (Scale Factors)")
ax.axis("on")
st.pyplot(fig, width=400)

_, buf = cv2.imencode(".png", resized_scale)
st.download_button("Download Image", buf.tobytes(), file_name=f"resized_image.png",key="scale_download")
st.markdown("---")

st.subheader("2. Resize Using Explicit Dimensions")

new_width = st.number_input("New Width", 10, 4096, 64)
new_height = st.number_input("New Height", 10, 4096, 64)
interpolation = st.selectbox("Select Interpolation Method", ("Nearest Neighbor", "Bilinear", "Bicubic"), width = "stretch", key="dim_interp")

if interpolation == "Nearest Neighbor":
    interp_method = cv2.INTER_NEAREST
elif interpolation == "Bilinear":
    interp_method = cv2.INTER_LINEAR
else:
    interp_method = cv2.INTER_CUBIC

resized_dim = cv2.resize( img, (int(new_width), int(new_height)), interpolation=interp_method)

fig, ax = plt.subplots()
if resized_dim.ndim == 2:
    ax.imshow(resized_dim, cmap="gray")
else:
    ax.imshow(cv2.cvtColor(resized_dim, cv2.COLOR_BGR2RGB))

ax.set_title("Resized Image (Width × Height)")
ax.axis("on")
st.pyplot(fig, width=400)

_, buf = cv2.imencode(".png", resized_dim)
st.download_button( "Download Image", buf.tobytes(), file_name=f"resized_{new_width}x{new_height}.png", key="dim_download")
st.markdown("---")

st.subheader("3. Simultaneous Downscaling and Upscaling")

interpolation = st.selectbox("Select Interpolation Method", 
                                ("Nearest Neighbor", "Bilinear", "Bicubic"), width = "stretch", key="down_up_interp")
if interpolation == "Nearest Neighbor":
    interp_method = cv2.INTER_NEAREST
elif interpolation == "Bilinear":
    interp_method = cv2.INTER_LINEAR
else:
    interp_method = cv2.INTER_CUBIC

scale_factor = st.slider("Scaling Factor", 1, 50, 4)

downscaled = cv2.resize( img, None, fx=1 / scale_factor, fy=1 / scale_factor, interpolation=interp_method)
upscaled = cv2.resize(downscaled, (w, h), interpolation=interp_method)

fig, ax = plt.subplots()
if upscaled.ndim == 2:
    ax.imshow(upscaled, cmap="gray")
else:
    ax.imshow(cv2.cvtColor(upscaled, cv2.COLOR_BGR2RGB))

ax.set_title("Downscaled then Upscaled Image")
ax.axis("on")
st.pyplot(fig, width=400)

_, buf = cv2.imencode(".png", upscaled)
st.download_button("Download Image", buf.tobytes(), file_name="down_up_interpolation.png",key="down_up_download")
