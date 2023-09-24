from django.db import models
from django import forms
from django.utils import timezone
from datetime import datetime


def uploaded_location(instance, filename):
    return ("%s/%s") %(instance.car_name,filename)

class Car(models.Model):
    image = models.ImageField(upload_to=uploaded_location,null=True, blank=True, width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    car_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    num_of_seats = models.IntegerField()
    cost_par_day = models.CharField(max_length=50)
    content = models.TextField()
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.car_name


    def get_absolute_url(self):
        return "/car/%s/" % (self.id)

class Order(models.Model):
    car_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    cell_no = models.CharField(max_length=10)
    address = models.TextField()
    date = models.DateTimeField()
    to = models.DateTimeField()
    nod=models.IntegerField()
   

    def __int__(self):
        return self.id

    def get_time(self):
        a = self.date.strftime('%m/%d/%Y')
        b = self.to.strftime('%m/%d/%Y')
        a= datetime.strptime(str(a),'%m/%d/%Y')
        b =datetime.strptime(str(b),'%m/%d/%Y')
        delta = b-a
        return delta.days

    def get_absolute_url(self):
        return "/payment/" 
    
    def get_newabsolute_url(self):
        return "/newcar/" 

    def get_editabsolute_url(self):
        return "/car/detail/%s/" % (self.id)

class PrivateMsg(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()


class payment(models.Model):
    paymentid = models.ForeignKey(Order,on_delete=models.CASCADE)
    total_amt = models.CharField(max_length=250)
    bill_date = models.DateTimeField(default=timezone.now)
    card_num =  models.CharField(max_length=16)
    month_year = models.CharField(max_length=5)
    CVV_code =  models.CharField(max_length=3)
    # def __int__(self):
    #     return self.payment_id

    def get_absolute_url(self):
        return "/car/detail/%s/" % (self.paymentid).id

class feedback(models.Model):
    username = models.CharField(max_length=200)
    date =  models.DateTimeField()
    mssg = models.TextField()
    rating = models.CharField(max_length=20)

    def get_absolute_url(self):
        return "/newcar/"

    