import streamlit as st
import cv2 # Importing OpenCV library
import matplotlib.pyplot as plt # Importing Matploblib library
import numpy as np # Importing NumPy library



st.write("### Resizing & Interpolations")
demo_img1 = plt.imread("images/Fig0222(b)(cameraman).tif").astype(np.float32)
img_file = st.file_uploader("Upload an image",type =["jpg", "png", "tif"], width="stretch")

if img_file is not None:
    img = plt.imread(img_file).astype(np.float32)
else:
    img = demo_img1

st.write("Below are two methods for resizing an image. You can either specify the scaling factors for both axes or directly input the desired dimensions. Additionally, you can choose from three interpolation methods: Nearest Neighbor, Bilinear, and Bicubic.")

if img.shape[0]>1024 or img.shape[1]>1024:
    st.warning("Please upload an image smaller than 1024x1024.", icon="⚠️")
    st.stop()

fig1, ax1 = plt.subplots()
ax1.imshow(img, cmap='gray')
ax1.set_title("Original Image")
ax1.axis("on")
st.pyplot(fig1,width=400)

fx = st.slider("fx (Scale Factor Horizontal Axis)", min_value=0.1, max_value=10.0, value=0.3, width = "stretch")
fy = st.slider("fy (Scale Factor Vertical Axis)", min_value=0.1, max_value=10.0, value=0.3, width = "stretch")
interpolation = st.selectbox("Select Interpolation Method", 
                                ("Nearest Neighbor", "Bilinear", "Bicubic"), width = "stretch")
if interpolation == "Nearest Neighbor":
    interp_method = cv2.INTER_NEAREST
elif interpolation == "Bilinear":
    interp_method = cv2.INTER_LINEAR
else:
    interp_method = cv2.INTER_CUBIC

resized_img = cv2.resize(img, None, fx=fx, fy=fy, interpolation=interp_method)
fig1, ax1 = plt.subplots()
ax1.imshow(resized_img, cmap='gray')
ax1.set_title("Resized Image")
ax1.axis("on")
st.pyplot(fig1,width=400)
_, buf = cv2.imencode(".png", resized_img)
st.download_button("Download Processed Image", buf.tobytes(),  file_name="processed.png", key="scale_download")

width = st.number_input("New Width", min_value=10, max_value=4096, value = 50, width = "stretch")
height = st.number_input("New Height", min_value=10, max_value=4096, value = 50, width = "stretch")
resized_img_dim = cv2.resize(img, (width, height), interpolation=interp_method)
fig1, ax1 = plt.subplots()
ax1.imshow(resized_img_dim, cmap='gray')
ax1.set_title("Resized Image with Specified Dimensions")
ax1.axis("on")
st.pyplot(fig1,width=400)
_, buf = cv2.imencode(".png", resized_img_dim)
st.download_button("Download Processed Image", buf.tobytes(),  file_name="processed.png", key="dim_download")

st.write("### Simultaneuos Downscaling and Upscaling")
st.write("To clearly view the difference between the different interpolation methods, we will first downscale the image by a factor you will specify and then upscale it back to its original size using the selected interpolation method.")
scale_factor = st.slider("Scaling Factor", min_value=1, max_value=50, value=5, width = "stretch")
st.write("Switch between different interpolation methods to see the difference in results.")
interpolation = st.selectbox("Select Interpolation Method", 
                                ("Nearest Neighbor", "Bilinear", "Bicubic"), width = "stretch", key="interp_down_up")
if interpolation == "Nearest Neighbor":
    interp_method = cv2.INTER_NEAREST
elif interpolation == "Bilinear":
    interp_method = cv2.INTER_LINEAR
else:
    interp_method = cv2.INTER_CUBIC
downscaled_img = cv2.resize(img, None, fx=1/scale_factor, fy=1/scale_factor, interpolation=interp_method)
upscaled_img = cv2.resize(downscaled_img, (img.shape[1], img.shape[0]), interpolation=interp_method)
fig1, ax1 = plt.subplots()
ax1.imshow(upscaled_img, cmap='gray')
ax1.set_title("Downscaled and Upscaled back to Original Size")  
ax1.axis("on")
st.pyplot(fig1,width=400)
_, buf = cv2.imencode(".png", upscaled_img)
st.download_button("Download Processed Image", buf.tobytes(),  file_name="processed.png", key="down_up_download")





