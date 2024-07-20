from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required


def main_page(request):
    return render(request,'main_page.html')