import streamlit as st

st.set_page_config(page_title="Reference Materials")
st.title("Reference Materials")
st.warning("Starting download may take upto 5 minutes. Please be patient. Download and **extract the zip files** below to access the lab manuals, images, lecture slides and books used in this course (EE418F).")

pdf_path = "docs/lab_manuals.zip"  # relative or absolute path

with open(pdf_path, "rb") as pdf_file:
    st.download_button(
        label="Download Lab Manuals",
        data=pdf_file,
        file_name="lab_manuals.zip",
        mime="application/zip"
    )

img_path = "docs/images.zip"  # relative or absolute path
with open(img_path, "rb") as img_file:
    st.download_button(
        label="Download Lab Images",
        data=img_file,
        file_name="images.zip",
        mime="application/zip"
    )

img_path = "docs/dip by gonzalez 4th ed.pdf"  # relative or absolute path
with open(img_path, "rb") as img_file:
    st.download_button(
        label="Download Dip by Gonzalez 4th Ed Book",
        data=img_file,
        file_name="dip_by_gonzalez.pdf",
        mime="application/pdf"
    )

img_path = "docs/lecture_slides.zip"  # relative or absolute path
with open(img_path, "rb") as img_file:
    st.download_button(
        label="Download Lecture Slides",
        data=img_file,
        file_name="lecture_slides.zip",
        mime="application/zip"
    )
