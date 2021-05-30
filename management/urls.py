from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from management import views

router = routers.SimpleRouter()

router.register(r'Machines', views.MachineViewSet, basename="machines_list")
router.register(r'MainPacks', views.MainPackViewSet, basename="main_packs_list")
router.register(r'Technicians', views.TechnicianViewSet, basename="technicians_list")
router.register(r'Filters', views.FilterViewSet, basename="filters_list")
router.register(r'Cases', views.CaseViewSet, basename="cases_list")
router.register(r'Product', views.ProductViewSet, basename="product_list")

urlpatterns = [path('update_technicien_info/', views.update_technicien_info),
               path('update_main_pack_info/', views.update_main_pack_info),
               path('update_filter_info/', views.update_filter_info),
               path('machine_search/', views.machine_search),
               path('list_machine_client/', views.list_machine_client),
               path('list_case_client/', views.list_case_client),
               path('list_code_client/', views.list_code_client),
               path('machine_search_client/', views.machine_search_client),
               path('client_name_and_id/', views.client_name_and_id),
               path('update_machine_info/', views.update_machine_info),
               path('update_case_info/', views.update_case_info),
               path('update_product_info/', views.update_product_info),

               ]
urlpatterns += router.urls
