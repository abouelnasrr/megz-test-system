# Generated by Django 4.2 on 2025-04-06 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0015_websitelogo'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockWarning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warning_limit', models.IntegerField()),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.products')),
            ],
        ),
    ]
