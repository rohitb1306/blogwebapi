
from operator import truediv
from django.db import models
from account.models import MyUser
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
# Create your models here.


class Blog(models.Model):
    blog_auther = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    blog_image = models.ImageField(
        upload_to="blog/images", default="", null=True)
    blog_content = RichTextField(null=True)
    blog_title = models.CharField(max_length=150, unique=True)
    blog_keywords = models.CharField(max_length=150, null=True)
    blog_description = models.CharField(max_length=150, null=True)
    blog_uploaded_on = models.DateTimeField(auto_now=True)
    blog_is_approved = models.BooleanField(default=False)
    blog_new_request = models.BooleanField(default=True)
    blog_del_request = models.BooleanField(default=False)

    new_slug = AutoSlugField(populate_from='blog_title',
                             unique=True, null=True, default=None)

    def __str__(self):
        return self.blog_title


class Comment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    blog_key = models.ForeignKey(Blog, on_delete=models.CASCADE)
    blog_comment = models.TextField()
    comment_added_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.user_name


class Search(models.Model):
    object_blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    search_content = models.CharField(max_length=30, null=True)
