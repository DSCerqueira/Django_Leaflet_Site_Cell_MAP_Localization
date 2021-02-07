from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class serverfiles(models.Model):
    id=models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    filename=models.FileField(upload_to='fileserver/',blank=True)

    def get_absolute_url(self):
        return reverse('file_detail',kwargs={'pk':str(self.pk)})

class fileserver(models.Model):
    id=models.UUIDField(primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    filename=models.FileField(upload_to='fileserver/',blank=True)

    def get_absolute_url(self):
        return reverse('file_detail',kwargs={'pk':str(self.pk)})


