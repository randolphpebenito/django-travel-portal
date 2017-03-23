import floppyforms.__future__ as forms
#from django import forms


from pagedown.widgets import PagedownWidget

from .models import EmployeeTourRequest

class EmployeeTourRequestForm(forms.ModelForm):
    purpose = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = EmployeeTourRequest
        fields = [
            'tour_name',
            'purpose',
            'start_date',
            'end_date',
            'mode_of_travel',
            'ticket_cost',
            'hotel_cost',
            'airport_cab_cost_home',
            'airport_cab_cost_dest',
            'bills_image',
            'bills_image_caption',
            'approving_manager',
            'local_conveyance',
            'draft',
        ]

    def clean(self):
        cleaned_data = super(EmployeeTourRequestForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date < start_date:
            msg = u"End date should be greater than or equal to start date."
            self._errors["end_date"] = self.error_class([msg])
