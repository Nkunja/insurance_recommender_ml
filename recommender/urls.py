from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommendations/<int:customer_id>/', views.recommendations, name='recommendations'),
]