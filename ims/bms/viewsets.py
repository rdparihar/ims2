from django.shortcuts import render
from .models import Category, Brand, Shop, Invoice, Quantity, Shift , BmsUser
from django.contrib.auth.models import User
from rest_framework import viewsets, filters
# from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CategorySerializer, BrandSerializer, ShopSerializer, InvoiceSerializer, QuantitySerializer, ShiftSerializer
from .serializers import BmsUserSerializer , UserSerializer
from .serializers import ReadCategorySerializer, ReadBrandSerializer, ReadShopSerializer, ReadInvoiceSerializer, ReadQuantitySerializer, ReadShiftSerializer
from .serializers import ReadBmsUserSerializer , ReadUserSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from .models import StockOpen
from .serializers import StockOpenSerializer , ReadStockOpenSerializer
from .models import StockClose
from .serializers import StockCloseSerializer , ReadStockCloseSerializer, BrandDetailSerializer
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend




class CategoryViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = Category.objects.all().order_by('category_id')
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadCategorySerializer
        elif self.request.method == 'POST' or 'PUT':
            return CategorySerializer
        else:
            return ReadCategorySerializer
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category_id', 'category_name', 'category_description')


class BrandViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = Brand.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadBrandSerializer
        elif self.request.method == 'POST' or 'PUT':
            return BrandSerializer
        else:
            return ReadBrandSerializer
    serializer_class = BrandSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['category_id__category_id','brand_name',]


class BrandDetailViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = Brand.objects.all()
    
        
    serializer_class = BrandDetailSerializer
     
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand_id', 'category_id', 'brand_name']

class UserViewSet(LoginRequiredMixin,viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadUserSerializer
        elif self.request.method == 'POST':
            return UserSerializer
        else:
            return ReadUserSerializer
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['username','user_id', ]
   
class BmsUserViewSet(LoginRequiredMixin,viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = BmsUser.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BmsUserSerializer
        elif self.request.method == 'POST' or 'PUT':
            return BmsUserSerializer
        else:
            return ReadBmsUserSerializer
    serializer_class = BmsUserSerializer

class ShopViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = Shop.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadShopSerializer
        elif self.request.method == 'POST' or 'PUT':
            return ShopSerializer
        else:
            return ReadShopSerializer
    serializer_class = ShopSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('shop_name', 'shop_keeper', 'shop_address', 'shop_admin')

class QuantityViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = Quantity.objects.all().order_by('quantity_bottles')
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadQuantitySerializer
        elif self.request.method == 'POST':
            return QuantitySerializer
        else:
            return ReadQuantitySerializer
    serializer_class = QuantitySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('quantity_name', 'quantity_bottles')



class ShiftViewSet(LoginRequiredMixin,viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = Shift.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShiftSerializer
        elif self.request.method == 'POST':
            return ShiftSerializer
        else:
            return ReadShiftSerializer
    serializer_class = ShiftSerializer 
    filter_backends = (filters.SearchFilter,)
    search_fields = ['brand_id__brand_id','stock_shift_date','stock_shift_from','stock_shift_to__shop_id']

class InvoiceViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = Invoice.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InvoiceSerializer
        elif self.request.method == 'POST':
            return InvoiceSerializer
        else:
            return ReadInvoiceSerializer
    serializer_class = InvoiceSerializer
    filter_backends = (filters.SearchFilter,)
    # search_fields = ['brand_id__brand_id']
 
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand_id', 'invoice_date']

# class TodayInvoiceViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
#     login_url = settings.LOGIN_REDIRECT_URL
#     queryset = Invoice.objects.all()
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return InvoiceSerializer
#         elif self.request.method == 'POST':
#             return InvoiceSerializer
#         else:
#             return ReadInvoiceSerializer
#     serializer_class = InvoiceSerializer
#     filter_backends = (filters.SearchFilter,)
#     # search_fields = ['brand_id__brand_id']
 
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['brand_id__brand_id', 'invoice_date']

class StockOpenViewSet(LoginRequiredMixin,viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = StockOpen.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StockOpenSerializer
        elif self.request.method == 'POST':
            return StockOpenSerializer
        else:
            return ReadStockOpenSerializer
    serializer_class = StockOpenSerializer
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('brand_id__brand_id','open_date')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand_id', 'open_date', 'open_shop_id']



class StockCloseViewSet(LoginRequiredMixin,viewsets.ModelViewSet):
    login_url = settings.LOGIN_REDIRECT_URL
    queryset = StockClose.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadStockCloseSerializer
        elif self.request.method == 'POST':
            return StockCloseSerializer
        else:
            return ReadStockCloseSerializer
    serializer_class = StockCloseSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('brand_id','close_shop_id','close_date')
