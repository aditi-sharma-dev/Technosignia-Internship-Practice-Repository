from django.db import models
class Employee(models.Model):
    Emp_Id=models.IntegerField(primary_key=True)
    Name=models.CharField(max_length=50)
    Email=models.EmailField(unique=True)
    Phone_No=models.CharField(max_length=10)
    Address=models.CharField(max_length=50)
    Department=models.CharField(max_length=20)
    Designation=models.CharField(max_length=20)
    Salary=models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return self.Name


