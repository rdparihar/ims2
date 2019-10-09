from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.views import generic
from .models import Category, Brand, Shop, Invoice, Quantity, Shift , BmsUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime
import xlrd,xlwt,os
from xlutils.filter import process,XLRDReader,XLWTWriter
from .models import Category, Brand, Shop, Invoice, Quantity, Shift , BmsUser , StockOpen,StockClose


from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in



@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    request.session['isLoggedIn'] = True
    request.session['isAdmin'] = True
    request.session['isUser'] = True
    request.session['isSubAdmin'] = True
    request.session['email'] = user.email
    request.session['username'] = user.username
    request.session['is_super'] = user.is_superuser
    username  = request.session.get('username')
    request.session['userid'] = user.id
    request.session['isBmsUser'] = True
    request.session['isSuperUser'] = user.is_superuser

    # request.session['emp_id'] = EmpProfile.objects.filter(username_id__exact = request.user.id).values('emp_id')[0]['emp_id']
    
    isLoggedIn = request.session.get('isLoggedIn',False)
    isAdmin = request.session.get('isAdmin',False)
    isUser = request.session.get('isUser',False)
    isSubAdmin = request.session.get('isSubAdmin',False)
    isSuperUser = request.session.get('isSuperUser',False)

    email = request.session.get('email','')
    emp_id = request.session.get('emp_id')
    request.session.save()

    return render(
        request,
        'registration/login.html',
        context = {'isLoggedIn':isLoggedIn,'isAdmin':isAdmin,'isUser':isUser, 'isSubAdmin':isSubAdmin, 'email':email, 'emp_id':emp_id, 'isSuperUser':isSuperUser, },
    )






class ShopListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'shop_list'
    model = Shop
    queryset = Shop.objects.all()
    template_name = 'stocks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        isAdmin = self.request.session['isAdmin']
        isUser = self.request.session['isUser']
        isSubAdmin = self.request.session['isSubAdmin']
        isSuperUser = self.request.session['isSuperUser']

        context = { "isAdmin" : isAdmin, 'isUser':isUser, 'isSubAdmin':isSubAdmin, 'isSuperUser': isSuperUser}
       

        userid = self.request.user.id
        context['user'] = self.request.user
        context['bms_users'] = BmsUser.objects.all()
        print(isSuperUser)
        print(isSuperUser)


        if isAdmin or isSuperUser:
            context['shop_list'] = self.model.objects.all()
        else:
            if isSubAdmin:
                context['shop_list'] = self.model.objects.filter(shop_admin = userid)
            elif isUser:
                context['shop_list'] = self.model.objects.filter(shop_keeper = userid)
            else:
                pass
        
        return context
 
     
class ShopDetailView(LoginRequiredMixin, generic.DetailView):
    model = Shop
    template_name = "shop_details.html"
    
    def shop_detail_view(request, primary_key):
        shop = get_object_or_404(Shop, pk=primary_key)
        return render(request, context={'shop': shop})


class AdminView(LoginRequiredMixin, generic.ListView):
    model = BmsUser
    template_name = "home_page.html"
    login_url = '/login/'

    # def get(self, request):
        

    
    def get_context_data(self, **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        isAdmin = self.request.session['isAdmin']
        print(isAdmin)
        context = { "isAdmin" : isAdmin}

            
        # Add in a QuerySet of all the books
        context['bms_users'] = BmsUser.objects.all()
        context['bms_suadmin'] = BmsUser.objects.filter(user_role="S")
        return context

class AdminDetailsView(LoginRequiredMixin, generic.DetailView):
    def get(self, request, *args, **kwargs):
        list = Shop.objects.filter(shop_admin=kwargs['pk'])
        user= get_object_or_404(BmsUser, pk=kwargs['pk'])
        context= {'shop_list':list, 'b_user':user}
        return render (request, "subadmin_page.html", context)
    # model = BmsUser
    # template_name = "subadmin_page.html"
    # # login_url = '/login/'
     
    # def get_context_data(request, primary_key):
    #     sub = get_object_or_404(BmsUser, pk=primary_key)
    #     print(primary_key)
    #     shop_list = Shop.objects.filter(shop_admin = primary_key)
    #     print(shop_list)
    #     return render(request, context={'sub': sub, 'shop_list':shop_list, })


@login_required(login_url='/accounts/login/')
def HomeView(request, id=None):
    # user = get_object_or_404(User, id=id) 
    # user = get_object_or_404(User) 
    request.session['userid'] = request.user.id
    request.session['isSuperUser'] = request.user.is_superuser
    id = request.session.get('userid')
    isSuperUser = request.session.get('isSuperUser')
    isAdminUser = False  # create the user seesion for admin true
    isUser = False
    isSubAdmin = False
    request.session['isAdmin'] = isAdminUser
    request.session['isUser'] = isUser
    request.session['isSubAdmin'] = isSubAdmin
    print(id)
    bms_count=BmsUser.objects.filter(user_role = 'A').count()
    if bms_count ==0:
        return HttpResponseRedirect("/new/")
    try:
        bms_role=BmsUser.objects.filter(username = id).values('user_role')[0]['user_role']

        request.session['isBmsUser'] = True
    except:
        request.session['isBmsUser'] = True
        # context = {'isLoggedIn':isLoggedIn,}
        if isSuperUser:
            request.session['isSuperUser'] = True
            return HttpResponseRedirect("/home/")

        return HttpResponseRedirect("/error/")

    if bms_role =='A':
        print("You are admin")
        request.session['isBmsUser'] = True
        request.session['isAdmin'] = True
        return HttpResponseRedirect("/home/")
    else:
        # bms_role_s=BmsUser.objects.all().filter(username = id, user_role = 'S').values('user_role')[0]['user_role']
        if bms_role =='S':
            print ("you are subadmin ")
            request.session['isBmsUser'] = True
            request.session['isSubAdmin'] = True
            return HttpResponseRedirect("/shop/")
        else:
            request.session['isBmsUser'] = True
            request.session['isUser'] = True

            print("You are shopkeeper")
            return HttpResponseRedirect("/shop/")

        





def serve_file(path, filename):
    with open(path, "rb") as excel:
        data = excel.read()
    response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def copy2(wb):
    w = XLWTWriter()
    process( XLRDReader(wb,'unknown.xls'), w )
    return w.output[0][1], w.style_list

def update_content(dsreport_date,ds_shop_name):
    dst=  os.path.dirname(os.path.realpath(__file__)) +  '\DAY_SALE_REPORT_TEMPLATE.xls'
    rdbook = xlrd.open_workbook(dst, formatting_info=True)
    sheetx = 0
    rdsheet = rdbook.sheet_by_index(sheetx)
    wtbook, style_list = copy2(rdbook)
    wtsheet = wtbook.get_sheet(sheetx)

    shop_name_xf_index=rdsheet.cell_xf_index(0, 0)
    shop_name_style=style_list[shop_name_xf_index]
    category_name_xf_index=rdsheet.cell_xf_index(3, 1)
    category_name_style=style_list[category_name_xf_index]
    brand_code_xf_index=rdsheet.cell_xf_index(4, 0)
    brand_code_style=style_list[brand_code_xf_index]
    brand_name_xf_index=rdsheet.cell_xf_index(4, 1)
    brand_name_style=style_list[brand_name_xf_index]
    ob_qty_xf_index=rdsheet.cell_xf_index(4, 2)
    ob_qty_style=style_list[ob_qty_xf_index]
    receipt_qty_xf_index=rdsheet.cell_xf_index(4, 9)
    receipt_qty_style=style_list[receipt_qty_xf_index]
    cb_qty_xf_index=rdsheet.cell_xf_index(4, 16)
    cb_qty_style=style_list[cb_qty_xf_index]
    sb_qty_xf_index=rdsheet.cell_xf_index(4, 23)
    sb_qty_style=style_list[sb_qty_xf_index]
    mrp_rate_xf_index=rdsheet.cell_xf_index(4, 30)
    mrp_rate_style=style_list[mrp_rate_xf_index]
    sv_xf_index=rdsheet.cell_xf_index(4, 37)
    sv_style=style_list[sv_xf_index]

    dsreport_date = dsreport_date
    ds_shop_name = ds_shop_name
    dsreport_date = datetime.datetime.strptime(dsreport_date, '%Y-%m-%d').date()
    
    row_num=3
    category_rows = Category.objects.all().values('category_id', 'category_name')
    for category in category_rows:
        category_id=category['category_id']
        category_name=category['category_name']
        wtsheet.write(row_num, 1, category_name, category_name_style)  ## Col=1(always)
        row_num=row_num+1
        brand_rows = Brand.objects.all().filter(category_id = category_id).values('brand_id', 'brand_name')
        for brand in brand_rows:
            brand_id=brand['brand_id']
            brand_name=brand['brand_name']
            wtsheet.write(row_num, 0, brand_id, brand_code_style)  ## Col=1(always)
            wtsheet.write(row_num, 1, brand_name, brand_name_style)  ## Col=1(always)
            stock_opens = StockOpen.objects.all().filter(brand_id=brand_id,open_shop_id=ds_shop_name,open_date=dsreport_date).values()
            for stock_open in stock_opens:
                wtsheet.write(row_num, 2, stock_open['open_p'], ob_qty_style)
                wtsheet.write(row_num, 3, stock_open['open_q'], ob_qty_style)
                wtsheet.write(row_num, 4, stock_open['open_n'], ob_qty_style)
                wtsheet.write(row_num, 5, stock_open['open_d'], ob_qty_style)
                wtsheet.write(row_num, 6, stock_open['open_l'], ob_qty_style)
                wtsheet.write(row_num, 7, stock_open['open_xg'], ob_qty_style)
                wtsheet.write(row_num, 8, stock_open['open_y'], ob_qty_style)
            
            Quantity_Master = ['P','Q','N','D','L','XG','Y']
            qty_cnt=0
            for quantity in Quantity_Master:
                stock_receipts = Invoice.objects.all().filter(brand_id=brand_id,shop_id=ds_shop_name,invoice_date=dsreport_date,invoice_brand_size=quantity).values('invoice_brand_qty').first()
                if stock_receipts:
                    wtsheet.write(row_num, 9+qty_cnt, stock_receipts['invoice_brand_qty'], receipt_qty_style)
                    qty_cnt=qty_cnt+1

            stock_closes = StockClose.objects.all().filter(brand_id=brand_id,close_shop_id=ds_shop_name,close_date=dsreport_date).values()
            for stock_close in stock_closes:
                wtsheet.write(row_num, 16, stock_close['close_qty_p'], cb_qty_style)
                wtsheet.write(row_num, 17, stock_close['close_qty_q'], cb_qty_style)
                wtsheet.write(row_num, 18, stock_close['close_qty_n'], cb_qty_style)
                wtsheet.write(row_num, 19, stock_close['close_qty_d'], cb_qty_style)
                wtsheet.write(row_num, 20, stock_close['close_qty_l'], cb_qty_style)
                wtsheet.write(row_num, 21, stock_close['close_qty_xg'], cb_qty_style)
                wtsheet.write(row_num, 22, stock_close['close_qty_y'], cb_qty_style)
                wtsheet.write(row_num, 23, stock_close['close_sale_p'], sb_qty_style)
                wtsheet.write(row_num, 24, stock_close['close_sale_q'], sb_qty_style)
                wtsheet.write(row_num, 25, stock_close['close_sale_n'], sb_qty_style)
                wtsheet.write(row_num, 26, stock_close['close_sale_d'], sb_qty_style)
                wtsheet.write(row_num, 27, stock_close['close_sale_l'], sb_qty_style)
                wtsheet.write(row_num, 28, stock_close['close_sale_xg'], sb_qty_style)
                wtsheet.write(row_num, 29, stock_close['close_sale_y'], sb_qty_style)

            
            row_num=row_num+1
        row_num=row_num+1

    output_file=  os.path.dirname(os.path.realpath(__file__)) + '\DAY_SALE_REPORT.xls'         
    wtbook.save(output_file)

def dsreport(request):
    if request.method =="POST":
        dsreport_date = request.POST['dsreport_date']
        ds_shop_name = request.POST['ds_shop_name']
        update_content(dsreport_date,ds_shop_name)
        response = HttpResponse(content_type='application/ms-excel')
        path=  os.path.dirname(os.path.realpath(__file__)) +  '\DAY_SALE_REPORT.xls'             
        return serve_file(path, 'DAY_SALE_REPORT.xls')
    else:
        return render(request,'daily_sales_report.html') 