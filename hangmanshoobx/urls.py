from django.contrib import admin
from django.urls import path, include
import hangman.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',hangman.views.home, name='home'),
    path('accounts/',include('accounts.urls') ),
    path('hangman/',include('hangman.urls')),
]
