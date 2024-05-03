from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Review
from .forms import MovieForm
from .models import Movie
from django.db.models import Q
from django.utils.safestring import mark_safe


def index(request):
    movie = Movie.objects.all()
    context = {
        'movie_list': movie
    }

    return render(request, 'index.html', context)


def login(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(username=uname, password=pwd)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, "invalid credentials")
            return redirect('movieapp:login')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        uname = request.POST['username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        Email = request.POST['email']
        PASSWORD = request.POST['password']
        Cpassword = request.POST['password1']

                if not uname or not fname or not lname or not Email or not PASSWORD or not Cpassword:
            error_message = "<strong style='font-size: 1.2em;'>All fields are required.</strong>"
            messages.error(request, mark_safe(error_message))
            return redirect('movieapp:register')

        
        if PASSWORD == Cpassword:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "username already used")
                return redirect('movieapp:register')
            elif User.objects.filter(email=Email).exists():
                messages.info(request, "email already used")
                return redirect('movieapp:register')
            else:
                user = User.objects.create_user(username=uname, password=PASSWORD, first_name=fname, last_name=lname,
                                                email=Email)
                user.save()

                messages.success(request, "Registration successful. You can now login.")
                return redirect('movieapp:register')


        else:
            messages.info(request, "password not match")
            return redirect('movieapp:register')
        return redirect('movieapp:login')

    return render(request, 'signup.html', {'messages': messages.get_messages(request)})


def detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    print(request.user.is_authenticated)
    context = {'movie1': movie, 'user': request.user,'reviews': reviews}
    return render(request, "detail.html", context)


@login_required
def uploader_profile(request, uploader_username):
    movies_uploaded = Movie.objects.filter(uploader__username=uploader_username)
    return render(request, 'uploader.html',
                  {'uploader_username': uploader_username, 'movies_uploaded': movies_uploaded})


@login_required
def add_movie(request):
    if request.method == "POST":
        name = request.POST.get('name')
        desc = request.POST.get('description')
        year = request.POST.get('released_date')
        cast = request.POST.get('cast')
        genre = request.POST.get('genre')
        youtube_link = request.POST.get('youtube_trailer_link')
        img = request.FILES.get('img')

        uploader = request.user

        movie = Movie(
            name=name,
            description=desc,
            released_date=year,
            cast=cast,
            genre=genre,
            youtube_trailer_link=youtube_link,
            img=img,
            uploader=uploader
        )
        movie.save()
        return redirect('movieapp:index')

    return render(request, 'add.html')


@login_required
def update(request, id):
    movie = Movie.objects.get(id=id)
    if request.user != movie.uploader:
        return HttpResponseForbidden("You are not allowed to update this movie,uploader only can update movie.")

    if request.method == 'POST':
        #movie = Movie.objects.get(id=id)
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()

        return redirect('movieapp:detail', movie_id=movie.id)

    else:
        movie = Movie.objects.get(id=id)
        form = MovieForm(instance=movie)

    return render(request, 'edit.html', {'form': form, 'movie': movie})


@login_required
def delete(request, id):
    movie = Movie.objects.get(id=id)
    if request.user != movie.uploader:
        return HttpResponseForbidden("You are not allowed to delete this movie,uploader only can delete movie")

    if request.method == "POST":
        #movie = Movie.objects.get(id=id)
        movie.delete()
        return redirect('/')
    return render(request, 'delete.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Review

def add_review(request, movie_id):
    if request.method == 'POST':
        review_text = request.POST['review']
        rating = request.POST['rating']
        user = request.user
        reviewer_name = user.username
        movie = Movie.objects.get(pk=movie_id)
        review = Review.objects.create(user=user, reviewer_name=reviewer_name, movie=movie, review_text=review_text, rating=rating)
        messages.success(request, "Review added successfully.")
        return redirect('movieapp:detail', movie_id=movie_id)
    else:
        return render(request, 'error.html', {'error_message': 'Invalid request method.'})


def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.user or request.user == review.movie.uploader:
        if request.method == 'POST':
            review.delete()
        return redirect('movieapp:detail', movie_id=review.movie.id)
    else:
        return HttpResponseForbidden("You are not authorized to delete this review.")



def genre_list(request, genre):
    movies = Movie.objects.filter(genre=genre)
    context = {'genre': genre, 'movies': movies}
    return render(request, 'genre_list.html', context)

def SearchResult(request):
    query = request.GET.get('q')
    print("Search query:", query)
    if query:
        results = Movie.objects.filter(Q(name__icontains=query))
        print("Search results:", results)
        return render(request, 'search_results.html', {'results': results, 'query': query})
    else:
        return render(request, 'search_results.html')
