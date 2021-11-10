from django.db import models


class Dictionary(models.Model):
    file = models.FileField(upload_to='files/')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Dictionaries"

