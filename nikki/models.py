from django.db import models

# Create your models here.
#クラスを定義
class Post(models.Model):
     title = models.CharField(max_length=20)
     body=models.TextField(max_length=500)