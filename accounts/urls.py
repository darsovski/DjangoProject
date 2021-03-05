from django.urls import path
from . import views


urlpatterns = [
    path('', views.home,name='home'),
    path('products', views.products,name='products'),
    path('custumer/<str:pk_test>/', views.custumer,name='custumer'),
    path('create_order',views.createOrder,name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('login',views.loginPage,name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register',views.registerPage,name='register'),
    path('api',views.apiOverview,name='api-overview'),
    path('api/product-list',views.productList,name='product-list'),
    path('api/product-detail/<str:pk>',views.productDetail,name='product-detail'),
    path('api/product-create', views.productCreate, name='product-create'),
    path('api/product-update/<str:pk>', views.productUpdate, name='product-update'),
    path('api/product-delete/<str:pk>', views.productDelete, name='product-delete'),

]
