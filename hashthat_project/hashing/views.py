"""
This module is used to produce web-pages and handle requests.
"""

from django.shortcuts import render, redirect
from .forms import *
from .models import *
import hashlib
from django.http import JsonResponse


def home(request):
    """
    Creates the homepage.

    :param request: request from client.

    :var form filled_form: holds filled out form data from the request.POST
    :var string text: holds cleaned form data associated with key 'text'
    :var form form: Hash form form.
    :var string template: holds homepage html template.
    :var dictionary context: holds items to add to html when rendered.
    :var string to: holds place to redirect the user to.

    :return: Rendered homepage with whatever context necessary.
    :return: For POST requests redirects user to hash page with information about the hash
    """
    if request.method == 'POST':
        filled_form = HashForm(request.POST)
        if filled_form.is_valid():
            text = filled_form.cleaned_data['text']
            text_hash = create_hash(text)
            try:
                Hash.objects.get(hash=text_hash)
            except Hash.DoesNotExist:
                hash = Hash()
                hash.text = text
                hash.hash = text_hash
                hash.save()
            to = 'hash'
            return redirect(to, hash=text_hash)

    form = HashForm()
    template = 'home.html'
    context = {
        'form': form
    }
    return render(request, template, context)


def hash(request, hash):
    """
    Renders hash/<str:hash>

    :param request: request from client or homepage.
    :param hash: a hash value used to reference the a specific page.

    :var Hash hash: created database hash instant.
    :var string template: holds homepage html template.

    :return: Rendered hash page with whatever context necessary.
    """
    hash = Hash.objects.get(hash=hash)
    template = 'hash.html'
    context = {
        'hash': hash
    }
    return render(request, template, context)


def quickhash(request):
    """

    :param request: Request from client

    :var string item: item to retrive from GET request
    :var string text: text inputed by user
    :var dictionary context: holds dictionary context to pass to html template.

    :return: Json Response (hash value)
    """
    item = 'text'
    text = request.GET[item]
    context = {
        'hash': create_hash(text)
    }
    return JsonResponse(context)


def create_hash(text):
    """
    Runs hashing function from hashlib

    :param text: text to hash

    :return: hash value of text
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
