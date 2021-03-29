from django.shortcuts import render, get_object_or_404, redirect
from .models import Cause, Contact, Donor
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from rest_framework.views import APIView 
from rest_framework.response import Response
from . serializer import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def home(request):
    context={'nbar':'home', 'projects':Cause.objects.filter(completed=True)}
    return render(request, "donate/home.html", context)

def about(request):
    context = {'nbar':'about'}
    return render(request, "donate/about.html", context)

def contact(request):
    if (request.method=='POST'):
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        newcontact = Contact.objects.create(name=name, email=email, subject=subject, message=message)
    context={'nbar':'contact'}
    return render(request, "donate/contact.html", context)

def donate(request):
    context = {'causes':Cause.objects.filter(completed=False, accepted=True), 'nbar':'donate'}
    return render(request, "donate/donate.html", context)

def raisefund(request):
    if(request.user.is_authenticated):
        if (request.method=='POST'):
            title = request.POST['title']
            description = request.POST['description']
            date_needed = request.POST['dateneeded']
            target = request.POST['target']
            newcause = Cause.objects.create(title=title, description=description, date_needed=date_needed, target=target, recepient=request.user)
        context={'nbar':'raise'}
        return render(request, "donate/raisefund.html", context)
    else:
        context={'nbar':'raise','redirect':'yes'}
        return render(request, "donate/raisefund.html", context)

def make_donations(request):
    msg=request.GET['id']
    targc = Cause.objects.get(id=msg)
    context={'msg':msg, 'cause':targc}
    if (request.method=='POST'):
        name = request.POST['name']
        comments = request.POST['comments']
        dob = request.POST['dob']
        if(dob==""):
            dob = None
        amount = request.POST['amount']
        account = request.POST['account']
        account = account.replace(" ", "")
        if(len(account)!=16):
            messages.info(request, 'Account number is invalid!', extra_tags="failure")
        else:
            if(targc.collected+int(amount) >= targc.target):
                targc.completed = True
            targc.collected = targc.collected+int(amount)
            targc.save()
            Donor.objects.create(name=name, comments=comments, dob=dob, amount=amount, accountno=account)
            messages.info(request, 'Donation successful!', extra_tags="success")

    return render(request, "donate/make_donations.html", context)


class ContactView(APIView):

    def get(self, request): 
        detail = [ {"id":detail.id ,"name": detail.name,"email": detail.email, "subject": detail.subject, "message": detail.message} for detail in Contact.objects.filter(unread=True)] 
        return Response(detail)
        
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            cid = serializer.data
            cid = cid['id']
            x = Contact.objects.get(id=cid)
            x.unread = False
            x.save()
            return Response(status=200)
        return Response(status=400)


class CauseView(APIView):
    
    def get(self, request):
        detail = [ {
            "id":detail.id,
            "title": detail.title,
            "description": detail.description, 
            "date_posted": detail.date_posted, 
            "date_needed": detail.date_needed, 
            "target": detail.target, 
            "collected": detail.collected, 
            "recepient_uname": detail.recepient.username,
            "recepient_name": detail.recepient.first_name, 
            "recepient_email": detail.recepient.email,
            "recepient_prev_d": Cause.objects.filter(recepient=detail.recepient).count()
            } for detail in Cause.objects.filter(accepted=False)]
        return Response(detail)

    def post(self, request):
        serializer = CausePostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            cid = data['id']
            accept = data['accept']
            x = Cause.objects.get(id=cid)
            if(accept==True):
                x.accepted = True
                x.save()
                return Response(status=200)
            else:
                x.delete()
                return Response(status=200)
        return Response(status=400)

class UserView(APIView):
    
    def post(self, request):
        serializer = UserPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            uname = data['uname']
            pwd = data['pwd']
            user = authenticate(request, username=uname, password=pwd)
            if(user is not None):
                staff = User.objects.filter(username=uname, is_staff=True)
                if (staff is not None):
                    return Response(status=200)

        return Response(status=400)