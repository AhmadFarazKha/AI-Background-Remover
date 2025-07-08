from rembg import remove, new_session
from PIL import Image
import io

# Initialize rembg session once
# The default model 'u2net' is usually a good start.
# Models are downloaded on first use, might take time.
session = new_session('u2net') 

def remove_background(image_bytes: bytes) -> Image.Image:
    """
    Removes the background from an image using rembg.
    Returns a PIL Image object with transparency.
    """
    if not image_bytes:
        raise ValueError("No image bytes provided for background removal.")
    
    input_image = Image.open(io.BytesIO(image_bytes))
    
    # Enable alpha_matting for higher quality edges (slower processing)
    output_image = remove(input_image, session=session, alpha_matting=True) # <<<--- CHANGED TO alpha_matting=True
    
    return output_image

def change_background(foreground_image: Image.Image, background_source) -> Image.Image:
    """
    Replaces the background of a foreground image.
    background_source can be an RGBA tuple (for color) or Image.Image (for image background).
    """
    if foreground_image.mode != 'RGBA':
        raise ValueError("Foreground image must have an alpha channel (transparent background).")

    new_bg = None
    if isinstance(background_source, tuple) and len(background_source) == 4:
        # Solid color background
        new_bg = Image.new('RGBA', foreground_image.size, background_source)
    elif isinstance(background_source, Image.Image):
        # Image background
        # Resize background using LANCZOS filter for high quality
        new_bg = background_source.convert("RGBA").resize(foreground_image.size, Image.LANCZOS) # <<<--- ADDED Image.LANCZOS filter
    else:
        raise ValueError("Invalid background_source. Must be RGBA tuple or PIL Image.")

    # Composite the foreground over the new background
    combined_image = Image.alpha_composite(new_bg, foreground_image)
    return combined_image.convert("RGB") # Convert to RGB for common image formats

# Example Usage (for testing - typically run via app.py)
if __name__ == "__main__":
    print("This module is designed to be imported by app.py for Streamlit functionality.")
    print("Please run app.py to see the background removal/changer in action.")