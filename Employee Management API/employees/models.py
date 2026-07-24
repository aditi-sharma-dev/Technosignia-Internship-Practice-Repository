from django.db import models
class Employee(models.Model):
    Emp_Id=models.AutoField(primary_key=True)
    Name=models.CharField(max_length=50)
    Email=models.EmailField(unique=True)
    Password=models.CharField(max_length=30,blank=True)
    Phone_No=models.CharField(max_length=10,blank=True, default="")
    City=models.CharField(max_length=30,blank=True, default="")
    Address=models.CharField(max_length=50,blank=True, default="")
    Department=models.CharField(max_length=20,blank=True, default="")
    Designation=models.CharField(max_length=20,blank=True, default="")
    Salary = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    Status = models.CharField(
        max_length=10,
        choices=[
            ("Active", "Active"),
            ("Inactive", "Inactive")
        ],
        default="Active"
    )
    
    def __str__(self):
        return self.Name


