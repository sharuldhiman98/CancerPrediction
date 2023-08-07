from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import doctor
from myapp.models import hospital
from myapp.models import medicine
from myapp.models import Post
from myapp.models import Contactus
from io import BytesIO
import io
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw
import PIL, PIL.Image
from io import StringIO
import base64
import keras
from tensorflow.keras.models import load_model 
from tensorflow.keras.preprocessing import image

import sklearn
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.impute import SimpleImputer
from myapp.models import Helpsupport
from myapp.models import Review
from myapp.models import Register
from django.core.mail import send_mail
from django.conf import settings


def fileupload(request):
    if request.method=='POST':
        f = request.FILES['sentFile'] # here you get the files needed
        handle_uploaded_file(f,f.name)
        classifier = load_model('skin_cnn_model.h5')

        test_image =image.load_img(f.name,target_size =(64,64))
        test_image =image.img_to_array(test_image)
        test_image =np.expand_dims(test_image, axis =0)
        result = classifier.predict(test_image)
        print(result)
        if result[0][0] >= 0.5:
            prediction = 'malignant'
            print(prediction)
            return  render (request,'yes.html',{})
        else:
            prediction = 'benign'
            print(prediction)
            return  render (request,'no.html',{})
    else :
        return  render (request,'fileupload.html',{})


def handle_uploaded_file(f,name):
    destination = open(name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
def mainproject(request):
     my_dict={}
     return render(request, "mainProject.html" ,context=my_dict)
     
def thankyou(request):
     my_dict={}
     return render(request, "thankyou.html" ,context=my_dict)                  

def viewContactus(request):        
      if request.method == 'POST':
          print("inside POST")
          if request.POST.get('name') and request.POST.get('email') :
                contactus=Contactus()
                contactus.name= request.POST.get('name')
                contactus.email= request.POST.get('email')
                contactus.contact= request.POST.get('contact')
                contactus.message= request.POST.get('message')
                contactus.save()
                return render(request,'thankyou.html')
          else:
                 print(error)
                

      else:
                      
                return render(request, 'contactus.html') 



def yes(request):
      my_dict={}
      return render(request, "yes.html" ,context=my_dict) 

     
def no(request):
      my_dict={}
      return render(request, "no.html" ,context=my_dict) 

def aboutus(request):
     my_dict={}
     return render(request, "aboutus.html" ,context=my_dict)

def services(request):
     my_dict={}
     return render(request, "services.html" ,context=my_dict)
    
def userlogin(request):
    if request.method=='POST':
        print("inside POST")
        
        formpost=True 
        
        us=request.POST.get('email')
        pw=request.POST.get('password')
        print("us",us)
        print("pw",pw)

        errormessage=""
        user= Register.objects.filter(email = us , password = pw)  
        k=len(user)
        if k>0:
            print("valid credentials ")
            request.session['email'] = us
            
            return render(request,"My Profile.html",{'user':user})      
           
        else:

            print("invalid credentials ")
            errormessage="invalid credentials"
            return render(request,'login.html',{'formpost':formpost,'errormessage':errormessage}) 
    else:
            formpost=False
            return render(request,'login.html',{'formpost':formpost})
    
        

def forgotpassword(request):
      
     if request.method=='POST':
        formpost=True 
        em=request.POST.get('email')
        user=Register.objects.filter(email=em)
        if len(user)>0:
           pw=user[0].password
           subject = 'password'
           message = 'Welcome to HEALTHFLEX, your password is' +pw
           email_from = settings.EMAIL_HOST_USER
           recipient_list = [em,]
           send_mail(subject, message, email_from, recipient_list,)
           return render(request,'forgotpassword.html',{'formpost':formpost}) 

        else:
           return HttpResponse("Invalid email or the email id not registered")
     else:
        my_dict={}
        return render(request, "forgotpassword.html" ,context=my_dict)  



def changepassword(request):
      if request.method == 'POST':
               print("inside POST")
               user=Register.objects.get(email=request.session['email'])

               oldpassword= request.POST.get('oldpassword')
               newpassword= request.POST.get('newpassword')
               repassword= request.POST.get('repassword')
               if newpassword==repassword:
                      p=user.password
                      if oldpassword==p:
                         user.password=newpassword
                         user.save() 
                         return render(request, "My Profile.html" ,{})            
                      else:
                         return HttpResponse(" old password is not same") 
               else:
                      return HttpResponse("password re-entered donot match")

                

      else:
               my_dict={}      
               return render(request, "changepass.html" ,context=my_dict)            


def vieweditprofile(request):
    
    if request.method == 'POST':
          e= request.POST.get('email')
          p=Register.objects.get(email=e)
          p.first_name= request.POST.get('first_name')
          p.last_name= request.POST.get('last_name')
          p.email= request.POST.get('email')
          p.city= request.POST.get('city')
          p.state= request.POST.get('state')                                
          p.pincode= request.POST.get('pincode')
          p.address= request.POST.get('address')
          p.dob= request.POST.get('dob')
          print("updated")
          p.save()
          user=Register.objects.get(email=request.session['email'])
          return render(request,"My Profile.html",{'user':user})           
    else:
          user=Register.objects.get(email=request.session['email'])

          return render(request,"editprofile.html",{'user':user}) 
                

   

def helpsupports(request):
    if request.method == 'POST':
          print("inside POST")
          if request.POST.get('subject') and request.POST.get('message') :
              helpsupport=Helpsupport()
              helpsupport.subject= request.POST.get('subject')
              helpsupport.message= request.POST.get('message')
              

              helpsupport.save()

              return render(request,'thankyou.html')
          else:
              print(error)
                

    else:
              my_dict={}
              return render(request, "help&support.html" ,context=my_dict)      


def viewreview(request):
    if request.method == 'POST':
          print("inside POST")
          if request.POST.get('subject') and request.POST.get('message') :
              review=Review()
              review.subject= request.POST.get('subject')
              review.message= request.POST.get('message')
              

              review.save()

              return render(request,'thankyou.html')
          else:
              print(error)
                

    else:
              my_dict={}
              return render(request, "Review.html" ,context=my_dict)      
         


def myprofile(request):
    
          user=Register.objects.get(email=request.session['email'])
          return render(request,"My Profile.html",{'user':user}) 
      


def viewregister(request):
    if request.method == 'POST':
        print("inside POST")
        formpost=True 
        if request.POST.get('password') and request.POST.get('email') :
                register=Register()
                register.first_name= request.POST.get('first_name')
                register.last_name= request.POST.get('last_name')
                register.email= request.POST.get('email')
                register.city= request.POST.get('city')
                register.state= request.POST.get('state')                                
                register.pincode= request.POST.get('pincode')
                register.phone= request.POST.get('phone')
                register.address= request.POST.get('address')
                register.password= request.POST.get('password')
                register.dob= request.POST.get('dob')
                us=register.email
                user= Register.objects.filter(email = us ,)  
                k=len(user) 
                if k>0:
                   formpost=True 

                   print("email already exists ")
                   return render(request,"register.html",{'formpost':formpost})      
           
                else:

            
                   register.save()
                   return redirect ('/login')
        else:
                return render(request,"register.html",{'formpost':formpost})      
    else:
                
                formpost=False
                return render(request,'register.html',{'formpost':formpost})   




def viewdoctor(request):
    Doctor = doctor.objects.all() 
    return render(request,"doctor.html",{'doctor': Doctor})  





def viewhospital(request):
    Hospital = hospital.objects.all() 
    return render(request,"hospital.html",{'hospital': Hospital}) 

def doctorlogin(request):
    if request.method=='POST':
        print("inside POST")
        
        formpost=True 
        
        us=request.POST.get('email')
        pw=request.POST.get('password')
        print("us",us)
        print("pw",pw)

        errormessage=""
        user= doctor.objects.filter(email = us , password = pw)  
        k=len(user)
        if k>0:
            print("valid credentials ")
            request.session['email'] = us
            
            return render(request,'medicine.html')   
           
        else:

            print("invalid credentials ")
            errormessage="invalid credentials"
            return render(request,'drlogin.html',{'formpost':formpost,'errormessage':errormessage}) 
    else:
            formpost=False
            return render(request,'drlogin.html',{'formpost':formpost})




def viewmedicine(request):
    Medicine = medicine.objects.all() 
    return render(request,"medicine.html",{'medicine': Medicine}) 

    






def logout(request):
     request.session.flush()
     my_dict={}
     return render(request, "userlogin.html" ,context=my_dict) 



















def aboutb(request):
     my_dict={}
     return render(request, "aboutb.html" ,context=my_dict)   

def visualb(request):
     my_dict={}
     return render(request, "visualb.html" ,context=my_dict)   

def dynamicbreast(request):
     my_dict={}
     if request.method == 'POST':  
        t=request.POST.get('type')
        print(t)
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        df = pd.read_csv('breastcancer.csv')
        df[[t]].boxplot()
        buf = io.BytesIO()
        plt.margins(0.8)
    # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
   
        fig.savefig('abc.png')
    
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
    
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})
     else:   
        return render(request, "visualb.html" ,context=my_dict) 


def breastpredict(request):
  if request.method == 'POST':
       dataset=pd.read_csv('breastcancer.csv')
      
       
       del dataset['id']
       labelEncoder = LabelEncoder()
       dataset.iloc[:,0] = labelEncoder.fit_transform(dataset.iloc[:,0])

       imputer=SimpleImputer(missing_values=np.nan, strategy='mean')
       imputer=imputer.fit(dataset.iloc[:,0:32])
       dataset.iloc[:,0:32]=imputer.transform(dataset.iloc[:,0:32])

       x=dataset.iloc[:,1:32].values 
       y=dataset.iloc[:, 0].values 
       x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=0)

      
     
      
       radius_mean =request.POST.get('radius_mean')
       print('radius_mean',radius_mean)

       texture_mean =request.POST.get('texture_mean')
       print('texture_mean',texture_mean)

       perimeter_mean =request.POST.get('perimeter_mean')
       print('perimeter_mean',perimeter_mean)

       area_mean =request.POST.get('area_mean')
       print('area_mean',area_mean)

       smoothness_mean =request.POST.get('smoothness_mean')
       print('smoothness_mean',smoothness_mean)

       compactness_mean =request.POST.get('compactness_mean')
       print('compactness_mean',compactness_mean)

       concavity_mean =request.POST.get('concavity_mean')
       print('concavity_mean',concavity_mean)

       concave_points_mean =request.POST.get('concave_points_mean')
       print('concave_points_mean',concave_points_mean)

       symmetry_mean =request.POST.get('symmetry_mean')
       print('symmetry_mean',symmetry_mean)

       fractal_dimension_mean =request.POST.get('fractal_dimension_mean')
       print('fractal_dimension_mean',fractal_dimension_mean)

       radius_se =request.POST.get('radius_se')
       print('radius_se',radius_se)

       texture_se =request.POST.get('texture_se')
       print('texture_se',texture_se)

       perimeter_se =request.POST.get('perimeter_se')
       print('perimeter_se',perimeter_se)

       area_se =request.POST.get('area_se')
       print('area_se',area_se)

       smoothness_se =request.POST.get('smoothness_se')
       print('smoothness_se',smoothness_se)

       compactness_se =request.POST.get('compactness_se')
       print('compactness_se',compactness_se)

       concavity_se =request.POST.get('concavity_se')
       print('concavity_se',concavity_se)

       concave_points_se =request.POST.get('concave_points_se')
       print('concave_points_se',concave_points_se)

       symmetry_se =request.POST.get('symmetry_se')
       print('symmetry_se',symmetry_se)

       fractal_dimension_se =request.POST.get('fractal_dimension_se')
       print('fractal_dimension_se',fractal_dimension_se)

       radius_worst =request.POST.get('radius_worst')
       print('radius_worst',radius_worst)

       texture_worst =request.POST.get('texture_worst')
       print('texture_worst',texture_worst)

       perimeter_worst =request.POST.get('perimeter_worst')
       print('perimeter_worst',perimeter_worst)

       area_worst =request.POST.get('area_worst')
       print('area_worst',area_worst)

       smoothness_worst =request.POST.get('smoothness_worst')
       print('smoothness_worst',smoothness_worst)

       compactness_worst =request.POST.get('compactness_worst')
       print('compactness_worst',compactness_worst)

       concavity_worst =request.POST.get('concavity_worst')
       print('concavity_worst',concavity_worst)

       concave_points_worst =request.POST.get ('concave_points_worst')
       print('concave_points_worst',concave_points_worst)

       symmetry_worst =request.POST.get('symmetry_worst')
       print('symmetry_worst',symmetry_worst)

       fractal_dimension_worst =request.POST.get('fractal_dimension_worst')
       print('fractal_dimension_worst',fractal_dimension_worst)
    
      

       print("before",x_test.shape)
       x_test= np.append(x_test,[[radius_mean,texture_mean,perimeter_mean,area_mean,smoothness_mean,compactness_mean,concavity_mean,concave_points_mean,symmetry_mean,fractal_dimension_mean,radius_se,texture_se,perimeter_se,area_se,smoothness_se,compactness_se,concavity_se,concave_points_se,symmetry_se,fractal_dimension_se,radius_worst,texture_worst,perimeter_worst,area_worst,smoothness_worst,compactness_worst,concavity_worst,concave_points_worst,symmetry_worst,fractal_dimension_worst]],axis=0)
       print("after",x_test.shape)
       print(x_test)
       sc=StandardScaler()
       x_train=sc.fit_transform(x_train)
       x_test=sc.transform(x_test)
       loaded_model = pickle.load(open('mymodel.sav', 'rb'))

       y_pred=loaded_model.predict(x_test)
       l=len(y_pred)
       if l==1:
         my_dict={}
         return render(request, "yes.html" ,context=my_dict) 
       else:
        my_dict={}
        return render(request, "no.html" ,context=my_dict) 
  else:
       my_dict={}
       return render(request, "breastprediction.html" ,context=my_dict)        











def aboutcervical(request):
     my_dict={}
     return render(request, "aboutcervical.html" ,context=my_dict)  

def visualcervical(request):
     my_dict={}
     return render(request, "visualcervical.html" ,context=my_dict)  

def dynamiccervical(request):
     my_dict={}
     if request.method == 'POST':  
        t=request.POST.get('type')
        print(t)
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        df = pd.read_csv('cervical.csv')
        df[[t]].boxplot()
        buf = io.BytesIO()
        plt.margins(0.8)
    # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
   
        fig.savefig('abc.png')
    
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
    
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphiccervical.html', {'graphic': graphic.decode('utf8')})
     else:   
        return render(request, "visualcervical.html" ,context=my_dict)                 


def cervicalpredict(request):
     
  if request.method == 'POST':
     dataset=pd.read_csv('cervical.csv')
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,1]=dataset.iloc[:,1].apply(check)   
     dataset.iloc[:,1].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,2]=dataset.iloc[:,2].apply(check)   
     dataset.iloc[:,2].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,3]=dataset.iloc[:,3].apply(check)   
     dataset.iloc[:,3].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,4]=dataset.iloc[:,4].apply(check)   
     dataset.iloc[:,4].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
      
     dataset.iloc[:,5]=dataset.iloc[:,5].apply(check)   
     dataset.iloc[:,5].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,6]=dataset.iloc[:,6].apply(check)   
     dataset.iloc[:,6].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,7]=dataset.iloc[:,7].apply(check)   
     dataset.iloc[:,7].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     
     dataset.iloc[:,8]=dataset.iloc[:,8].apply(check)   
     dataset.iloc[:,8].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,9]=dataset.iloc[:,9].apply(check)   
     dataset.iloc[:,9].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,10]=dataset.iloc[:,10].apply(check)   
     dataset.iloc[:,10].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,11]=dataset.iloc[:,11].apply(check)   
     dataset.iloc[:,11].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)

     
     dataset.iloc[:,12]=dataset.iloc[:,12].apply(check)   
     dataset.iloc[:,12].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,13]=dataset.iloc[:,13].apply(check)   
     dataset.iloc[:,13].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,14]=dataset.iloc[:,14].apply(check)   
     dataset.iloc[:,14].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,15]=dataset.iloc[:,15].apply(check)   
     dataset.iloc[:,15].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)

     dataset.iloc[:,16]=dataset.iloc[:,16].apply(check)   
     dataset.iloc[:,16].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,17]=dataset.iloc[:,17].apply(check)   
     dataset.iloc[:,17].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,18]=dataset.iloc[:,18].apply(check)   
     dataset.iloc[:,18].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,19]=dataset.iloc[:,19].apply(check)   
     dataset.iloc[:,19].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)


     
     dataset.iloc[:,20]=dataset.iloc[:,20].apply(check)   
     dataset.iloc[:,20].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,21]=dataset.iloc[:,21].apply(check)   
     dataset.iloc[:,21].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,22]=dataset.iloc[:,22].apply(check)   
     dataset.iloc[:,22].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,23]=dataset.iloc[:,23].apply(check)   
     dataset.iloc[:,23].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)

     
     dataset.iloc[:,24]=dataset.iloc[:,24].apply(check)   
     dataset.iloc[:,24].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,25]=dataset.iloc[:,25].apply(check)   
     dataset.iloc[:,25].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,26]=dataset.iloc[:,26].apply(check)   
     dataset.iloc[:,26].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,27]=dataset.iloc[:,27].apply(check)   
     dataset.iloc[:,27].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)

     
     dataset.iloc[:,28]=dataset.iloc[:,28].apply(check)   
     dataset.iloc[:,28].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,29]=dataset.iloc[:,29].apply(check)   
     dataset.iloc[:,29].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,30]=dataset.iloc[:,30].apply(check)   
     dataset.iloc[:,30].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,31]=dataset.iloc[:,31].apply(check)   
     dataset.iloc[:,31].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)

     
     dataset.iloc[:,32]=dataset.iloc[:,32].apply(check)   
     dataset.iloc[:,32].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,33]=dataset.iloc[:,33].apply(check)   
     dataset.iloc[:,33].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,34]=dataset.iloc[:,34].apply(check)   
     dataset.iloc[:,34].isna().sum() 
     def check(x):
        if x=='?':
          return('NaN')
        else :
          return(x)
     dataset.iloc[:,35]=dataset.iloc[:,35].apply(check)   
     dataset.iloc[:,35].isna().sum() 
     
                                   

     x=dataset.iloc[:,0:35] 
     y=dataset.iloc[:, -1]  
     imputer=SimpleImputer(missing_values=np.nan, strategy='mean')
     imputer=imputer.fit(x.iloc[:,1:35])
     x.iloc[:,1:35]=imputer.transform(x.iloc[:,1:35])

    
     x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=0)

     Age=request.POST.get("Age")
     print('Age',Age)
     sexual_partners=request.POST.get("sexual_partners") 
     print('sexual_partners',sexual_partners)
     First_sexual_intercourse=request.POST.get("First_sexual_intercourse") 
     print('First_sexual_intercourse',First_sexual_intercourse)

     Pregnancies=request.POST.get("Pregnancies") 
     print('Pregnancies',Pregnancies)

     Smokes=request.POST.get("Smokes") 
     print('Smokes',Smokes)

     Smokes_years=request.POST.get("Smokes_years") 
     print('Smokes_years',Smokes_years)

     Smokes_packsoryear=request.POST.get("Smokes_packsoryear")
     print('Smokes_packsoryear',Smokes_packsoryear)

     Hormonal_Contraceptives=request.POST.get("Hormonal_Contraceptives")
     print('Hormonal_Contraceptives',Hormonal_Contraceptives)

     Hormonal_Contraceptives_years=request.POST.get(" Hormonal_Contraceptives_years")
     print('Hormonal_Contraceptives',Hormonal_Contraceptives)
      
     IUD=request.POST.get("IUD")
     print('IUD',IUD)

     IUD_years=request.POST.get("IUD_years")
     print('IUD_years',IUD_years)

     STDs=request.POST.get("STDs") 
     print('STDs',STDs)
     
     STDs_number=request.POST.get("STDs_number")
     print('STDs_number',STDs_number)
     
     STDs_condylomatosis=request.POST.get("STDs_condylomatosis") 
     print('STDs_condylomatosis',STDs_condylomatosis)
     
     STDs_cervical_condylomatosis=request.POST.get("STDs_cervical_condylomatosis")
     print('STDs_cervical_condylomatosis',STDs_cervical_condylomatosis)
     
     STDs_vaginal_condylomatosis=request.POST.get("STDs_vaginal_condylomatosis") 
     print('STDs_vaginal_condylomatosis',STDs_vaginal_condylomatosis)
     
     STDs_vulvoperineal_condylomatosis=request.POST.get("STDs_vulvoperineal_condylomatosis")
     print('STDs_vulvoperineal_condylomatosis',STDs_vulvoperineal_condylomatosis)
     
     STDs_syphilis=request.POST.get("STDs_syphilis")
     print('STDs_syphilis',STDs_syphilis)
     
     STDs_pelvic_inflammatory_disease=request.POST.get("STDs_pelvic_inflammatory_disease") 
     print('STDs_pelvic_inflammatory_disease',STDs_pelvic_inflammatory_disease)
     
     STDs_genital_herpes=request.POST.get("STDs_genital_herpes")
     print('STDs_genital_herpes',STDs_genital_herpes)
     
     STDs_molluscum_contagiosum=request.POST.get("STDs_molluscum_contagiosum")
     print('STDs_molluscum_contagiosum',STDs_molluscum_contagiosum)
     
     STDs_AIDS= request.POST.get("STDs_AIDS") 
     print('STDs_AIDS',STDs_AIDS)
     
     STDs_HIV=request.POST.get("STDs_HIV")
     print('STDs_HIV',STDs_HIV)
     
     STDs_Hepatitis_B=request.POST.get("STDs_Hepatitis_B")
     print('STDs_Hepatitis_B',STDs_Hepatitis_B)
     
     STDs_HPV=request.POST.get("STDs_HPV") 
     print('STDs_HPV',STDs_HPV)
     
     STDs_diagnosis=request.POST.get("STDs_diagnosis" )
     print('STDs_diagnosis',STDs_diagnosis)
     
     STDs_Time_since_first_diagnosis=request.POST.get("STDs_Time_since_first_diagnosis") 
     print('STDs_Time_since_first_diagnosis',STDs_Time_since_first_diagnosis)
     
     STDs_Time_since_last_diagnosis = request.POST.get("STDs_Time_since_last_diagnosis")
     print('STDs_Time_since_last_diagnosis',STDs_Time_since_last_diagnosis)
     
     Dx_Cancer=request.POST.get("Dx_Cancer")
     print('Dx_Cancer',Dx_Cancer)
     
     Dx_CIN=request.POST.get("Dx_CIN")
     print('Dx_CIN',Dx_CIN)
     
     Dx_HPV=request.POST.get("Dx_HPV") 
     print('Dx_HPV',Dx_HPV)
     
     Dx=request.POST.get("Dx" )
     print('Dx',Dx)
     
     Hinselmann=request.POST.get("Hinselmann")
     print('Hinselmann',Hinselmann)
    
     Schiller=request.POST.get("Schiller")
     print('Schiller',Schiller)
     
     Citology=request.POST.get("Citology") 
     print('Citology',Citology)
     
     


     print("before",x_test.shape)
     x_test= np.append(x_test,[[Age,sexual_partners,First_sexual_intercourse,Pregnancies,Smokes,Smokes_years,Smokes_packsoryear,Hormonal_Contraceptives,Hormonal_Contraceptives_years,IUD,IUD_years,STDs,STDs_number,STDs_condylomatosis,STDs_cervical_condylomatosis,STDs_vaginal_condylomatosis,STDs_vulvoperineal_condylomatosis,STDs_syphilis,STDs_pelvic_inflammatory_disease,STDs_genital_herpes,STDs_molluscum_contagiosum,STDs_AIDS,STDs_HIV,STDs_Hepatitis_B,STDs_HPV,STDs_diagnosis,STDs_Time_since_first_diagnosis,STDs_Time_since_last_diagnosis,Dx_Cancer,Dx_CIN,Dx_HPV,Dx,Hinselmann,Schiller,Citology]],axis=0)
     print("after",x_test.shape)
     sc=StandardScaler()
     x_train=sc.fit_transform(x_train)
     x_test=sc.transform(x_test)

     loaded_model = pickle.load(open('mymodelcerv.sav', 'rb'))
     print(x_test)
     y_pred=loaded_model.predict(x_test)
     l=len(y_pred)
     if l==1:
        my_dict={}
        return render(request, "yes.html" ,context=my_dict) 
     else:
        my_dict={}
        return render(request, "no.html" ,context=my_dict) 
  else:
     my_dict={}
     return render(request, "cervicalprediction.html" ,context=my_dict)          



 















def aboutlung(request):
     my_dict={}
     return render(request, "aboutlung.html" ,context=my_dict) 

def visuallung(request):
     my_dict={}
     return render(request, "visuallung.html" ,context=my_dict)  


def dynamiclung(request):
     my_dict={}
     if request.method == 'POST':  
        t=request.POST.get('type')
        print(t)
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        df = pd.read_csv('lungcancer.csv')
        df[[t]].boxplot()
        
        buf = io.BytesIO()
        plt.margins(0.8)
    # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
   
        fig.savefig('abc.png')
    
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
    
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphiclung.html', {'graphic': graphic.decode('utf8')})
     else:   
        return render(request, "visuallung.html" ,context=my_dict)         




def lungpredict(request):
     
  if request.method == 'POST':
       dataset=pd.read_csv('lungcancer.csv')
      
       labelEncoder = LabelEncoder()
       dataset.iloc[:,0] = labelEncoder.fit_transform(dataset.iloc[:,0])

       x=dataset.iloc[:,2:6].values 
       y=dataset.iloc[:, 6].values 
       x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=0)
       Age =request.POST.get('Age')
       Smokes =request.POST.get('Smokes')
       AreaQ =request.POST.get('AreaQ')
       Alkhol =request.POST.get('Alkhol')
       print("Age",Age)
       print("Smokes",Smokes)
       print("AreaQ",AreaQ)
       print("Alkhol",Alkhol)

       print("before",x_test.shape)
       x_test= np.append(x_test,[[Age,Smokes,AreaQ,Alkhol]],axis=0)
       print("after",x_test.shape)
       sc=StandardScaler()
       x_train=sc.fit_transform(x_train)
       x_test=sc.transform(x_test)
     
      
       
       loaded_model = pickle.load(open('mymodellung.sav', 'rb'))
       print(x_test)
       y_pred=loaded_model.predict(x_test)
       l=len(y_pred)
       if l==1:
          my_dict={}
          return render(request, "yes.html" ,context=my_dict) 
       else:
          my_dict={}
          return render(request, "no.html" ,context=my_dict)  
  else:
       my_dict={}
       print("not in post")
       return render(request, "lungprediction.html" ,context=my_dict)        
















def aboutprostate(request):
     my_dict={}
     return render(request, "aboutprostate.html" ,context=my_dict) 

def visualprostate(request):
     my_dict={}
     return render(request, "visualprostate.html" ,context=my_dict)  


def dynamicprostate(request):
     my_dict={}
     if request.method == 'POST':  
        t=request.POST.get('type')
        print(t)
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='w', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        df = pd.read_csv('Prostate_Cancer.csv')
        df[[t]].boxplot()
        buf = io.BytesIO()
        plt.margins(0.8)
    # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
   
        fig.savefig('abc.png')
    
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
    
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphicprostate.html', {'graphic': graphic.decode('utf8')})
     else:   
        return render(request, "visualprostate.html" ,context=my_dict) 



def prostatepredict(request):
     
  if request.method == 'POST':
       dataset=pd.read_csv('Prostate_Cancer.csv')
       del dataset['id']

       x=dataset.iloc[:,1:9].values 
       y=dataset.iloc[:, 0].values  

       x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=0)

      
     

       radius=request.POST.get('radius')
       texture =request.POST.get('texture')
       perimeter=request.POST.get('perimeter')
       area =request.POST.get('area')
       smoothness =request.POST.get('smoothness')
       compactness=request.POST.get('compactness')
       symmetry =request.POST.get('symmetry')
       fractal_dimension =request.POST.get('fractal_dimension')
      
       print("before",x_test.shape)
       x_test= np.append(x_test,[[radius,texture,perimeter,area,smoothness,compactness,symmetry,fractal_dimension]],axis=0)
       print("after",x_test.shape)
       sc=StandardScaler()
       x_train=sc.fit_transform(x_train)
       x_test=sc.transform(x_test)

       loaded_model = pickle.load(open('mymodelprostate.sav', 'rb'))
       print(x_test)
       y_pred=loaded_model.predict(x_test)
       l=len(y_pred)
       if l==1:
          my_dict={}
          return render(request, "yes.html" ,context=my_dict) 
       else:
          my_dict={}
          return render(request, "no.html" ,context=my_dict)  
  else:
       my_dict={}
       return render(request, "prostateprediction.html" ,context=my_dict)         





def aboutskin(request):
     my_dict={}
     return render(request, "aboutskin.html" ,context=my_dict)      
def visualskin(request):
     my_dict={}
     return render(request, "visualskin.html" ,context=my_dict)  















