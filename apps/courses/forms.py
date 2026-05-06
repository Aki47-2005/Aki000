from django import forms

from .models import Course, Registration


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "code",
            "title",
            "credit_units",
            "department",
            "prerequisites",
            "semester",
            "capacity",
            "day_of_week",
            "start_time",
            "end_time",
        ]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ["course", "semester"]

    def __init__(self, *args, **kwargs):
        semester = kwargs.pop("semester", None)
        super().__init__(*args, **kwargs)
        courses = Course.objects.all()
        if semester:
            courses = courses.filter(semester=semester)
        self.fields["course"].queryset = courses
