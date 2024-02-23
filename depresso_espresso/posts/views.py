from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import Posts
from django.http import JsonResponse
# Create your views here.


class PostView(TemplateView):
    template_name = "posts/posts.html"

    def get(self, request):
        return render(request, "dist/index.html")
    class Meta:
        model = Posts
        fields = ("content", "image_url", "username")

    def save(self, request, commit=True):
        post = super(PostView, self).save(commit=False)

        post.content = self.cleaned_data["content"]
        post.image_url = self.cleaned_data["image_url"]
        post.authorid = self.cleaned_data[request.user.username]
        if commit:
            post.save()
        return post

  
def index(request):
    data ={}
    if request.method == 'POST':
        form = PostView(request.POST)
        if form.is_valid():  
            form.save()
            data['success'] = True  
            return JsonResponse(data) 
        else:
            data['success'] = False  
            return JsonResponse(data) 

    rend = PostView().get(request)
    return rend


