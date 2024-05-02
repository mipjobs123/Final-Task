from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = 'movieapp'  #for namespacing

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.detail, name='detail'),
    path('add/', views.add_movie, name='add_movie'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('add_review/<int:movie_id>/', views.add_review, name='add_review'),
    path('profile/<str:uploader_username>/', views.uploader_profile, name='uploader_profile'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('genre/<str:genre>/', views.genre_list, name='genre_list'),
    path('search',views.SearchResult,name='SearchResult'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
