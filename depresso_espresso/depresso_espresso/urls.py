from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView
from home import views

urlpatterns = [
    path('', views.StreamView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path("", include('authentication.urls')),
    path("", include('author_profile.urls')),
    path("", include("home.urls")),
    path("", include("posts.urls")),
    #path("", include('base.urls'))

]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
