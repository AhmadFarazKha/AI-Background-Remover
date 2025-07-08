import streamlit as st
from PIL import Image
import io
from src.core.background_processor import remove_background, change_background
from src.utils.file_handler import create_directories_if_not_exist # For consistency

# Ensure data directory exists if you plan to save anything locally
create_directories_if_not_exist("data")

# --- Streamlit Session State Initialization ---
if 'uploaded_image_bytes' not in st.session_state:
    st.session_state.uploaded_image_bytes = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'background_option' not in st.session_state:
    st.session_state.background_option = 'color' # 'color' or 'image'
if 'selected_color' not in st.session_state:
    st.session_state.selected_color = '#007bff' # Default blue
if 'uploaded_background_image_bytes' not in st.session_state:
    st.session_state.uploaded_background_image_bytes = None
if 'show_processed_image' not in st.session_state:
    st.session_state.show_processed_image = False


# --- Page Configuration (Theme controlled by .streamlit/config.toml) ---
st.set_page_config(
    page_title="AI Background Remover",
    page_icon="✂️", # Scissor emoji
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for visual polish (if needed beyond config.toml) ---
# This can be used for very specific styling not covered by config.toml
st.markdown("""
<style>
/* Adjust Streamlit's default padding for a tighter look if desired */
.st-emotion-cache-z5fcl4 { 
    padding-top: 2rem;
    padding-bottom: 2rem;
}
/* Ensure columns have equal height if necessary, typically for side-by-side elements */
div[data-testid="stColumns"] > div > div {
    display: flex;
    flex-direction: column;
}
</style>
""", unsafe_allow_html=True)


# --- Application Content ---
st.title("✂️ AI Image Background Remover")
st.markdown("<p style='text-align: center; color: #f0f0f0; font-size: 1.1rem; margin-bottom: 2rem;'>Upload an image, remove its background, and replace it with a color or another image using AI!</p>", unsafe_allow_html=True)

col_main_l, col_main_center, col_main_r = st.columns([1, 4, 1])

with col_main_center:
    st.markdown("### 1. Upload Your Image")
    uploaded_file = st.file_uploader(
        "Choose a high-quality image of an object or person.",
        type=["jpg", "jpeg", "png"],
        key="main_image_uploader"
    )

    if uploaded_file is not None:
        st.session_state.uploaded_image_bytes = uploaded_file.getvalue()
        st.session_state.processed_image = None # Reset processed image
        st.session_state.show_processed_image = False
        st.success("Image uploaded successfully! Now configure the background.")
        st.image(st.session_state.uploaded_image_bytes, caption='Original Image', use_column_width=True)
    elif st.session_state.uploaded_image_bytes is not None:
        st.image(st.session_state.uploaded_image_bytes, caption='Original Image', use_column_width=True)
        st.info("Upload a new image or proceed with the current one.")
    else:
        st.info("Please upload an image to get started.")

    st.markdown("---")

    st.markdown("### 2. Choose New Background")
    bg_option_cols = st.columns(2)
    with bg_option_cols[0]:
        if st.button("Solid Color Background 🎨", key='btn_color_bg', use_container_width=True):
            st.session_state.background_option = 'color'
            st.session_state.uploaded_background_image_bytes = None # Clear image if switching
            st.rerun()
    with bg_option_cols[1]:
        if st.button("Image Background 🖼️", key='btn_image_bg', use_container_width=True):
            st.session_state.background_option = 'image'
            st.rerun()

    if st.session_state.background_option == 'color':
        st.session_state.selected_color = st.color_picker(
            "Pick a background color:",
            value=st.session_state.selected_color,
            key="color_picker"
        )
    else: # st.session_state.background_option == 'image'
        uploaded_bg_file = st.file_uploader(
            "Upload a background image (JPG, PNG).",
            type=["jpg", "jpeg", "png"],
            key="bg_image_uploader"
        )
        if uploaded_bg_file is not None:
            st.session_state.uploaded_background_image_bytes = uploaded_bg_file.getvalue()
            st.success("Background image uploaded!")
            st.image(st.session_state.uploaded_background_image_bytes, caption='New Background', use_column_width=True)
        elif st.session_state.uploaded_background_image_bytes is not None:
             st.image(st.session_state.uploaded_background_image_bytes, caption='Current Background', use_column_width=True)
             st.info("Upload a new background image or use the current one.")
        else:
            st.info("Please upload an image to use as background.")

    st.markdown("---")

    col_btn_process, col_btn_clear = st.columns(2)
    with col_btn_process:
        if st.button("Process Image 🪄", use_container_width=True, key="btn_process_image"):
            if st.session_state.uploaded_image_bytes:
                background_source_for_processing = None
                if st.session_state.background_option == 'color':
                    # Convert hex color to RGBA tuple for PIL
                    hex_color = st.session_state.selected_color.lstrip('#')
                    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                    background_source_for_processing = rgb + (255,) # Add alpha for full opacity
                elif st.session_state.uploaded_background_image_bytes:
                    background_source_for_processing = Image.open(io.BytesIO(st.session_state.uploaded_background_image_bytes))
                else:
                    st.warning("Please select a background color or upload a background image.")
                    st.stop() # Stop execution if no background source

                with st.spinner("Removing background and applying new one..."):
                    try:
                        foreground_img_rgba = remove_background(st.session_state.uploaded_image_bytes)
                        
                        if background_source_for_processing:
                            final_image_rgb = change_background(foreground_img_rgba, background_source_for_processing)
                            st.session_state.processed_image = final_image_rgb
                            st.session_state.show_processed_image = True
                            st.success("Image processed successfully!")
                        else:
                             # If only background removal was intended (e.g., if user skipped background select)
                             st.session_state.processed_image = foreground_img_rgba.convert("RGB") # Display with transparent background as white
                             st.session_state.show_processed_image = True
                             st.success("Background removed (no new background applied).")

                    except Exception as e:
                        st.error(f"Error during image processing: {e}. Please ensure the image is clear and try again.")
                        st.session_state.show_processed_image = False
            else:
                st.warning("Please upload an image first to process.")
        
    with col_btn_clear:
        if st.button("Clear All 🗑️", use_container_width=True, key="btn_clear_all"):
            st.session_state.uploaded_image_bytes = None
            st.session_state.processed_image = None
            st.session_state.background_option = 'color'
            st.session_state.selected_color = '#007bff'
            st.session_state.uploaded_background_image_bytes = None
            st.session_state.show_processed_image = False
            st.info("All cleared! Ready for a new image.")
            st.rerun() # Force rerun to clear uploaders and image display


# Display Processed Image Result
if st.session_state.show_processed_image and st.session_state.processed_image:
    with col_main_center:
        st.markdown("---")
        st.subheader("✨ Processed Image:")
        st.image(st.session_state.processed_image, caption='Image with New Background', use_column_width=True)

        # Download button for the result
        buf = io.BytesIO()
        st.session_state.processed_image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="Download Processed Image ⬇️",
            data=byte_im,
            file_name="processed_image.png",
            mime="image/png",
            use_container_width=True,
            key="btn_download_image"
        )
    
st.markdown("---")
st.info("Powered by AI (rembg library) and Streamlit.")
st.markdown("<p style='text-align: center; font-size: 0.9rem; color: #a0a0a0; margin-top: 2rem;'>Developed with ❤️ in Mianwali, Punjab, Pakistan</p>", unsafe_allow_html=True)