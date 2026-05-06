from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["user", "full_name", "reg_number", "programme", "year_of_study"]
