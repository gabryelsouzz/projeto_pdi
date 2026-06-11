from PIL import Image
from PIL.Image import Image as IMG

def load(path: str) -> IMG:
    return Image.open(path).convert('L') # isso converte para uma escala de cinza de 8 bits

def save(img: IMG, path: str) -> None:
    img.save(path)
