from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView
import depresso_espresso.views as views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/', include('authors.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('inbox.urls')),
    re_path(r"site*", TemplateView.as_view(template_name='index.html')),
    path("", RedirectView.as_view(url='/site')),
]
