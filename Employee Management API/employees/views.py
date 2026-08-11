from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
from.serializers import EmployeeSerializer,AdminSerializer
from.models import Employee,Admin
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
from django.utils import timezone
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_employee(request):
    try:
        admin = Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
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

            employee = serializer.save(
                CreatedBy=admin.Name,
                UpdatedBy=admin.Name
            )
            employee.user = user
            employee.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_employee(request):
    try:
       admin = Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
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
    try:
       admin = Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
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
        serializer.save(
            UpdatedBy=admin.Name
        )
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_employee(request,Emp_Id):
    try:
       admin = Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
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
    employee.UpdatedBy=admin.Name
    employee.save()
    return Response({"message":"Employee delete successfully"},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_name(request):
    try:
      Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
       return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    name=request.GET.get('name')
    employees=Employee.objects.filter(Name__icontains=name,isDeleted=False)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_department(request):
    try:
       Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
     return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    department=request.GET.get('department')
    employees=Employee.objects.filter(Department__icontains=department,isDeleted=False)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_email(request):
    try:
      Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
     return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    email=request.GET.get('email')
    employees=Employee.objects.filter(Email__icontains=email,isDeleted=False)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_city(request):
    try:
       Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
       return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    city=request.GET.get('city')
    employees=Employee.objects.filter(City__icontains=city,isDeleted=False)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pagination_employee(request):
    try:
       Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
      return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    employees=Employee.objects.filter(isDeleted=False)
    paginator=PageNumberPagination()
    paginator.page_size=8
    result=paginator.paginate_queryset(employees,request)
    serializer=EmployeeSerializer(result,many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sort_ascending(request):
    try:
      Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
       return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    employees=Employee.objects.filter(isDeleted=False).order_by('Name')
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sort_descending(request):
    try:
     Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
     return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    employees=Employee.objects.filter(isDeleted=False).order_by('-Name')
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recently_added(request):
    try:
      Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
       return Response(
         {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )

    employees = Employee.objects.filter(isDeleted=False).order_by("-Emp_Id")[:5]

    serializer = EmployeeSerializer(employees, many=True)

    return Response(serializer.data)
@api_view(['POST'])
def signup_employee(request):

    role = request.data.get("Role")

    if role == "Admin":

        if Admin.objects.exists():
            return Response(
                {"message": "Admin already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AdminSerializer(data={
            "Name": request.data.get("Name"),
            "Email": request.data.get("Email")
        })

        if serializer.is_valid():

            with transaction.atomic():

                user = User.objects.create_user(
                    username=request.data["Email"],
                    email=request.data["Email"],
                    password=request.data["Password"]
                )

                admin = serializer.save(
                    CreatedBy=request.data.get("Name"),
                    UpdatedBy=request.data.get("Name")
                )
                admin.user = user
                admin.save()

            return Response(
                {"message": "Admin Registered Successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)

    else:

        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():

            with transaction.atomic():

                user = User.objects.create_user(
                    username=request.data["Email"],
                    email=request.data["Email"],
                    password=request.data["Password"]
                )

                employee = serializer.save(
                       CreatedBy=request.data.get("Name"),
                       UpdatedBy=request.data.get("Name")
                )
                employee.user = user
                employee.save()

            return Response(
                {"message": "Employee Registered Successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)

def get_tokens(user, role, id, email):

    refresh = RefreshToken.for_user(user)

    refresh["id"] = id
    refresh["Email"] = email
    refresh["Role"] = role

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    

@api_view(['POST'])
def login_employee(request):

    email = request.data.get("Email")
    password = request.data.get("Password")
    role = request.data.get("Role")

    user = authenticate(
        username=email,
        password=password
    )

    if user is None:
        return Response(
            {"message": "Invalid Email or Password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if role == "Admin":

        try:
            admin = Admin.objects.get(user=user)

            tokens = get_tokens(
                user,
                "Admin",
                admin.id,
                admin.Email
            )

            request.session["admin_id"] = admin.id
            request.session["admin_name"] = admin.Name
            request.session["role"] = "Admin"

            return Response({
                "message": "Login Successful",
                "role": "Admin",
                "access": tokens["access"],
                "refresh": tokens["refresh"]
            })

        except Admin.DoesNotExist:

            return Response(
                {"message": "Admin not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    else:

        try:

            employee = Employee.objects.get(user=user)

            tokens = get_tokens(
                user,
                "User",
                employee.Emp_Id,
                employee.Email
            )

            request.session["employee_id"] = employee.Emp_Id
            request.session["employee_name"] = employee.Name
            request.session["role"] = "User"

            return Response({
                "message": "Login Successful",
                "role": "User",
                "access": tokens["access"],
                "refresh": tokens["refresh"]
            })

        except Employee.DoesNotExist:

            return Response(
                {"message": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND
            )
@api_view(['POST'])
def logout_employee(request):
    request.session.flush()
    return Response({"message":"Logout Successfull"},status=status.HTTP_200_OK)

def login_page(request):
    return render(request,"login.html")

def signup_page(request):  
    admin_exists = Admin.objects.exists()
    context={
        "admin_exists":admin_exists
    }
    return render(request,"signup.html",context)
def dashboard(request):

    if "admin_id" not in request.session:
        return redirect("login_page")

    admin = Admin.objects.get(id=request.session["admin_id"])

    context = {
        "total_employees": Employee.objects.filter(
            isDeleted=False
        ).count(),

        "active_records": Employee.objects.filter(
            Status="Active",
            isDeleted=False
        ).count(),

        "recently_added": Employee.objects.filter(
            isDeleted=False
        ).order_by("-Emp_Id")[:5].count(),

        "admin_name": admin.Name,
        "profile_photo": admin.Profile_Photo.url,
    }

    return render(request, "dashboard.html", context)
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
    try:
       Admin.objects.get(user=request.user)
    except Admin.DoesNotExist:
     return Response(
        {"message": "Access Denied"},
        status=status.HTTP_403_FORBIDDEN
    )
    status_value=request.GET.get("status")
    if status_value:
        employees=Employee.objects.filter(Status=status_value,isDeleted=False)
    else:
        employees=Employee.objects.filter(isDeleted=False)
    serializer=EmployeeSerializer(employees,many=True)
    return Response(serializer.data)
def user_dashboard(request):
    if "employee_id" not in request.session:
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

    role = request.session.get("role")

    if role == "Admin":

        try:
            admin = Admin.objects.get(user=request.user)
            serializer = AdminSerializer(admin)
            return Response(serializer.data)

        except Admin.DoesNotExist:
            return Response(
                {"message": "Admin profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    else:

        try:
            employee = Employee.objects.get(user=request.user)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)

        except Employee.DoesNotExist:
            return Response(
                {"message": "Employee profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )      

def profile_page(request):
    return render(request,'profile.html')
def user_profile_page(request):
    return render(request, "user_profile.html")
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        admin = Admin.objects.get(user=request.user)

        serializer = AdminSerializer(
            admin,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save(
                UpdatedBy=admin.Name
            )

            admin.user.email = admin.Email
            admin.user.username = admin.Email
            admin.user.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    except Admin.DoesNotExist:
        return Response(
            {"message": "Admin profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )

def update_profile_page(request):
    return render(request, "update_profile.html")
def user_update_profile_page(request):
    return render(request, "user_update_profile.html")
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def user_update_profile(request):

    try:
        employee = Employee.objects.get(user=request.user)

        serializer = EmployeeSerializer(
            employee,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save(
                UpdatedBy=employee.Name
                
            )

            
            employee.user.email = employee.Email
            employee.user.username = employee.Email
            employee.user.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    except Employee.DoesNotExist:

        return Response(
            {"message": "Employee profile not found"},
            status=status.HTTP_404_NOT_FOUND
        )
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
        return Response({"message":"Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST
)
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

    email = request.data.get("Email")

    if not email:
        return Response(
            {"message": "Email is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    otp = random.randint(100000, 999999)

    # Admin Check
    try:
        admin = Admin.objects.get(Email=email)

        admin.OTP = str(otp)
        admin.OTP_Created_At = timezone.now()
        admin.save()

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

    except Admin.DoesNotExist:
        pass

    # Employee Check
    try:
        employee = Employee.objects.get(Email=email)

        employee.OTP = str(otp)
        employee.OTP_Created_At = timezone.now()

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

    except Employee.DoesNotExist:
        return Response(
            {"message": "Email not found"},
            status=status.HTTP_400_BAD_REQUEST
        )
@api_view(["POST"])
def verify_otp(request):

    email = request.data.get("Email")
    otp = request.data.get("OTP")

    if not email or not otp:
        return Response(
            {"message": "Email and OTP are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Admin Check
    try:
        admin = Admin.objects.get(Email=email)

        if admin.OTP == otp:
            return Response(
                {"message": "OTP verified successfully"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Invalid OTP"},
            status=status.HTTP_400_BAD_REQUEST
        )

    except Admin.DoesNotExist:
        pass

    # Employee Check
    try:
        employee = Employee.objects.get(Email=email)

        if employee.OTP == otp:
            return Response(
                {"message": "OTP verified successfully"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Invalid OTP"},
            status=status.HTTP_400_BAD_REQUEST
        )

    except Employee.DoesNotExist:
        return Response(
            {"message": "Email not found"},
            status=status.HTTP_400_BAD_REQUEST
        )
@api_view(["POST"])
def reset_password(request):

    email = request.data.get("Email")
    otp = request.data.get("OTP")
    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")

    if not email or not otp or not new_password or not confirm_password:
        return Response(
            {"message": "All fields are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_password != confirm_password:
        return Response(
            {"message": "Password do not match"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Admin Check
    try:
        admin = Admin.objects.get(Email=email, OTP=otp)

        user = admin.user
        user.set_password(new_password)
        user.save()

        admin.OTP = ""
        admin.save()

        return Response(
            {"message": "Password reset successfully"},
            status=status.HTTP_200_OK
        )

    except Admin.DoesNotExist:
        pass

    # Employee Check
    try:
        employee = Employee.objects.get(Email=email, OTP=otp)

        user = employee.user
        user.set_password(new_password)
        user.save()

        employee.OTP = ""
        employee.save()

        return Response(
            {"message": "Password reset successfully"},
            status=status.HTTP_200_OK
        )

    except Employee.DoesNotExist:
        return Response(
            {"message": "Invalid Email or OTP"},
            status=status.HTTP_400_BAD_REQUEST
        )

def verify_otp_page(request):
    return render(request, "verify_otp.html")

def reset_password_page(request):
    return render(request, "reset_password.html")