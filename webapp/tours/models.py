from __future__ import unicode_literals

from django.db import models
from django.db.models import signals
from django.utils.text import slugify


from employee_accounts.models import EmployeeAccount 

def submit_request_if_not_draft(sender, instance, created, **kwargs):
    if instance.draft is False and instance.is_submitted is False:
        instance.is_submitted = True
        instance.save()

class EmployeeRequestStatus(models.Model):
    status_name = models.CharField(max_length=64, null=True)
    status_link = models.CharField(max_length=64, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = u"Employee Request Status"

    def __unicode__(self):
        return self.status_name

class EmployeeTourRequest(models.Model):
    tour_name = models.CharField(max_length=64, default='My Tour', blank=True)
    purpose = models.TextField()
    employee = models.ForeignKey(EmployeeAccount, limit_choices_to={'account_position_id': 1}, related_name='employee')  
    start_date = models.DateField()
    end_date = models.DateField()
    mode_of_travel = models.CharField(max_length=64, blank=True)
    ticket_cost = models.DecimalField(max_digits=11, decimal_places=2)
    hotel_cost = models.DecimalField(max_digits=11, decimal_places=2, blank=True)
    airport_cab_cost_home = models.DecimalField(max_digits=11, decimal_places=2)
    airport_cab_cost_dest = models.DecimalField(max_digits=11, decimal_places=2)
    bills_image = models.ImageField(null=True, blank=True)
    bills_image_caption = models.CharField(max_length=160, blank=True)
    approving_manager = models.ForeignKey(EmployeeAccount, limit_choices_to={'account_position_id': 2}, related_name='manager')  
    local_conveyance = models.CharField(max_length=128, blank=True)
    draft = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False, db_index=True)
    #request_status = models.CharField(max_length=32, default='Pending')
    request_status = models.ForeignKey(EmployeeRequestStatus, null=True, blank=True, related_name='emp_req_stat')
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u"Employee Tour Request"

    def __unicode__(self):
        return "%s%s/%s/%s" %(
                self.employee.firstname, 
                self.employee.lastname, 
                self.pk,
                slugify(self.tour_name)
            )

signals.post_save.connect(submit_request_if_not_draft, sender=EmployeeTourRequest)

class EmployeeTourRequestStatus(models.Model):
    emp_tour_req = models.ForeignKey(EmployeeTourRequest, related_name='emp_request_status')
    approved_by_manager = models.ForeignKey(EmployeeRequestStatus, default=1, related_name='manager_status')
    submitted_to_finance_manager = models.BooleanField(default=False, db_index=True)
    approving_finance_manager = models.ForeignKey(
            EmployeeAccount, 
            limit_choices_to={'account_position_id': 3}, 
            related_name='finance_manager',
            blank=True, 
            null=True,
        )
    approved_by_finance_manager = models.ForeignKey(EmployeeRequestStatus, default=1, related_name='finance_manager_status')
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = u"Employee Tour Request Status"

    def __unicode__(self):
        return str(self.emp_tour_req)
