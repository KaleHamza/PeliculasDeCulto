from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .forms import PeliculasDeCultoCreateForm, PeliculasDeCultoEditForm
from .models import PeliculasDeCulto,Category
from django.core.paginator import Paginator
# Her bir metot view olarak adlandırılır

db = {
    "movies": [
        {
            "title":"El Topo",
            "description":"By Alejandro Jodorowsky. This film incorporates elements of traditional Western movies but stands out with its fantasy and psychedelic elements. It is also a dramatic and suspenseful story.",
            "imageUrl":"ElTopo.jpg",
            "slug":"El-Tapo-movie-link",
            "date": date(1970,11,18),
            "isActive":True,
            "isUpdated":True
        },
        {
            "title":"Viridiana",
            "description":"By Luis Buñuel. This film is filled with Luis Buñuel's signature absurd and black comedy elements. It can be described as a drama that questions social issues and moral values.",
            "imageUrl":"Viridiana.jpg",
            "slug":"Viridiana-movie-link",
            "date": date(1961,10,10),
            "isActive":True,
            "isUpdated":True
            
        },
         {
            "title":"Todo sobre mi madre",
            "description":"By Pedro Almodóvar. This film, with Pedro Almodóvar's distinctive style of colorful and emotional storytelling, combines elements of drama and comedy. It has a melodramatic tone and explores themes such as gender roles, motherhood, and friendship.",
            "imageUrl":"TodoSobreMiMadre.jpg",
            "slug":"Todo-sobre-mi-madre-movie-link",
            "date": date(1999,5,26),
            "isActive":True,
            "isUpdated":True
        }
    ],
    "categories": [
        {"id":1,"name":"Psychedelic","slug":"Psychedelic"},
        {"id":2,"name":"Absurd","slug":"Absurd"},
        {"id":3,"name":"Melodrama.","slug":"Melodrama"},
        ]
}

def index(request):
    #list comphension
    movies = PeliculasDeCulto.objects.filter(isActive=1,isHome=True)
    categories = Category.objects.all()
    
    return render(request, 'PeliculasDeCulto/index.html', {
                  'categories': categories,
                  "movies": movies
                  })

def create_movie(request):
    if request.method == "POST":
        form = PeliculasDeCultoCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/movies")
    else:
        form = PeliculasDeCultoCreateForm()
    return render(request, "PeliculasDeCulto/create-movie.html", {"form":form})

def movie_list(request):
    movies = PeliculasDeCulto.objects.all()

    return render(request, 'PeliculasDeCulto/movie-list.html', {
                  "movies": movies
                  })
def movie_edit(request, id):
    movie = get_object_or_404(PeliculasDeCulto,pk=id)
    if request.method == "POST":
        form = PeliculasDeCulto(request.POST, instance=movie)
        form.save()
        return redirect("movie_list")
    else:
        form=PeliculasDeCultoEditForm(instance=movie)
    return render(request, "PeliculasDeCulto/edit-movie.html", {"form":form})

def movie_delete(request,id):
    movie = get_object_or_404(PeliculasDeCulto,pk=id)

    if request.method == "POST":
        movie.delete()
        return redirect("movie_list")

    return render(request,"PeliculasDeCulto/movie-delete.html", {"movie":movie})

def upload(request):
    if request.method == "POST":
        uploaded_image = request.FILES['image']
        print(uploaded_image)
        return render(request, "PeliculasDeCulto/success.html")    
    return render('PeliculasDeCulto/upload.html')
def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q = request.GET["q"]
        movies = PeliculasDeCulto.objects.filter(isActive=True,title__contains=q).order_by("date")
        categories = Category.objects.all()
    else:
        return redirect("/movies")
    
    

    return render(request, 'PeliculasDeCulto/search.html', {
        'categories': categories,
        'movies': movies,
    })

def dizilerdetay(request, slug):
    movie = get_object_or_404(PeliculasDeCulto, slug=slug)
    context = {
        'movie': movie
    }
    return render(request, 'PeliculasDeCulto/details.html', context)

#def commends(request):
 #   return HttpResponse('Yorumlar(commends())')

#def starsmovie(request):
#    return HttpResponse('Yıldız filmler')

def getMoviesByCategory(request, slug):
    movies = PeliculasDeCulto.objects.filter(categories__slug=slug, isActive=True).order_by("title")
    categories = Category.objects.all()

    paginator = Paginator(movies, 4)
    page = request.GET.get('page',1)
    page_obj = paginator.page(page)

    return render(request, 'PeliculasDeCulto/list.html', {
        'categories': categories,
        'page_obj': page_obj,
        'selectedCategory':slug
    })