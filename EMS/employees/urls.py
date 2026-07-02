from django.urls import path
from . import views 
urlpatterns = [
    path('add/',views.add_employee,name='add_employee'),
    path('view/',views.view_employee,name='view_employee'),
    path('search/<int:Emp_Id>/',views.serach_employee,name='serach_employee'),
    path('update/<int:Emp_Id>/',views.update_employee,name='update_employee'),
    path('delete/<int:Emp_Id>/',views.delete_employee,name='delete_employee'),
]