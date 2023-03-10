from django.http import JsonResponse
from django.shortcuts import redirect, render, reverse
from store.forms import FormContact, FormUser, FormUserProfileInfo
from store.models import Contact, Product, SubCategory
from django.core.paginator import Paginator
from cart.cart import Cart
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions
from store.serializers import ProductSerializer
from urllib.parse import urlencode
import pandas as pd
import re
import os
from django.conf import settings


# Create your views here.
def index(request):
    cart = Cart(request)
    tbgd_subcategory = SubCategory.objects.filter(category=1).values_list('id')
    ddnb_subcategory = SubCategory.objects.filter(category=2).values_list('id')
    tbgd_list_sub = []
    ddnb_list_sub = []
    for sub in tbgd_subcategory:
        tbgd_list_sub.append(sub[0])

    for sub in ddnb_subcategory:
        ddnb_list_sub.append(sub[0])
    tbdg_products = Product.objects.filter(subcategory__in=tbgd_list_sub).order_by('-public_day')
    ddnb_products = Product.objects.filter(subcategory__in=tbgd_list_sub).order_by('-public_day')
    return render(request, 'store/index.html', {
        'tbgd_products': tbdg_products[:21], 
        'ddnb_products': ddnb_products[:21],
        'cart': cart,
        })


def formcontact(request):
    cart = Cart(request)
    result = ''
    form = FormContact()
    if request.POST.get('btnSendMessage'):
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()

            result = '''
                <div class="alert alert-success" role="alert">
                    Submit Successfully!!!
                </div>
            '''
    return render(request, 'store/contact.html', {
        'result': result,
        'form': form,
        'cart': cart,
    })


def productdetail(request, pk):
    cart = Cart(request)
    product = Product.objects.get(pk=pk)
    sub_category_id = Product.objects.filter(pk=pk).values_list('subcategory')
    list_sub = []
    for sub in sub_category_id:
        list_sub.append(sub[0])
    same_products = Product.objects.filter(subcategory__in=sub_category_id).exclude(id=pk)
    sub_cats = SubCategory.objects.all()
    sub_cat_name = SubCategory.objects.get(id__in=sub_category_id)

    rules = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'analysis/rules.csv'), squeeze=True, index_col=0)
    lst = rules.values.tolist()

    list_rules = []
    for item in lst:
        if str(pk) in re.findall('\d+[, \d+]*', item[0])[0].split(','):
            list_rules = re.findall('\d+[, \d+]*', item[1])[0].split(',')
    list_asc_products = []
    for i in list_rules:
        list_asc_products.append(Product.objects.get(pk=int(i)))

    
    return render(request, 'store/product-detail.html', {
        'product': product,
        'sub_cats': sub_cats,
        'same_products': same_products,
        'sub_cat_name': sub_cat_name,
        'cart': cart,
        'list_asc_products': list_asc_products,
    })


def productlist(request, pk):
    cart = Cart(request)
    sub_cats = SubCategory.objects.all()
    if pk == 0:
        products = Product.objects.all().order_by('-public_day')
        sub_name = 'T???t c??? s???n ph???m (' + str(len(products)) + ') '
    else:
        products = Product.objects.filter(subcategory=pk).order_by('-public_day')
        select_name = SubCategory.objects.get(id=pk)
        sub_name = select_name.name + ' (' + str(len(products)) + ')'

    #l???c gi??
    from_price=''
    to_price = ''
    product_name = ''
    if request.GET.get('from_price'):
        from_price = int(request.GET.get('from_price'))
        to_price = int(request.GET.get('to_price'))
        product_name = request.GET.get('product_name')

        if product_name != '':
            products = Product.objects.filter(name__contains=product_name).order_by('-public_day')
            
        products = [product for product in products if from_price <= product.price <= to_price] #list comprehension
        sub_name = f'S??? s???n ph???m c?? gi?? t??? "{from_price}" ?????n "{to_price}": ' + '(' + str(len(products)) + ')'

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    products_pager = paginator.page(page)
    return render(request, 'store/product-list.html', {
        'sub_cats': sub_cats,
        'products': products_pager,
        'all_products': products,
        'sub_name': sub_name,
        'cart': cart,
        'from_price': from_price,
        'to_price': to_price,
        'product_name': product_name
    })


def search(request):
    cart = Cart(request)
    from_price=''
    to_price = ''
    product_name = ''
    if request.GET.get('product_name'):
        sub_cats = SubCategory.objects.all()
        product_name = request.GET.get('product_name').strip()
        products_search = Product.objects.filter(name__contains=product_name).order_by('-public_day')
        sub_name = f'S??? s???n ph???m c?? t??? kh??a "{product_name}": ' + '(' + str(len(products_search)) + ')'

    page = request.GET.get('page', 1)
    paginator = Paginator(products_search, 15)
    products_pager = paginator.page(page)

    if request.GET.get('from_price'):
        from_price = int(request.GET.get('from_price'))
        to_price = int(request.GET.get('to_price'))
        
        base_url = reverse('store:product-list', kwargs={'pk':0})
        query_string = urlencode({
            'from_price': from_price,
            'to_price': to_price,
            'product_name': product_name
        })
        url = '%s?%s' % (base_url, query_string)
        return redirect(url)

    return render(request, 'store/product-list.html',{
        'products': products_pager,
        'all_products_search': products_search,
        'sub_cats': sub_cats,
        'cart': cart,
        'sub_name': sub_name,
        'from_price': from_price,
        'to_price': to_price,
        'product_name': product_name
    })


def demo_user(request):
    cart = Cart(request)
    frm_user = FormUser()
    frm_profile = FormUserProfileInfo()
    result = ''
    if request.POST.get('btnSignup'):
        frm_user = FormUser(request.POST)
        frm_profile = FormUserProfileInfo(request.POST)
        if frm_user.is_valid() and frm_profile.is_valid():
            if frm_user.cleaned_data['password'] == frm_user.cleaned_data['confirm_password']:
                # User
                user = frm_user.save()
                user.set_password (user.password)
                user.save()

                # UserProfileInfo
                profile = frm_profile.save(commit=False)
                profile.user = user
                profile.save()

                result = '''
                    <div class="alert alert-success" role="alert">
                        Submit Successfully!!!
                    </div>
                '''

    if request.POST.get('btnLogin'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:user')

    return render(request, 'store/user.html', {
        'cart': cart,
        'frm_user': frm_user,
        'frm_profile': frm_profile,
        'result': result
    })


def logout_user(request):
    logout(request)
    return redirect('store:user')


def product_service(request):
    product = Product.objects.all().order_by('-public_day')
    result_list = list(product.values('name', 'price', 'image', 'public_day'))
    return JsonResponse(result_list, safe=False)


def product_service_detail(request, pk):
    product = Product.objects.filter(id=pk)
    result_list = list(product.values())[0]
    return JsonResponse(result_list, safe=False)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('-public_day')
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser] # ?????c / Ghi
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Ch??? ?????c