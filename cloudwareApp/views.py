from django.shortcuts import render
from django.http import HttpResponse
from .models import File

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the cloudwareApp index.")

def upload(request):
    if request.method == "POST":
        # Fetching the form data
        fileName = request.POST["fileName"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = File(
            name = fileName,
            uploadedFile = uploadedFile,
            owner = request.user
        )
        document.save()

    documents = File.objects.all()

    return render(request, "upload.html", context = {
        "files": documents
    })
    