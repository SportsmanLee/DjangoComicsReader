from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from blog.models import Article, ArticleForm, Image, Album
from os import path

# Create your views here.
def home(request):
    # https://stackoverflow.com/questions/17621324/relative-path-to-css-file
    albums = Album().get_albums('Albums')
    images_dict = [{'cover_path': '', 'how_many': 0} for k in range(len(albums))]

    for i, album in enumerate(albums):
        image_list = Image().get_image_paths(path.join('Albums', album))
        images_dict[i] = {'cover_path': image_list[0], 'how_many': len(image_list)}

    return render(request, "home.html", {'albums': albums, 'images_dict': images_dict})


def detail(request, pk):
    article = Article.objects.get(pk=int(pk))
    return render(request, "detail.html", {'article': article})


def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save()
            return HttpResponseRedirect('/article/' + str(new_article.pk))

    form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})


def album(request, pk):
    if not pk:
        return HttpResponseRedirect('/')

    albums = Album().get_albums('Albums')
    image_paths = Image().get_image_paths(path.join('Albums', albums[int(pk)]))
    images_need_resizing = Image().get_image_sizes(path.join('Albums', albums[int(pk)]))
    
    return render(request, "album.html", {'album_title': albums[int(pk)],
                                          'image_paths': image_paths, 
                                          'images_need_resizing': images_need_resizing})
