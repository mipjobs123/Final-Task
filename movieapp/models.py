from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
class Movie(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Thriller', 'Thriller'),
        ('Drama', 'Drama'),
    ]
    name = models.CharField(max_length=250)
    description = models.TextField()
    released_date = models.DateField()
    cast = models.CharField(max_length=250)
    genre = models.CharField(max_length=100,choices=GENRE_CHOICES,default='Unknown')
    youtube_trailer_link = models.URLField()
    img = models.ImageField(upload_to='gallery')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=150)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_text = models.TextField()
    RATING_CHOICES = (
        ('Good', 'Good'),
        ('Average', 'Average'),
        ('Bad', 'Bad'),
    )
    rating = models.CharField(max_length=20, choices=RATING_CHOICES)

    def __str__(self):
        return f"{self.reviewer_name}'s review for {self.movie.name}"