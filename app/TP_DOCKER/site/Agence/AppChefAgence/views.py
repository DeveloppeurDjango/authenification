from django.shortcuts import render, redirect, get_object_or_404
from .models import ListRetraite, OperateRetraite
from .forms import ListRetraiteForm, OperateRetraiteForm
from django.http import JsonResponse
from django.http import HttpResponseBadRequest 
from django.core.paginator import Paginator
from django.db.models import Sum
from django.db.models import Count






#fonction pour la page d'accueil

def ChefAgence(request):
   
    listretraite_par_ville = ListRetraite.objects.values('ville').annotate(nombre_retraites=Count('id'))

    total_retraites = ListRetraite.objects.aggregate(total_retraites=Count('id'))
    
    total_operation = OperateRetraite.objects.aggregate(total_operation=Count('id'))
    

    operate_retraites = OperateRetraite.objects.all()
    
    
    montant_inf_100000 = operate_retraites.filter(montant__lt=100000).count()
    
    montant_100000_300000 = operate_retraites.filter(montant__range=[100000, 300000]).count()
    
    montant_300000_600000 = operate_retraites.filter(montant__range=[300000, 600000]).count()
    
    montant_sup_600000 = operate_retraites.filter(montant__gte=600000).count()


    context = {
        
        'listretraite_par_ville': listretraite_par_ville,
        
        'total_retraites': total_retraites['total_retraites'], 
        
        'operate_retraites': operate_retraites,



        'montant_inf_100000': montant_inf_100000,
        
        'montant_100000_300000': montant_100000_300000,
        
        'montant_300000_600000': montant_300000_600000,
        
        'montant_sup_600000': montant_sup_600000,
        
        'total_operation': total_operation['total_operation'], 
    }

    return render(request, 'Home_branch_manage.html', context)



#fonction pour ajouter un retraité


def AjoutListRetrait(request):

    
    if request.method == 'POST':
        
        form = ListRetraiteForm(request.POST)
        
        if form.is_valid():
            
            form.save()
        else:
            
            form = ListRetraiteForm()
          
    else:
        
        form = ListRetraiteForm()
        
    
    Listeretraire = ListRetraite.objects.order_by('-created_at')[:3]
    
    context = {'form': form, 'operate': Listeretraire}
    
    return render(request, 'Add_retired.html', context)



#fonction pour ajourter une operation

def OperateRetrait(request):
    
    if request.method == 'POST':
        
        form = OperateRetraiteForm(request.POST)
        
        if form.is_valid():
            
            form.save()
    else:
        
        form = OperateRetraiteForm()
    

    operations = OperateRetraite.objects.order_by('-date_operation')[:3]

    beneficiaire = ''
    
    nni = ''
    
    if 'Numero_titre' in request.GET:
        
        numero_titre_id = request.GET.get('Numero_titre')
        
        if numero_titre_id:
            
            numero_titre = ListRetraite.objects.get(id=numero_titre_id)
            
            beneficiaire = numero_titre.beneficiaire
            
            nni = numero_titre.nni
            
            form.initial['beneficiaire'] = beneficiaire
            
            form.initial['nni'] = nni
    
    context = {'form': form, 'operate': operations, 'beneficiaire': beneficiaire, 'nni': nni}
    
    return render(request, 'Add_operation.html', context)



#fonction pour voir la liste des retraités

def VoirListRetrait(request):
    
    listretraite = ListRetraite.objects.all()
    
    paginator = Paginator(listretraite, 10)  
    
    page_number = request.GET.get('page')
    
    operate = paginator.get_page(page_number)
    
    return render(request, 'View_list_retired.html', {'operate': operate})



#fonction pour voir la liste des operations


def VoirOperation(request):

    operations = OperateRetraite.objects.all()


    paginator = Paginator(operations, 50)  
    
    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

 
    total_montant = operations.aggregate(total_montant=Sum('montant'))['total_montant']

    if total_montant is None:
        
        total_montant = 0

    return render(request, 'View_list_operation.html', { 'page_obj': page_obj,  'total_montant': total_montant})




#fonction pour reucperer des champs beneficiaire et nni  et les affichés automatiquement

def AfficherChampsAuto(request):
    
    numero_titre_id = request.GET.get('Numero_titre')
    
    if numero_titre_id:
        
        numero_titre = ListRetraite.objects.get(id=numero_titre_id)
        
        beneficiaire = numero_titre.beneficiaire
        
        nni = numero_titre.nni
        
        return JsonResponse({'beneficiaire': beneficiaire, 'nni': nni})
    
    else:
        
        return JsonResponse({'error': 'No data found'})
    


#fonction pour la modification d'une operation

def Modification_Operation(request, id):
    
    if request.method == 'POST':
        
        identifiant = OperateRetraite.objects.get(pk=id)
        
        form = OperateRetraiteForm(request.POST, instance=identifiant)
        
        if form.is_valid():
            
            form.save()
            
        return redirect('operateretraite')
    else:
        identifiant = OperateRetraite.objects.get(pk=id)
        
        form = OperateRetraiteForm(instance=identifiant)
           

    operations = OperateRetraite.objects.all()[:10]

    beneficiaire = ''
    
    nni = ''
    
    if 'Numero_titre' in request.GET:
        
        numero_titre_id = request.GET.get('Numero_titre')
        
        if numero_titre_id:
            
            numero_titre = ListRetraite.objects.get(id=numero_titre_id)
            
            beneficiaire = numero_titre.beneficiaire
            
            nni = numero_titre.nni
            

            form.initial['beneficiaire'] = beneficiaire
            
            form.initial['nni'] = nni
    
    context = {'form': form, 'operate': operations, 'beneficiaire': beneficiaire, 'nni': nni}
    
    return render(request, 'Update_operation.html', context)



#fonction pour la suppression d'une operation

def Supprimer_Operation(request, operation_id):
    
    operation = get_object_or_404(OperateRetraite, pk=operation_id)
    
    if request.method == 'POST':
        
        operation.delete()
        
        return redirect('operateretraite')  
    
    return HttpResponseBadRequest("Méthode non autorisée")




#fonction pour supprimer toutes les operations

def SupprimerTouteOperation(request):

    OperateRetraite.objects.all().delete()
    
    return redirect('voir_operation') 



#fonction pour supprimer une operation lorsqu'on est sur la page de visualisation

def Supprimer_Operation_Visualisation(request, operation_id):
    
    operation = get_object_or_404(OperateRetraite, pk=operation_id)
    
    if request.method == 'POST':
        
        operation.delete()
        
        return redirect('voir_operation')  
    
    return HttpResponseBadRequest("Méthode non autorisée")




#fonction pour la modification d'un retraité

def Modification_Retraite(request, id):
    
    if request.method == 'POST':
        
        identifiant = ListRetraite.objects.get(pk=id)
        
        form = ListRetraiteForm(request.POST, instance=identifiant)
        
        if form.is_valid():
            
            form.save()
        return redirect('voir_listretraite')
    else:
        identifiant = ListRetraite.objects.get(pk=id)
        
        form = ListRetraiteForm(instance=identifiant)
        
        

    listeretraite = ListRetraite.objects.all()

    context = {'form': form, 'operate': listeretraite}
    
    return render(request, 'Update_operation.html', context)



#fonction pour supprimer un retraité

def Supprimer_Retraite(request, operation_id):
    
    listeretraite = get_object_or_404(ListRetraite, pk=operation_id)
    
    if request.method == 'POST':
        
        listeretraite.delete()
        
        return redirect('ajoutlistretraite')  
    
    return HttpResponseBadRequest("Méthode non autorisée")


#fonction pour supprimer tous les retraités 

def SupprimerTousRetraités(request):

    ListRetraite.objects.all().delete()
    
    return redirect('voir_listretraite') 


#fonction pour supprimer les retraité lorsqu'on est sur la page de visualisation

def Supprimer_Retraite_Visualisation(request, operation_id):
    
    operation = get_object_or_404(ListRetraite, pk=operation_id)
    
    if request.method == 'POST':
        
        operation.delete()
        
        return redirect('voir_listretraite')  
    
    return HttpResponseBadRequest("Méthode non autorisée")

