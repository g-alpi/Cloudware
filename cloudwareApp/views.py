from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import File
from django.views.decorators.http import require_http_methods, require_GET, require_POST


def index(request):
    return HttpResponse("Hello, world. You're at the cloudwareApp index.")


def upload(request):
    documents = File.objects.all()
    return render(request, "upload_file.html", context = {
        "files": documents
    })

@require_POST
def save_file(request):
    uploaded_file = request.FILES["uploaded_file"]
    new_file(uploaded_file, request)
    return redirect("cloud:upload")
    

def new_file(uploaded_file, request):
    document = File(
            uploaded_file = uploaded_file,
            owner = request.user
        )
    document.save()
    