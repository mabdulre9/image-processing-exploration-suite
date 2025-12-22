import streamlit as st
import cv2
import numpy as np
from matplotlib import pyplot as plt


st.set_page_config(page_title="Morphological Operations")
st.title("Morphological Operations")

# =========================
# 1. Erosion and Dilation
# =========================
st.subheader("1. Erosion and Dilation")

default_img_ed = "images/Fig0905(a)(wirebond-mask).tif"  # Default image for erosion/dilation
uploaded_file_ed = st.file_uploader(
    "Upload image for Erosion/Dilation (or use default)", 
    type=["jpg","jpeg","png","tif","tiff"], key="ed"
)

if uploaded_file_ed is not None:
    img_ed = plt.imread(uploaded_file_ed)
else:
    img_ed = plt.imread(default_img_ed)
    st.info("Using default demo image. You can also upload your own image.")


fig, ax = plt.subplots()
ax.imshow(img_ed, cmap='gray')
ax.set_title("Original Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)


operation_ed = st.selectbox("Select Operation", ["Erosion", "Dilation"])
se_type_ed = st.selectbox("Select Structuring Element", ["Rectangular","Ellipse","Cross"], key="ed_se")
se_size_ed = st.slider("Structuring Element Size", 1, 100, 37, key="ed_size")
se_dict = {"Rectangular": cv2.MORPH_RECT,"Ellipse": cv2.MORPH_ELLIPSE,"Cross": cv2.MORPH_CROSS}
kernel_ed = cv2.getStructuringElement(se_dict[se_type_ed], (se_size_ed, se_size_ed))

if operation_ed == "Erosion":
    result_ed = cv2.erode(img_ed, kernel_ed)
else:
    result_ed = cv2.dilate(img_ed, kernel_ed)

fig, ax = plt.subplots()
ax.imshow(result_ed, cmap='gray')
ax.set_title("Processed Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)

_, buffer = cv2.imencode('.png', result_ed)
st.download_button(f"Download Image", buffer.tobytes(), file_name=f"{operation_ed.lower()}.png")
# =========================


# =========================
# 2. Opening and Closing
# =========================
st.markdown("---")
st.subheader("2. Opening and Closing")

default_img_oc = "images/Fig0911(a)(noisy_fingerprint).tif"  # Default image for opening/closing
uploaded_file_oc = st.file_uploader(
    "Upload image for Opening/Closing (or use default)", 
    type=["jpg","jpeg","png","tif","tiff"], key="oc"
)
if uploaded_file_oc is not None:
    img_oc = plt.imread(uploaded_file_oc)
else:
    img_oc = plt.imread(default_img_oc)
    st.info("Using default demo image. You can also upload your own image.")

fig, ax = plt.subplots()
ax.imshow(img_oc, cmap='gray')
ax.set_title("Original Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)

op_choice = st.selectbox("Select Operation", ["Opening","Closing"], key="oc_op")
se_type_oc = st.selectbox("Select Structuring Element", ["Rectangular","Ellipse","Cross"], key="oc_se")
se_size_oc = st.slider("Structuring Element Size", 1, 21, 3, key="oc_size")
se_dict = {"Rectangular": cv2.MORPH_RECT,"Ellipse": cv2.MORPH_ELLIPSE,"Cross": cv2.MORPH_CROSS}
kernel_oc = cv2.getStructuringElement(se_dict[se_type_oc], (se_size_oc, se_size_oc))
op_dict = {"Opening": cv2.MORPH_OPEN, "Closing": cv2.MORPH_CLOSE}

morph_img = cv2.morphologyEx(img_oc, op_dict[op_choice], kernel_oc)

fig, ax = plt.subplots()
ax.imshow(morph_img, cmap='gray')
ax.set_title("Processed Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)

_, buffer = cv2.imencode('.png', morph_img)
st.download_button(f"Download Image", buffer.tobytes(), file_name=f"{op_choice.lower()}.png")

# =========================
# =========================


# =========================
# 3. Connected Component Analysis
# =========================
st.markdown("---")
st.subheader("3. Connected Component Analysis")

default_img_cc = "images/Fig0918(a)(Chickenfilet with bones).tif"  # Default image for connected components
uploaded_file_cc = st.file_uploader(
    "Upload image for Connected Components (or use default)", 
    type=["jpg","jpeg","png","tif","tiff"], key="cc"
)
if uploaded_file_cc is not None:
    img_cc = plt.imread(uploaded_file_cc)
    if img_cc.ndim == 3:
        img_cc = cv2.cvtColor(img_cc, cv2.COLOR_RGB2GRAY)
else:
    img_cc = plt.imread(default_img_cc)
    st.info("Using default demo image. You can also upload your own image.")

fig, ax = plt.subplots()
ax.imshow(img_cc, cmap='gray')
ax.set_title("Original Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)
# Convert to binary

thresh_val = st.slider("Threshold Value", 0, 255, 200, key="cc_thresh")
_, binary_cc = cv2.threshold(img_cc, thresh_val, 255, cv2.THRESH_BINARY)


num_labels, labels_im = cv2.connectedComponents(binary_cc)
st.write(f"Total number of objects detected: {num_labels - 1}")  # subtract background

retain_n = st.slider("Retain Top N Largest Objects", 1, max(1, num_labels-1), 3, key="cc_retain")

# 1. Calculate the size (area) of every object found
object_areas = []
for i in range(1, num_labels):
    size = np.sum(labels_im == i)
    object_areas.append(size)

# 2. Find the indices of the largest N objects
# np.argsort returns indices from smallest to largest; [-retain_n:] takes the end of that list
largest_indices = np.argsort(object_areas)[-retain_n:]

# 3. Create a blank canvas and "paint" the chosen objects onto it
largest_img = np.zeros_like(binary_cc)

for idx in largest_indices:
    # We add 1 because our object_areas list started at label 1 (index 0)
    actual_label_value = idx + 1
    largest_img[labels_im == actual_label_value] = 255
    

fig, ax = plt.subplots()
ax.imshow(largest_img, cmap='gray')
ax.set_title("Processed Image")
ax.axis("on")  # Show axes
st.pyplot(fig, width=400)

_, buffer = cv2.imencode('.png', largest_img)
st.download_button("Download Image", buffer.tobytes(), file_name="top_objects.png")

