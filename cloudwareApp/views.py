from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, require_POST
from .models import *
import os
import mimetypes

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


@login_required
def downloadFile(request, fileId):
    file = authorizeFileAccess(request.user, fileId)
    filePath = str(file.uploaded_file)
    fileName = str(file.uploaded_file).split(os.sep)[-1]
    try:
        return obtainFile(filePath, fileName)
    except FileNotFoundError:
        raise Http404

def authorizeFileAccess(user, fileId):
    return get_object_or_404(File, pk = fileId, owner = user.pk)

def obtainFile(filePath, fileName):
    absoluteFilePath = getAbsoluteFilePath(filePath)
    response = getFileResponse(absoluteFilePath, fileName)
    return response

def getAbsoluteFilePath(filePath):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return BASE_DIR + os.sep + filePath

def getFileResponse(absoluteFilePath, fileName):
    file = open(absoluteFilePath, 'rb')
    mimeType = mimetypes.guess_type(absoluteFilePath)
    response = HttpResponse(file, content_type=mimeType)
    response['Content-Disposition'] = f"attachment; filename={fileName}"
    return response


def page_not_found(request, exception):
    return render(request, '404.html', status = 404)