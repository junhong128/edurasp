from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def test(request):
    template = loader.get_template('format.html')
    return HttpResponse(template.render())