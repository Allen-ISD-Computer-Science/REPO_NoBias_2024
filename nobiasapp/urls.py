from django.urls import path

from . import views
from .views import submitLink, aboutus
urlpatterns = [
    path("aboutus", views.aboutus, name="aboutus"),
    path('', submitLink, name='submitLink'),
]  