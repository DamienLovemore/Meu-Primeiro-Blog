from django.shortcuts import render
from django.utils import timezone
from .models import Post #Import a classe Post do arquivo models que está dentro desta pasta(.)

def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/post_list.html',{'posts':posts})