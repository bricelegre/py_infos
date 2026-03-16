from django.db import models
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import OuterRef, Subquery, Max
#from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)  # 🟢 Clé primaire
    cust_status = models.IntegerField(default=1)
    cust_plan = models.IntegerField()
    cust_subscrip_duration = models.IntegerField(default=12)
    cust_identifiant = models.CharField(max_length=200)
    cust_slug = models.CharField(max_length=200)
    cust_company_name= models.CharField(max_length=250)
    cust_fone = models.CharField(max_length=20)
    cust_start_date = models.DateTimeField(auto_now_add=True)
    cust_email = models.CharField(max_length=50)
    cust_connect_statut = models.IntegerField(default=0)
    cust_ip = models.CharField(max_length=200)
    admin_code = models.CharField(max_length=10, default=1)
    cust_end_subscription = models.DateField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        managed = False  # 🔴 Très important !
        db_table = 'customers' 
    
    @property
    def days_before_end_subscription(self):
        """Retourne le nombre de jours avant la fin de l’abonnement"""
        if self.cust_end_subscription:
            today = date.today()
            delta = self.cust_end_subscription - today
            return delta.days  # peut être négatif
        return None   
    
    @property
    def validite_restante(self):
        if self.cust_plan == 1:
            return 'Illimité'
        
        if self.cust_end_subscription:
            return (self.cust_end_subscription.date() - date.today()).days
        return None
    
    @property
    def plan_name(self):
        if self.cust_plan == 1:
            return 'Formule Free'
        elif self.cust_plan == 2:
            return 'Formule Starter'
        elif self.cust_plan == 3:
            return 'Formule Premium'
        return 'Formule non-definit'
    
    @property
    def nb_users(self):
        from .models import Users  # Import local pour éviter des boucles
        return Users.objects.filter(cust_id=self.cust_id).count()

class AccountChart(models.Model):
    acc_id = models.AutoField(primary_key=True)
    cust = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='cust_id')
    acc_account_number = models.IntegerField()
    acc_account_name = models.CharField(max_length=25)
    acc_class_level_2 = models.IntegerField()
    acc_class_level_3 = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'tbl_accounts_chart'

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    cust = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='cust_id')
    user_pseudo = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    user_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user_status = models.IntegerField(default=1)
    super_admin = models.IntegerField() # ou ForeignKey si possible
    
    class Meta:
        managed = True
        db_table = 'tbl_users_py'
        constraints = [
            models.UniqueConstraint(fields=['cust', 'user_pseudo'], name='uniq_cust_pseudo')
        ]
     
class UserRole(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    roles_id = models.IntegerField(primary_key=True)
    module_id = models.IntegerField()
    class Meta:
        managed = True
        db_table = 'tbl_user_roles'

class Module(models.Model): # ou ForeignKey si possible
    module_id = models.IntegerField(primary_key=True)
    module_name = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'tbl_modules'

class Roles(models.Model):
    roles_id = models.IntegerField(primary_key=True) 
    roles_name = models.CharField(max_length=200)  # ou ForeignKey si possible

    class Meta:
        managed = True
        db_table = 'tbl_roles' 

class UserAnnouncement(models.Model):
    id = models.AutoField(primary_key=True)
    announcement_id = models.IntegerField()
    user_id = models.IntegerField()
    is_read = models.IntegerField()  # ou ForeignKey si possible
    dismissed = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'tbl_user_announcements'      

class UserPermission(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    perm_id = models.IntegerField()  # ou ForeignKey si possible
    class Meta:
        managed = True
        db_table = 'tbl_user_permissions'  

class Permissions(models.Model):
    perm_id = models.AutoField(primary_key=True)
    perm_name = models.CharField(max_length=250)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, db_column='module_id', null=True, blank=True)
    perm_description = models.CharField(max_length=250, null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'tbl_permissions_py'

class RolesPermissions(models.Model):
    roles_id = models.ForeignKey(Roles, on_delete=models.CASCADE, db_column='roles_id', null=True, blank=True)
    perm_id = models.ForeignKey(Permissions, on_delete=models.CASCADE, db_column='perm_id', null=True, blank=True)
    
    class Meta:
        managed = True
        db_table = 'tbl_role_permissions'
        
class UserConnect(models.Model):
    user = models.ForeignKey('Users', db_column='user_id', on_delete=models.DO_NOTHING)
    connect_id = models.AutoField(primary_key=True)
    cust_id = models.IntegerField()
    user_times_connect = models.DateTimeField()
    user_ip = models.CharField(max_length=300)

    class Meta:
        managed = True
        db_table = 'tbl_users_connect'

    @staticmethod
    def last_connects(cust_id):
        """y
        Retourne la dernière connexion de chaque utilisateur pour un client donné.
        """
        # Sous-requête pour obtenir le dernier timestamp par utilisateur
        latest_time = UserConnect.objects.filter(
            cust_id=cust_id,
            user_id=OuterRef('user_id')
        ).order_by('-user_times_connect').values('user_times_connect')[:1]

        return UserConnect.objects.filter(
            cust_id=cust_id,
            user_times_connect=Subquery(latest_time)
        ).select_related('user').order_by('-user_times_connect')

    @staticmethod
    def last_n_connects(cust_id, limit=10, user_ids=None):
        qs = UserConnect.objects.filter(cust_id=cust_id)
        if user_ids is not None:
            qs = qs.filter(user_id__in=user_ids)  # Filtre AVANT le slicing
        return qs.select_related('user').order_by('-user_times_connect')[:limit]

class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=150)
    is_active = models.IntegerField(default=1)  # ou ForeignKey si possible
    admin_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tbl_announcements'  
    
    @staticmethod
    def last_annonces():
        return Announcement.objects.all().order_by('-created_at')
                                           
class CompanyData(models.Model):
    company_id = models.AutoField(primary_key=True)
    cust = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='cust_id')
    company_name = models.CharField(max_length=100)
    company_email = models.CharField(max_length=50)
    company_fone = models.CharField(max_length=50)
    company_adress = models.CharField(max_length=100)
    company_cc = models.CharField(max_length=20, default='1234567A')
    company_cnps_number = models.CharField(max_length=20, default='111111')
    company_rccm = models.CharField(max_length=20, default='RCCM-000000000')
    company_logo = models.CharField(max_length=100)
    
    class Meta:
        managed = True
        db_table = 'tbl_company_data'
    

class ExpendTypeTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    et_account_nb = models.IntegerField()
    et_account_name = models.CharField(max_length=250)
    
    class Meta:
        managed = False
        db_table = 'sources_expend_types'

class ExpendType(models.Model):
    et_id = models.AutoField(primary_key=True)
    cust_id = models.IntegerField()
    et_account_nb = models.IntegerField()
    et_account_name = models.CharField(max_length=250)
    
    class Meta:
        managed = False
        db_table = 'tbl_expend_types'  

class ListJrxTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    journal_code = models.CharField(max_length=11)
    journal_name = models.CharField(max_length=25)
    
    class Meta:
        managed = False
        db_table = 'sources_list_jrx'
        
class ListJrx(models.Model):
    journal_id = models.AutoField(primary_key=True)
    cust_id = models.IntegerField()
    journal_code = models.CharField(max_length=20)
    journal_name = models.CharField(max_length=25)
    
    class Meta:
        managed = False
        db_table = 'tbl_list_jrx'   
        
class ThirdAccountTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    third_type = models.CharField(max_length=11)
    third_name = models.CharField(max_length=25)
    third_ncc = models.CharField(max_length=11)
    third_rccm = models.CharField(max_length=25)
    third_adress = models.CharField(max_length=11)
    third_fone = models.CharField(max_length=25)
    third_email = models.CharField(max_length=25)
    third_interl_function_1 = models.CharField(max_length=50)
    third_interlocuteur_1 = models.CharField(max_length=100)
    third_interl_contact_1 = models.CharField(max_length=11)
    third_interl_email_1 = models.CharField(max_length=25)
    third_account = models.IntegerField(11)
    third_payement_ddl = models.IntegerField(11)
    third_others_infos = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'sources_third_account'      

class ThirdAccount(models.Model):
    third_id = models.AutoField(primary_key=True)
    cust_id = models.IntegerField()
    third_type = models.CharField(max_length=11)
    third_name = models.CharField(max_length=25)
    third_slug_name = models.CharField(max_length=25)
    third_ncc = models.CharField(max_length=11)
    third_rccm = models.CharField(max_length=25)
    third_adress = models.CharField(max_length=11)
    third_fone = models.CharField(max_length=25)
    third_email = models.CharField(max_length=25)
    third_interl_function_1 = models.CharField(max_length=50)
    third_interlocuteur_1 = models.CharField(max_length=100)
    third_interl_contact_1 = models.CharField(max_length=11)
    third_interl_email_1 = models.CharField(max_length=25)
    third_interl_function_2 = models.CharField(max_length=50)
    third_interlocuteur_2 = models.CharField(max_length=100)
    third_interl_contact_2 = models.CharField(max_length=11)
    third_interl_email_2 = models.CharField(max_length=25)
    third_account = models.IntegerField(11)
    third_payement_ddl = models.IntegerField(11)
    third_others_infos = models.CharField(max_length=250)
    third_status = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = 'tbl_third_account'               




class CustomerConnect(models.Model):
    cust_connect_id = models.AutoField(primary_key=True) 
    cust = models.OneToOneField(
        Customer, on_delete=models.CASCADE, db_column='cust_id',
        related_name='connect'
    )
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    url_current = models.CharField(max_length=200)
    cust_user_time_connect = models.DateTimeField(null=True, blank=True)
        
    class Meta:
        managed = False
        db_table = 'adminapp_customerconnect' 
           
    @property
    def status_cust(self):
        """Détermine si le client est connecté (ON) ou déconnecté (OFF)"""
        if self.cust_user_time_connect:
            now = timezone.now()  # ⏰ aware datetime
            return 'ON' if now <= self.cust_user_time_connect + timedelta(minutes=3) else 'OFF'
        return 'OFF'      

class AccountsChartAssoTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    name = models.CharField(max_length=600)

    class Meta:
        managed = False
        db_table = 'sources_accounts_chart_asso'
        
class ExpendTypeAssoTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    et_account_nb = models.IntegerField()
    et_account_name = models.CharField(max_length=250)
    
    class Meta:
        managed = False
        db_table = 'sources_expend_types_asso'
                
class PayParameters(models.Model):
    pp_id = models.AutoField(primary_key=True)
    cust_id = models.IntegerField()
    pp_cmu = models.CharField(max_length=3, default="NON")
    pp_anciennete = models.CharField(max_length=3, default="NON")
    pp_cnps_tx = models.IntegerField()
    pp_pay_rounded = models.CharField(max_length=3, default="NON")
    class Meta:
        managed = False
        db_table = "tbl_pay_parameters"