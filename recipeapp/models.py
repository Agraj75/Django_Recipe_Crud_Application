from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class receipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    receipe_name = models.CharField(max_length=100, null=False)
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to="receipe")

    class meta:
        db_table="receipes"
