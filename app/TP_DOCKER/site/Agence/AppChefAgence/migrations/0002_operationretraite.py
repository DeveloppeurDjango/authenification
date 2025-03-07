# Generated by Django 5.0.4 on 2024-05-16 01:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppChefAgence', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationRetraite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_operation', models.DateTimeField(auto_now_add=True)),
                ('list_retraite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppChefAgence.listretraite')),
            ],
        ),
    ]
