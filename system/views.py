from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse , HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from .models import Car, Order, PrivateMsg, payment, feedback
from .forms import CarForm, OrderForm, MessageForm, PaymentForm, FeedbackForm
from datetime import date, datetime

ls = []

def home(request):
    context = {
        "title" : "Car Rental"
    }
    return render(request,'home.html', context)

def home1(request):
    context = {
        "title" : "Car Rental"
    }
    return render(request,'home1.html', context)

def car_list(request):
    car = Car.objects.all()

    query = request.GET.get('q')
    if query:
        car = car.filter(
                     Q(car_name__icontains=query) |
                     Q(company_name__icontains = query) |
                     Q(num_of_seats__icontains=query) |
                     Q(cost_par_day__icontains=query)
                            )

    # pagination
    paginator = Paginator(car, 8)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        car = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        car = paginator.page(paginator.num_pages)
    context = {
        'car': car,
    }
    return render(request, 'car_list.html', context)

def car_detail(request, id=None):
    f_back = feedback.objects.all().values_list('username','rating','date','mssg')
    # f_back.append(feedback.objects.all())[0]
    detail = get_object_or_404(Car,id=id)
    val =ls
    context = {
        "val":val,
        "f_back": f_back,
        "detail": detail
    }
    return render(request, 'car_detail.html', context)

def car_created(request):
    form = CarForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/")
    context = {
        "form" : form,
        "title": "Create Car"
    }
    return render(request, 'car_create.html', context)

def car_update(request, id=None):
    detail = get_object_or_404(Car, id=id)
    form = CarForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title": "Update Car"
    }
    return render(request, 'car_create.html', context)

def car_delete(request,id=None):
    query = get_object_or_404(Car,id = id)
    query.delete()

    car = Car.objects.all()
    context = {
        'car': car,
    }
    return render(request, 'admin_index.html', context)

#order

def order_list(request):
    order = Order.objects.all()

    query = request.GET.get('q')
    if query:
        order = order.filter(
            Q(movie_name__icontains=query)|
            Q(employee_name__icontains=query)
        )

    # pagination
    paginator = Paginator(order, 8)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        order = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        order = paginator.page(paginator.num_pages)
    context = {
        'order': order,
    }
    return render(request, 'order_list.html', context)

def order_detail(request, id=None):
    detail = get_object_or_404(Order,id=id)
    context = {
        "detail": detail,
    }
    return render(request, 'order_detail.html', context)


def order_created(request):
    form = OrderForm(request.POST or None)
    global ls
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.get_time()>30:
            messages.info(request, "Oops, Cannot rent beyond 30 days!")
            # return HttpResponseRedirect("/createOrder/")
            # instance.nod = 0
            # instance.save()
            # return render(request,"ord_create.html", {"error":"Can't rent beyond 30 days"})
        elif instance.get_time()==0: 
            messages.info(request, "Oops, Choose atleast 1 day")
        else:  
            instance.nod = instance.get_time()
            ls.append(instance.car_name)
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "title": "Create Order"
    }
    return render(request, 'order_create.html', context)

def order_update(request, id=None):
    detail = get_object_or_404(Order, id=id)
    form = OrderForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_editabsolute_url())
    context = {
        "form": form,
        "title": "Update Order"
    }
    return render(request, 'order_create.html', context)

def order_delete(request,id=None):
    query = get_object_or_404(Order,id = id)
    global ls,us
    del ls[-1]
    us=""
    messages.info(request, "Your order has been succesfully cancelled!")
    query.delete()
    
    return HttpResponseRedirect("/car/nicecar/")

def newcar(request):
    new = Car.objects.order_by('-id')
    #seach
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query)
        )

    # pagination
    paginator = Paginator(new, 8)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        new = paginator.page(paginator.num_pages)
  
    val =ls
    
    context = {
        'val':val,
        'car': new,
    }
    return render(request, 'new_car.html', context)

def nicecar(request):
    new = Car.objects.order_by('-id')
    #seach
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query)
        )

    # pagination
    paginator = Paginator(new, 8)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        new = paginator.page(paginator.num_pages)
  

    
    context = {

        'car': new,
    }
    return render(request, 'nicecar.html', context)

def like_update(request, id=None):
    new = Car.objects.order_by('-id')
    like_count = get_object_or_404(Car, id=id)
    like_count.like+=1
    like_count.save()
    # context = {
    #     'car': new,
    # }
    return HttpResponseRedirect("/car/newcar/")

def popular_car(request):
    new = Car.objects.order_by('-like')
    # seach
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query)
        )
    

    # pagination
    paginator = Paginator(new,8)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        new = paginator.page(paginator.num_pages)

    val =ls
    context = {
        'val':val,
        'car': new,
    }
    return render(request, 'popular_car.html', context)

def contact(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/car/newcar/")
    context = {
        "form": form,
        "title": "Contact With Us",
    }
    return render(request,'contact.html', context)

def p_payment(request):
    amount = Car.objects.all()[0].cost_par_day
    obj = Order.objects.last()
    fobj = Order._meta.get_field('nod')
    nd = fobj.value_from_object(obj)
    t_amt = str(nd*int(amount))
    form = PaymentForm(request.POST or None)
    b_date = datetime.now()
    if form.is_valid():
        instance = form.save(commit=False)
        instance.paymentid = Order.objects.all().last()
        instance.total_amt = t_amt
        instance.CVV_code = "***"
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "b_date": b_date,
        "t_amt": t_amt,
        "form": form,
        "title": "Payment"
    }
    return render(request, 'payment.html', context)

def f_feedback(request, id =None):
    form = FeedbackForm(request.POST or None)
    f_date = datetime.now()
    if form.is_valid():
        instance = form.save(commit=False)
        instance.username = request.user
        instance.date = f_date
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "f_date": f_date,
        "form": form,
        "title": "Feed Back",
    }
    return render(request,'feedback.html', context)
    

#-----------------Admin Section-----------------

def admin_car_list(request):
    car = Car.objects.order_by('-id')

    query = request.GET.get('q')
    if query:
        car = car.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query)
        )

    # pagination
    paginator = Paginator(car, 8)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        car = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        car = paginator.page(paginator.num_pages)
    context = {
        'car': car,
    }
    return render(request, 'admin_index.html', context)

def admin_msg(request):
    msg = PrivateMsg.objects.order_by('-id')
    context={
        "car": msg,
    }
    return render(request, 'admin_msg.html', context)

def msg_delete(request,id=None):
    query = get_object_or_404(PrivateMsg, id=id)
    query.delete()
    return HttpResponseRedirect("/message/")
