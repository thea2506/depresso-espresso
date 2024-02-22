from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('authentication.urls')),
    path("", include('author_profile.urls')),
    path("", include("home.urls")),
    #path("", include('base.urls'))

]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
