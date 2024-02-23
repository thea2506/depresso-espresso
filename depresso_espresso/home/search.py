from django.views.generic import ListView
from django.contrib.auth import get_user_model


class SearchView(ListView):
    model = get_user_model()
    template_name = 'search.html'
    