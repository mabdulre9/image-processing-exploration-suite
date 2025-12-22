import streamlit as st

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Image Processing Exploration Suite",
    layout="centered"
)

# =========================
# Retro CSS (Adjusted)
# =========================
st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background-color: #ECE9DF;
        
        font-family: "Times New Roman", serif;
    }

    /* Push main container DOWN to avoid top bar overlap */
    .block-container {
        margin-top: 100px;
        border: 4px double black;
        padding: 30px;
        background-color: #FFFFFF;
        max-width: 900px;
    }

    /* Title styling */
    h1 {
        text-align: center;
        font-size: 36px;
        text-transform: uppercase;
        border-bottom: 2px solid black;
        padding-bottom: 10px;
    }

    /* Subheader */
    h3 {
        text-align: center;
        font-size: 18px;
        font-weight: normal;
    }

    /* Text blocks */
    p, div {
        font-size: 16px;
        line-height: 1.6;
    }

    /* Footer */
    .retro-footer {
        text-align: center;
        font-size: 12px;
        margin-top: 40px;
        border-top: 1px solid black;
        padding-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Content (UNCHANGED)
# =========================
st.title("IMAGE PROCESSING EXPLORATION SUITE")

st.subheader(
    "EE-418F | Digital Image Processing Lab | Instructor: Dr. Junaid Mir")

st.text(
    "This web app allows users to perform various image processing tasks and provides an interactive interface to visualize the effects of these operations on the uploaded image.")

st.write(
    "**Click on the sidebar** to navigate to different image processing techniques including Resizing & Interpolations, Channels and Histogram, Arithmetic Operations, Geometric Transformations, Spatial Filtering, Edge Detection, Convolution, Morphological Operations, and Color Space Conversions.")


# =========================
# Retro Footer
# =========================

st.markdown(
    """
    <div class="retro-footer">
        © 2022–2026 Image Processing Exploration Suite<br>
        Electrical Engineering Department,
        University of Engineering and Technology (UET), Taxila<br>
        Developed by Muhammad Abdul Rehman (22-EE-040)<br>
        
    </div>
    """,
    unsafe_allow_html=True
)
