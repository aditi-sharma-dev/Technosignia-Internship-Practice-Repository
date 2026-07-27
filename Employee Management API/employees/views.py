from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from.serializers import EmployeeSerializer
from.models import Employee
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
@api_view(['POST'])
def add_employee(request):
    serializer=EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def view_employee(request):
    employees=Employee.objects.all()
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)
@api_view(['GET'])
def search_employee(request,Emp_Id):
    try:
        employee=Employee.objects.get(Emp_Id=Emp_Id)
        serializer=EmployeeSerializer(employee)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response(
            {"message":"Employee Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )
@api_view(['PUT'])
def update_employee(request,Emp_Id):
    try:
        employee=Employee.objects.get(Emp_Id=Emp_Id)
    except Employee.DoesNotExist:
        return Response(
            {"message":"Employee Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer=EmployeeSerializer(employee,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def delete_employee(request,Emp_Id):
    try:
        employee=Employee.objects.get(Emp_Id=Emp_Id)
    except Employee.DoesNotExist:
        return Response(
            {"message":"Employee Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )
    employee.delete()
    return Response({"message":"Employee delete successfully"},status=status.HTTP_200_OK)

@api_view(['GET'])
def search_name(request):
    name=request.GET.get('name')
    employees=Employee.objects.filter(Name__icontains=name)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_department(request):
    department=request.GET.get('department')
    employees=Employee.objects.filter(Department__icontains=department)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_email(request):
    email=request.GET.get('email')
    employees=Employee.objects.filter(Email__icontains=email)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_city(request):
    city=request.GET.get('city')
    employees=Employee.objects.filter(City__icontains=city)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)
@api_view(['GET'])
def pagination_employee(request):
    employees=Employee.objects.all()
    paginator=PageNumberPagination()
    paginator.page_size=3
    result=paginator.paginate_queryset(employees,request)
    serializer=EmployeeSerializer(result,many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def sort_ascending(request):
    employees=Employee.objects.all().order_by('Name')
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def sort_descending(request):
    employees=Employee.objects.all().order_by('-Name')
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)
@api_view(['POST'])
def signup_employee(request):
    if request.data.get("Role")=="Admin" and Employee.objects.filter(Role="Admin").exists():
         return Response(
            {"message": "Admin already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer=EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Employee registerd successfully"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
def get_tokens_for_employee(employee):
    refresh=RefreshToken()
    refresh["Emp_Id"]=employee.Emp_Id
    refresh["Email"]=employee.Email
    refresh["Role"]=employee.Role
    
    return{
        "refresh":str(refresh),
        "access":str(refresh.access_token),
    }
    
    
@api_view(['POST'])
def login_employee(request):
    email=request.data.get('Email')
    password=request.data.get('Password')
    role=request.data.get('Role')
    try:
        employee=Employee.objects.get(Email=email,Password=password,Role=role)
        tokens=get_tokens_for_employee(employee)
        request.session["admin_name"]=employee.Name
        request.session["role"] = employee.Role
        request.session["employee_id"] = employee.Emp_Id
        return Response({"message":"Login Successfull","role":employee.Role,"access":tokens["access"],"refresh":tokens["refresh"]},status=status.HTTP_201_CREATED)
    except Employee.DoesNotExist:
        return Response({"message":"Invalid email or password"},status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
def logout_employee(request):
    request.session.flush()
    return Response({"message":"Logout Successfull"},status=status.HTTP_200_OK)

def login_page(request):
    return render(request,"login.html")

def signup_page(request):  
    admin_exists=Employee.objects.filter(Role="Admin").exists()
    context={
        "admin_exists":admin_exists
    }
    return render(request,"signup.html",context)
def dashboard(request):
    if "admin_name" not in request.session:
        return redirect("login_page")
    total_employees=Employee.objects.count()
    context={
        "total_employees":total_employees,
         "active_records":total_employees,
          "recently_added":Employee.objects.order_by("-Emp_Id")[:2].count(),
          "admin_name":request.session.get("admin_name")
    }
    return render(request,"dashboard.html",context)
def add_employee_page(request):
    return render(request,'add_employee.html')    
def view_employee_page(request):
    return render(request,'view_employee.html')  
def update_employee_page(request,Emp_Id):
    try:
        employee=Employee.objects.get(Emp_Id=Emp_Id)
    except Employee.DoesNotExist:
             return render(request,'update_employee.html')
    context={
        "employee":employee
    }
    return render(request,'update_employee.html',context)
@api_view(['GET'])
def filter_status(request):
    status_value=request.GET.get("status")
    if status_value:
        employees=Employee.objects.filter(Status=status_value)
    else:
        employees=Employee.objects.all()
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)
def user_dashboard(request):
    if "admin_name" not in request.session:
        return redirect("login_page")
    employee = Employee.objects.get(Emp_Id=request.session["employee_id"])

    context = {
        "employee": employee
    }

    return render(request,'user_dashboard.html',context)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_route(request):
    return Response({
        "message": "JWT Token Verified Successfully"
    })
    