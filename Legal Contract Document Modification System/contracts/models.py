from django.db import models

class Role(models.Model):
    name=models.CharField(max_length=30,unique=True)
    description=models.TextField(blank=True)
    
    def __str__(self):
        return self.name
class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    role=models.ForeignKey(Role,on_delete=models.PROTECT,related_name='users')
    
    def __str__(self):
        return self.name
    
class Contract(models.Model):
    STATUS_CHOICES=[
        ('draft','Draft'),
        ('under_review','Under Review'),
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('active','Active'),
        ('expired','Expired')
        
    ]
    title=models.CharField(max_length=100)
    contract_number=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='draft')
    start_date=models.DateField()
    end_date=models.DateField(null=True,blank=True)
    created_by=models.ForeignKey(User,on_delete=models.PROTECT,related_name='contracts_created')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return(self.title)
    
class Document(models.Model):
    DOCUMENT_TYPE_CHOICES=[
        ('pdf','Pdf'),
        ('docx','Docx'),
        ('other','Other')
    ]
    contract=models.ForeignKey(Contract,on_delete=models.CASCADE,related_name='documents')
    name=models.CharField(max_length=50)
    file_path=models.FileField(upload_to='contracts')
    document_type=models.CharField(max_length=20,choices=DOCUMENT_TYPE_CHOICES,default='other')
    uploaded_by=models.ForeignKey(User,on_delete=models.PROTECT,related_name='documents_uploaded')
    uploaded_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Clause(models.Model):
    contract=models.ForeignKey(Contract,on_delete=models.PROTECT,related_name='clauses')
    title=models.CharField(max_length=50)
    content=models.TextField()
    clause_number=models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.clause_number} - {self.title}"
    
class Modification(models.Model):
    STATUS_CHOICES=[
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('pending','Pending')
    ]
    clause=models.ForeignKey(Clause,on_delete=models.CASCADE,related_name='modifications')
    modified_by=models.ForeignKey(User,on_delete=models.PROTECT,related_name='modifications_made')
    old_content=models.TextField()
    new_content=models.TextField()
    reason=models.TextField(blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Modification -{self.clause.title}"   
    
class Approval(models.Model):
     STATUS_CHOICES=[
         ('approved','Approved'),
         ('rejected','rejected'),
         ('pending','Pending'),
    
     ]
     modification=models.ForeignKey(Modification,on_delete=models.CASCADE,related_name='approvals')
     approved_by=models.ForeignKey(User,on_delete=models.PROTECT,related_name='approvals_given')
     status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
     comments=models.TextField(blank=True)
     approved_at=models.DateTimeField(null=True,blank=True)
     
     def __str__(self):
         return f"Approval -{self.modification.id}"
     
class Version(models.Model):
    contract=models.ForeignKey(Contract,on_delete=models.CASCADE,related_name='versions')
    version_number=models.CharField(max_length=20)
    changes=models.TextField(blank=True)
    created_by=models.ForeignKey(User,on_delete=models.PROTECT,related_name='version_created')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.contract.title} -{self.version_number}"

class AuditLog(models.Model):
    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name='audit_logs')
    action=models.CharField(max_length=50)
    entity_type=models.CharField(max_length=50)
    entity_id=models.IntegerField()
    description=models.TextField(blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
         return f"{self.user.name} - {self.action}"
    
    
     