from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            if not isinstance(field.field.widget, forms.CheckboxInput):
                field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Reservation
        exclude = ['user', ]