from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('signup_view/',views.signup_view,name='signup_view'),
    path('login_view/',views.login_view,name='login_view'),
    

    # path('fulfill-request/<int:request_id>/', views.fulfill_request, name='fulfill_request'),
    

]
