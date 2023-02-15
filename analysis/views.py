from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from analysis.utils import get_bar, get_box, get_hist
from django.conf import settings

from analysis.utils import get_hist

# Create your views here.
def series(request):
    views_1 = pd.Series([90006,1001141,97297,117182,99637])
    views_1 = pd.DataFrame({'views':views_1})
    views_1 = views_1.to_html()
    
    views_2 = pd.Series([90006,1001141,97297,117182,99637],['a','b','c','d','e'])
    views_2 = pd.DataFrame({'views':views_2})
    views_2 = views_2.to_html()

    views_3 = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'analysis/data_views.csv'), squeeze=True)
    views_3 = pd.DataFrame({'views': views_3})
    views_3 = views_3.to_html()

    return render(request,'store/series.html', {
        'views_1': views_1,
        'views_2': views_2,
        'views_3': views_3,
    })

def work_with_chart_1(request):
    #Histogram
    data_second = pd.read_excel(os.path.join(settings.MEDIA_ROOT,'analysis/dataset.xlsx'), sheet_name='Wait_times')
    hist = get_hist(data_second, 'seconds', 'Customer Wait Time')
    data_salaries = pd.read_excel(os.path.join(settings.MEDIA_ROOT,'analysis/salaries.xlsx'))
    boxplot = get_box(data_salaries, 'salary', 'Salary')
    activity = pd.read_excel(os.path.join(settings.MEDIA_ROOT,'analysis/dataset.xlsx'), sheet_name='Activity')
    barchart = get_bar(activity, 'Activity', 'Number_of_Students', 'After-school Activities')

    return render(request, 'store/chart.html', {
        'hist': hist,
        'boxplot': boxplot,
        'barchart': barchart
    })