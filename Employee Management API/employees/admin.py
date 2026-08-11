from django.contrib import admin
from.models import Employee, Admin
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display=("Emp_Id",
                  "Name",
                  "Email",
                  "Password",
                  "Phone_No",
                  "City",
                  "Address",
                  "Department",
                  "Designation",
                  "Salary",
                  "Status",
                  "Role",
                  "Profile_Photo",
                   "CreatedBy",
                  "CreatedDate",
                  "UpdatedBy",
                  "UpdatedDate",
                   "OTP",
                  "OTP_Created_At",
                  )
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display=("Name",
                  "Email",
                  "Profile_Photo",
                     "CreatedBy",
                      "CreatedDate",
                      "UpdatedBy",
                      "UpdatedDate",
                       "OTP",
                      "OTP_Created_At",
                      )
    

