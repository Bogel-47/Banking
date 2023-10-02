from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Customer(models.Model):
    account_id = models.IntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    account = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    description = models.CharField(max_length=255)
    debit_credit_status = models.CharField(max_length=1, choices=[('D', 'Debit'), ('C', 'Credit')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.debit_credit_status == 'D':
            previous_balance = Transaction.objects.filter(account=self.account, transaction_date__lt=self.transaction_date).order_by('-transaction_date').first()
            if previous_balance:
                self.balance = previous_balance.balance + self.amount
            else:
                self.balance = self.amount
        else:
            previous_balance = Transaction.objects.filter(account=self.account, transaction_date__lt=self.transaction_date).order_by('-transaction_date').first()
            if previous_balance:
                self.balance = previous_balance.balance - self.amount
            else:
                self.balance = -self.amount

        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.account.name} - {self.description}"


class Point(models.Model):
    account = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_point = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.account.name} - Point: {self.total_point}"

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique= True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=17)
    email = models.EmailField(unique= True)
    address = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='images/')
    is_active = models.BooleanField(default=True)
    agency = models.CharField(max_length=255)
    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return self.username
    
class CustomerVico(models.Model):
    customer_id = models.AutoField(primary_key=True)
    VICID = models.CharField(max_length=8)
    ACCTNO = models.CharField(max_length=10)
    NO_IDEN = models.CharField(max_length=16)
    NAMA_NASABAH = models.CharField(max_length=50)

class Transaksi(models.Model):
    history_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    Nama_field = models.CharField(max_length=15)
    field_awal = models.CharField(max_length=50)
    field_update = models.CharField(max_length=50)
    record_Del = models.CharField(max_length=255)
    TGL_UPDT = models.CharField(max_length=8)
    JM_UPDT = models.CharField(max_length=6)
    TGL_APPRV_UPDATE = models.CharField(max_length=8)
    JM_APPRV_UPDT = models.CharField(max_length=6)
    USR_UPDT = models.CharField(max_length=15)
    APPRV_UPDT = models.CharField(max_length=15)
    TGL_DELETE = models.CharField(max_length=8)
    JM_DELETE = models.CharField(max_length=6)
    TGL_APPRV_DELETE = models.CharField(max_length=8)
    JM_APPRV_DELETE = models.CharField(max_length=6)
    USR_Delete = models.CharField(max_length=15)
    APPRV_DELETE = models.CharField(max_length=15)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, address, agency, password=None):
        if not email:
            raise ValueError('Email harus diisi.')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            agency=agency,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, address, agency, password):
        user = self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            agency=agency,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=17)
    address = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='images/')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number', 'address', 'agency']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
