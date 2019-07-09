from django.shortcuts import render,redirect
from django.views.generic import TemplateView ,CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from administration.decorators import manager_required
from administration.models import User
from django.contrib.auth import login
from administration.forms import ManagerSignUpForm
from django.http import HttpResponse , JsonResponse,HttpResponseRedirect
import calendar
from datetime import date
from administration.models import Employee,EmployeeStatus,workHours
from django.contrib import messages


@method_decorator([login_required,manager_required] , name='dispatch')
class SignUpView(TemplateView):
    template_name = 'registration/signup.html'



@method_decorator([login_required,manager_required] , name='dispatch')
class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Signup as a Manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('signup')


def home(request):
    if request.user.is_authenticated:
        if request.user.is_empolyee:
            return redirect('employee:home')#employee home page
        else:
            return redirect('manager:home')#manager home page
    return  render(request,'work/home.html')#home pag


@login_required
@manager_required
def Manager_Home(request):
    if request.method == 'POST':
        month = (date.today().month) +1
        month_type=1
    else:
        month_type=0
        month=date.today().month
    year = date.today().year
    days=[]
    data=[]
    day_types=[]
    all_type=[]
    # collecting data with the month in work
    employees=Employee.objects.all()
    month_range=calendar.monthrange(year,month)
    for i in range(month_range[1]):
        day=date(year,month,i+1)
        # add this day to those month days
        days.append(day)
        for emp in employees:
            if EmployeeStatus.objects.filter(employee=emp,day=day).count() == 0 :
                #     create defualt object to this employee in this day
                emp_type=EmployeeStatus.objects.create(employee=emp,day=day)
            else:
                # get the object belong to this employee
                emp_type=EmployeeStatus.objects.get(employee=emp,day=day)
            # add the object to this day types
            day_types.append(emp_type)
        data.append({
            'day':day,
            'day_types':day_types
            })
        day_types=[]
        # add those day types to all type
        all_type.append(day_types)
    return render(request,'work/manager/manager_home.html',{
        'days' : days,
        'data':data,
        'all_types':all_type,
        'employees':employees,
        'month_type':month_type
    })


@login_required
@manager_required
def Change_Status(request,type_num,status_pk):
    emp = EmployeeStatus.objects.get(pk=status_pk)
    emp.type=type_num
    emp.save()
    return JsonResponse({"success": True}, status=200)


@login_required
@manager_required
def Work_Hours_show(request):
    if request.method == 'POST':
        if not request.POST['date']:
            messages.error(request,"must select date")
            return redirect('manager:home')
        day_pattern=request.POST['date'].split('-')
        if int(day_pattern[0]) != date.today().year or abs(int(day_pattern[1])-date.today().month) > 1 :
            messages.warning(request, "please select valid date")
            return redirect('manager:home')
        data=[]
        day=date(int(day_pattern[0]),int(day_pattern[1]),int(day_pattern[2]))
        shift=int(request.POST['shift'])
        Shift_hours = EmployeeStatus.objects.filter(day=day,type=shift)
        # collect the Work hours from database for each empolyee
        for ele in Shift_hours:
            if workHours.objects.filter(status=ele).count() == 0:
                #     create default object
                work_object = workHours.objects.create(status=ele)
            else:
                #        get the object existed in database
                work_object = workHours.objects.get(status=ele)
            data.append({
                'shift':ele,
                'workhour':work_object
            })

        return render(request,'work/manager/shiftworks.html',{
            'type':shift,
            'data':data
        })
    else:
        return redirect('manager:home')


@login_required
@manager_required
def Work_Hours_manage(request,hour_num,hour_type,work_pk):
    work = workHours.objects.get(pk=work_pk)
    breakNum=work.breakNum
    if breakNum == 2 and hour_type == 0:
    #     not valid
        return JsonResponse({'success':False},status=200)
    elif breakNum == 0 and hour_type ==1 :
        print("noooooooooooooooooo")
        return JsonResponse({'success':True},status=200)
    if hour_type == 0:
        if hour_num == 1:
             if work.one:
                 work.one = False
                 work.breakNum = breakNum + 1
        elif hour_num == 2:
            if work.two:
                work.two = False
                work.breakNum = breakNum + 1
        elif hour_num == 3:
            if work.three:
                work.three = False
                work.breakNum = breakNum + 1

        elif hour_num == 4:
            if work.four:
                work.four = False
                work.breakNum = breakNum + 1
        elif hour_num == 5:
            if work.five:
                work.five = False
                work.breakNum = breakNum + 1
        elif hour_num == 6:
            if work.six:
                work.six = False
                work.breakNum = breakNum + 1
        elif hour_num == 7:
            if work.seven:
                work.seven = False
                work.breakNum = breakNum + 1
        elif hour_num == 8:
            if work.eight:
                work.eight = False
                work.breakNum = breakNum + 1
    #     ============================================

    else:
        if hour_num == 1:
             if not work.one:
                 work.one = True
                 work.breakNum = breakNum - 1
        elif hour_num == 2:
            if not work.two:
                work.two = True
                work.breakNum = breakNum -1
        elif hour_num == 3:
            if not work.three:
                work.three = True
                work.breakNum = breakNum - 1

        elif hour_num == 4:
            if not work.four:
                work.four = True
                work.breakNum = breakNum - 1
        elif hour_num == 5:
            if not work.five:
                work.five = True
                work.breakNum = breakNum - 1
        elif hour_num == 6:
            if not work.six:
                work.six = True
                work.breakNum = breakNum - 1
        elif hour_num == 7:
            if not work.seven:
                work.seven = True
                work.breakNum = breakNum - 1
        elif hour_num == 8:
            if not work.eight:
                work.eight = True
                work.breakNum = breakNum - 1
    work.save()
    return JsonResponse({"success": True}, status=200)



@login_required
@manager_required
def reports_show(request):
    data=[]
    employees = Employee.objects.all()
    for emp in employees:
        data.append({
            'employee':emp,
            'hour_number':get_work_hour(emp,year = date.today().year, month = date.today().month)[0]
        })

    return render(request,'work/manager/reports.html',{
        'data':data,
        'employees':employees
    })


@login_required
@manager_required
def report_show(request):
    month=date.today().month
    year=date.today().year
    if request.method == 'POST' :
        print("==================",request.POST)
        if not request.POST['date']:
            messages.error(request,"must select date")
            return redirect('manager:reports')
        day_pattern=request.POST['date'].split('-')
        if int(day_pattern[0]) != year or abs(int(day_pattern[1])-month) > 2 :
            messages.warning(request, "please select valid date")
            return redirect('manager:reports')
        emp=Employee.objects.get(pk=request.POST['employee'])
        report=get_work_hour(emp,int(day_pattern[0]),int(day_pattern[1]))
        return render(request,'work/manager/report_show.html',{
            'hour_num':report[0],
            'break_num': report[1],
            'work_day':report[2],
            'off_day':report[3],
            'employee':emp,
            'date':f"{month} / {year}"
        })


    else:
        return redirect('home')

def get_work_hour(emp:Employee,year:int,month:int):
    month_range = calendar.monthrange(year,month)
    data=[]
    for i in range(month_range[1]):
        day= date(date.today().year,date.today().month,i+1)
        temp = EmployeeStatus.objects.get(employee=emp,day=day)
        data.append(temp)

    num = 0
    breaks = 0
    work_days = 0
    off_day = 0
    for ele in data :
        if not hasattr(ele, 'workhours'):
            workHours.objects.create(status=ele)
        if ele.type < 4:
            work_days = work_days + 1
            if ele.workhours.breakNum == 0 :
                num = num + 8
            elif ele.workhours.breakNum == 1:
                num =num +7
                breaks =breaks+1
            else:
                num = num + 6
                breaks =breaks + 2
        else:
            off_day = off_day + 1
    return [num,breaks,work_days,off_day]
