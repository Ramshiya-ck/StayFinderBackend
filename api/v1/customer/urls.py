from django.urls import path
from api.v1.customer import views

urlpatterns=[
    # Authentication
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    
    # Customer Management
    path('customers/', views.customers, name='customers'),

    # Profile Management
    path('profile/', views.profile, name='profile_list'),  # Get all profiles
    path('profile/create/', views.profile_create, name='profile_create'),  # Create new profile
    path('profile/<int:profile_id>/', views.profile_detail, name='profile_detail'),  # Get single profile
    path('profile/<int:profile_id>/update/', views.profile_update, name='profile_update'),  # Update profile
    path('profile/<int:profile_id>/delete/', views.profile_delete, name='profile_delete'),  # Delete profile

    # Public endpoints
    path('index/', views.index, name='index'),
    path('slider/', views.slider, name='slider'),
]
