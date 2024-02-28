from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
#catchall = TemplateView.as_view(template_name='index.html')

#https://medium.com/@taohidulii/serving-react-and-django-together-2089645046e4
def index(request):
    return render(request, "index.html")

