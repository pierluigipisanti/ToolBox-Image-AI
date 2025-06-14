from rembg import remove
from PIL import Image
import io

def remove_background(image_data: bytes) -> bytes:
    return remove(image_data)

def resize_image(image_data: bytes, width: int, height: int) -> bytes:
    img = Image.open(io.BytesIO(image_data))
    img = img.resize((width, height))
    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()
