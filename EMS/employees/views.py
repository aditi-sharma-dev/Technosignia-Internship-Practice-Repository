from django.shortcuts import render
from rest_framework.decorators import api_view
from.serializers import EmployeeSerializer
from.models import Employee
from rest_framework.response import Response
from rest_framework import status

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
def serach_employee(request,Emp_Id):
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