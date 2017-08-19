from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
import os
import PIL

def list_images(dir_path):
    included_extensions = ['jpg', 'bmp', 'png', 'gif']
    file_names = [fn for fn in os.listdir(dir_path)
        if any(fn.endswith(ext) for ext in included_extensions)]
    return file_names

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
        file_names = list_images(album_path)

        image_paths = []
        for file_name in file_names:
            #now we have found the desired file.
            #we want to use this information to create a url based on our static path, so we need only the path sections past "static"
            #we can achieve this like so (just one way)
            path = os.sep.join(os.path.join(album_path, file_name).split(os.sep)[-2:])
            image_paths.append(path)

        return image_paths

    def get_cover_path(self, album_path):
        file_names = list_images(album_path)
        cover_path = os.sep.join(os.path.join(album_path, file_names[0]).split(os.sep)[-2:])

        return cover_path

    def get_image_sizes(self, album_path):
        file_names = list_images(album_path)

        images_need_resizing = []
        for file_name in file_names:
            img = PIL.Image.open(os.path.join(album_path, file_name))
            if img.height > img.width:
                images_need_resizing.append(True)
            else:
                images_need_resizing.append(False)
        return images_need_resizing

class Album(models.Model):
    def get_albums(self, album_path):
        dirs = os.listdir(album_path)
        albums = dirs
        return albums