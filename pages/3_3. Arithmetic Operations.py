import streamlit as st
import cv2 # Importing OpenCV library
import matplotlib.pyplot as plt # Importing Matploblib library
import numpy as np # Importing NumPy library
import sys


st.set_page_config(page_title="Arithmetic Operations I")
st.title("Arithmetic Operations Ⅰ")

st.write("This section allows you to perform basic arithmetic operations (Addition, Subtraction, Multiplication, and Division) **between your uploaded image and the low-level of detail version of the same image**.")
st.warning("There are two sections in this page. The first section allows you to perform arithmetic operations between an image and its low level of detail version. The second section allows more flexibility to perform arithmetic operations between two user uploaded images.")
demo_img1 = plt.imread("images/lena_gray_256.tif")
img_file = st.file_uploader("Upload an image",type =["jpg", "png", "tif"], width="stretch")

if img_file is not None:
    img = plt.imread(img_file)
else:
    img = demo_img1
    st.info("Using default demo image. You can also upload your own image.")


if img.shape[0]>4096 or img.shape[1]>4096:
    st.warning("Please upload an image smaller than 4096x4096.", icon="⚠️")
    st.stop()

st.subheader("Original Image")
fig1, ax1 = plt.subplots()
ax1.imshow(img, cmap='gray')
ax1.axis("on")
st.pyplot(fig1,width=400)
st.markdown("---")

st.subheader("Same Image with Low Level of Detail")

size = st.slider(
    "The low level of detail image is created by applying a box filter of kernel size below to the original image.", 
    min_value=1,   # Changed from 0 to 1
    max_value=100, 
    value=3,       # Set a default starting value that isn't 0
    key="info_slider"
)

result_ed = cv2.blur(img, (size,size))
fig1, ax1 = plt.subplots()
ax1.imshow(result_ed, cmap='gray')
ax1.axis("on")
st.pyplot(fig1,width=400)

_, buf = cv2.imencode(".png", result_ed)
st.download_button("Download Image", buf.tobytes(),  file_name="image.png", key="download")


st.write("### Select Arithmetic Operation")
operation = st.selectbox("Select Operation",
                                ("Subtraction","Addition","Multiplication", "Division"), width = "stretch")
if operation == "Addition":
    result_img = cv2.add(img.astype(np.float32), result_ed.astype(np.float32))
elif operation == "Subtraction":
    result_img = cv2.subtract(img.astype(np.float32), result_ed.astype(np.float32))
elif operation == "Multiplication":
    result_img = cv2.multiply(img.astype(np.float32), result_ed.astype(np.float32))
else:
    result_img = cv2.divide(img.astype(np.float32), result_ed.astype(np.float32)+1e-5) # Adding small value to avoid division by zero
fig1, ax1 = plt.subplots()
ax1.imshow(result_img, cmap='gray')
ax1.set_title(f"Result of {operation}")
ax1.axis("on")
st.pyplot(fig1,width=400)
_, buf = cv2.imencode(".png", result_img)
st.download_button("Download Image", buf.tobytes(),  file_name="image.png", key="arithmetic_download")

st.markdown("---")

st.title("Arithmetic Operations ⅠⅠ")

st.error("This section is under development and highly prone to errors. Use at your own risk!", icon="⚠️")
st.warning("This section allows you to perform basic arithmetic operations (Addition, Subtraction, Multiplication, and Division) between two images. It works only if both images are of the same dimensions and both have same number and type of channels. Also this requires that both images must be in float. So be careful while uploading images.")

# --------------------------------------------------
# Load demo images FIRST
# --------------------------------------------------
demo_img4 = plt.imread("images/Fig0229(a)(tungsten_filament_shaded).tif")
demo_img5 = plt.imread("images/Fig0229(b)(tungsten_sensor_shading).tif")

# --------------------------------------------------
# Uploaders (DO NOT overwrite images)
# --------------------------------------------------
img4_file = st.file_uploader(
    "Upload first image", type=["jpg", "png", "tif"]
)

# --------------------------------------------------
# Decide which images to use
# --------------------------------------------------
if img4_file is not None:
    img4 = plt.imread(img4_file)

else:
    img4 = demo_img4
    st.info("Using default demo image. You can also upload your own image.")

img5_file = st.file_uploader(
    "Upload second image", type=["jpg", "png", "tif"]
)

if img5_file is not None:
    img5 = plt.imread(img5_file)

else:
    img5 = demo_img5
    st.info("Using default demo image. You can also upload your own image.")


# --------------------------------------------------
# Validation
# --------------------------------------------------
if img4.shape != img5.shape:
    st.error("Images must have the same dimensions.")
    st.stop()

if img4.shape[0] > 4096 or img4.shape[1] > 4096 or img5.shape[0] > 4096 or img5.shape[1] > 4096:
    st.warning("Image must be smaller than 4096x4096.", icon="⚠️")
    st.stop()

if img4.ndim != img5.ndim:
    st.error("Both images must have the same number of channels.")
    st.stop()


# --------------------------------------------------
# Display inputs
# --------------------------------------------------

fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()
ax1.imshow(img4, cmap='gray')
ax1.set_title("First Image")
ax1.axis("on")
st.pyplot(fig1,width=400)

fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()
ax1.imshow(img5, cmap='gray')
ax1.set_title("Second Image")
ax1.axis("on")
st.pyplot(fig1,width=400)

# --------------------------------------------------
# Operation selection (always visible)
# --------------------------------------------------
operation = st.selectbox(
    "Select Operation",
    ("Division","Subtraction", "Multiplication", "Addition")
)

if operation == "Addition":
    result_img = cv2.add(img4.astype(np.float32), img5.astype(np.float32))
elif operation == "Subtraction":
    result_img = cv2.subtract(img4.astype(np.float32), img5.astype(np.float32))
elif operation == "Multiplication":
    result_img = cv2.multiply(img4.astype(np.float32), img5.astype(np.float32))
else:
    result_img = cv2.divide(img4.astype(np.float32), img5.astype(np.float32) + 1e-5)

# --------------------------------------------------
# Show result
# --------------------------------------------------
fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()
ax1.imshow(result_img, cmap='gray')
ax1.set_title("Result of " + operation)
ax1.axis("on")
st.pyplot(fig1,width=400)

result_to_save = cv2.normalize(
    result_img, None, 0, 255, cv2.NORM_MINMAX
)
result_to_save = result_to_save.astype(np.uint8)

_, buf = cv2.imencode(".png", result_to_save)
st.download_button("Download Image", buf.tobytes(),  file_name="image.png", key="arithmetic_download6")

