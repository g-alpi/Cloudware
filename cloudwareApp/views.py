from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .models import *
import os
import mimetypes

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the cloudwareApp index.")

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