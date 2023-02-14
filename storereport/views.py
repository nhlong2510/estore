from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
import pdfkit
import os
from datetime import datetime
from store.models import Product
from django.db.models import Count

# Create your views here.
def html_to_pdf_view(request):
    today = datetime.now().strftime('%d-%m-%Y')
    products = Product.objects.values('subcategory', 'subcategory__name').annotate(total=Count('subcategory')).order_by('subcategory')

    list_name_of_subcategory = [product['subcategory__name'] for product in products]
    list_quantity_of_product = [product['total'] for product in products]

    html_string = render_to_string('storereport/report.html', {
        'today': today,
        'products': products,
        'list_name_of_subcategory': list_name_of_subcategory,
        'list_quantity_of_product': list_quantity_of_product
    })

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\wkhtmltopdf.exe')
    filename = 'report' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.pdf'
    pdfkit.from_string(html_string, os.path.join(os.path.expanduser('~'), 'Documents', filename), configuration=config)
    # pdfkit.from_string(html_string, "D:\\" + filename, configuration=config)

    return HttpResponse(html_string)