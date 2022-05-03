from hashlib import new
from time import process_time_ns
from unicodedata import name
from webbrowser import get
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from operator import truediv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import *

import os
import mimetypes
import re

def landing_page(request):
        return render(request, 'landing_page.html')

@login_required
def upload(request):
    documents = File.objects.all()
    return render(request, "upload_file.html", context = {
        "files": documents
    })

@require_POST
@csrf_exempt
def upload_file(request):
    uploaded_file = request.FILES.get('uploaded_file')
    owner = get_object_or_404(User, pk = request.user.pk)
    parent_id = request.POST.get('parent_id')

    if parent_id == None:
        save_new_file(uploaded_file, owner)
        
    else:
        parent = get_object_or_404(Directory, pk = parent_id)
        save_new_file(uploaded_file, owner,parent)
        
    return redirect("cloud:upload")

def save_new_file(uploaded_file, owner,parent = None):  
    document = File(
            uploaded_file = uploaded_file,
            owner = owner,
            parent = parent
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
    check_media_directory()
    check_upload_directory()
    
    user_dir = check_user_directory(request.user)  
    dir_name = request.POST.get('name')
    path=[]
    
    if request.POST.get('parent_id') == None:
        new_directory(user_dir,dir_name,request.user)
        
    else:
        
        actual_directory = Directory.objects.get(pk = request.POST.get('parent_id'))
        path = get_full_path(actual_directory)
        user_dir = os.path.join(user_dir,*path[::-1]) 
        new_directory(user_dir,dir_name,request.user,actual_directory)
        
    return render(request, 'directory.html')

def check_media_directory():
    media_path = os.path.join(settings.BASE_DIR,'cloudwareApp', 'media')
    if not os.path.exists(media_path):
        os.mkdir(media_path)
        
def check_upload_directory():
    uploaded_files_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files')
    if not os.path.exists(uploaded_files_path):
        os.mkdir(uploaded_files_path)
        
def check_user_directory(user):
    uploaded_files_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files')
    user_path = os.path.join(uploaded_files_path, str(user))
    if not os.path.exists(user_path):
        os.mkdir(user_path)
    return user_path

def get_full_path(directory):
    path = []
    actual_directory = directory
    while  True:
        path.append(actual_directory.name)
        if actual_directory.parent == None:
            break
        actual_directory = actual_directory.parent
    return path

def new_directory(path_dir, dir_name, owner, parent = None):
    os.mkdir(os.path.join(path_dir, dir_name))
    directory = Directory(
        name = dir_name,
        owner = owner,
        parent = parent
    )
    directory.save()


@csrf_exempt
def shareFile(request, fileId):
    fileToShare = File.objects.get(pk = fileId)
    userEmail = request.user.mail
    emails = re.split(' , |, |,', request.POST["mails"])
    emailsRejected = []
    for email in emails:
        if (not validateEmail(email) or email == userEmail):
            emailsRejected.append(email)
        else:
            try:
                newShareFile(email, fileToShare)
            except:
                emailsRejected.append(email)
    return redirect("cloud:upload")

def validateEmail(possibleEmail):
    regexToValidateEmail = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if (re.search(regexToValidateEmail, possibleEmail)):
        return True
    return False

def newShareFile(userEmail, fileToShare):
    user = User.objects.get(email = userEmail)
    newShareFile = SharedFile(file = fileToShare, user = user)
    newShareFile.save()


def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('cloud:landing_page')

@csrf_exempt
def authenticate_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)
    if user is not None:
        login(request, user)
        return redirect("cloud:cloudware_app")
    else:
        messages.error(request, 'Las credenciales no son correctas')
        return redirect('cloud:login')

def signup(request):
    return render(request, 'signup.html')


def cloudware_app(request):
    return render(request, 'cloudware_app.html')


def profile(request):
    return render(request, 'profile.html')


def page_not_found(request, exception):
    return render(request, '404.html', status = 404)


