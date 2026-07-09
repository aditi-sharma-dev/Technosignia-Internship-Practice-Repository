from django.urls import path
from . import views 
urlpatterns = [
    path('add/',views.add_employee,name='add_employee'),
    path('view/',views.view_employee,name='view_employee'),
    path('search/<int:Emp_Id>/',views.serach_employee,name='serach_employee'),
    path('update/<int:Emp_Id>/',views.update_employee,name='update_employee'),
    path('delete/<int:Emp_Id>/',views.delete_employee,name='delete_employee'),
    path('search-name/',views.search_name,name='search_name'),
    path('search-email/',views.search_email,name='search_email'),
    path('search-department/',views.search_department,name='search_department'),
    path('search-city/',views.search_city,name='search_city'),
    path('pagination/',views.pagination_employee,name='pagination_employee'),
    path('sort-ascending/',views.sort_ascending,name='sort_ascending'),
    path('sort-descending/',views.sort_descending,name='sort_descending'),
    path('signup/',views.signup_employee,name='signup_employee'),
    path('login/',views.login_employee,name='login_employee'),
    path('logout/',views.logout_employee,name='logout_employee'),
]