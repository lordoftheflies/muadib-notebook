from django.db import models

# Create your models here.
class NoteBookEndpointModel(models.Model):
    slug = models.CharField(max_length=20)
    local_path = models.FilePathField(max_length=200)

class FrontendEnpointModel(models.Model):
    slug = models.CharField(max_length=20)
    relative_uri = models.URLField(max_length=200)
