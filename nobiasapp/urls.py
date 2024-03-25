from django.urls import path

from . import views
from .views import submitLink
urlpatterns = [
    path("aboutus", views.aboutus, name="aboutus"),
    path('submitLink', submitLink, name='submitLink'),
    path("tech", views.tech, name="tech"),
    path('', views.home, name="home")
]  