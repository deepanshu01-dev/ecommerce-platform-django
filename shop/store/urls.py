from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('logout/', views.logout, name='logout'),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search', views.search, name='search'),
]
