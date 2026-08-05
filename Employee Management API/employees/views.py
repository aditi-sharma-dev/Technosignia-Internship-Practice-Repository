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
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.conf import settings
import random
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_employee(request):
    employee = Employee.objects.get(user=request.user)
    if employee.Role != "Admin":
       return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    serializer=EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():

            user = User.objects.create_user(
                username=request.data["Email"],
                email=request.data["Email"],
                password=request.data["Password"]
            )

            employee = serializer.save()
            employee.user = user
            employee.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_employee(request):
    employee = Employee.objects.get(user=request.user)
    if employee.Role != "Admin":
      return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    employees=Employee.objects.filter(isDeleted=False)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_employee(request,Emp_Id):
    try:
        employee=Employee.objects.get(Emp_Id=Emp_Id,isDeleted=False)
        serializer=EmployeeSerializer(employee)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response(
            {"message":"Employee Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_employee(request,Emp_Id):
    employee = Employee.objects.get(user=request.user)

    if employee.Role != "Admin":
       return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    try:
        employee=Employee.objects.get(Emp_Id=Emp_Id,isDeleted=False)
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
@permission_classes([IsAuthenticated])
def delete_employee(request,Emp_Id):
    employee = Employee.objects.get(user=request.user)
    if employee.Role != "Admin":
      return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    try:
        employee=Employee.objects.get(Emp_Id=Emp_Id)
    except Employee.DoesNotExist:
        return Response(
            {"message":"Employee Not Found"},
            status=status.HTTP_404_NOT_FOUND
        )
    employee.isDeleted=True
    employee.Status="Inactive"
    employee.save()
    return Response({"message":"Employee delete successfully"},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_name(request):
    name=request.GET.get('name')
    employees=Employee.objects.filter(Name__icontains=name,isDeleted=False)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_department(request):
    department=request.GET.get('department')
    employees=Employee.objects.filter(Department__icontains=department,isDeleted=False)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_email(request):
    email=request.GET.get('email')
    employees=Employee.objects.filter(Email__icontains=email,isDeleted=False)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_city(request):
    city=request.GET.get('city')
    employees=Employee.objects.filter(City__icontains=city,isDeleted=False)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pagination_employee(request):
    employees=Employee.objects.filter(isDeleted=False)
    paginator=PageNumberPagination()
    paginator.page_size=8
    result=paginator.paginate_queryset(employees,request)
    serializer=EmployeeSerializer(result,many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sort_ascending(request):
    employees=Employee.objects.filter(isDeleted=False).order_by('Name')
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sort_descending(request):
    employees=Employee.objects.filter(isDeleted=False).order_by('-Name')
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recently_added(request):

    employees = Employee.objects.filter(isDeleted=False).order_by("-Emp_Id")[:5]

    serializer = EmployeeSerializer(employees, many=True)

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
         with transaction.atomic():
             user=User.objects.create_user(
                 username=request.data["Email"],
                 email=request.data["Email"],
                password=request.data["Password"]
             )
             employee=serializer.save()
             employee.user=user
             employee.save()
             return Response({"message":"Employee registerd successfully"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
def get_tokens_for_employee(employee,user):
    refresh = RefreshToken.for_user(user)
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
    user=authenticate(
        username=email,
        password=password
    )
    
    if user is None:
        return Response(
            {"message": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    try:
        
        employee=Employee.objects.get(user=user)
        if employee.Role != role:
            return Response(
                {"message": "Invalid role"},
                status=status.HTTP_401_UNAUTHORIZED
            )


        tokens=get_tokens_for_employee(employee,user)
        request.session["admin_name"]=employee.Name
        request.session["role"] = employee.Role
        request.session["employee_id"] = employee.Emp_Id
        return Response({"message":"Login Successfull","role":employee.Role,"access":tokens["access"],"refresh":tokens["refresh"]},status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response({"message":"Employee profile not found"},status=status.HTTP_404_NOT_FOUND)
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
    total_employees=Employee.objects.filter(isDeleted=False).count()
    admin = Employee.objects.get(Emp_Id=request.session["employee_id"])

    context={
        "total_employees":total_employees,
         "active_records":Employee.objects.filter(Status="Active",isDeleted=False).count(),
          "recently_added":Employee.objects.filter(isDeleted=False).order_by("-Emp_Id")[:5].count(),
              "admin_name": admin.Name,

          "profile_photo": admin.Profile_Photo.url,

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
@permission_classes([IsAuthenticated])
def filter_status(request):
    status_value=request.GET.get("status")
    if status_value:
        employees=Employee.objects.filter(Status=status_value,isDeleted=False)
    else:
        employees=Employee.objects.filter(isDeleted=False)
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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile(request):
    try:
        employee=Employee.objects.get(user=request.user)
        serializer=EmployeeSerializer(employee)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response({"message":"Profile not found"},status=status.HTTP_404_NOT_FOUND)
def profile_page(request):
    return render(request,'profile.html')
def user_profile_page(request):
    return render(request, "user_profile.html")

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    employee=Employee.objects.get(user=request.user)
    serializer=EmployeeSerializer(employee,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=400)
def update_profile_page(request):
    return render(request, "update_profile.html")
def user_update_profile_page(request):
    return render(request, "user_update_profile.html")

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    employee=Employee .objects.get(user=request.user)
    if "Profile_Photo" not in request.FILES:
        return Response(
            {"message": "No image selected"},
            status=status.HTTP_400_BAD_REQUEST
        )
    employee.Profile_Photo=request.FILES["Profile_Photo"]
    employee.save()
    serializer=EmployeeSerializer(employee)
    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password(request):
    old_password=request.data.get("old_password")
    new_password=request.data.get("new_password")
    confirm_password=request.data.get("confirm_password")
    if not old_password or not new_password or not confirm_password:
        return Response({"message":"All fileds are required"},status=status.HTTP_400_BAD_REQUEST)
    if new_password!=confirm_password:
        return Response({"message":"New password and confirm password do not match"},status=status.HTTP_400_BAD_REQUEST)
    user=request.user
    if not user.check_password(old_password):
        return Response({"message":"Old password is incorrect"}, status=status.HTTP_100_CONTINUE)
    user.set_password(new_password)
    user.save()
    return Response(
        {"message": "Password changed successfully"},
        status=status.HTTP_200_OK
    )


            

def change_password_page(request):
    return render(request, "change_password.html")
def user_change_password_page(request):
    return render(request, "user_change_password.html")
def forgot_password_page(request):
    return render(request, "forgot_password.html")
@api_view(["POST"])
def forgot_password(request):
    email=request.data.get("Email")
    if not email:
        return Response({"message":"Email is required"},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        employee=Employee.objects.get(Email=email)
    except Employee.DoesNotExist:
        return Response({"message":"Employee not found"},status=status.HTTP_400_BAD_REQUEST)
    otp=random.randint(100000,999999)
    employee.OTP=str(otp)
    employee.save()
    
    send_mail(
        subject="Password Reset OTP",
        message=f"Your OTP is: {otp}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response(
        {"message": "OTP sent successfully"},
        status=status.HTTP_200_OK
    )
@api_view(["POST"])
def verify_otp(request):
    email=request.data.get("Email")
    otp=request.data.get("OTP")
    if not email or not otp:
        return Response({"message":"Email and OTP are required"},status=status.HTTP_400_BAD_REQUEST)
    try:
        employee=Employee.objects.get(Email=email)
    except Employee.DoesNotExist:
        return Response({"message":"Employee not found"},status=status.HTTP_400_BAD_REQUEST)
    if employee.OTP!=otp:
        return Response({"message":"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"OTP verified successfully"},status=status.HTTP_200_OK)
def verify_otp_page(request):
    return render(request, "verify_otp.html")
@api_view(["POST"])
def reset_password(request):
    email=request.data.get("Email")
    otp=request.data.get("OTP")
    new_password=request.data.get("new_password")
    confirm_password=request.data.get("confirm_password")
    if not email or not otp or not new_password or not confirm_password:
           return Response({"message":"All fields are required"},status=status.HTTP_400_BAD_REQUEST)
   
    if new_password!=confirm_password:
        return Response({"message":"Password do not match"},status=status.HTTP_400_BAD_REQUEST)
    try:
        employee=Employee.objects.get(Email=email,OTP=otp)
    except Employee.DoesNotExist:
        return Response({"message":"Invalid email or OTP"},status=status.HTTP_400_BAD_REQUEST)
    user=employee.user
    user.set_password(new_password)
    user.save()
    
    employee.OTP=""
    employee.save()
    return Response({"message":"Password reset successfully"},status=status.HTTP_200_OK)
def reset_password_page(request):
    return render(request, "reset_password.html")