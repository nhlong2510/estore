from django.shortcuts import redirect, render
from customers.models import KhachHang
from customers.forms import FormDangKy, FormDoiMatKhau, FormDangKy2
from cart.cart import Cart
from django.contrib.auth.hashers import Argon2PasswordHasher
from cart.models import OrderItem, Order
from customers.my_module import read_json_internet


# Create your views here.
def customer_login_signup2(request):
    cart = Cart(request)
    if 's_customer' in request.session:
        return redirect('store:index')

    frm_sign_up = FormDangKy2()
    signup_result = ''
    login_result = ''

    info = read_json_internet('http://api.laptrinhpython.net/vietnam')
    
    #Tỉnh/TP
    list_province = []
    list_district = []
    list_ward = []
    data_district = []
    for province in info:
        list_province.append(province['name'])

        #Quận/Huyện
        districts = []
        for district in province['districts']:
            d = district['prefix']+' '+district['name']
            districts.append(d)
            data_district.append(d)

            #Phường/Xã
            wards = []
            for ward in district['wards']:
                w = ward['prefix']+' '+ward['name']
                wards.append(w)
            else:
                str_wards = "|".join(wards)
                list_ward.append(str_wards)

        else:
            str_districts = "|".join(districts)
            list_district.append(str_districts)

    if request.POST.get('btnSignup'):
        frm_sign_up = FormDangKy2(request.POST, KhachHang)
        if frm_sign_up.is_valid() and frm_sign_up.cleaned_data['mat_khau']==frm_sign_up.cleaned_data['xac_nhan_mat_khau']:
            hasher = Argon2PasswordHasher()
            request.POST.__mutable = True
            post = frm_sign_up.save(commit=False)
            post.ho = frm_sign_up.cleaned_data['ho']
            post.ten = frm_sign_up.cleaned_data['ten']
            post.dien_thoai = frm_sign_up.cleaned_data['dien_thoai']
            post.mat_khau = hasher.encode(frm_sign_up.cleaned_data['mat_khau'], 'abcd1234')
            post.email = frm_sign_up.cleaned_data['email']
            post.dia_chi = frm_sign_up.cleaned_data['dia_chi']+', '+frm_sign_up.cleaned_data['phuong_xa']+', '+frm_sign_up.cleaned_data['quan_huyen']+', '+frm_sign_up.cleaned_data['tinh_tp']
            post.save()
            signup_result = '''
                <div class="alert alert-success" role="alert">
                    Đã đăng ký thành công
                </div>
            '''
    if request.POST.get('btnLogin'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        hasher = Argon2PasswordHasher()
        encode = hasher.encode(password, 'abcd1234')
        customer = KhachHang.objects.filter(email=email, mat_khau=encode)
        if customer.count() > 0:
            #tạo session
            request.session['s_customer'] = customer.values()[0]
            return redirect('store:index')
        else:
            login_result = '''
                <div class="alert alert-danger" role="alert">
                    E-mail hoặc mật khẩu không đúng!!! Vui lòng đăng nhập lại!!!
                </div>
            '''

    return render (request, 'store/login2.html',{
        'frm_signup': frm_sign_up,
        'signup_result': signup_result,
        'login_result': login_result,
        'cart': cart,
        'tuple_province': tuple(list_province),
        'tuple_district': tuple(list_district),
        'tuple_ward': tuple(list_ward),
        'data_district': tuple(data_district)
    })


def customer_login_signup(request):
    cart = Cart(request)
    if 's_customer' in request.session:
        return redirect('store:index')

    frm_sign_up = FormDangKy()
    signup_result = ''
    login_result = ''
    if request.POST.get('btnSignup'):
        frm_sign_up = FormDangKy(request.POST, KhachHang)
        if frm_sign_up.is_valid() and frm_sign_up.cleaned_data['mat_khau']==frm_sign_up.cleaned_data['xac_nhan_mat_khau']:
            hasher = Argon2PasswordHasher()
            request.POST.__mutable = True
            post = frm_sign_up.save(commit=False)
            post.ho = frm_sign_up.cleaned_data['ho']
            post.ten = frm_sign_up.cleaned_data['ten']
            post.dien_thoai = frm_sign_up.cleaned_data['dien_thoai']
            post.mat_khau = hasher.encode(frm_sign_up.cleaned_data['mat_khau'], 'abcd1234')
            post.email = frm_sign_up.cleaned_data['email']
            post.dia_chi = frm_sign_up.cleaned_data['dia_chi']
            post.save()
            signup_result = '''
                <div class="alert alert-success" role="alert">
                    Đã đăng ký thành công
                </div>
            '''
    if request.POST.get('btnLogin'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        hasher = Argon2PasswordHasher()
        encode = hasher.encode(password, 'abcd1234')
        customer = KhachHang.objects.filter(email=email, mat_khau=encode)
        if customer.count() > 0:
            #tạo session
            request.session['s_customer'] = customer.values()[0]
            return redirect('store:index')
        else:
            login_result = '''
                <div class="alert alert-danger" role="alert">
                    E-mail hoặc mật khẩu không đúng!!! Vui lòng đăng nhập lại!!!
                </div>
            '''

    return render (request, 'store/login.html',{
        'frm_signup': frm_sign_up,
        'signup_result': signup_result,
        'login_result': login_result,
        'cart': cart,
    })


def customer_logout(request):
    if 's_customer' in request.session:
        del request.session['s_customer']
    return redirect('customers:login')


def myaccount(request):
    result = ''
    result_pass = ''
    if 's_customer' not in request.session:
        return redirect('customers:login')
    
    if request.POST.get('btnUpdate'):
        ho = request.POST.get('ho')
        ten = request.POST.get('ten')
        dien_thoai = request.POST.get('dien_thoai')
        dia_chi = request.POST.get('dia_chi')

        s_khach_hang = request.session.get('s_customer')
        khach_hang = KhachHang.objects.get(id=s_khach_hang['id'])
        khach_hang.ho = ho
        khach_hang.ten = ten
        khach_hang.dien_thoai = dien_thoai
        khach_hang.dia_chi = dia_chi
        khach_hang.save()

        s_khach_hang['ho'] = ho
        s_khach_hang['ten'] = ten
        s_khach_hang['dien_thoai'] = dien_thoai
        s_khach_hang['dia_chi'] = dia_chi
        result = '''
                <div class="alert alert-sucess" role="alert">
                    Đã cập nhật thông tin thành công
                </div>
            '''
    
    form = FormDoiMatKhau()
    if request.POST.get('btnChangePass'):
        form = FormDoiMatKhau(request.POST, KhachHang)
        if form.is_valid():
            mat_khau_hien_tai = form.cleaned_data['mat_khau_hien_tai']
            s_khach_hang = request.session.get('s_customer')
            khach_hang = KhachHang.objects.get(id=s_khach_hang['id'])
            
            hasher = Argon2PasswordHasher()
            encoded = hasher.encode(mat_khau_hien_tai, 'abcd1234')
            
            if encoded == khach_hang.mat_khau:
                if form.is_valid() and form.cleaned_data['mat_khau'] == form.cleaned_data['xac_nhan_mat_khau']:
                    khach_hang.mat_khau = form.cleaned_data['mat_khau']
                    khach_hang.save()
                    result_pass = '''
                        <div class="alert alert-sucess" role="alert">
                            Đã cập nhật thông tin thành công
                        </div>
                    '''
                else:
                    result_pass = '''
                        <div class="alert alert-danger" role="alert">
                            Mật khẩu nhập chưa đúng
                        </div>
                    '''            

    cart = Cart(request)
    order = Order.objects.all()
    item = OrderItem.objects.all()
        
    return render(request, 'store/my-account.html', {
        'cart': cart,
        'orders': order,
        'items': item,
        'result': result,
        'result_pass': result_pass,
        'form': form
    })


