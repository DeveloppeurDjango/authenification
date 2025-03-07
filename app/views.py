from django.shortcuts import render, redirect
from authentification import settings
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.

def home(request):
    return render(request, 'app/index.html')



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if User.objects.filter(username=username):
            messages.error(request, 'Ce nom existe deja')
            return redirect('register')
        
        if User.objects.filter(email=email):
            messages.error(request, 'Ce email est deja utilisé')
            return redirect('register')
        
        if not username.isalnum():
            messages.error(request, 'Le nom doit etre alphanumeric')
            return redirect('register')
        
        if  password != password1:
            messages.error(request, 'Les deux mots de passe sont differents!')
            return redirect('register')
        
        mon_utilisateur = User.objects.create_user(username, email, password)
        mon_utilisateur.first_name = firstname
        mon_utilisateur.last_name = lastname
        mon_utilisateur.save()
        messages.success(request, 'Votre compte a été créé avec succès!')
        subject = "Bienvenue sur notre application"
        message = "Bienvenue "+ mon_utilisateur.last_name+ "\n Nous sommes heureux de vous compter parmi nous\n\n\n Merci!!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [mon_utilisateur.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        return redirect('login')
        
        
    return render(request, 'app/register.html')

def logIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'app/index.html', {'firstname':firstname})
        else:
            messages.error(request, 'Mauvaise authentification')
            return redirect('login')
        
    return render(request, 'app/login.html')

def logOut(request):
    logout(request)
    messages.success(request, 'Vous avez ete bien deconnecté')
    return redirect('home')