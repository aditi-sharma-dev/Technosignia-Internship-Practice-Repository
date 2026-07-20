from rest_framework import serializers
from .models import Employee
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields="__all__"
    def validate_Email(self,value):
        if Employee.objects.filter(Email=value).exists():
            raise serializers.ValidationError("Email already exist")
        return value
    def validate_Phone_No(self,value):
        if len(value)!=10:
            raise serializers.ValidationError("Phone no must be 10 digit")
        return value
    def validate_Salary(self,value):
        if value<=0:
            raise serializers.ValidationError("Salary must be greater than zero")
        return value