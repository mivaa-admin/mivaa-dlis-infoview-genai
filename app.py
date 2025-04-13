import streamlit as st
from dlisio import dlis
import tempfile
import base64
import info
import data
import export

# 💡 Page setup
st.set_page_config(layout="wide", page_title='DLIS InfoView')

# 📷 Load and encode QR code (optional placeholder — not used)
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# 📤 Load DLIS file
def dlis_load(uploaded_file):
    if uploaded_file is not None:
        st.session_state.uploaded_file_name = uploaded_file.name
        try:
            # Save the uploaded file as a temporary file to get the path
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read())  # Read the uploaded file content
                tmp_file_path = tmp_file.name  # Get the temporary file path

            # Now pass the file path to dlis.load
            dlis_file = dlis.load(tmp_file_path)  # This should work correctly

            if dlis_file:
                st.sidebar.success('✅ File Loaded Successfully!')
                st.sidebar.markdown(f"**📄 File Name:** `{uploaded_file.name}`")
                st.sidebar.write(f"🧱 Number of Logical Files: {len(dlis_file)}")
            else:
                st.sidebar.error('❌ Failed to load DLIS file.')

            return dlis_file  # Return the loaded DLIS file
        except Exception as e:
            st.error(f"Error preprocessing the DLIS file: {e}")
            return None
    else:
        st.sidebar.info("📂 Please select a DLIS file.")
        return None

# 🏠 Welcome page
def home_page():
    st.markdown("<h1 style='text-align:center; color:#2c3e50;'>📘 DLIS InfoView</h1>", unsafe_allow_html=True)
    st.markdown("### 🔍 Explore & Export Well Log Data from DLIS Files", unsafe_allow_html=True)

    st.markdown(""" **DLIS InfoView** is a modern, interactive application to inspect and visualize DLIS files used in well logging. Built for geoscientists and data specialists working with subsurface data.""")

    st.markdown("### ✨ What You Can Do:")
    st.markdown("""
    - 📁 Upload and parse DLIS files  
    - 🔍 View metadata, frames, and log channels  
    - 📈 Visualize curves with track layout  
    - 💾 Export selected logs to LAS format
    """)

    st.markdown("---")
    st.markdown("Made with ❤️ using [Streamlit](https://streamlit.io) and [dlisio](https://github.com/equinor/dlisio)")

# 🧭 Sidebar
st.sidebar.title('📁 DLIS InfoView')
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    '📤 Upload a DLIS File',
    type=['.dlis'],
    help='DLIS File is a binary file format for well logs, developed by Schlumberger in the late 80s and published by the American Petroleum Institute (API) in 1991.'
)

# ⬇️ Load file
if uploaded_file:
    dlis_file = dlis_load(uploaded_file)
else:
    dlis_file = None

st.sidebar.markdown("---")
st.sidebar.title("📌 Menu")
options = st.sidebar.radio('Select a page:', options=[
    'Home', 'General Information', 'Data Visualization', 'Export'
])

# 🧭 Navigation
if options == 'Home':
    home_page()
elif dlis_file:
    if options == 'General Information':
        info.info(dlis_file)
    elif options == 'Data Visualization':
        data.data(dlis_file)
    elif options == 'Export':
        export.export()
else:
    if options != 'Home':
        st.warning("⚠️ Please upload a DLIS file to proceed.")
