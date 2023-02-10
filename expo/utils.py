import os
import docx
import zipfile
import openai
from django.conf import settings

MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL
OPENAI_KEY = settings.OPENAI_SECRET_KEY

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

    # Iterate over document paragraphs
    texts = []
    for paragraph in doc_file.paragraphs:
        ex = paragraph.text.replace(
            "answer", "<b> answer</b>").replace("ANS", "<b> ans</b>").replace("Ans", "<b> ans</b>").replace("ans", "<b> ans</b>")
        texts.append(ex)
        # If heading paragraph then create a new chapter
        if paragraph.style.name.split(' ')[0] == 'Heading':
            # If chapter is not empty, save it
            if obj.title:
                obj.text = text
                obj.save()
            obj = Model.objects.create(
                title=paragraph.text.strip(), document=doc)
            text = ''
        # If paragraph has an image, insert an image tag with the image file
        elif 'Graphic' in paragraph._p.xml:
            for rId in rels:
                if rId in paragraph._p.xml:
                    text += ('\n<img style="width: 50vw;" src="' +
                             os.path.join(MEDIA_URL, 'images/word/media', rels[rId]) + '">')
        # If paragraph has text, just insert text inside paragraph tags
        else:
            text += ('\n<p class="lead text-base font-semibold">' +
                     ex + '</p>')
    if name:
        obj = Model.objects.create(title=name, document=doc)
        obj.save()
        if not Textz == None:
            for ex in texts:
                qs = Textz.objects.filter(paragraph=ex, chapter=obj).first()
                if qs is None:
                    pc = Textz.objects.create(paragraph=ex, chapter=obj)
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
        temperature=0.9,
        max_tokens=100,
        n=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=['\n', 'answer:']
    )

    return completion.choices[0].text
