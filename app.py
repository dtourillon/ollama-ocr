from PIL import Image

import streamlit as st

from models.anthropic import extract_text as anthropic_extract_text
from models.ollama import extract_text as ollama_extract_text
from models.openai import extract_text as openai_extract_text


# Page configuration
st.set_page_config(
    page_title="Llama OCR",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.title("🦙 Llama OCR DOM")

# Add clear button to top right
col1, col2 = st.columns([6,1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract structured text from images!</p>', unsafe_allow_html=True)
st.markdown("---")

# Move upload controls to sidebar
with st.sidebar:
    selected_llm_povider = st.selectbox(
        'Which LLM provider should we use?',
        ["ollama", "openai", "anthropic"],
    )
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner(f"Processing image with {selected_llm_povider}..."):
                try:
                    if selected_llm_povider == "ollama":
                        st.session_state['ocr_result'] = ollama_extract_text(uploaded_file)
                    elif selected_llm_povider == "openai":
                        st.session_state['ocr_result'] = openai_extract_text(uploaded_file)
                    elif selected_llm_povider == "anthropic":
                        st.session_state['ocr_result'] = anthropic_extract_text(uploaded_file
                        )
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Llama Vision Model2")
