import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Spatial Filtering")
st.title("Spatial Filtering")

demo_img1 = plt.imread("images/Fig0333(a)(test_pattern_blurring_orig).tif")
demo_img2 = plt.imread("images/Fig0335(a)(ckt_board_saltpep_prob_pt05).tif")
demo_img3 = plt.imread("images/Task1Fig1.jpg")
demo_img4 = plt.imread("images/Fig0338(a)(blurry_moon).tif")


st.subheader("1. Box and Gaussian Filtering")
uploaded_file_ed = st.file_uploader(
    "Upload image for Box/Gaussian filtering (or use default)", 
    type=["jpg","jpeg","png","tif","tiff"], key="ed"
)

if uploaded_file_ed is not None:
    img_ed = plt.imread(uploaded_file_ed)
else:
    img_ed = demo_img1
    st.info("Using default demo image. You can also upload your own image.")


fig, ax = plt.subplots()
ax.imshow(img_ed, cmap='gray')
ax.set_title("Original Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)

filter_type = st.selectbox("Select Filter Type", ["Box Filter", "Gaussian Filter"], key="filter_type")
filter_size = st.slider("Filter Size", 1, 100, 25, key="filter_size")

if filter_type == "Box Filter":
    result_ed = cv2.blur(img_ed, (filter_size, filter_size))
else:
    result_ed = cv2.GaussianBlur(img_ed, (filter_size, filter_size), 0)

fig, ax = plt.subplots()
ax.imshow(result_ed, cmap='gray')
ax.set_title("Filtered Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)

# Convert from RGB (what streamlit/plt uses) to BGR (what cv2 expects for saving)
result_bgr = cv2.cvtColor(result_ed, cv2.COLOR_RGB2BGR)

# Encode the BGR version
_, buffer = cv2.imencode('.png', result_bgr)

st.download_button(
    label="Download Image",
    data=buffer.tobytes(),
    file_name="image.png",
    mime="image/png"
)
# =========================

st.markdown("---")
st.subheader("2. Median Filtering")
uploaded_file_med = st.file_uploader(
    "Upload image for Median filtering (or use default)", 
    type=["jpg","jpeg","png","tif","tiff"], key="med"
)

if uploaded_file_med is not None:
    img_med = plt.imread(uploaded_file_med)
else:
    img_med = demo_img2
    st.info("Using default demo image. You can also upload your own image.")

fig, ax = plt.subplots()
ax.imshow(img_med, cmap='gray')
ax.set_title("Original Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)

median_filter_size = st.slider("Median Filter Size", 1, 99, 3, step=2, key="median_filter_size")

result_med = cv2.medianBlur(img_med, median_filter_size)

fig, ax = plt.subplots()
ax.imshow(result_med, cmap='gray')
ax.set_title("Filtered Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)

# Convert from RGB (what streamlit/plt uses) to BGR (what cv2 expects for saving)
result_bgr = cv2.cvtColor(result_med, cv2.COLOR_RGB2BGR)

# Encode the BGR version
_, buffer = cv2.imencode('.png', result_bgr)

st.download_button(
    label="Download Image",
    data=buffer.tobytes(),
    file_name="image.png",
    mime="image/png",
    key="download_med"
)

# =========================
# Edge Detection
# =========================

# =========================
st.markdown("---")
st.subheader("3. Edge Detection / Derivative Filtering")
st.warning("Edge Detection works on grayscale images. If you upload a colored image, it will be converted to grayscale automatically.")

uploaded_file_der = st.file_uploader(
    "Upload image for derivative filtering", 
    type=["jpg","jpeg","png","tif","tiff"], key="der"
)

if uploaded_file_der is not None:
    img_der = plt.imread(uploaded_file_der)
else:
    img_der = demo_img3
    st.info("Using default demo image.")

# Convert to grayscale if needed
if img_der.ndim == 3:
    img_der = cv2.cvtColor(img_der, cv2.COLOR_RGB2GRAY)

fig, ax = plt.subplots()
ax.imshow(img_der, cmap='gray')
ax.set_title("Original Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)


w_x_fod = np.array([[0,0,0],[0,-1,1],[0,0,0]])
w_y_fod = np.array([[0,0,0],[0,-1,0],[0,1,0]])
w_both_fod = np.array([[0,1,0],[1,-4,1],[0,1,0]])

w_x_sod = np.array([[0,0,0],[1,-2,1],[0,0,0]])
w_y_sod = np.array([[0,1,0],[0,-2,0],[0,1,0]])
w_both_sod = np.array([[0,1,0],[1,-4,1],[0,1,0]])

derivative_type = st.selectbox("Select Derivative Type", ["First Order Derivative (FOD)", "Second Order Derivative (SOD)"], key="derivative_type")
direction = st.selectbox("Select Direction", ["X Direction", "Y Direction", "Both Directions/Laplacian"], key="direction")
if derivative_type == "First Order Derivative (FOD)":
    if direction == "X Direction":
        kernel = w_x_fod
    elif direction == "Y Direction":
        kernel = w_y_fod
    else:
        kernel = w_both_fod

else:
    if direction == "X Direction":
        kernel = w_x_sod
    elif direction == "Y Direction":
        kernel = w_y_sod
    else:
        kernel = w_both_sod

result_der = cv2.filter2D(img_der, -1, kernel)
fig, ax = plt.subplots()
ax.imshow(result_der, cmap='gray')
ax.set_title("Filtered Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', result_der)
st.download_button(f"Download Image", buffer.tobytes(), file_name=f"image.png", key="download_der")
st.markdown("---")

# =========================
# Unsharp Masking / High Boost Filtering
# =========================


st.subheader("4. Unsharp Masking / High Boost Filtering")

uploaded_file_sharp = st.file_uploader(
    "Upload image for Unsharp Masking / Sharpening", 
    type=["jpg","jpeg","png","tif","tiff"], key="sharp"
)
if uploaded_file_sharp is not None:
    img_sharp = plt.imread(uploaded_file_sharp)
    if img_sharp.ndim == 3:
        img_sharp = cv2.cvtColor(img_sharp, cv2.COLOR_RGB2GRAY)

else:
    img_sharp = demo_img4
    st.info("Using default demo image. You can also upload your own image.")

st.info("Guassian blur will used to create the blurred version of the image for unsharp masking. Filter size and sharpening amount can be adjusted. Filter size is of Guassian blur and sharpening amount is the multiplier for the mask (High Boost Filtering).")

fig, ax = plt.subplots()
ax.imshow(img_sharp, cmap='gray')
ax.set_title("Original Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', img_sharp)
st.download_button(f"Download Image", buffer.tobytes(), file_name=f"image.png", key="download_der1")

filter_size = st.slider("Filter Size for guassian blurring", 1, 49, 3, step=2, key="filter_size,key=sharp")
blurred_img = cv2.GaussianBlur(img_sharp, (filter_size, filter_size), 0)
fig, ax = plt.subplots()
ax.imshow(blurred_img, cmap='gray')
ax.set_title("Blurred Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', blurred_img)
st.download_button(f"Download Image", buffer.tobytes(), file_name=f"image.png", key="download_der2")


mask = img_sharp - blurred_img
fig, ax = plt.subplots()
ax.imshow(mask, cmap='gray')
ax.set_title("Mask (Original - Blurred)")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', mask)
st.download_button(f"Download Image", buffer.tobytes(), file_name=f"image.png", key="download_der3")

sharpening_amount = st.slider("Sharpening Amount 'A'", 0.0, 10.0, 1.0, step=0.1, key="sharpening_amount")
sharpened_img = img_sharp + sharpening_amount * mask

st.write("#### Sharpened Image = Original + A x (Original - Blurred)")
fig, ax = plt.subplots()
ax.imshow(sharpened_img, cmap='gray')
ax.set_title("Sharpened Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', sharpened_img)
st.download_button(f"Download Image", buffer.tobytes(), file_name=f"image.png", key="download_sharp")