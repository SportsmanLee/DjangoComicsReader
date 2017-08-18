from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(u'Name', max_length=50)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    content = models.TextField(u'Content')
    title = models.CharField(u'Title', max_length=50)
    category = models.ForeignKey('Category', blank=True, null=True)

    def __unicode__(self):
        return self.title

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', ]

class Image(models.Model):
    def get_image_paths(self, album_path):
        for root, dirs, files in os.walk(album_path + os.sep):
            #debug information, just to get an idea how walk works.
            #currently we are traversing over all files with any extension
            # print("Current directory", root)
            # for dir in dirs:
            #     print("Sub directories", dir)
            # print("Files", files)
            if not files:
                continue

            image_paths = []
            for file in files:
                #now we have found the desired file.
                #we want to use this information to create a url based on our static path, so we need only the path sections past "static"
                #we can achieve this like so (just one way)
                path = os.sep.join(os.path.join(root, file).split(os.sep)[-2:])
                image_paths.append(path)
                #print("image_path", path)

            return image_paths

class Album(models.Model):
    def get_albums(self):
        dirs = os.listdir('./Albums/')
        albums = dirs
        return albums