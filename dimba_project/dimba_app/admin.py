from django.contrib import admin
from .models import Expense
from .models import Savings
from .models import Loan

# Register your models here.

admin.site.register(Expense)
admin.site.register(Savings)
admin.site.register(Loan)
