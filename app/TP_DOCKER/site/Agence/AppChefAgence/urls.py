from django.urls import path
from .views import AjoutListRetrait, OperateRetrait, SupprimerTousRetraités, Supprimer_Retraite, SupprimerTouteOperation, Supprimer_Retraite_Visualisation, VoirOperation, VoirListRetrait, Supprimer_Operation_Visualisation, ChefAgence,AfficherChampsAuto, Modification_Operation,Supprimer_Operation


urlpatterns = [
    path('',ChefAgence, name="chefagence"),
    path('ajout/', AjoutListRetrait, name="ajoutlistretraite"),
    path('voir_listretraite/', VoirListRetrait, name="voir_listretraite"),
    path('operate/', OperateRetrait, name="operateretraite"),
    path('voir_operation/', VoirOperation, name="voir_operation"),
    path('afficherchampsauto/',AfficherChampsAuto, name='afficherchampsauto'),
    path('modification_operation/<int:id>/', Modification_Operation, name='modification_operation'),
    path('supprimer_operation/<int:operation_id>/', Supprimer_Operation, name='suppression_operation'),
    path('supprimer_retraite/<int:operation_id>/', Supprimer_Retraite, name='supprimer_retraite'),
    path('supprimer_operation_visualisation/<int:operation_id>/', Supprimer_Operation_Visualisation, name='supprimer_operation_visualisation'),
    path('supprimer_retraite_visualisation/<int:operation_id>/', Supprimer_Retraite_Visualisation, name='supprimer_retraite_visualisation'),
    path('supprimer_toute_operation/', SupprimerTouteOperation, name='supprimer_toute_operation'),
    path('supprimer_tous_retraités/', SupprimerTousRetraités, name='supprimer_tous_retraités'),
  
 
    
  





    
    
    



     
  

]
