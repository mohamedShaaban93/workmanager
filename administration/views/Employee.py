from administration.decorators import manager_required ,employee_required
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from administration.models import User ,EmployeeStatus,Employee,SwapRequest
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from administration.forms import EmployeeSignupForm
from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
import calendar




@method_decorator([login_required,manager_required] , name='dispatch')
class EmployeeSignupView(CreateView):
    model = User
    form_class = EmployeeSignupForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'add new employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request,'Done! , Add new Employee successfully .......')
        return redirect('employee_signup')


@login_required
@employee_required
def Employee_Home(request):
    year = date.today().year
    month = date.today().month
    data=[]
    month_range=calendar.monthrange(year,month)
    for i in range(month_range[1]):
        day = date(year, month, i + 1)
        if EmployeeStatus.objects.filter(employee=request.user.employee, day=day).count() == 0:
            #     create defualt object to this employee in this day
            emp_type = EmployeeStatus.objects.create(employee=request.user.employee, day=day)
        else:
            # get the object belong to this employee
            print("pppppppppppppppppppp")
            emp_type = EmployeeStatus.objects.get(employee=request.user.employee, day=day)
            print(emp_type)
        data.append({
            'day': day,
            'day_types': emp_type
        })
    #     check if there any swap request
    swapRequest= request.user.employee.SwapRequests.filter(answer=False)
    print("======-------------------------------==========",swapRequest)

    return render(request,'work/employee/employee_home.html',{
            'data':data,
            'swaps':swapRequest
        })


@login_required
@employee_required
def Swap_Request(request,pk):
    shift = EmployeeStatus.objects.get(pk=pk)
    if not SwapRequest.objects.filter(shift = shift).count() == 0 :
        messages.info(request,"your request in progress  , please wait others employee answer")
        return redirect('employee:home')
    else:
        # check if there is employee free
        if EmployeeStatus.objects.filter(day=shift.day, type=4).count() == 0:
            messages.warning(request,"sorry threre is no employee free to take your shift")
            return redirect('employee:home')
        # collocting avalable Employee
        users_ids=[]
        for ele in EmployeeStatus.objects.filter(day=shift.day,type=4):
            users_ids.append(ele.employee.pk)
        users=Employee.objects.filter(pk__in = users_ids)
        # create swap request
        swapRequest = SwapRequest(owner=request.user.employee)
        swapRequest.shift=shift
        swapRequest.save()
        for user in users:
            swapRequest.users.add(user)
        swapRequest.save()
        messages.success(request,'you request sent successfuly , please wait the response !!! ')
        return redirect('employee:home')


@login_required
@employee_required
def Swap_Accept(request,pk):
    swap = SwapRequest.objects.get(pk=pk)
    if swap.answer :
        swap.users.remove(request.user.employee)
        swap.save()
        messages.info(request,"thank you , anther employee take this shift before you")
        return redirect("employee:home")
    else:
        myshift = EmployeeStatus.objects.get(employee=request.user.employee,day=swap.shift.day)
        myshift.type=swap.shift.type
        myshift.save()
        swap.shift.type = 6
        swap.shift.save()
        swap.answer=True
        swap.save()
        messages.success(request,"thank you , you  take this shift")
        return redirect("employee:home")




@login_required
@employee_required
def Swap_Refuse(request,pk):
    swap = SwapRequest.objects.get(pk=pk)
    swap.users.remove(request.user.employee)
    swap.save()
    return redirect("employee:home")



