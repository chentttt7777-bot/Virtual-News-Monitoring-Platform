from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

class UserHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    #created_at = models.DateTimeField(auto_now_add=True)
    #truncated_content = models.CharField(max_length=15)  # 存储截断后的内容



    def __str__(self):
         #return self.username
         return f"{self.user.username} - {self.content}"