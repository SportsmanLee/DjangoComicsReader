from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from blog.models import Article, ArticleForm, Image, Album

# Create your views here.
def home(request):
    albums = Album().get_albums()
    images = []
    for album in albums:
        images.append(Image().get_cover_path('.\\Albums\\' + album))
    print(images[0])
    return render(request, "home.html", {'albums': albums, 'images': images})

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

    albums = Album().get_albums()
    image_paths = Image().get_image_paths('.\\Albums\\' + albums[int(pk)])
    images_need_resizing = Image().get_image_sizes('.\\Albums\\' + albums[int(pk)])
    return render(request, "album.html", {'image_paths': image_paths, 'images_need_resizing': images_need_resizing})