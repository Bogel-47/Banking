from django.shortcuts import render, redirect
from .models import Customer, Transaction, Point, CustomerVico
from .forms import CustomerForm, TransactionForm, CustomUserLoginForm, RegistrationForm, ExcelUploadForm
from django.template import loader
from django.http import HttpResponse
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from decimal import Decimal
from django.shortcuts import get_object_or_404
import datetime
from django.contrib.auth import authenticate, login
from django.contrib import messages
import pandas as pd

def input_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'banking/input_customer.html', {'form': form})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'banking/customer_list.html', {'customers': customers})

def calculate_points(amount,transaction_type, transaction_desc,account_id):
    point, created = Point.objects.get_or_create(account_id=account_id)
    if point :
        if transaction_type == 'C':
            if transaction_desc == 'Beli Pulsa':
                if amount <= 10000:
                    point.total_point += 0
                elif 10000 < amount <= 30000:
                    point_awal = point.total_point
                    hitungan= (amount - 10000) / 1000
                    point.total_point = point_awal + hitungan
                else:
                    point_awal = point.total_point
                    hitungan = (amount - 30000) / 1000
                    point_tambahan = (2 * hitungan) + 20
                    point.total_point = point_awal +  point_tambahan
            elif transaction_desc == 'Bayar Listrik':
                if amount <= 50000:
                    point.total_point += 0
                elif 50000 < amount <= 100000:
                    point_awal = point.total_point
                    hitungan= (amount - 50000) / 2000
                    point.total_point = point_awal + hitungan
                else:
                    point_awal = point.total_point
                    hitungan = (amount - 100000) / 2000
                    point_tambahan = (2 * hitungan) + 25
                    point.total_point = point_awal +  point_tambahan
            point.save()

def input_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['debit_credit_status']
            transaction_desc = form.cleaned_data['description']
            account = form.cleaned_data['account']
            customer = get_object_or_404(Customer, name=account)
            calculate_points(amount, transaction_type, transaction_desc, customer.id)
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'banking/input_transaction.html', {'form': form})

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'banking/transaction_list.html', {'transactions': transactions})

def main(request):
    year = datetime.datetime.now().year
    return render(request, 'base.html', {'year': year})

def point_list(request):
    points = Point.objects.all()
    return render(request, 'banking/point_list.html', {'points': points})

def report_buku_tabungan(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        customer = get_object_or_404(Customer, account_id=account_id)

        transactions = Transaction.objects.filter(
            account_id = customer,
            transaction_date__range=[start_date, end_date]
        )

        balance = Decimal(0)
        for transaction in transactions:
            if transaction.debit_credit_status == 'C':
                balance -= transaction.amount
            else:
                balance += transaction.amount

            transaction.balance = balance

        return render(request, 'banking/report_buku_tabungan.html', {'transactions': transactions})
    else:
        return render(request, 'banking/input_report.html')

def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect ke halaman setelah login sukses
                return redirect('customer_list')
            else:
                # Username atau password salah, tambahkan pesan kesalahan
                messages.error(request, 'Username atau password salah. Silakan coba lagi.')
        else:
            # Form tidak valid, tambahkan pesan kesalahan
            messages.error(request, 'Form login tidak valid. Silakan coba lagi.')
    else:
        form = CustomUserLoginForm()
    return render(request, 'banking/login.html', {'form': form})

def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('customer_list')
    else:
        form = RegistrationForm()
    return render(request, 'banking/registration.html', {'form': form})

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            if excel_file.name.endswith('.xlsx'):
                df = pd.read_excel(excel_file)
                for _, row in df.iterrows():
                    CustomerVico.objects.create(
                        NAMA_NASABAH=row['Customer Name'],
                        ACCTNO=row['Nomor Rekening '],
                        NO_IDEN=row['Nomor Identitas']
                    )
                return redirect('customer_list')  # Ganti 'success_page' dengan halaman sukses Anda
            else:
                form.add_error('excel_file', 'Harap unggah file Excel dengan format .xlsx')
    else:
        form = ExcelUploadForm()
    return render(request, 'banking/upload_excel.html', {'form': form})