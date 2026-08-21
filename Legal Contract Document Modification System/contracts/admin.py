from django.contrib import admin
from .models import(Role,User,Contract,Document,Clause,Modification,Approval,Version,AuditLog)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display=('id','name','description')
    search_fields=('name',)
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('id','name','email','role')
    search_fields=('name','email')
    list_filter=('role',)
    
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display=('id','contract_number','title','status','start_date','end_date','created_by','created_at')
    search_fields=('contract_number','title')
    list_filter=('status',)
    
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display=('id','name','document_type','contract','uploaded_by','uploaded_at')
    search_fields=('name',)
    list_filter=('document_type',)
    
@admin.register(Clause)
class ClauseAdmin(admin.ModelAdmin):
    list_display=('id','clause_number','title','contract')
    search_fields=('clause_number','title')
    
@admin.register(Modification)
class ModificationAdmin(admin.ModelAdmin):
    list_display=('id','clause','modified_by','status','created_at')
    search_fields=('clause__title',)
    list_filter=('status',)
    
@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display=('id','modification','approved_by','status','approved_at')
    list_filter=('status',)
    
@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display=('id','contract','version_number','created_by','created_at')
    search_fields=('version_number',)
    list_filter=('version_number',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display=('id','user','action','entity_type','entity_id','timestamp')
    search_fields=('action','entity_type',)
    list_filter=('action','entity_type',)