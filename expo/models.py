from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from skitte.utils import random_string_generator, truncate_string

from .utils import import_docx
# , delete_docx

# Define Document model


class Document(models.Model):
    file = models.FileField(upload_to='documents',
                            max_length=100000, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

# Define Chapter model


class Chapter(models.Model):
    title = models.CharField(max_length=255, null=False)
    document = models.ForeignKey(
        Document, related_name='chapters', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def questions(self):
        return self.text.all()

class Question(models.Model):
    chapter = models.ForeignKey(
        Chapter, related_name='text', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class Passcode(models.Model):
    code = models.CharField(
        max_length=5, null=True, blank=True, unique=True)
    transactionId = models.CharField(
        max_length=20, null=True, blank=True, unique=True)
    used_count = models.IntegerField(default=0, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sr = self.code
        return f"{sr} => {self.used_count}"


# Set signal to delete all document objects and it's files when another one is created
# @receiver(models.signals.pre_save, sender=Document)
# def delete_older_documents(sender, instance, **kwargs):
#     documents = Document.objects.all()
#     if documents:
#         for doc in documents:
#             delete_docx(doc)
#         Chapter.objects.all().delete()
#         documents.delete()

# Set signal for importing .docx after uploading it
@receiver(models.signals.post_save, sender=Document)
def create_document(sender, instance, **kwargs):
    import_docx(Chapter, instance, Question)
    # Clear all blank chapters after every import
    Chapter.objects.filter(title='').delete()


def create_passcode(sender, instance, *args, **kwargs):
    if not instance.code:
        word = random_string_generator(size=4)
        if not instance.transactionId:
            instance.transactionId = random_string_generator(size=17).upper()
        instance.code = truncate_string(
            value="divuzki"+word, max_length=5, suffix=word)


pre_save.connect(create_document, sender=Document)
pre_save.connect(create_passcode, sender=Passcode)
