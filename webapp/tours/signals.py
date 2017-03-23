from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EmployeeTourRequest, EmployeeTourRequestStatus 

@receiver(post_save, sender=EmployeeTourRequest)
def create_employee_tour_request_status(sender, instance, created, **kwargs):
    if created:
        if instance.is_submitted:
            EmployeeTourRequestStatus.objects.create(emp_tour_req=instance)
