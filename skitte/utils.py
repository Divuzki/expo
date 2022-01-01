from moviepy.editor import *
import string
from django.utils.text import slugify
import random
from pathlib import Path
from PIL import Image
from io import BytesIO
import textwrap
from PIL import Image, ImageDraw, ImageFont
from django.core.files.storage import default_storage as storage
from django.core.files import File

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def format_string(str, min_length):
    while len(str) > min_length:
        str += random_string_generator(size=5)
    return str

# ROT13 ENCRYPTION
rot13trans = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                           'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm')

# Function to translate plain text


def rot13_encrypt(text):
    return text.translate(rot13trans)


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        text = instance.timestamp
        if instance.content:
            text = instance.content
        elif instance.caption:
            text = instance.caption
        elif instance.image:
            text = f"{instance.image.size}"
        if instance.user:
            slug = slugify(f"@{instance.user.username}-posted-{text}")
        else:
            slug = slugify(f"@{text}")
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4))

        return unique_slug_generator(instance, new_slug=new_slug)
    return rot13_encrypt(slug).upper()


image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def image_resize(image, width, height):
    # Open the image using Pillow
    img = Image.open(image)
    # check if either the width or height is greater than the max
    if img.width > width or img.height > height:
        output_size = (width, height)
        # Create a new resized “thumbnail” version of the image with Pillow
        img.thumbnail(output_size)
        # Find the file name of the image
        img_filename = Path(image.file.name).name
        # Spilt the filename on “.” to get the file extension only
        img_suffix = Path(image.file.name).name.split(".")[-1]
        # Use the file extension to determine the file type from the image_types dictionary
        img_format = image_types[img_suffix]
        # Save the resized image into the buffer, noting the correct file type
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        # Wrap the buffer in File object
        file_object = File(buffer)
        # Save the new resized file as usual, which will save to S3 using django-storages
        image.save(img_filename, file_object)


def video_converter(video_path, resolution):
    # Import everything needed to edit video clips

    # loading video dsa gfg intro video and getting only first 5 seconds
    clip1 = VideoFileClip("dsa_skitte.webm").subclip(0, 60)

    # getting width and height of clip 1
    w1 = clip1.w
    h1 = clip1.h

    print("Width x Height of clip 1 : ", end=" ")
    print(str(w1) + " x ", str(h1))

    print("---------------------------------------")

    # showing final clip
    clip1.ipython_display(width=720)


def chat_unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        text = instance.timestamp
        if instance.title:
            text = f"{instance.title}-desc={instance.description}"
    slug = slugify(f"@{text}#{instance.timestamp}+{instance.pk}")
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4))

        return chat_unique_slug_generator(instance, new_slug=new_slug)
    return chat_unique_slug_generator(rot13_encrypt(slug).upper().replace("-", "₦"))


def make_text_bg(self):
    memfile = BytesIO()
    caption = self.caption
    imgpath = f'skitte-images\\contentBackgroundImage\\skt_cation\\{self.user.username}\\skt_cation+{rot13_encrypt(slugify(caption))}_image.png'
    imgpath = f"{imgpath.replace(' ', '0')}.png"
    wrapper = textwrap.TextWrapper(width=35)
    word_list = wrapper.wrap(text=caption)
    msg = ''

    for ii in word_list[:-1]:
        msg = msg + ii + '\n'
    msg += word_list[-1]

    W, H = (800, 600)
    img = Image.new("RGBA", (W, H), "black")
    draw = ImageDraw.Draw(img)

    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype(os.path.join(
        BASE_DIR, "static/fonts/seguiemj.ttf"), 48, layout_engine=ImageFont.LAYOUT_RAQM)
    w, h = draw.textsize(msg, font=font)
    draw.text(((W - w) / 2, (H-h)/2), msg,
              fill="#faa", font=font
              #   , embedded_color=True
              )
    img.save(memfile, 'PNG', quality=95)
    storage.save(imgpath, memfile)
    memfile.close()
    img.close()
    self.content = ''
    self.caption = ''
    self.image = imgpath
    return imgpath
