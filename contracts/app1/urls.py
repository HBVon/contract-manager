from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notaires', views.notaires, name='notaires'),
        path('contrats', views.contrats, name='contrats'),
    path('q', views.q, name='home'),
    path('create_notaire', views.newnotaire, name='gogo'),
    path('location/', views.location_view, name='location'),
    path('get_location_details/', views.get_location_details, name='get_location_details'),
       path('notaire/<int:id>/', views.notaire_detail, name='notaire_detail'),
       path('notaire/search/', views.notaire_search, name='notaire_search'),
              path('site/search/', views.site_search, name='site_search'),
        path('ccreate-notaire/', views.create_notaire, name='create_notaire'),
                path('inst/', views.instance_generator, name='inst'),
    path('sites', views.sites, name='sitess'),
        path('site/<int:id>/', views.site_detail, name='site_detail'),
            path('site', views.setnprofile, name='siteprof'),
                path('create-site/', views.create_site, name='create_site'),
                path('site/modify/<int:id>', views.mod_site, name='modsitee'),
                path('site/update/<int:id>/', views.update_site, name='update_site'),
        path('delete-site/<int:site_id>/', views.delete_site, name='delete_site'),
                    path('contrats/search/', views.contrat_search, name='contrat_search'),
            path('contrat/<int:id>/', views.contrat_detail, name='contrat_detail'),
            path('contract/<int:contrat_id>/renew/', views.renew_contract, name='renew_contract'),
            
    # Other URL patterns
    path('statistics/', views.calculate_statistics, name='calculate_statistics'),
                path('con', views.contrat_new, name='cnew'),
                                path('conm/<int:id>/', views.contratmod, name='cnemw'),
            path('notaire/modify/<int:id>', views.mod_notaire, name='modnot'),
             path('notaire/update/<int:id>/', views.update_notaire, name='update_notaire'),
        path('delete-notaire/<int:not_id>/', views.delete_notaire, name='delete_notaire'),
                    path('ncontrat', views.contnprofile, name='contt'),
                    path('create-contrat/', views.create_contrat, name='create_contrat'),

                    path('delete-contrat/<int:c_id>/', views.delete_contrat, name='delete_contrat'),
                    path('nbail', views.bailnprofile, name='baill'),
                        path('create-bail/', views.create_bail, name='create_bail'),

]