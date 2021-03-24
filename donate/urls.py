from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('about/', views.about, name='app-about'),
    path('contact/', views.contact, name='app-contact'),
    path('donate/', views.donate, name='app-donate'),
    path('raisefund/', views.raisefund, name='app-raise-fund'),
    path('make_donations/', views.make_donations, name='app-make-donations'),
    path('rcontact/', views.ContactView.as_view(), name='r-contact'),
    path('rcauses/', views.CauseView.as_view(), name='r-cause'),
    path('ruser/', views.UserView.as_view(), name='r-user')
]