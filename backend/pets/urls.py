from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_pets, name='get_pets'),
    path('create/', views.create_pet, name='create_pet'),
    path('<int:pet_id>/', views.get_pet_detail, name='get_pet_detail'),
    path('<int:pet_id>/availability/', views.check_pet_availability, name='check_pet_availability'),
    path('featured/', views.get_featured_pets, name='get_featured_pets'),
]