from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
User=get_user_model()
#tbl_tag
class Tag(models.Model):
    tag_name = models.CharField(max_length=255)
    def __str__(self):
        return self.tag_name
    
#tbl_Blog
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image=models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.title


#tbl_profile
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(default='')
    profile_picture = models.ImageField(upload_to='media/profile_pictures', blank=True,default="")
