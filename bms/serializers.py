from .models import Category, Brand , Shop, Invoice, Quantity, Shift,BmsUser, StockOpen, StockClose
from django.contrib.auth.models import User
from rest_framework import serializers

class ReadCategorySerializer(serializers.HyperlinkedModelSerializer):
    category_id = serializers.ReadOnlyField()
    class Meta:
        model = Category
        fields = ['category_id','category_name','category_description']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    category_id = serializers.ReadOnlyField()
    class Meta:
        model = Category
        fields = ['category_id','category_name','category_description']


class ReadBrandSerializer(serializers.HyperlinkedModelSerializer):
    brand_id = serializers.ReadOnlyField()
    category_id = CategorySerializer()
    class Meta:
        model = Brand
        fields =  ['brand_id','brand_name','brand_code','category_id','brand_p_cost','brand_q_cost','brand_n_cost','brand_d_cost','brand_l_cost','brand_xg_cost','brand_y_cost','brand_p_sale','brand_q_sale','brand_n_sale','brand_d_sale','brand_l_sale','brand_xg_sale','brand_y_sale']

class BrandSerializer(serializers.ModelSerializer):
        brand_id = serializers.ReadOnlyField()
        category_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Category.objects.all())
        class Meta:
            model = Brand
            fields =  ['brand_id','brand_name','brand_code','category_id','brand_p_cost','brand_q_cost','brand_n_cost','brand_d_cost','brand_l_cost','brand_xg_cost','brand_y_cost','brand_p_sale','brand_q_sale','brand_n_sale','brand_d_sale','brand_l_sale','brand_xg_sale','brand_y_sale']

class BrandDetailSerializer(serializers.ModelSerializer):
    brand_id = serializers.ReadOnlyField()
    category_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Category.objects.all())
    class Meta:
        model = Brand
        fields =  ['brand_id','brand_name','brand_code','category_id','brand_p_cost','brand_q_cost','brand_n_cost','brand_d_cost','brand_l_cost','brand_xg_cost','brand_y_cost','brand_p_sale','brand_q_sale','brand_n_sale','brand_d_sale','brand_l_sale','brand_xg_sale','brand_y_sale']




class QuantitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quantity
        fields = ['quantity_name','quantity_bottles']



class ReadQuantitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quantity
        fields = ['quantity_name','quantity_bottles']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name','last_name', 'password', 'is_active']
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class ReadUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username','id', 'is_active']

class BmsUserSerializer(serializers.ModelSerializer):
    username = serializers.PrimaryKeyRelatedField(read_only=False, queryset=User.objects.all())
    class Meta:
            model = BmsUser
            fields = ['username','user_id','user_first_name','user_last_name','user_role']

class ReadBmsUserSerializer(serializers.HyperlinkedModelSerializer):
    username = UserSerializer()
    class Meta:
        model = BmsUser
        fields = ['username','user_id','user_first_name','user_last_name','user_role']

class ReadShopSerializer(serializers.HyperlinkedModelSerializer):
    shop_id = serializers.ReadOnlyField()
    shop_admin = BmsUserSerializer()
    class Meta: 
        model = Shop
        fields =   ['shop_id','shop_name', 'shop_keeper', 'shop_address','shop_admin']

class ShopSerializer(serializers.HyperlinkedModelSerializer):
    shop_id = serializers.ReadOnlyField()
    shop_admin = serializers.PrimaryKeyRelatedField(read_only=False, queryset=BmsUser.objects.all())
    class Meta:
        model = Shop
        fields =   ['shop_id','shop_name', 'shop_keeper', 'shop_address','shop_admin']


class ReadShiftSerializer(serializers.HyperlinkedModelSerializer):
    brand_id = BrandSerializer()
    stock_shift_to = ShopSerializer()
    class Meta:
        model = Shift
        fields = ['brand_id','stock_shift_date','stock_shift_from','stock_shift_to','stock_shift_p','stock_shift_q','stock_shift_n','stock_shift_d','stock_shift_l','stock_shift_xg','stock_shift_y']

class ShiftSerializer(serializers.HyperlinkedModelSerializer):
    brand_id =  serializers.PrimaryKeyRelatedField(read_only=False, queryset=Brand.objects.all())
    stock_shift_to =  serializers.PrimaryKeyRelatedField(read_only=False, queryset=Shop.objects.all())
    class Meta:
        model = Shift
        fields = ['brand_id','stock_shift_date','stock_shift_from','stock_shift_to','stock_shift_p','stock_shift_q','stock_shift_n','stock_shift_d','stock_shift_l','stock_shift_xg','stock_shift_y']



class ReadInvoiceSerializer(serializers.HyperlinkedModelSerializer):
    invoice_transaction_id = serializers.ReadOnlyField()
    shop_id = ShopSerializer()
    brand_id = BrandSerializer()
    category_id = CategorySerializer()
    class Meta:
        model = Invoice
        fields =   ['invoice_transaction_id','shop_id','brand_id', 'invoice_date','category_id','invoice_brand_size','invoice_brand_qty','invoice_rate_per_case','invoice_no_of_cases','invoice_total']

class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    invoice_transaction_id = serializers.ReadOnlyField()
    shop_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Shop.objects.all())
    brand_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Brand.objects.all())
    category_id = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Category.objects.all())
    class Meta:
        model = Invoice
        fields =   ['invoice_transaction_id','shop_id','brand_id', 'invoice_date','category_id','invoice_brand_size','invoice_brand_qty','invoice_rate_per_case','invoice_no_of_cases','invoice_total']


class ReadStockOpenSerializer(serializers.HyperlinkedModelSerializer):
    brand_id = BrandSerializer()
    open_shop_id = ShopSerializer()
    class Meta:
        model = StockOpen
        fields = ['brand_id','open_shop_id','open_date','open_p','open_q','open_n','open_d','open_l','open_xg','open_y']

class StockOpenSerializer(serializers.HyperlinkedModelSerializer):
    brand_id =  serializers.PrimaryKeyRelatedField(read_only=False, queryset=Brand.objects.all())
    open_shop_id =  serializers.PrimaryKeyRelatedField(read_only=False, queryset=Shop.objects.all())
    class Meta:
        model = StockOpen
        fields = ['brand_id','open_shop_id','open_date','open_p','open_q','open_n','open_d','open_l','open_xg','open_y']






class ReadStockCloseSerializer(serializers.HyperlinkedModelSerializer):
    brand_id = BrandSerializer()
    category_id = CategorySerializer()
    close_shop_id = ShopSerializer()
    class Meta:
        model = StockClose
        fields = ['brand_id','category_id','close_shop_id','close_date','close_qty_p','close_qty_q','close_qty_n','close_qty_d','close_qty_l','close_qty_xg','close_qty_y','close_sale_p','close_sale_q','close_sale_n','close_sale_d','close_sale_l','close_sale_xg','close_sale_y','total_sale']

class StockCloseSerializer(serializers.HyperlinkedModelSerializer):
    brand_id =  serializers.PrimaryKeyRelatedField(read_only=False, queryset=Brand.objects.all())
    category_id =  serializers.PrimaryKeyRelatedField(read_only=False, queryset=Category.objects.all())
    close_shop_id =  serializers.PrimaryKeyRelatedField(read_only=False, queryset=Shop.objects.all())
    class Meta:
        model = StockClose
        fields = ['brand_id','category_id','close_shop_id','close_date','close_qty_p','close_qty_q','close_qty_n','close_qty_d','close_qty_l','close_qty_xg','close_qty_y','close_sale_p','close_sale_q','close_sale_n','close_sale_d','close_sale_l','close_sale_xg','close_sale_y','total_sale']