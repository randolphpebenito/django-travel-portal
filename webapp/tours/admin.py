from django.contrib import admin
from .models import EmployeeRequestStatus, EmployeeTourRequest, EmployeeTourRequestStatus 

class EmpReqStatusAdmin(admin.ModelAdmin):
    list_display = (
                '__unicode__', 
                'status_link', 
                'timestamp', 
            )

class EmpTourReqAdmin(admin.ModelAdmin):
    list_display = (
                '__unicode__', 
                'start_date',
                'end_date',
                'mode_of_travel',
                'bills_image',
                'approving_manager',
                'draft',
                'is_submitted',
                'request_status',
                'date_modified',
            )
    
class EmpTourReqStatusAdmin(admin.ModelAdmin):
    list_display = (
                '__unicode__', 
                'approving_manager',
                'approved_by_manager',
                'submitted_to_finance_manager',
                'approving_finance_manager',
                'approved_by_finance_manager',
                'date_modified',
            )

    def approving_manager(self, obj):
        return obj.emp_tour_req.approving_manager

admin.site.site_header = "Moving Walls Travel Portal Admin"
admin.site.register(EmployeeRequestStatus, EmpReqStatusAdmin)
admin.site.register(EmployeeTourRequest, EmpTourReqAdmin)
admin.site.register(EmployeeTourRequestStatus, EmpTourReqStatusAdmin)

