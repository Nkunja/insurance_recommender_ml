from django.db import models

class Customer(models.Model):
    age = models.IntegerField()
    income = models.FloatField()
    credit_score = models.IntegerField()
    gender = models.CharField(max_length=10)
    occupation = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=20)
    number_of_dependents = models.IntegerField()

class InsuranceProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Recommendation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(InsuranceProduct, on_delete=models.CASCADE)
    score = models.FloatField()