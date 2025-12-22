import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(page_title="Intensity Transformations")
st.title("Intensity Transformations")
st.write("This section allows you to perform various intensity transformations on an image, including Negative, Logarithmic, and Power-Law (Gamma) transformations.")
st.warning(" This section works properly only on grayscale images. If you upload a colored image, it will be converted to grayscale automatically.", icon="⚠️")

demo_img1 = plt.imread("images/lena_gray_256.tif")
img_file = st.file_uploader("Upload an image",type =["jpg", "png", "tif"], width="stretch")


if img_file is not None:
    img = plt.imread(img_file)
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
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


# Negative transformation
st.subheader("1. Negative Image")
neg_img = 255 - img
fig, ax = plt.subplots()
ax.imshow(neg_img, cmap='gray')
ax.set_title("Negative Image")
ax.axis("on")
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', neg_img)
st.download_button("Download Image", buffer.tobytes(), file_name="image.png",key="neg_download")

st.markdown("---")

# Logarithmic transformation
st.subheader("2. Logarithmic Transformation")
c = 255 / np.log(1 + np.max(img))
log_img = c * (np.log(1 + img.astype(np.float32)))
fig, ax = plt.subplots()
ax.imshow(log_img, cmap='gray')
ax.axis("on")
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', log_img)
st.download_button("Download Image", buffer.tobytes(), file_name="image.png", key="log_download")

st.markdown("---")

# Inverse Logarithmic transformation
st.subheader("3. Inverse Logarithmic Transformation")
c_inv = 255 / np.log(1 + np.max(img))
inv_log_img = np.exp(img.astype(np.float32) / c_inv) - 1
fig, ax = plt.subplots()
ax.imshow(inv_log_img, cmap='gray')
ax.axis("on")
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', inv_log_img)
st.download_button("Download Image", buffer.tobytes(), file_name="image.png", key="inv_log_download")

st.markdown("---")

# Power-Law (Gamma) transformation
st.subheader("4. Power-Law (Gamma) Transformation")
gamma = st.slider("Select Gamma Y Value", 0.1, 10.0, 1.0)
c_gamma = 1
power_law_img = c_gamma * (img.astype(np.float32) ** gamma)
fig, ax = plt.subplots()
ax.imshow(power_law_img, cmap='gray')
ax.axis("on")
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', power_law_img)
st.download_button("Download Image", buffer.tobytes(), file_name="image.png", key="power_law_download")

st.markdown("---")

# Fourier Transform
st.subheader("5. Fourier Transform")
st.write("This section first computes fft of image then shifts the zero-frequency component to the center and finally computes the magnitude spectrum and displays it.")
f_transform = np.fft.fft2(img)
f_shift = np.fft.fftshift(f_transform)
magnitude_spectrum = 20 * np.log(np.abs(f_shift) + 1)
fig, ax = plt.subplots()
ax.imshow(magnitude_spectrum, cmap='gray')
ax.set_title("Magnitude Spectrum")
ax.axis("on")
st.pyplot(fig, width=400)
_, buffer = cv2.imencode('.png', magnitude_spectrum)
st.download_button("Download Image", buffer.tobytes(), file_name="image.png", key="fourier_download")

