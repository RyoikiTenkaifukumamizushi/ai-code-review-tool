from PIL import Image
def resize_image(image_path, size):
    with Image.open(image_path) as img:
        img=img.resize(size)
        return img
def convert_to_grayscale(image_path):
    with Image.open(image_path) as img:
        return img.convert("L")
