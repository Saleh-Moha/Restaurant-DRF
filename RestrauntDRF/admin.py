from django.contrib import admin
from . models import *

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(order_list)
admin.site.register(Cart)