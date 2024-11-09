from django.contrib import admin  # Import the admin module for the Django admin panel
from django.urls import path  # Import the path function to define URL patterns
from home import views  # Import views from the 'home' app (your views.py file)

urlpatterns = [
    path('admin/', admin.site.urls),  # Path for the Django admin panel
    path('', views.login_page, name='login'),  # Home (login) page
    path('signup/', views.signup_page, name='signup'),  # Sign up page
    path('logout/', views.logout_page, name='logout'),  # Logout page
    path('home/', views.home_page, name='home'),  # Home page (after login)
    path('about/', views.about, name='about'),  # About page
    path('adWeight/', views.addWeight, name='adWeight'),  # Page to add weight
    path('addedWeight/', views.addedWeight, name='addedWeight'),  # Page to view added weight entries
    path('update/<int:pk>/', views.weight_update, name='update'),  # Update a specific weight entry by ID
    path('delete/<int:pk>/', views.weight_delete, name='delete'),  # Delete a specific weight entry by ID
    path('weight-list/', views.weight_list, name='weight_list'),  # List all weight entries with pagination
    path('weight-loss/', views.weight_loss_calculator, name='weight_loss_calculator'),  # Weight loss calculator
]
