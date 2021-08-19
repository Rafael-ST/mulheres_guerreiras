from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('cadastro-proponente/', views.cadastro_proponente, name="cadastro_proponente"),
    path('cadastro-proposta/', views.cadastro_proposta, name="cadastro_proposta"),
    path('cadastro-contrato/', views.cadastro_contrato, name="cadastro_contrato"),
    path('to_pdf/(?P<contrato>[0-9]+)$', views.to_pdf, name="to_pdf"),
    path('cadastro-investimento/', views.cadastro_investimento, name="cadastro_investimento"),
    path('delete-investimento/<uuid:pk>/', views.delete_investimento, name='delete_investimento'),

    path('ajax/load-atividades/', views.load_atividades, name='ajax_load_atividades'),
    path('export-proposta-pdf/', views.export_proposta_pdf, name="export_proposta_pdf"),
    path('export_proposta_pdf_prop/', views.export_proposta_pdf_prop, name="export_proposta_pdf_prop"),
    path('entrega-chip/', views.entrega_chip, name="entrega_chip"),

    path('submeter-proposta/', views.submeter_proposta, name="submeter_proposta"),
    path('submeter-proponente/', views.submeter_proponente, name="submeter_proponente"),

    path('inscricao/', views.inscricao, name='inscricao'),
    path('cancelar_inscricao/', views.cancelar_inscricao, name='canecelar_inscricao')

]