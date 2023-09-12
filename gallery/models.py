from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
