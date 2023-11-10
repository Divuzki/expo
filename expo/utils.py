import os
import docx
import zipfile
import openai
from django.conf import settings
import string
import random

MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL
OPENAI_KEY = settings.OPENAI_SECRET_KEY



def truncate_string(value, max_length=45, suffix="skt"):
    string_value = str(value)
    string_truncated = string_value[:min(
        len(string_value), (max_length - len(suffix)))]
    suffix = (suffix if len(string_value) > max_length else '')
    return suffix+string_truncated


def random_string_generator(size=50, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Import images from docx
def import_images(doc):
    img_dir = os.path.join(MEDIA_ROOT, 'images')

    # Create directory to save all image files if it doesn't exist
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    # Extract all images from .docx
    with zipfile.ZipFile(doc.file, 'r') as zipFile:
        filelist = zipFile.namelist()
        for filename in filelist:
            if filename.startswith('word/media/'):
                zipFile.extract(filename, path=img_dir)

    return img_dir

# Check for .emf images format and convert them and
# save all 'rId:filenames' relationships in an dictionary named rels


def relate_images(img_dir, doc_file):
    rels = {}
    for r in doc_file.part.rels.values():
        if isinstance(r._target, docx.parts.image.ImagePart):
            img = os.path.basename(r._target.partname)
            if img.split('.')[-1] == 'emf':
                dir = os.path.join(img_dir, 'word/media')
                command = 'inkscape --file {0} --export-plain-svg {1}.svg'.format(
                    os.path.join(dir, img), os.path.join(dir, img.split('.')[0]))
                if os.system(command) != 0:
                    print(
                        'Could not import .docx images properly. Please, install inkscape. \'$ apt install inkscape\'')
                img = img.split('.')[0] + '.svg'
            rels[r.rId] = img

    return rels


def import_docx(Model, doc, Textz=None, name=None):
    # Declare variables for text extraction
    doc_file = docx.Document(doc.file)
    obj = Model()
    text = ''

    # Import and relate all images
    img_dir = import_images(doc)
    rels = relate_images(img_dir, doc_file)

    # Iterate over document texts
    texts = []
    for text in doc_file.texts:
        ex = text.text.replace(
            "answer", "<b> answer</b>").replace("ANS", "<b> ans</b>").replace("Ans", "<b> ans</b>").replace("ans", "<b> ans</b>")
        texts.append(ex)
        # If heading text then create a new chapter
        if text.style.name.split(' ')[0] == 'Heading':
            # If chapter is not empty, save it
            if obj.title:
                obj.text = text
                obj.save()
            obj = Model.objects.create(
                title=text.text.strip(), document=doc)
            text = ''
        # If text has an image, insert an image tag with the image file
        elif 'Graphic' in text._p.xml:
            for rId in rels:
                if rId in text._p.xml:
                    text += ('\n<img style="width: 50vw;" src="' +
                             os.path.join(MEDIA_URL, 'images/word/media', rels[rId]) + '">')
        # If text has text, just insert text inside text tags
        else:
            text += ('\n<p class="lead text-base font-semibold">' +
                     ex + '</p>')
    if name:
        obj = Model.objects.create(title=name, document=doc)
        obj.save()
        if not Textz == None:
            for ex in texts:
                qs = Textz.objects.filter(text=ex, chapter=obj).first()
                if qs is None:
                    pc = Textz.objects.create(text=ex, chapter=obj)
                    pc.save()
    # Save the remaining object
    obj.text = text
    obj.save()

# Delete .docx document and it's image folder


def delete_docx(doc):
    if doc.file:
        if os.path.exists(doc.file.path):
            os.remove(doc.file.path)
    img_dir = os.path.join(MEDIA_ROOT, 'images')
    for root, dirs, files in os.walk(img_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

# function to get ai results
def get_ai_results(prompt):
    openai.api_key = OPENAI_KEY

    model_engine = 'text-davinci-003'

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        n=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    return completion.choices[0].text
