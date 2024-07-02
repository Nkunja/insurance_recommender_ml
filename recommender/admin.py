from django.contrib import admin
from .models import InsuranceProduct, Customer, Recommendation

admin.site.register(InsuranceProduct)
admin.site.register(Customer)
admin.site.register(Recommendation)
