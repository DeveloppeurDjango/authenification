from django.urls import path
from .views import CreatedPDF, upload_excel, ExportExcel, Print


urlpatterns = [

    path('pdf', CreatedPDF, name='created_pdf'),
    path('Excel', ExportExcel, name='export_excel'),
    path('print', Print, name='print'),
    path('upload_excel/', upload_excel, name='upload_excel'),




]
