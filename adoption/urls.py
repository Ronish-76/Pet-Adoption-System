from django.urls import path
from . import views

urlpatterns = [
    # User endpoints
    path('', views.AdoptionRequestListView.as_view(), name='adoption-list'),
    path('<int:pk>/', views.AdoptionRequestDetailView.as_view(), name='adoption-detail'),
    path('history/', views.user_adoption_history, name='adoption-history'),
    
    # Admin endpoints
    path('admin/', views.AdminAdoptionRequestListView.as_view(), name='admin-adoption-list'),
    path('admin/<int:pk>/', views.AdminAdoptionRequestDetailView.as_view(), name='admin-adoption-detail'),
    path('admin/statistics/', views.adoption_statistics, name='adoption-statistics'),
    path('admin/bulk-update/', views.bulk_update_adoptions, name='bulk-update-adoptions'),
    
    # Shelter endpoints
    path('shelter/', views.shelter_adoption_requests, name='shelter-adoption-requests'),
    path('<int:request_id>/approve/', views.approve_adoption_request, name='approve-adoption-request'),
    path('<int:request_id>/reject/', views.reject_adoption_request, name='reject-adoption-request'),
    
    # Update adoption request status
    path('<int:pk>/update/', views.AdoptionRequestUpdateView.as_view(), name='adoption-update'),
] 