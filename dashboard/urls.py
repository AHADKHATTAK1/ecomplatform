from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Store-specific dashboard URLs
    path('store/<slug:store_slug>/', views.store_dashboard, name='store_dashboard'),
    path('store/<slug:store_slug>/products/', views.store_manage_products, name='store_products'),
    path('store/<slug:store_slug>/products/add/', views.store_add_product, name='store_add_product'),
    path('store/<slug:store_slug>/category/add/', views.store_add_category, name='store_add_category'),
    path('store/<slug:store_slug>/products/edit/<int:product_id>/', views.store_edit_product, name='store_edit_product'),
    path('store/<slug:store_slug>/products/delete/<int:product_id>/', views.store_delete_product, name='store_delete_product'),
    path('store/<slug:store_slug>/orders/', views.store_manage_orders, name='store_orders'),
    path('store/<slug:store_slug>/orders/<int:order_id>/', views.store_view_order, name='store_view_order'),
    path('store/<slug:store_slug>/orders/<int:order_id>/update/', views.store_update_order_status, name='store_update_order_status'),
    path('store/<slug:store_slug>/customize/', views.store_customize, name='store_customize'),
]
