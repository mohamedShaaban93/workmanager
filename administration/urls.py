from django.urls import path , include
from administration.views import Manager,Employee


urlpatterns=[
    path('', Manager.home, name='home'),
    path('manager/', include(([
                                  path('', Manager.Manager_Home, name='home'),
                                  path('changestatus/<int:type_num>/<int:status_pk>', Manager.Change_Status, name='change_status'),
                                  path('manageWork/', Manager.Work_Hours_show , name='work_hour'),
                                  path('WorkHourManage/<int:hour_num>/<int:hour_type>/<int:work_pk>', Manager.Work_Hours_manage , name='work_hour_manage'),
                                  path('reports/', Manager.reports_show , name='reports'),
                                  path('report/', Manager.report_show , name='show_report'),
                              ], 'administration'), namespace='manager')),
    path('employee/', include(([
                                   path('', Employee.Employee_Home, name='home'),
                                   path('swap/<int:pk>', Employee.Swap_Request, name='swap'),
                                   path('swapaccept/<int:pk>', Employee.Swap_Accept, name='swapaccept'),
                                   path('swaprefuse/<int:pk>', Employee.Swap_Refuse, name='swaprefuse'),
                               ], 'administration'), namespace='employee')),
]