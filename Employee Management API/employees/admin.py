from django.contrib import admin
from.models import Employee, Admin,ActivityLog
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
    

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display=("user","role","action","description","timestamp","ip_address")
    list_filter=("action","role","timestamp")
    search_fields=("description","user__username","role","user__email")
    ordering=("-timestamp",)