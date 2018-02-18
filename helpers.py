import base64
import io

from PIL import Image


def base64_png_image_to_pillow_image(base64_string):
    img_data = base64.b64decode(str(base64_string))  # Decode base64
    image = Image.open(io.BytesIO(img_data))  # Decode the PNG data
    return image
