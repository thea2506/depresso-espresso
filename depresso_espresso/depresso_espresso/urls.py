from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic.base import TemplateView
import posts.views as posts_views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='1.0.0',
        description="API Documentation for Espresso",
    ), public=True,
)


urlpatterns = [
    path("docs/", schema_view.with_ui('swagger',
         cache_timeout=0), name="schema-swagger-ui"),
    path('admin/', admin.site.urls),
    path('api/feed/', posts_views.api_feed, name='api_feed'),

    path('', include('authentication.urls')),
    path('', include('authors.urls')),
    path('', include('posts.urls')),
    path('', include('inbox.urls')),

    re_path(r"site*", TemplateView.as_view(template_name='index.html')),
    path("", RedirectView.as_view(url='/site')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
