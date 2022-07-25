from django.db import models

# Create your models here.
class Comment(models.Model):
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']