from django.contrib.auth.forms import UserCreationForm
from administration.models import User,Employee
from django.db import transaction





class ManagerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        if commit:
            user.save()
        return user



class EmployeeSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic()
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_empolyee = True
        user.save()
        employee = Employee.objects.create(user=user)
        return user

