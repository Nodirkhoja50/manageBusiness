from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from fpdf import FPDF
from datetime import datetime
from django.core.files import File

current_time = datetime.now()

date = f"{current_time.day}{current_time.month}{current_time.year}"


class Rulon(models.Model):
    rulon = models.IntegerField()
    information_pastel = models.FileField(upload_to='D:\\REPO\\PastelBot\\')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.rulon}'
    
 
        # Perform your desired actions with the new_object
        # ...
    @classmethod
    def create_rulon_obj(cls,rulon_number):
        file = cls.create_file(date)
        
        rulon_obj = Rulon(rulon=rulon_number)
        rulon_obj.information_pastel.save(file.name, file, save=True)
        return (rulon_obj.information_pastel.path)
        
    @classmethod
    def create_file(cls,date):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('helvetica','',16)
        file_path = f'{date}.pdf'
        pdf.output(file_path)
        
        file = File(open(file_path, 'rb'))
        #file.close()
        return file
    

    


class Price(models.Model):
    price_big = models.CharField(max_length=50)
    price_small = models.CharField(max_length=50)
    price_nalichka = models.CharField(max_length=50)
    price_gastiniy = models.CharField(max_length=50)



class Pastel(models.Model):
    rulon = models.ForeignKey(Rulon,on_delete=models.CASCADE)
    big_pastel = models.IntegerField(default=0)
    small_pastel = models.IntegerField(default=0)
    nalichka = models.IntegerField(default=0)
    gastiniy = models.IntegerField(default=0)
    xisob = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    #user_id = models.CharField(max_length=200,unique=True)

    
    
    class Meta:
        verbose_name = _('pastel')
        verbose_name_plural = _('pastel')
        
    def __str__(self) -> str:
        return f'{self.created_at}'
    

    

    @classmethod 
    def model_field_attr(cls,object):
        latest_pastel = Rulon.objects.order_by('-created_at').first()
        object_pastel = Pastel(rulon = latest_pastel,big_pastel=int(object["big_pastel"]),
                               small_pastel=int(object["small_pastel"]),nalichka = int(object["nalichka"]),gastiniy=int(object["gastiniy"]),xisob =int(object['kunlik_pul']))
        object_pastel.save()
        return object_pastel
        
'''@receiver(post_save, sender=Rulon)
def handle_new_object(sender, instance, created, **kwargs):
    if created:
        

        # Newly created object
        '''