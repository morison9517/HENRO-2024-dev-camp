from django.db import models

# Create your models here.
#クラスを定義
class Post(models.Model):
     title = models.CharField(max_length=20)
     content = models.TextField(max_length=500)
     created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return self.title
