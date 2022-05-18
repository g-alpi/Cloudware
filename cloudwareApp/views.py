import email
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
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import *

import os
import re
import shutil
import mimetypes

def landing_page(request):
        return render(request, 'landing_page.html')

@login_required
def upload(request):
    documents = File.objects.all()
    return render(request, "cloudware_app.html", context = {
        "files": documents
    })

@require_POST
@csrf_exempt
def upload_file(request):
    uploaded_file = request.FILES.get('uploaded_file')
    owner = get_object_or_404(User, pk = request.user.pk)
    parent_id = request.POST.get('parent_id')

    if parent_id == None:
        path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files', str(owner), uploaded_file.name)
        
        if len(path) <=500:
            save_new_file(uploaded_file, owner)
        else:
            messages.error(request, 'The path is too long, revise your folders')
            return redirect('cloud:cloudware_app')
        
    else:
        parent = get_object_or_404(Directory, pk = parent_id)
        path = get_parents_path(parent)
        full_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files', str(owner), *path[::-1], uploaded_file.name)
        
        if len(full_path) <= 500:
            save_new_file(uploaded_file, owner, parent)
        else:
            messages.error(request, 'The path is too long, revise your folders')
            return redirect('cloud:get_directory', parent_id)
        
    return redirect("cloud:cloudware_app")

def save_new_file(uploaded_file, owner,parent = None):  
    document = File(
            uploaded_file = uploaded_file,
            owner = owner,
            parent = parent
        )
    document.save()



@login_required
@csrf_exempt

def downloadFile(request, fileId):
    file = authorizeFileAccess(request.user, fileId)
    filePath = str(file.uploaded_file)
    fileName = os.path.basename(file.uploaded_file.name)
    print(fileName)
    print(file.owner)
    print(request.user)
    try:
        return obtainFile(filePath, fileName)
    except FileNotFoundError:
        raise Http404

def authorizeFileAccess(user, fileId):
    file = get_object_or_404(File, pk = fileId)
    if user == file.owner:
        print("True")
        return file
    sharedFile = get_object_or_404(SharedFile, file = file, user = user)
    return sharedFile.file

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
@csrf_exempt
def delete_file(request):
    file_id = request.POST['id']
    file = authorizeFileAccess(request.user, file_id)
    delete_file_local(file)
    file.delete()
    
    return redirect("cloud:upload")

def delete_file_local(file):
    filename = os.path.split(str(file.uploaded_file))[-1]
    if file.parent == None:
        os.remove(str(file.uploaded_file))
    else:
        os.remove(os.path.join('media','uploaded_files', str(file.owner), *get_parents_path(file.parent)[::-1], filename))
@require_POST
@csrf_exempt
def delete_directory(request):
    directory_id = request.POST['id']
    directory = Directory.objects.get(owner = request.user, pk= directory_id)
    delete_directory_local(directory)
    directory.delete()
    
    return redirect("cloud:upload")

def delete_directory_local(directory):
    if directory.parent == None:
        shutil.rmtree(os.path.join('media','uploaded_files', str(directory.owner),str(directory.name)))
    else:
        shutil.rmtree(os.path.join('media','uploaded_files', str(directory.owner), *get_parents_path(directory.parent)[::-1], directory.name))

@require_POST
@csrf_exempt
def edit_file(request):
    file_id = request.POST['id']
    new_file_name = request.POST['name']
    file = authorizeFileAccess(request.user, file_id)
    path= calculate_new_file_paths(file, new_file_name)
    update_file(file, path['new_path_admin'],path['actual_path_local'],path['new_path_local'])
    
    return redirect("cloud:cloudware_app")

def update_file(file, new_path_admin, actual_path_local,new_path_local,):
    file.uploaded_file = new_path_admin   
    file.upload_time = timezone.now()
    file.save()
    os.rename(actual_path_local, new_path_local)

def calculate_new_file_paths(file, new_file_name):
    actual_path_admin = str(file.uploaded_file)
    extension = os.path.splitext(str(file.uploaded_file))[1]
    new_path_admin = actual_path_admin.replace(os.path.split(actual_path_admin)[-1], new_file_name + extension)
    actual_path_local = os.path.join(os.getcwd(), actual_path_admin)
    new_path_local = actual_path_local.replace(os.path.split(actual_path_local)[-1], new_file_name + extension) 
    actual_path_admin = normalize_path(actual_path_admin)
    actual_path_local = normalize_path(actual_path_local)
    new_path_local = normalize_path(new_path_local)
    
    return {'actual_path_admin': actual_path_admin, 'new_path_admin': new_path_admin, 'actual_path_local': actual_path_local, 'new_path_local': new_path_local}
    
def normalize_path(path):
    return  os.path.normpath(path)


    

@login_required 
def file_manager(request):
    directories = Directory.objects.filter(owner = request.user, parent = None)
    files = File.objects.filter(owner = request.user , parent = None)
    return render(request, "cloudware_app.html", context = {
        "files": files,
        "directories": directories,
    })
    
@login_required
def shared_sources(request):
    shared_files = SharedFile.objects.filter(user = request.user)
    shared_directories = SharedDirectory.objects.filter(user = request.user)
    
    files = []
    for i in shared_files:
        if i.file.parent == None:
            files.append(i.file)
    directories = []
    for i in shared_directories:
        if i.directory.parent == None:
            directories.append(i.directory)
        
    return render(request, "shared_sources.html", context = {
        "files": files,
        "directories": directories,
    })
    
@require_GET
@csrf_exempt
def get_share_directory (request, dir_id):
    directory = Directory.objects.get(pk = dir_id)
    files = File.objects.filter(parent = directory)
    directories = Directory.objects.filter(parent = directory)
    breadcrumbs = get_breadcrumbs(directory)
    return render(request, "shared_sources.html", context = {
        'directory':directory,
        "files": files,
        "directories": directories,
        "breadcrumbs": breadcrumbs
    })
    
@require_GET
@csrf_exempt
def get_directory (request, dir_id):
    directory = Directory.objects.get(pk = dir_id)
    files = File.objects.filter(parent = directory)
    directories = Directory.objects.filter(parent = directory)
    breadcrumbs = get_breadcrumbs(directory)
    return render(request, "cloudware_app.html", context = {
        'directory':directory,
        "files": files,
        "directories": directories,
        "breadcrumbs": breadcrumbs,
    })

def get_breadcrumbs(directory):
    directoryToCheck = directory
    breadcrumbsList = [directoryToCheck]
    while directoryToCheck.parent is not None:
        directoryToCheck = directoryToCheck.parent
        breadcrumbsList.insert(0, directoryToCheck)
    return breadcrumbsList

@require_POST
@csrf_exempt
def create_directory(request):
    check_media_directory()
    check_upload_directory()
    
    user_dir = check_user_directory(request.user)  
    dir_name = request.POST['name']
    path=[]
    
    if validate_directory_name(dir_name) == True:
        if request.POST.get('parent_id') == None:
            new_directory(user_dir,dir_name,request.user)

        else:
            
            actual_directory = Directory.objects.get(pk = request.POST.get('parent_id'))
            path = get_parents_path(actual_directory)
            user_dir = os.path.join(user_dir,*path[::-1]) 
            new_directory(user_dir,dir_name,request.user,actual_directory) 
        return render(request, 'cloudware_app.html')
    messages.error(request, 'Incorrect Directory name')
    actual_url = request.META.get('HTTP_REFERER')
    return redirect(actual_url)

def validate_directory_name(name):
    regex_to_validate_name =  r"^[^\s^\x00-\x1f\\?*:\"\";<>|\/.][^\x00-\x1f\\?*:\"\";<>|\/]*[^\s^\x00-\x1f\\?*:\"\";<>|\/.]+$"
    if (re.search(regex_to_validate_name, name)):
        return True
    return False

def check_media_directory():
    media_path = os.path.join(settings.BASE_DIR, 'media')
    if not os.path.exists(media_path):
        os.mkdir(media_path)
        
def check_upload_directory():
    uploaded_files_path = os.path.join('media', 'uploaded_files')
    if not os.path.exists(uploaded_files_path):
        os.mkdir(uploaded_files_path)
        
def check_user_directory(user):
    uploaded_files_path = os.path.join('media', 'uploaded_files')
    user_path = os.path.join(uploaded_files_path, str(user))
    if not os.path.exists(user_path):
        os.mkdir(user_path)
    return user_path

def get_parents_path(directory):
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

@require_POST
@csrf_exempt
def edit_directory(request):
    directory_id = request.POST.get('id')
    new_directory_name = request.POST.get('name')
    directory = Directory.objects.get(pk = directory_id)
    
    rename_directory(directory, new_directory_name)
    
    return redirect(to = "cloud:cloudware_app")

def rename_directory(directory, new_name):
    user_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files', str(directory.owner)) 
    
    if directory.parent == None:
        os.rename(os.path.join(user_path, directory.name), os.path.join(user_path, new_name))
        directory.name = new_name
    else:
        path = get_parents_path(directory)
        actual_directory = os.path.join(user_path, *path[::-1])
        
        os.rename (actual_directory, os.path.join(os.path.split(actual_directory)[:-1][0], new_name))
        directory.name = new_name
        
    directory.save()
    
@require_POST
@csrf_exempt
def shareFile(request, fileId):
    fileToShare = File.objects.get(pk = fileId)
    userEmail = request.user.email
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

def newShareFile(userEmail, fileToShare):
    user = User.objects.get(email = userEmail)
    newShareFile = SharedFile(file = fileToShare, user = user)
    newShareFile.save()

@require_POST
@csrf_exempt
def share_directory(request, directoryId):
    directory = Directory.objects.get(pk = directoryId)
    userEmail = request.user.email
    emails = re.split(' , |, |,', request.POST["mails"])
    emailsRejected = []
    for email in emails:
        if (not validateEmail(email) or email == userEmail):
            emailsRejected.append(email)
        else:
            try:
                newShareDirectory(email, directory)
            except:
                emailsRejected.append(email)
    return redirect("cloud:upload")

def newShareDirectory(userEmail, directory):
    user = User.objects.get(email = userEmail)
    newShareDirectory = SharedDirectory(directory = directory, user = user)
    newShareDirectory.save()
    
    files = File.objects.filter(parent = directory)
    for file in files:
        newShareFile(userEmail, file)
    
    get_all_children_directory(directory,user,userEmail)
    
def get_all_children_directory(directory,user,userEmail):
    directories = Directory.objects.filter(parent = directory)
    for i in directories:
        files = File.objects.filter(parent = i)
        for file in files:
            newShareFile(userEmail, file)
        newShareDirectory = SharedDirectory(directory = i, user = user)
        newShareDirectory.save()
        get_all_children_directory(i,user,userEmail)

def validateEmail(possibleEmail):
    regexToValidateEmail = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if (re.search(regexToValidateEmail, possibleEmail)):
        return True
    return False




def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('cloud:landing_page')

def authenticate_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)
    if user is not None:
        login(request, user)
        return redirect("cloud:cloudware_app")
    else:
        messages.error(request, 'Incorrect credentials')
        return redirect('cloud:login')

def signup(request):
    possibleErrors = ['nameError', 'emailError', 'passwordError']
    signupErrors = checkErrors(request, possibleErrors)
    return render(request, 'signup.html', signupErrors)

def checkErrors(request, errorsToCheck):
    errors = {}
    for error in errorsToCheck:
        if error in request.session:
            errors[error] = request.session[error]
            request.session.pop(error)
    return errors


def validate_signup(request):
    nameValidation = validateRegisterUsername(request, 'nameError')
    emailValidation = validateRegisterEmail(request, 'emailError')
    passwordValidation = validateRegisterPassword(request, 'passwordError')
    
    if nameValidation or emailValidation or passwordValidation:
        return redirect('cloud:signup')
    newUser = User(username = request.POST['username'], email=request.POST['email'])
    newUser.set_password(request.POST['password'])
    newUser.save()
    return redirect('cloud:login')

def validateRegisterUsername(request, keyName, usernameKey = 'username'):
    usernameExist = User.objects.filter(username=request.POST[usernameKey]).exists()
    print("ola")
    if usernameExist:
        request.session[keyName] = 'Username already exists'
        return True
    if len(request.POST[usernameKey]) <= 0:
        request.session[keyName] = 'Username must contain at least 1 character'
        return True
    if not request.POST[usernameKey].isalnum():
        request.session[keyName] = 'Username must contain alphanumeric characters only'
        return True
    return False

def validateRegisterEmail(request, keyName, emailKey = 'email'):
    emailExist = User.objects.filter(email=request.POST[emailKey]).exists()
    if emailExist:
        request.session[keyName] = 'Email already exists'
        return True
    if len(request.POST[emailKey]) < 5:
        request.session[keyName] = 'Email must contain at least 5 characters'
        return True
    if not validateEmail(request.POST[emailKey]):
        request.session[keyName] = 'Email don\'t have a valid format'
        return True
    return False

def validateRegisterPassword(request, keyName, passwordKey = 'password'):
    if len(request.POST[passwordKey]) < 8:
        request.session[keyName] = 'Password must contain at least 8 characters'
        return True
    if request.POST[passwordKey] != request.POST[passwordKey + 'Confirmation']:
        request.session[keyName] = 'Password and password confirmation are not the same'
        return True
    return False


@login_required
def profile(request):
    possibleErrors = ['updateError']
    updateErrors = checkErrors(request, possibleErrors)
    return render(request, 'profile.html', updateErrors)

@login_required
def update_username(request):
    usernameValidated = validateRegisterUsername(request, 'updateError', 'newUsername')
    if usernameValidated:
        return redirect('cloud:profile')

    userToUpdate = authenticate(username=request.user.username, password=request.POST['password'])
    if userToUpdate is not None:
        userToUpdate.username = request.POST["newUsername"]
        userToUpdate.save()
        return redirect('cloud:profile')
    
    request.session['updateError'] = 'Wrong Password'
    return redirect('cloud:profile')

@login_required
def update_email(request):
    emailValidated = validateRegisterEmail(request, 'updateError', 'newEmail')
    if emailValidated:
        return redirect('cloud:profile')

    userToUpdate = authenticate(username=request.user.username, password=request.POST['password'])
    if userToUpdate is not None:
        userToUpdate.email = request.POST["newEmail"]
        userToUpdate.save()
        return redirect('cloud:profile')
    
    request.session['updateError'] = 'Wrong Password'
    return redirect('cloud:profile')

@login_required
def update_password(request):
    passwordValidated = validateRegisterPassword(request, 'updateError', 'newPassword')
    if passwordValidated:
        return redirect('cloud:profile')

    userToUpdate = authenticate(username=request.user.username, password=request.POST['password'])
    if userToUpdate is not None:
        userToUpdate.set_password(request.POST['newPassword'])
        userToUpdate.save()
        update_session_auth_hash(request, userToUpdate)
        return redirect('cloud:profile')
    
    request.session['updateError'] = 'Wrong Password'
    return redirect('cloud:profile')

@login_required
def delete_account(request):
    userAuthentication = authenticate(username=request.POST['username'], password=request.POST['password'])
    if userAuthentication is None:
        request.session['updateError'] = 'Wrong Credentials'
        return redirect('cloud:profile')

    userConfirm = compareUsers(request.user, userAuthentication)
    if not userConfirm:
        request.session['updateError'] = 'Wrong Credentials'
        return redirect('cloud:profile')

    userToDelete = User.objects.get(pk=request.user.pk)
    userToDelete.delete()
    return redirect('cloud:landing_page')
    

def compareUsers(user1, user2):
    return user1.pk == user2.pk


def page_not_found(request, exception):
    return render(request, '404.html', status = 404)


