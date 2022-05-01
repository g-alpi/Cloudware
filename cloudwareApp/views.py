from time import process_time_ns
from unicodedata import name
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from .models import *

import os
import mimetypes

def index(request):
    return HttpResponse("Hello, world. You're at the cloudwareApp index.")

@login_required
def upload(request):
    documents = File.objects.all()
    return render(request, "upload_file.html", context = {
        "files": documents
    })

@require_POST
@csrf_exempt
def save_file(request):
    uploaded_file = request.POST #request.FILES.get('uploaded_file')
    print(uploaded_file.get('file'))
    print(uploaded_file.get('parent_id'))
    print(uploaded_file)
    print(uploaded_file)
    print(uploaded_file)
    # new_file(uploaded_file, request)
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

@require_POST
def delete_file(request):
    file_id = request.POST['id']
    file = authorizeFileAccess(request.user, file_id)
    file.delete()
    return redirect("cloud:upload")

@require_POST
def edit_file(request):
    file_id = request.POST['id']
    new_file = request.POST['file']
    file = authorizeFileAccess(request.user, file_id)
    file.uploaded_file = new_file
    file.upload_time = timezone.now()
    file.save()
    return redirect("cloud:upload")

@login_required 
def directories(request):
    directories = Directory.objects.filter(owner = request.user, parent = None)
    files = File.objects.filter(owner = request.user , parent = None)
    
    return render(request, "directory.html", context = {
        "files": files,
        "directories": directories,
    })

    
@require_GET
@csrf_exempt
def get_directory (request, dir_id):
    directory = Directory.objects.get(pk = dir_id)
    files = File.objects.filter(parent = directory)
    directories = Directory.objects.filter(parent = directory)
    return render(request, "directory.html", context = {
        'directory':directory,
        "files": files,
        "directories": directories,
    })

@require_POST
@csrf_exempt
def create_directory(request):
    user_dir = os.path.join(settings.MEDIA_ROOT,str(request.user))  
    if not os.path.exists(user_dir):
        os.mkdir(os.path.join(settings.MEDIA_ROOT,str(request.user)))   
    dir_name = request.POST.get('name')
    ruta=[]
    if request.POST.get('parent_id') == None:
        os.mkdir(os.path.join(user_dir, dir_name))
        directory = Directory(
            name = dir_name,
            owner = request.user
        )
    else:
        parent_dir = Directory.objects.get(pk = request.POST.get('parent_id'))
        padre=parent_dir.pk
        while True:
            parent_dir = Directory.objects.get(pk =padre)
            ruta.append(parent_dir.name)
            if parent_dir.parent == None:
                break
            else:
                padre=parent_dir.parent.pk
                
        for i in reversed(ruta):
            user_dir = os.path.join(user_dir,i)
        os.mkdir(os.path.join(user_dir, dir_name))
        directory = Directory(
        name = dir_name,
        owner = request.user,
        parent = Directory.objects.get(pk = request.POST.get('parent_id'))
        )
    directory.save()
    return render(request, 'directory.html')



def page_not_found(request, exception):
    return render(request, '404.html', status = 404)


