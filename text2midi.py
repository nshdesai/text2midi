"""
text2midi

A program that converts an string to MIDI art.

Try something like:

$ text2midi "Hello, World!" hello_world.mid
"""

__version__ = "0.0.1"

import fire
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import mido

import matplotlib.pyplot as plt


def rasterize_text(msg: str) -> Image:
    """Takes in a string and generates an image of the rendered string

    Args:
        msg (str): Message to be rendered

    Returns:
        Image: Message rendered onto a binary image
    """
    image = Image.new("RGBA", (10 * (len(msg) + 2), 20), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("fonts/moeda.ttf", 20)

    pos = 1
    for i, word in enumerate(msg.split()):
        draw.text((pos, 0), word, (0, 0, 0), font=font)
        pos += 10 * (len(word) + 1)

    return image


def preprocess_image(image: Image) -> np.array:
    """Preprocesses image to generate a 2D numpy array from a Pillow image

    Args:
        image (Image): Pillow image to preprocessed to write MIDI data

    Returns:
        np.array: 2D numpy array where the brightness of each pixel has been converted to a note velocity
    """
    image = image.convert("L")
    note_vels = np.array(image)
    note_vels[note_vels == 255] = 0
    note_vels //= 2
    note_vels = note_vels.astype(np.byte)
    note_vels[note_vels <= 0] = 0

    return note_vels


def write_midi(note_vels: np.array, out_file: Path):
    """Writes a MIDI file of the message written out as MIDI notes

    Args:
        note_vels (np.array): 2D array of note velocities needed to generate MIDI art
        out_file (Path): path to the output MIDI file
    """
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    track.append(mido.Message("note_off", note=30, velocity=127, time=32))

    new_col = True
    for i, col in enumerate(note_vels.T):
        for j, note_vel in enumerate(col):
            if note_vel != 0:
                time = 20 if new_col else 0
                track.append(
                    mido.Message(
                        "note_on", note=60 - 2 * j, velocity=note_vel, time=time
                    )
                )
                track.append(
                    mido.Message("note_off", note=60 - 2 * j, velocity=127, time=0)
                )
                new_col = False
        new_col = True

    mid.save(str(out_file))


def generate_midi(msg: str, out_file: Path) -> None:
    """Generates MIDI art from a message string

    Args:
        msg (str): Message to be written out in MIDI
        out_file (Path): Path to output MIDI file
    """
    image = rasterize_text(msg)
    note_vels = preprocess_image(image)
    write_midi(note_vels, out_file)


if __name__ == "__main__":
    fire.Fire(generate_midi)
