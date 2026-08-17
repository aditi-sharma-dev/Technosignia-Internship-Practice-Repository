from django.db import models 
from django.contrib.auth.models import User 
class Admin(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    Name = models.CharField(max_length=50)

    Email = models.EmailField(unique=True)

    Profile_Photo = models.ImageField(
        upload_to="admin_photos/",
        blank=True,
        null=True,
        default="admin_photos/default.jpg"
    )
    OTP = models.CharField( max_length=6, blank=True,default="")
    OTP_Created_At = models.DateTimeField(blank=True,null=True)
    CreatedBy=models.CharField(max_length=50,blank=True)
    CreatedDate=models.DateTimeField(auto_now_add=True)
    UpdatedBy=models.CharField(max_length=50,blank=True)
    UpdatedDate=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.Name
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
    OTP=models.CharField(max_length=6,blank=True,default="")
    OTP_Created_At=models.DateTimeField(blank=True,null=True)
    CreatedBy=models.CharField(max_length=50,blank=True)
    CreatedDate=models.DateTimeField(auto_now_add=True)
    UpdatedBy=models.CharField(max_length=50,blank=True)
    UpdatedDate=models.DateTimeField(auto_now=True)
    isDeleted=models.BooleanField(default=False)
    def __str__(self):
        return self.Name


class ActivityLog(models.Model):
    ACTION_CHOICES=[
        ("Registration","Registration"),
        ("Login","Login"),
        ("Logout","Logout"),
        ("Create","Create"),
        ("Update","Update"),
        ("Delete","Delete"),
        ("Password Change","Password Change"),
    ]
    ROLE_CHOICES=[("Admin","Admin"),
                  ("User","User")]
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES, null=True,blank=True)
    action=models.CharField(max_length=30,choices=ACTION_CHOICES)
    description=models.CharField(max_length=100)
    timestamp=models.DateTimeField(auto_now_add=True)
    ip_address=models.GenericIPAddressField(null=True,blank=True)
    
    def __str__(self):
        return f"{self.action}-{self.user}"
    
    
    