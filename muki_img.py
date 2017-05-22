import math
from wand.image import Image
from wand.color import Color
from wand.exceptions import BlobError

def _image_to_one_bit_byte_array(img):
    pixels = bytearray(math.ceil(img.width * img.height / 8))
    bit_index = 0
    byte_index = 0
    for row in img:
        for pixel in row:
            # modify the bit
            is_black = pixel.red_int8 == 0 and pixel.green_int8 == 0 and pixel.blue_int8 == 0
            pixels[byte_index] = pixels[byte_index] | (is_black << bit_index)

            bit_index = bit_index + 1
            if bit_index == 8:
                byte_index = byte_index + 1
                bit_index = 0

    return pixels

def load_one_bit_byte_array (image_filename):
    try:
        img = Image(filename=image_filename)

        # scale
        # option 1: seam carving
        #img.liquid_rescale(176,264)

        # option 2: scale with aspect ratio:
        img.transform(resize='176x264^')
        img.crop(width=176, height=264, gravity='center')

        # OrderedDitherImage would allow using 'h4x4a' dither but it's not in python API?
        img.type = 'bilevel'
        # screen is rotated
        img.rotate(90)

        # Write a binary array of b/w pixels
        return _image_to_one_bit_byte_array(img)
    except BlobError:
        img = None
        return None

