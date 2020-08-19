# Generated by Django 3.0.5 on 2020-04-23 20:42

import creditcards.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cc_type', models.CharField(choices=[('Master', 'Master'), ('Visa', 'Visa')], default='Master', max_length=256, verbose_name='Credit Card Type')),
                ('cc_number', creditcards.models.CardNumberField(max_length=25, verbose_name='card number')),
                ('cc_expiry', creditcards.models.CardExpiryField(verbose_name='expiration date')),
                ('cc_code', creditcards.models.SecurityCodeField(max_length=4, verbose_name='security code')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField(default=0, verbose_name='X Coordinate of Delivery Address')),
                ('y', models.IntegerField(default=0, verbose_name='Y Coordinate of Delivery Address')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0, verbose_name='Amount')),
            ],
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('warehouse_id', models.AutoField(primary_key=True, serialize=False)),
                ('x', models.IntegerField(default=0, verbose_name='X Coordinate of Ware House')),
                ('y', models.IntegerField(default=0, verbose_name='Y Coordinate of Ware House')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('apple', 'apple'), ('orange', 'orange'), ('banana', 'banana'), ('strawberry', 'strawberry'), ('pineapple', 'pineapple')], default='apple', max_length=256, verbose_name='Product Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('price', models.FloatField(blank=True, default=0, null=True)),
                ('storage', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Storage')),
                ('order', models.ManyToManyField(blank=True, null=True, related_name='order', to='miniamazon_app.Order')),
                ('warehouse', models.ManyToManyField(related_name='warehouse', to='miniamazon_app.WareHouse')),
            ],
        ),
        migrations.CreateModel(
            name='OrderCollection',
            fields=[
                ('order_collection_id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='', max_length=256)),
                ('truck_id', models.IntegerField(null=True, verbose_name='Truck ID')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordercollection', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order_collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='miniamazon_app.OrderCollection'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='warehouse',
            field=models.ManyToManyField(related_name='warehouse_order', to='miniamazon_app.WareHouse'),
        ),
        migrations.CreateModel(
            name='LocalStorage',
            fields=[
                ('local_storage_id', models.AutoField(primary_key=True, serialize=False)),
                ('storage', models.IntegerField(default=0, verbose_name='Storage')),
                ('product', models.ManyToManyField(related_name='product_local', to='miniamazon_app.Product')),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='localstorage', to='miniamazon_app.WareHouse')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Amount')),
                ('order', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='miniamazon_app.Order')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_cart', to=settings.AUTH_USER_MODEL)),
                ('product', models.ManyToManyField(related_name='product_cart', to='miniamazon_app.Product')),
                ('warehouse', models.ManyToManyField(related_name='warehouse_cart', to='miniamazon_app.WareHouse')),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='credit_card',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='myuser', to='miniamazon_app.CreditCard'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='delivery_address',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='myuser', to='miniamazon_app.DeliveryAddress'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
