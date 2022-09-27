from django.shortcuts import render, get_object_or_404
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_image
from django.shortcuts import HttpResponse
from .models import Report
from django.views.generic import ListView, DetailView, TemplateView

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils.dateparse import parse_date

from transactions.models import Sale, Position, CSV
from categories.models import Category
from shops.models import Shopkeeper
import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

food= ['Tea Tradition', 'Chilling Point', 'Dev Sweets', 'Dialog Cafe', 'Crazy Chef', 'Lets Go Live', 'Tandoor', 'Black Rabbit', 'Havmour', 'Saras', 'Kebab Nation', 'Lotus', 'Sai Chaap', 'Bade Miya', 'Tea Post', 'Chatkara', 'The Italian Oven']
bookandstationery = ['Stationery']
general = ['All Mart', 'Trendz']
# Create your views here.
def storecheck(name):
    category = ['Food','Stationery','General']
    shop=['DIALOG CA', 'THE ITALI']
    if name == 'THE ITALI':
        return 'The Italian Oven'
    elif name == 'DIALOG CA':
        return 'Dialog Cafe'
    elif name == 'SUNIL SON' :
        return 'Tandoor'
    elif name == 'GIRIRAJ S':
        return 'Lotus'
    elif name == 'M S PARTH':
        return 'Stationery'
    elif name == 'RAMNARAYA':
        return 'Dev Sweets'
    elif name == 'chilling ':
        return 'Chilling Point'
    elif name == 'Hariram i':
        return 'Saras'
    elif name == 'BharatPe':
        return 'Bade Miya'
    else:
        return 'unidentified'

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/detail.html'

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/from_file.html'

@login_required
def csv_upload_view(request):
    print('file is being sent')

    if request.method== 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)

        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()
                l = []
                m = []
                for row in reader:
                    m.append(row)
                    transaction = row[2].split('/')
                    try:
                        transaction = transaction[3]
                    except:
                        transaction = row[2]
                    
                    if not transaction in l:
                        l.append(transaction)

                    transaction_id = l.index(transaction) + 1
                    try:
                        amount = float(row[3])
                    except:
                        continue
                    # customer,product
                    shop = storecheck(transaction)
                    if shop in food:
                        category = 'FOOD'
                    elif shop in general:
                        category = 'GENERAL STORE'
                    elif shop in bookandstationery:
                        category = 'Stationery'
                    else:
                        category = 'Individual'

                    date = row[0]
                    date = date[6:]+date[2:6]+date[:2] 
                    # print(date)

                    try:
                        category_obj = Category.objects.get(name__iexact=category)
                    except Category.DoesNotExist:
                        category_obj = None

                    if category_obj is not None:
                        shop_obj, _ = Shopkeeper.objects.get_or_create(name=shop)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(Category=category_obj, amount=amount, created=date)

                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=shop_obj, salesman=salesman_obj, created=date)

                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
                    # print(transaction,amount,shop,category,transaction_id, date)    
                print(l)
    return HttpResponse()

@login_required
def create_report_view(request):
    if is_ajax(request):
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')

        img = get_report_image(image)

        author = Profile.objects.get(user=request.user)
        Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        # return HttpResponse({'msg': 'send'})
        return JsonResponse({'msg': 'send'})
    return JsonResponse({})

@login_required
def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # id download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    