from rest_framework import routers
from bms.viewsets import CategoryViewSet, BrandViewSet, ShopViewSet, InvoiceViewSet, QuantityViewSet, ShiftViewSet
from bms.viewsets import BmsUserViewSet,UserViewSet
from bms.viewsets import StockOpenViewSet, StockCloseViewSet, BrandDetailViewSet

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'brand-detail',BrandDetailViewSet)
router.register(r'shop', ShopViewSet)
router.register(r'invoice', InvoiceViewSet)
router.register(r'quantity', QuantityViewSet)
router.register(r'shift', ShiftViewSet)
router.register(r'user', UserViewSet)
router.register(r'bmsuser', BmsUserViewSet)
router.register(r'open', StockOpenViewSet)
router.register(r'close', StockCloseViewSet)
