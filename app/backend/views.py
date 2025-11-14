from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def calculateXYZ(a, b):
    x = a + b
    y = a - b
    z = a * b
    return x, y, z

def test(request):
    x = calculateXYZ(5, 3)
    template = loader.get_template('format.html', x)
    return HttpResponse(template.render())