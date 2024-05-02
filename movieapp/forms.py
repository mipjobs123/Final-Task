from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'description', 'released_date', 'cast', 'genre', 'youtube_trailer_link', 'img','uploader']
