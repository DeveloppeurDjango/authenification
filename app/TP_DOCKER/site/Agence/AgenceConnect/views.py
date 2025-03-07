from django.shortcuts import render
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm


def home(request):
    return render(request, "home.html")



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            prenoms = form.cleaned_data['prenoms']
            email = form.cleaned_data['email']
            sujet = form.cleaned_data['sujet']
            message = form.cleaned_data['message']
            
         
            message_email = f"Nom: {nom}\nPrenoms: {prenoms}\nEmail: {email}\nSujet: {sujet}\nMessage: {message}"
       
            send_mail(
                'Nouveau message de contact',
                message_email,
                email,
                [''],
                fail_silently=False,
            )
            return render(request, 'confirmation.html')  
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})




def PageAccess(request):
    return render(request, "page_access.html")




def communique(request):
    return render(request, "communique.html")




    

    