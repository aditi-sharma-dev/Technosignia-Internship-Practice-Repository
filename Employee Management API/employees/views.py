from django.shortcuts import render
from rest_framework.decorators import api_view
from.serializers import EmployeeSerializer
from.models import Employee
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

@api_view(['POST'])
def add_employee(request):
    serializer=EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
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
    serializer=EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"Employee registerd successfully"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_employee(request):
    email=request.data.get('Email')
    password=request.data.get('Password')
    try:
        employee=Employee.objects.get(Email=email,Password=password)
        return Response({"message":"Login Successfull"},status=status.HTTP_201_CREATED)
    except Employee.DoesNotExist:
        return Response({"message":"Invalid email or password"},status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
def logout_employee(request):
    return Response({"message":"Logout Successfull"},status=status.HTTP_200_OK)

def login_page(request):
    return render(request,"login.html")

def signup_page(request):
    return render(request,"signup.html")
def dashboard(request):
    total_employees=Employee.objects.count()
    context={
        "total_employees":total_employees,
         "active_records":total_employees,
          "recently_added":Employee.objects.order_by("-Emp_Id")[:2].count()
    }
    return render(request,"dashboard.html",context)
