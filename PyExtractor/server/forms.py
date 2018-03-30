from datetime import date
from django import forms
from server.models import DEPARTMENTS, asset, CHOICE


def setup_field(field, placeholder=None):
    """
    This configures the given field to play nice with the bootstrap theme. Additionally, you can add
    an additional argument to set a placeholder text on the field.
    """
    field.widget.attrs['class'] = 'form-control'
    if placeholder is not None:
        field.widget.attrs['placeholder'] = placeholder


class BasicForm(forms.Form):
    def disable_field(self, field):
        """
        marks field as disabled
        :param field: name of the field
        """
        self.fields[field].widget.attrs['disabled'] = ""

    def mark_error(self, field, description):
        """
        Marks the given field as errous. The given description is displayed when the form it generated
        :param field: name of the field
        :param description: The error description
        """
        self._errors[field] = self.error_class([description])
        del self.cleaned_data[field]

    def clear_errors(self):
        self._errors = {}


class QueryForm(BasicForm):
	department = forms.ChoiceField(choices=DEPARTMENTS)
	setup_field(department,'Select the department')
	latitude = forms.CharField(required=True, max_length=50)
	setup_field(latitude,'Enter the latitude')
	longitude = forms.CharField(required=True, max_length=50)
	setup_field(longitude,'Enter the longitude')
	distance = forms.CharField(required=True, max_length=50)
	setup_field(distance,'Enter the distance(in km)')
	choice = forms.ChoiceField(choices=CHOICE)
	setup_field(choice,'Choose your choice')
	input_text = forms.CharField(required=True, max_length=50)
	setup_field(input_text,'Enter the value')

	def assign(self, query):
		query.department = self.cleaned_data['department']
		query.latitude = self.cleaned_data['latitude']
		query.longitude = self.cleaned_data['longitude']
		query.distance = self.cleaned_data['distance']
		query.choice = self.cleaned_data['choice']
		query.input_text = self.cleaned_data['input_text']
 