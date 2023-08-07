"""healthflex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('fileupload/', views.fileupload, name= 'fileupload'),

    path('admin/', admin.site.urls, name= 'admin'),
    path('contactus/', views.viewContactus, name= 'contactus' ),
    path('thankyou/', views.thankyou, name= 'thankyou' ),
    path('aboutus/', views.aboutus , name= 'aboutus'),
    path('changepassword/', views.changepassword , name= 'changepassword'),
    path('forgotpassword/', views.forgotpassword , name= 'forgotpassword'),
    path('logout/', views.logout , name= 'logout'),

    path('editprofile/', views.vieweditprofile , name= 'editprofile'),
    path('helpsupport/', views.helpsupports  , name= 'helpsupport'),
    path('userlogin/', views.userlogin  , name= 'login'),
    path('doctorlogin/', views.doctorlogin  , name= 'doctorlogin'),
    path('mainproject/', views.mainproject  , name= 'mainproject'),
    path('myprofile/', views.myprofile  , name= 'myprofile'),
    path('register/', views.viewregister  , name= 'register'),
    path('review/', views.viewreview  , name= 'review'),
    path('services/', views.services,   name= 'services'),

    path('viewdoctor/', views.viewdoctor,   name= 'viewdoctor' ),
    path('viewhospital/', views.viewhospital,   name= 'viewhospital' ),
    path('viewmedicine/', views.viewmedicine,   name= 'viewmedicine' ),

    path('aboutb/', views.aboutb , name= 'aboutb'),
    path('aboutcervical/', views.aboutcervical , name= 'aboutcervical'),
    path('aboutlung/', views.aboutlung , name= 'aboutlung'),
    path('aboutprostate/', views.aboutprostate , name= 'aboutprostate'),
    path('aboutskin/', views.aboutskin, name= 'aboutskin'),

    path('visualb/', views.dynamicbreast , name= 'visualb'),
    path('visualcervical/', views.dynamiccervical , name= 'visualcervical'),
    path('visuallung/', views.dynamiclung , name= 'visuallung'),
    path('visualprostate/', views.dynamicprostate , name= 'visualprostate'),
    path('visualskin/', views.visualskin, name= 'visualskin'),

    path('dynamicbreast/', views.dynamicbreast, name= 'dynamicbreast'),
    path('dynamiclung/', views.dynamiclung, name= 'dynamiclung'),
    path('dynamicprostate/', views.dynamicprostate, name= 'dynamicprostate'),
    path('dynamiccervical/', views.dynamiccervical, name= 'dynamiccervical'),

    path('cervicalpredict/', views.cervicalpredict, name= 'cervicalpredict'),
    path('prostatepredict/', views.prostatepredict, name= 'prostatepredict'),   
    path('breastpredict/', views.breastpredict, name= 'breastpredict'),
    path('lungpredict/', views.lungpredict, name= 'lungpredict'),

    path('yes/', views.yes, name= 'yes'),
    path('no/', views.no, name= 'no'),



]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
