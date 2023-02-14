from django import forms
from customers.models import KhachHang

class FormDangNhap:
    ten_dang_nhap = forms.CharField(max_length=100)
    mat_khau = forms.CharField(max_length=20)


class FormDangKy(forms.ModelForm):
    ho = forms.CharField(max_length=264, label='Họ', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Họ",
    }))
    ten = forms.CharField(max_length=264, label='Tên', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Tên",
    }))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Email",
    }))
    mat_khau = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Mật khẩu",
    }))
    xac_nhan_mat_khau = forms.CharField(label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Xác nhận Mật khẩu",
    }))
    dien_thoai = forms.CharField(max_length=20, label='Điện thoại', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Điện thoại",
    }))
    dia_chi = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        "class": "form-control", "placeholder": "Địa chỉ", "rows": "3",
    }))

    class Meta:
        model = KhachHang
        fields = ['ho', 'ten', 'email', 'mat_khau', 'dien_thoai', 'dia_chi']


class FormDangKy2(forms.ModelForm):
    ho = forms.CharField(max_length=264, label='Họ', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Họ",
    }))
    ten = forms.CharField(max_length=264, label='Tên', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Tên",
    }))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Email",
    }))
    mat_khau = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Mật khẩu",
    }))
    xac_nhan_mat_khau = forms.CharField(label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Xác nhận Mật khẩu",
    }))
    dien_thoai = forms.CharField(max_length=20, label='Điện thoại', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Điện thoại",
    }))
    dia_chi = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        "class": "form-control", "placeholder": "Địa chỉ", "rows": "3",
    }))
    tinh_tp = forms.CharField(label='Tỉnh/TP', widget=forms.Select(attrs={
        "class": "form-control"
    }))
    quan_huyen = forms.CharField(label='Quận/Huyện', widget=forms.Select(attrs={
        "class": "form-control"
    }))
    phuong_xa = forms.CharField(label='Phường/Xã', widget=forms.Select(attrs={
        "class": "form-control"
    }))

    class Meta:
        model = KhachHang
        fields = ['ho', 'ten', 'email', 'mat_khau', 'dien_thoai', 'dia_chi']


class FormDoiMatKhau(forms.ModelForm):
    mat_khau_hien_tai = forms.CharField(label='Mật khẩu hiện tại', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Mật khẩu hiện tại",
    }))
    mat_khau = forms.CharField(label='Mật khẩu mới', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Mật khẩu mới",
    }))
    xac_nhan_mat_khau = forms.CharField(label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Xác nhận Mật khẩu",
    }))

    class Meta:
        model = KhachHang
        fields = ['mat_khau_hien_tai', 'mat_khau', 'xac_nhan_mat_khau']
        # fields = '__all__'
