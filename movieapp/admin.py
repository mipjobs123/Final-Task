from django.contrib import admin
from . models import Movie
from .models import Review

admin.site.register(Review)
admin.site.register(Movie)
