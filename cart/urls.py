from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_transfer, name='search_transfer'),
    path('add_to_cart/<int:option_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('search/', views.search_transfer, name='search_transfer'),
    path('view_cart/', views.view_cart, name='view_cart'),
]

