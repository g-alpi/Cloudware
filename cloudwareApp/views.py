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