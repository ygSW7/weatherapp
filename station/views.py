#from django.shortcuts import render
from django.template.response import TemplateResponse
from station.models import Reading

# Create your views here.
def home(request):  # home for homepage
    data = Reading.objects.last()

    return TemplateResponse(request, 'index.html', {'data': data})
