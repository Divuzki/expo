from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


from .utils import import_docx, delete_docx

# Define Document model
class Document(models.Model):
    file = models.FileField(upload_to='documents', max_length=100000, null=True)
    timestamp = timestamp = models.DateTimeField(auto_now_add=True)

# Define Chapter model
class Chapter(models.Model):
    title = models.CharField(max_length=255, null=False)
    text = models.TextField(blank=True, null=True)
    document = models.ForeignKey(Document, related_name='chapters', on_delete=models.CASCADE, null=True, blank=True)

class Textz(models.Model):
    paragraph = models.TextField(blank=True, null=True)
    timestamp = timestamp = models.DateTimeField(auto_now_add=True)

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
    import_docx(Chapter, instance, Textz)
    # Clear all blank chapters after every import
    # Chapter.objects.filter(title='').delete()


pre_save.connect(create_document, sender=Document)
