from django.shortcuts import render
from django.http import HttpResponse
from .models import File

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the cloudwareApp index.")

def upload(request):
    if request.method == "POST":
        # Fetching the form data
        uploaded_file = request.FILES["uploaded_file"]

        # Saving the information in the database
        document = File(
            uploaded_file = uploaded_file,
            owner = request.user
        )
        document.save()

    documents = File.objects.all()

    return render(request, "upload_file.html", context = {
        "files": documents
    })

