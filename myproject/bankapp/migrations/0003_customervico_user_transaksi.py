# Generated by Django 4.2.5 on 2023-10-02 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0002_auto_20230918_0949'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerVico',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('VICID', models.CharField(max_length=8)),
                ('ACCTNO', models.CharField(max_length=10)),
                ('NO_IDEN', models.CharField(max_length=16)),
                ('NAMA_NASABAH', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=17)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('profile_photo', models.ImageField(upload_to='images/')),
                ('is_active', models.BooleanField(default=True)),
                ('agency', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Transaksi',
            fields=[
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('Nama_field', models.CharField(max_length=15)),
                ('field_awal', models.CharField(max_length=50)),
                ('field_update', models.CharField(max_length=50)),
                ('record_Del', models.CharField(max_length=255)),
                ('TGL_UPDT', models.CharField(max_length=8)),
                ('JM_UPDT', models.CharField(max_length=6)),
                ('TGL_APPRV_UPDATE', models.CharField(max_length=8)),
                ('JM_APPRV_UPDT', models.CharField(max_length=6)),
                ('USR_UPDT', models.CharField(max_length=15)),
                ('APPRV_UPDT', models.CharField(max_length=15)),
                ('TGL_DELETE', models.CharField(max_length=8)),
                ('JM_DELETE', models.CharField(max_length=6)),
                ('TGL_APPRV_DELETE', models.CharField(max_length=8)),
                ('JM_APPRV_DELETE', models.CharField(max_length=6)),
                ('USR_Delete', models.CharField(max_length=15)),
                ('APPRV_DELETE', models.CharField(max_length=15)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bankapp.customer')),
            ],
        ),
    ]
