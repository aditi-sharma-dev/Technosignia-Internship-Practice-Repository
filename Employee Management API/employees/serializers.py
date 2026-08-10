from rest_framework import serializers
from .models import Employee,Admin
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        exclude = ["user"]
        
    def validate_Email(self,value):
        employee = Employee.objects.filter(Email=value).first()
        if employee and self.instance != employee:
            raise serializers.ValidationError("Email already exist")
        return value
   
    def validate_Phone_No(self,value):
        if len(value)!=10:
            raise serializers.ValidationError("Phone no must be 10 digit")
        return value
    def validate_Salary(self,value):
      if value is not None and value <= 0:
            raise serializers.ValidationError("Salary must be greater than zero")
      return value
class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        exclude = ["user"]
