from django.contrib import admin

from .models import EmployeeAccountPosition, EmployeeAccount

class EmpAccPosAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'timestamp')

class EmpAccAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'account_position', 'date_modified', 'date_created')

admin.site.register(EmployeeAccountPosition, EmpAccPosAdmin)
admin.site.register(EmployeeAccount, EmpAccAdmin)
