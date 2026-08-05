from django.db import models 
from django.contrib.auth.models import User 
class Employee(models.Model):
   
    Emp_Id=models.IntegerField(primary_key=True)
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    
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
    Role=models.CharField(
        max_length=10,
        choices=[
            ("Admin","Admin"),
            ("User","User"),
        ],
        default="User"
    )
    Profile_Photo=models.ImageField(upload_to='profile_photos/',blank=True,null=True, default="profile_photos/default.jpg")
    OTP=models.CharField(max_length=6,blank=True,default=True)
    OTP_Created_At=models.DateTimeField(blank=True,null=True)
    
    isDeleted=models.BooleanField(default=False)
    def __str__(self):
        return self.Name


