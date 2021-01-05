from django.http import request
from django.shortcuts import render, redirect

# Create your views here.
from drLink.models import *


def home(request):

    return render(request, "")