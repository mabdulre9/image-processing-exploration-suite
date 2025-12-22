import streamlit as st
import cv2 # Importing OpenCV library
import matplotlib.pyplot as plt # Importing Matploblib library
import numpy as np # Importing NumPy library
import sys


st.set_page_config(page_title="Channels & Histogram")
st.title("Channels & Histogram")

st.warning("⚠️ If your image is not properly loading, make sure that bit depth of image is 8 bits per channel and also if you want to see different channels then make sure you are uploading a colored image which have 3 channels rgb. Some color images have more than 3 channels i.e 4th channel to display transparency. So don't use that.")

demo_img1 = plt.imread("images/mandril_color.tif")
img_file = st.file_uploader("Upload an image",type =["jpg", "png", "tif"], width="stretch")

if img_file is not None:
    img = plt.imread(img_file)
else:
    img = demo_img1
    st.info("Using default demo image. You can also upload your own image.")


img2 = img.copy()

if img.shape[0]>4096 or img.shape[1]>4096:
    st.warning("Please upload an image smaller than 4096x4096.", icon="⚠️")
    sys.exit()

st.subheader("Original Image")
fig1, ax1 = plt.subplots()
ax1.imshow(img, cmap='gray')
ax1.axis("on")
st.pyplot(fig1,width=400)
st.markdown("---")

img_flat = img.flatten()
# Calculate histogram using np.histogram
bins_slider = st.slider("Number of bins for histogram", min_value=2, max_value=256, value = 10)

# Compute histogram
hist, bins = np.histogram(img_flat, bins=bins_slider, range=(0, 255))

# Display histogram
st.subheader("1. Histogram")
fig, ax = plt.subplots(figsize=(6,4))
ax.hist(img_flat, bins=bins_slider, range=(0,255), color='blue', edgecolor='black')
ax.set_title(f"Pixel Distribution (bins={bins_slider})")
ax.set_xlabel("Pixel Intensity")
ax.set_ylabel("Frequency")
st.pyplot(fig)


if len(cv2.split(img2))==3:
    st.write("Sometimes TIFF images may not display correctly due to compatibility issues. If you encounter any problems, please consider converting the image to JPG or PNG format.")
    r_channel, g_channel, b_channel = cv2.split(img)   
    st.markdown("---")
 
    st.subheader("2. Blue Channel")
    fig1, ax1 = plt.subplots()
    ax1.imshow(b_channel, cmap='gray')
    ax1.set_title("Blue Channel")
    ax1.axis("on")
    st.pyplot(fig1,width=400)
    _, buf = cv2.imencode(".png", b_channel)
    st.download_button("Download Image", buf.tobytes(),  file_name="image.png", key="b_channel_download")
    st.markdown("---")

    st.subheader("3. Green Channel")
    fig1, ax1 = plt.subplots()
    ax1.imshow(g_channel, cmap='gray')
    ax1.set_title("Green Channel")
    ax1.axis("on")
    st.pyplot(fig1,width=400)
    _, buf = cv2.imencode(".png", g_channel)
    st.download_button("Download Image", buf.tobytes(),  file_name="image.png", key="g_channel_download")
    st.markdown("---")

    st.subheader("4. Red Channel")
    fig1, ax1 = plt.subplots()
    ax1.imshow(r_channel, cmap='gray')
    ax1.set_title("Red Channel")
    ax1.axis("on")
    st.pyplot(fig1,width=400)
    _, buf = cv2.imencode(".png", r_channel)
    st.download_button("Download Image", buf.tobytes(),  file_name="image.png", key="r_channel_download")
    st.markdown("---")


