# Generated by Django 5.0.6 on 2024-07-02 11:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('income', models.FloatField()),
                ('credit_score', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('occupation', models.CharField(max_length=100)),
                ('marital_status', models.CharField(max_length=20)),
                ('number_of_dependents', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='InsuranceProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.insuranceproduct')),
            ],
        ),
    ]