from django.contrib import admin
from .models import Car, Order, PrivateMsg, payment, feedback
# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ("car_name", "image", "company_name")
class OrderAdmin(admin.ModelAdmin):
    list_display = ("car_name", "date", "to", "full_name")

class PrivateMsgAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message")

class paymentAdmin(admin.ModelAdmin):
    list_display = ("total_amt","bill_date","card_num","month_year","CVV_code","paymentid")

class feedbackAdmin(admin.ModelAdmin):
    list_display = ("username","date","mssg","rating")
    


admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PrivateMsg, PrivateMsgAdmin)
admin.site.register(payment,paymentAdmin )
admin.site.register(feedback,feedbackAdmin )