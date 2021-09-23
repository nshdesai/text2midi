import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def rasterize_text(msg: str) -> Image:
    image = Image.new("RGBA", (100, 20), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('fonts/moeda.ttf', 20)

    draw.text((10, 0), msg, (0, 0, 0), font=font)

    return image


def preprocess_image(image: Image) -> np.array:
    image = image.convert('L') 
    note_vels = np.array(image)
    note_vels[note_vels == 255] = 0

    return note_vels 

def write_midi(note_vels: np.array):
    pass

def generate_midi(msg: str, out_file: Path) -> None:
    image = rasterize_text(msg)
    note_vels = preprocess_image(image)
    write_midi(note_vels, out_file)

if __name__=='__main__':
    pass