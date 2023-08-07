


# Create your models here.
from django.db import models
class Person(models.Model):
        first_name= models.CharField(max_length=30, primary_key=True)
        last_name= models.CharField(max_length=30, null=True)
        def __str__(self):
	        return self.first_name

class doctor(models.Model): 
        name = models.CharField(max_length=30) 
        phoneno = models.BigIntegerField()
        password = models.CharField(max_length=20,default="123456")
        email = models.EmailField(primary_key=True)
        profile_pic= models.ImageField(upload_to='doctor', blank=True)
        Portfolio=models.CharField(max_length=5000)
        Achievements=models.CharField(max_length=1000 , null=True)
        Speciality =models.CharField(max_length=1000,  null=True)
        def __str__(self):
                return self.email

class hospital(models.Model): 
        Name = models.CharField(max_length=300 , primary_key=True) 
        Contact = models.BigIntegerField()
        Address=models.CharField(max_length=1000) 
        Image = models.ImageField(upload_to='hospital', blank=True)
        Speciality= models.CharField(max_length=1000, null=True)
        Services=models.CharField(max_length=1000, null=True)
        def __str__(self):
                return self.Name

class medicine(models.Model):
        Name = models.CharField(max_length=300) 
        Usage= models.CharField(max_length=1000)
        Manufacturer= models.CharField(max_length=1000, primary_key=True)
        Salts= models.CharField(max_length=1000)
        SideEffects= models.CharField(max_length=1000, null=True)
        Dosage=models.CharField(max_length=1000, null=True)
        Precautions=models.CharField(max_length=1000, null=True)
        Storage=models.CharField(max_length=1000, null=True)
        def __str__(self):
                return self.Name


class Post(models.Model):
    title= models.CharField(max_length=300,)
    content= models.TextField()               



class Contactus(models.Model):
        name= models.CharField(max_length=300)
        email = models.EmailField()
        contact = models.BigIntegerField()
        message = models.TextField() 


class Helpsupport(models.Model):
        subject= models.CharField(max_length=300)
        message= models.CharField(max_length=1000)  

class Review(models.Model):
        subject= models.CharField(max_length=300)
        message= models.CharField(max_length=1000) 
              
class Register(models.Model):
        email = models.EmailField(primary_key=True)
        first_name= models.CharField(max_length=100)
        last_name= models.CharField(max_length=100)
        city= models.CharField(max_length=300)                
        state= models.CharField(max_length=300)
        pincode= models.BigIntegerField()
        phone = models.BigIntegerField()
        address = models.TextField() 
        password = models.CharField(max_length=100) 
        dob= models.DateField()

