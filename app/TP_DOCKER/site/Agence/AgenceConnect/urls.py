from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('contact', contact, name="contact"),
    path('communique', communique, name="communique"),
    path('page_access', PageAccess, name="page_access"),
]
