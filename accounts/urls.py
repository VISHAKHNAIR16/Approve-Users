from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('approve_users/', views.approve_users, name='approve_users'),
    path('hello_world/', views.hello_world, name='hello_world'),
    path('search/', include("cart.urls"), name='search_transfer'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # New admin dashboard URL
    path('add_listing/', views.add_listing, name='add_listing'), # URL to add listing
    path('remove_listing/<int:listing_id>/', views.remove_listing, name='remove_listing'),  # Remove Listing
    path('logout/', views.logout_view, name='logout'),  # Logout

]
