from django.shortcuts import render, redirect
from .forms import CustomerForm
from .models import Customer, InsuranceProduct, Recommendation
from .ml_model import train_model, get_recommendations



def home(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('recommendations', customer_id=customer.id)
    else:
        form = CustomerForm()
    return render(request, 'home.html', {'form': form})

def recommendations(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    model, scaler = train_model()  # You might want to cache this
    recommendations = get_recommendations(model, scaler, customer)

    
    # Save recommendations to database
    for product, score in recommendations:
        Recommendation.objects.create(customer=customer, product=product, score=score)
    
    return render(request, 'recommendations.html', {'recommendations': recommendations})