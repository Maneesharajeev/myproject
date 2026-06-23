
# Register your models here.
from django.contrib import admin


from django.contrib import admin
from .models import customer, Worker, Saree

admin.site.register(customer)
admin.site.register(Worker)
admin.site.register(Saree)

