from django.urls import path
from . import views

app_name = 'pets'
 
urlpatterns = [
    # Public endpoints
    path('', views.PetListView.as_view(), name='pet-list'),
    path('featured/', views.featured_pets, name='featured-pets'),
    path('statistics/', views.pet_statistics, name='pet-statistics'),
    path('search/', views.search_pets, name='search-pets'),
    path('<int:pk>/', views.PetDetailView.as_view(), name='pet-detail'),
    
    # Admin endpoints
    path('create/', views.PetCreateView.as_view(), name='pet-create'),
    path('<int:pk>/update/', views.PetUpdateView.as_view(), name='pet-update'),
    path('<int:pk>/delete/', views.PetDeleteView.as_view(), name='pet-delete'),
    
    # Shelter endpoints
    path('shelter/', views.shelter_pets, name='shelter-pets'),
    path('shelter/adoptions/', views.shelter_adoption_requests, name='shelter-adoption-requests'),
] 