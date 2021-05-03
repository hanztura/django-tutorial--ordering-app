# Django Ordering App - Tutorial

## Installation

- `python3.9 -m venv env`
- `source env/bin/activate`
- `pip install django==3.2`
- `cd djangoorders`
- test if all went well by running `python manage.py runserver` and open <http://localhost:8000>
- `python manage.py migrate`

## Django Models (Database Modelling)

### Customer

- `python manage.py startapp customers`
- define model Class 'Customer'
- make sure to define the **str** instance method
- register the customers app, insert at `djangoorders.settings.INSTALLED_APPS`
- `python manage.py makemigrations customers`
- `python manage.py migrate`
- Create/Update a sample customer through management console `python manage.py shell`

```python
from customers.models import Customer
c = Customer(first_name='Hanz', last_name='Tura')
c.first_name
c.last_name

c.pk  # returns none
c.save()
c.pk  # returns 1

c.street
c.country

c.street = '123 St.'
c.city = 'Cagayan de Oro'
c.state = 'Misamis Oriental'
c.zip_code = '9000'
c.save()  # to update record in database
c.street
c.country

c2 = Customer(first_name='John', last_name='Doe')
c2.save()
```

- List/Get/Delete a record via management console:

```python
from customers.models import Customer
queryset = Customer.objects.all()  # get the list of customers
queryset

c = Customer.objects.get(pk=1)  # get one record
c
c.delete()
```

### Item

- `python manage.py startapp items`
- define model Class 'Item'
- make sure to define the **str** instance method
- register the items app, insert at `djangoorders.settings.INSTALLED_APPS`
- `python manage.py makemigrations items`
- `python manage.py migrate`
- Create/List/Get sample items through management console `python manage.py shell`

```python
from items.models import Item
obj = Item(name='Macbook Air', description='Apple M1 Chip with 8-Core CPU and 7-Core GPU 256 GB Storage', price='54990', code='202100001')
obj.save()

obj2 = Item(name='Printer', description='Epson Printer', price='2550', code='202100002')
obj2.save()

queryset = Item.objects.all()
queryset
```

### Order

- `python manage.py startapp orders`
- define model Class 'Order'
- make sure to define the **str** instance method
- register the orders app, insert at `djangoorders.settings.INSTALLED_APPS`
- `python manage.py makemigrations orders`
- `python manage.py migrate`

### Order Item

- define model Class 'OrderItem' inside `orders.models` file
- make sure to define the **str** instance method
- `python manage.py makemigrations orders`
- `python manage.py migrate`

## Django Views

### Function Views

- Define a function view called `customer_list` inside the customers app's `views.py` file.

```python
from django.shortcuts import HttpResponse

def customer_list(request):
    return HttpResponse('Customer List')
```

- Connect the view into the Django URL configuration file `djangoorders/urls.py`

```python
from django.contrib import admin
from django.urls import path
from customers import views as customer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', customer_views.customer_list)
]
```

- Open <http://localhost:8000/customers/>
- Let's return a list of customers in our record. But first, create another customer named Hanz Tura.

```python
#customers/views.py/
from django.shortcuts import HttpResponse

from customers.models import Customer


def customer_list(request):
    customers = Customer.objects.all()
    return HttpResponse(customers)
```

### Django Template

- Render a simple html file using Django template.
- Inside the customers app, create a folder called `templates`
- Inside the `templates` folder, create another folder called `customers`
- Inside the `customers/templates/customers` folder, create an html file called `customer_list.html`.
- Edit the HTML file so it would contain:

```html
<html>
  <head>
    <title>Customer List</title>
  </head>
  <body>
    <h1>Customers</h1>
    <ul>
      <li>John Doe</li>
      <li>Hanz Tura</li>
    </ul>
  </body>
</html>
```

- Edit our `customer_list` view to render our html template:

```python
from django.shortcuts import render
from django.shortcuts import HttpResponse

from customers.models import Customer


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html')
```

- Let's improve the template and render the list of customers based on the records from our database:

```html
<html>
  <head>
    <title>Customer List</title>
  </head>
  <body>
    <h1>Customers</h1>
    <ul>
      {% for customer in customers %}
      <li>{{ customer.last_name }}, {{ customer.first_name }}</li>
      {% endfor %}
    </ul>
  </body>
</html>
```

- Pass the customers variable as a context in the `customer_list` view:

```python
from django.shortcuts import render

from customers.models import Customer


def customer_list(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'customers/customer_list.html', context=context)
```

- Let's try another way of displaying a list of records by using tables. Create `templates/customers/customer_table.html`:

```html
<html>
  <head>
    <title>Customer List</title>
  </head>
  <body>
    <h1>Customers</h1>
    <section>
      <table>
        <thead>
          <tr>
            <th colspan="3"></th>
            <th colspan="5">Address</th>
          </tr>
          <tr>
            <th>ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Street</th>
            <th>City</th>
            <th>State</th>
            <th>ZIP Code</th>
            <th>Country</th>
          </tr>
        </thead>
        <tbody>
          {% for customer in customers %}
          <tr>
            <td>{{ customer.pk }}</td>
            <td>{{ customer.first_name }}</td>
            <td>{{ customer.last_name }}</td>
            <td>{{ customer.street }}</td>
            <td>{{ customer.city }}</td>
            <td>{{ customer.state }}</td>
            <td>{{ customer.zip_code }}</td>
            <td>{{ customer.country }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </section>
  </body>
</html>
```

- Add another view function named `customer_table` in the `customers/views.py` file:

```python
from django.shortcuts import render

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
```

- Connect the view in the URL configuration:

```python
from django.contrib import admin
from django.urls import path

from customers import views as customer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', customer_views.customer_list),
    path('customers/t', customer_views.customer_table),  # insert this line
]
```

#### Reusable Templates

- Inside the project directory, create a root `templates` folder.
- In the settings file `djangoorders/settings.py`, update the `TEMPLATES.DIRS` variable:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('templates')  # insert this
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

- In the root `templates` folder, create a template file `base.html`

```html
<html>
  <head>
    <title>{% block title %}{% endblock title %}</title>
  </head>
  <body>
    <h1>{% block h1 %}{% endblock h1 %}</h1>
    <main>{% block main %}{% endblock main %}</main>
  </body>
</html>
```

- Update the `templates/customers/customer_table.html`:

```html
{% extends 'base.html' %} {% block title %}Customer List{% endblock title %} {%
block h1 %}Customers{% endblock h1 %} {% block main %}
<table>
  <thead>
    <tr>
      <th colspan="3"></th>
      <th colspan="5">Address</th>
    </tr>
    <tr>
      <th>ID</th>
      <th>First Name</th>
      <th>Last Name</th>
      <th>Street</th>
      <th>City</th>
      <th>State</th>
      <th>ZIP Code</th>
      <th>Country</th>
    </tr>
  </thead>
  <tbody>
    {% for customer in customers %}
    <tr>
      <td>{{ customer.pk }}</td>
      <td>{{ customer.first_name }}</td>
      <td>{{ customer.last_name }}</td>
      <td>{{ customer.street }}</td>
      <td>{{ customer.city }}</td>
      <td>{{ customer.state }}</td>
      <td>{{ customer.zip_code }}</td>
      <td>{{ customer.country }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock main %}
```

### URL Naming

- Go to the `djangoorders/urls.py` and add a name paramater on each URL entry:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', customer_views.customer_list, name="customer_list"),
    path('customers/t', customer_views.customer_table, name="customer_table"),
    path('', customer_views.home, name="home"),
]
```

- Inside the root `templates` folder, create a `home.html` file:

```html
{% extends 'base.html' %} {% block title %}Ordering App{% endblock title %} {%
block h1 %}Ordering App - Home{% endblock h1 %} {% block main %}
<p>Welcome to Django Ordering App.</p>
<p>To start, click here to login.</p>
<ul>
  <li><a href="{% url 'customer_table' %}">Customers</a></li>
  <li>Items</li>
  <li>Orders</li>
</ul>
{% endblock main %}
```

### App Views

#### Customer Views

##### Customer Create View

- In the `templates/customers/` create `customer_create.html` file:

```html
{% extends 'base.html' %} {% block title %}New Customer{% endblock title %} {%
block h1 %}New Customer{% endblock h1 %} {% block main %}
<form method="POST">
  {% csrf_token %}
  <table>
    <tbody>
      <tr>
        <th><label>Last Name</label></th>
        <td><input type="text" name="last_name" /></td>
      </tr>
      <tr>
        <th><label>First Name</label></th>
        <td><input type="text" name="first_name" /></td>
      </tr>
      <tr>
        <th><label>Street</label></th>
        <td><input type="text" name="street" /></td>
      </tr>
      <tr>
        <th><label>City</label></th>
        <td><input type="text" name="city" /></td>
      </tr>
      <tr>
        <th><label>State</label></th>
        <td><input type="text" name="state" /></td>
      </tr>
      <tr>
        <th><label>ZIP</label></th>
        <td><input type="text" name="zip_code" /></td>
      </tr>
      <tr>
        <th><label>Country</label></th>
        <td>
          <select name="country">
            <option value="ph">Philippines</option>
            <option value="" disabled>Others</option>
          </select>
        </td>
      </tr>
      <tr>
        <th></th>
        <td>
          <button type="submit">Save</button>
        </td>
      </tr>
    </tbody>
  </table>
</form>
{% endblock main %}
```

- Define another view function inside the `customers/views.py`:

```python
# ... previous lines here

def customer_create(request):
    return render(request, 'customers/customer_create.html')
```

- Connect the `customer_create` view in the URLs config:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/new/', customer_views.customer_create, name="customer_create"),  # add this line
    path('customers/t/', customer_views.customer_table, name="customer_table"),
    path('customers/', customer_views.customer_list, name="customer_list"),
    path('', customer_views.home, name="home"),
]
```

- Notice that the order of the URL entries are rearranged.
- Now go to <http://localhost:8000/customers/new>
- Clicking the `save` button and going to <http://localhost:8000/customers/t> will show that our app did not save the new customer we submitted.
- Let's edit the `customers/views/customer_create` function:

```python
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
```

##### Customer Detail View

- In the `templates/customers/` create `customer_detail.html` file:

```html
{% extends 'base.html' %} {% block title %} {{ customer|default:'' }} - Customer
Detail{% endblock title %} {% block h1 %}{{ customer|default:'' }} - Customer{%
endblock h1 %} {% block main %} {% if customer %}
<table>
  <tbody>
    <tr>
      <th>Last Name</th>
      <td>{{ customer.last_name }}</td>
    </tr>
    <tr>
      <th>First Name</th>
      <td>{{ customer.first_name }}</td>
    </tr>
    <tr>
      <th>Street</th>
      <td>{{ customer.street }}</td>
    </tr>
    <tr>
      <th>City</th>
      <td>{{ customer.city }}</td>
    </tr>
    <tr>
      <th>State</th>
      <td>{{ customer.state }}</td>
    </tr>
    <tr>
      <th>ZIP Code</th>
      <td>{{ customer.zip_code }}</td>
    </tr>
    <tr>
      <th>Country</th>
      <td>{{ customer.country }}</td>
    </tr>
  </tbody>
</table>
{% else %}
<p>Unable to find this customer.</p>
{% endif %} {% endblock main %}
```

- Define another view function inside the `customers/views.py`:

```python
# ... previous lines here

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
```

- Connect the `customer_detail` view in the URLs config:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/new/', customer_views.customer_create, name="customer_create"),
    path('customers/t/', customer_views.customer_table, name="customer_table"),
    path('customers/<int:pk>/', customer_views.customer_detail,
         name="customer_detail"),
    path('customers/', customer_views.customer_list, name="customer_list"),
    path('', customer_views.home, name="home"),
]
```

##### Customer Update View

- In the `templates/customers/` create `customer_update.html` file:

```html{% extends 'customers/base.html' %}

{% block title %} {{ customer|default:'' }} - Edit Customer{% endblock title %}
{% block h1 %}{{ customer|default:'' }} - Edit Customer{% endblock h1 %}

{% block main %}
<form method="POST">
  {% csrf_token %}
  <table class="table">
    <tbody>

      {% if errors %}
        <tr>
          <td colspan="2"><span>{{ errors }}</span></td>
        </tr>
      {% endif %}

      <tr>
        <th><label>Last Name</label></th>
        <td><input type="text" name="last_name" value="{{ customer.last_name }}" /></td>
      </tr>
      <tr>
        <th><label>First Name</label></th>
        <td><input type="text" name="first_name" value="{{ customer.first_name }}" /></td>
      </tr>
      <tr>
        <th><label>Street</label></th>
        <td><input type="text" name="street" value="{{ customer.street }}" /></td>
      </tr>
      <tr>
        <th><label>City</label></th>
        <td><input type="text" name="city" value="{{ customer.city }}" /></td>
      </tr>
      <tr>
        <th><label>State</label></th>
        <td><input type="text" name="state" value="{{ customer.state }}" /></td>
      </tr>
      <tr>
        <th><label>ZIP</label></th>
        <td><input type="text" name="zip_code" value="{{ customer.zip_code }}" /></td>
      </tr>
      <tr>
        <th><label>Country</label></th>
        <td>
          <select name="country">
            <option selected value="ph">Philippines</option>
            <option value="" disabled>Others</option>
          </select>
        </td>
      </tr>
      <tr>
        <th></th>
        <td>
          <button type="submit">Save</button>
        </td>
      </tr>
    </tbody>
  </table>
</form>
{% endblock main %}
```

- Define another view function inside the `customers/views.py`:

```python
# ... previous lines here

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
```

- Connect the `customer_update` view in the URLs config:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/new/', customer_views.customer_create, name="customer_create"),
    path('customers/t/', customer_views.customer_table, name="customer_table"),
    path('customers/<int:pk>/', customer_views.customer_detail,
         name="customer_detail"),
    path('customers/<int:pk>/edit', customer_views.customer_update,
         name="customer_update"),  # add this line
    path('customers/', customer_views.customer_list, name="customer_list"),
    path('', customer_views.home, name="home"),
]
```

- Let's make the look of our app a bit more interesting by using a [CSS Framework](#css).

##### Customer Delete View

#### Orders

## Other Topics

### CSS

- Copy the root `base.html` and name it `base_bulma.html` add this line inside the head element:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <title>{% block title %}{% endblock title %}</title>
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bulma@0.9.2/css/bulma.min.css"
    />
  </head>
  <body>
    <div class="container">
      <h1 class="title is-1">{% block h1 %}{% endblock h1 %}</h1>
    </div>
    <main class="container">{% block main %}{% endblock main %}</main>
  </body>
</html>
```

- In the `templates/customers/` folder, create a new file `base.html`:

```html
{% extends 'base_bulma.html' %}
```

- Edit the first line of the following files (the line with the extends statement):

  - customer_create.html

  - customer_detail.html

  - customer_table.html

  - customer_update.html

```html
<!-- {% extends 'base.html' %} FROM THIS-->
{% extends 'customers/base.html' %}
<!-- TO THIS -->
```

- On every `table` elements, add class attribute with the value `class="table"`
