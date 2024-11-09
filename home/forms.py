# Import necessary modules
from django import forms
from .models import WeightEntry  # Import the WeightEntry model to use it in forms

# Form for adding a weight entry
class AddWeightForm(forms.ModelForm):
    class Meta:
        model = WeightEntry  # Specifies the model that this form will interact with
        fields = ['weight']  # The form will only have a 'weight' field (not other fields like 'user' or 'date')

# Form for selecting a date range
class DateRangeForm(forms.Form):
    # This form is not tied to a model, so we use forms.Form
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))  # 'start_date' field with a date input widget
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))  # 'end_date' field with a date input widget
