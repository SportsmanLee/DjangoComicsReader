from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from blog.models import Article, ArticleForm, Image, Album

# Create your views here.
def home(request):
    albums = Album().get_albums()
    return render(request, "home.html", {'albums': albums})

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
    albums = Album().get_albums()
    image_paths = Image().get_image_paths('./Albums/')
    return render(request, "album.html", {'image_paths': image_paths})