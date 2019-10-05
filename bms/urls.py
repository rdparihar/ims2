from django.urls import path, include
from django.views.generic import TemplateView
from . import views

# urls of the app_users
urlpatterns = [
    # path('', views.IndexView.as_view()),
    # path('', TemplateView.as_view(template_name='home.html'), name="home"),
    path('', views.HomeView, name="home"),
    path('category/', TemplateView.as_view(template_name='categories.html'), name="category"),
    path('brand/', TemplateView.as_view(template_name='brands.html'), name="brand"),
    # path('brand/(?<id>.+)/$', TemplateView.as_view(template_name='brand.html'), name="brand"),
    path('home/', views.AdminView.as_view(), name='admin-home'),
    path('home/<int:pk>', views.AdminDetailsView.as_view(), name='admin-detail'),
    path('shop/', views.ShopListView.as_view(), name='shop'),
    path('shop/<int:pk>', views.ShopDetailView.as_view(), name='stock-detail'),
    # path('shop/', TemplateView.as_view(template_name='shop.html'), name="shop"),
    path('invoice/', TemplateView.as_view(template_name='invoices.html'), name="invoice"),
    path('quantity/', TemplateView.as_view(template_name='quantities.html'), name="quantity"),
    path('shift/', TemplateView.as_view(template_name='shifts.html'), name="shift"),
    # path('account/', TemplateView.as_view(template_name='registration/login.html'), name="account"),
    path('user/', TemplateView.as_view(template_name='user.html'), name="user"),  
    path('new/', TemplateView.as_view(template_name='new.html'), name="new"),  
    path('created/', TemplateView.as_view(template_name='created.html'), name="created"),  
    
    path('error/', TemplateView.as_view(template_name='error.html'), name="error"),  
    path('test/', TemplateView.as_view(template_name='test.html')),
]