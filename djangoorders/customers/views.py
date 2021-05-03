from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy

from customers.models import Customer


def customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'customers/customer_list.html', context=context)


def customer_table(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'customers/customer_table.html', context=context)


def home(request):
    return render(request, 'home.html')


def customer_create(request):
    data = {}
    if request.method == 'POST':
        data['first_name'] = request.POST.get('first_name')
        data['last_name'] = request.POST.get('last_name')
        data['street'] = request.POST.get('street', '')
        data['city'] = request.POST.get('city', '')
        data['state'] = request.POST.get('state', '')
        data['zip_code'] = request.POST.get('zip_code', '')
        data['country'] = request.POST.get('country', '')
        customer = Customer(**data)

        # make first and last name required
        if data['first_name'] and data['last_name']:
            try:
                customer.save()
                customer_list_url = reverse_lazy('customer_list')
                return HttpResponseRedirect(customer_list_url)
            except Exception as e:
                print(e)
        else:
            data['errors'] = 'First Name and Last Name fields are required'

    return render(request, 'customers/customer_create.html', context=data)


def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist as e:
        print(e)
        customer = Customer.objects.none()

    context = {
        'customer': customer,
    }
    return render(request, 'customers/customer_detail.html', context=context)


def customer_update(request, pk):
    customer = Customer.objects.get(pk=pk)
    data = {'customer': customer}
    if request.method == 'POST':
        customer.first_name = request.POST.get(
            'first_name', customer.first_name)
        customer.last_name = request.POST.get('last_name', customer.last_name)
        customer.street = request.POST.get('street', customer.street)
        customer.city = request.POST.get('city', customer.city)
        customer.state = request.POST.get('state', customer.state)
        customer.zip_code = request.POST.get('zip_code', customer.zip_code)
        customer.country = request.POST.get('country', customer.country)

        if customer.first_name and customer.last_name:
            try:
                customer.save()
                customer_detail_url = reverse_lazy(
                    'customer_detail', kwargs={'pk': pk})
                return HttpResponseRedirect(customer_detail_url)
            except Exception as e:
                print(e)
                data['errors'] = str(e)
        else:
            data['errors'] = 'First Name and Last Name fields are required'

    return render(request, 'customers/customer_update.html', context=data)
