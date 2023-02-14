from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from store.models import Product
from django.views.decorators.http import require_POST
from cart.models import Order, OrderItem


def cart_detail(request):
    cart = Cart(request)

    chuoi_kq = ''
    if request.POST.get('btnCoupon'):
        coupon_code = request.POST.get('coupon_code')
        if coupon_code == 'TTTH':
            cart_new = {}
            for c in cart:
                product = c['product']
                product_cart = {
                    'quantity': c['quantity'],
                    'price': str(product.price),
                    'coupone': '0.9',
                }
                cart_new.update(product_cart)
                c['coupon'] = 0.9
            request.session['cart'] = cart_new
        else:
            chuoi_kq = 'Mã không hợp lệ!'

    if request.POST.get('btnUpdateCart'):
        cart_new = {}
        for c in cart:
            product = c['product']
            quantity_new = int(request.POST.get('quantity_'+ str(product.pk)))
            if quantity_new != 0:
                product_cart = {
                    str(product.pk): {
                        'quantity': quantity_new,
                        'price': str(product.price),
                        'coupon': str(c['coupon'])
                    }
                }
                cart_new.update(product_cart)
                c['quantity'] = quantity_new
            else:
                cart.remove(product)

        request.session['cart'] = cart_new
    return render(request, 'store/cart.html', {
        'cart': cart,
    })


@require_POST
def buy_now(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('quantity'):
        cart.add(product=product, quantity=int(request.POST.get('quantity')))
    return redirect('cart:cart_detail')


@require_POST
def remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('cart:cart_detail')



def checkout(request):
    cart = Cart(request)
    if request.POST.get('btnDatHang'):
        khach_hang = request.session.get('s_customer')
        order = Order()

        #Gán giá trị
        order.username = khach_hang['email']
        order.last_name = khach_hang['ho']
        order.first_name = khach_hang['ten']
        order.phone = khach_hang['dien_thoai']
        order.address = khach_hang['dia_chi']
        order.total = cart.get_final_total_price()
        order.save()

        for c in cart:
            OrderItem.objects.create(order=order, product=c['product'], price=c['price'], quantity=c['quantity'])

        cart.clear()

        return render(request, 'store/result.html', {
            'cart': cart,
        })

    return render(request, 'store/checkout.html', {
        'cart': cart,
    })