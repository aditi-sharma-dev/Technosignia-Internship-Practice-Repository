from rest_framework import serializers
from .models import Employee,Admin,ActivityLog
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



class ActivityLogSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog

        fields = [
            "id",
            "user_id",
            "user",
            "role",
            "action",
            "description",
            "ip_address",
            "timestamp"
        ]

    def get_user(self, obj):

        if not obj.user:
            return "-"

        try:
            admin = Admin.objects.get(user=obj.user)
            return admin.Name

        except Admin.DoesNotExist:
            pass

        try:
            employee = Employee.objects.get(user=obj.user)
            return employee.Name

        except Employee.DoesNotExist:
            return obj.user.username

    def get_user_id(self, obj):

        if not obj.user:
            return "-"

        try:
            admin = Admin.objects.get(user=obj.user)
            return 1

        except Admin.DoesNotExist:
            pass

        try:
            employee = Employee.objects.get(user=obj.user)

           
            return employee.Emp_Id

        except Employee.DoesNotExist:
            return "-"