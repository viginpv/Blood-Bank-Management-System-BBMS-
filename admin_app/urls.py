from django.contrib import admin
from django.urls import path
from admin_app import views

# urls.py
urlpatterns = [
    path('main_page',views.main_page,name='main_page')
  
    # other paths...
]
