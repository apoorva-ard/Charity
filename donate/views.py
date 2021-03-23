from django.shortcuts import render, get_object_or_404, redirect
from .models import Cause, Contact, Donor
from django.contrib import messages
from datetime import datetime

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
        context={'redirect':'yes'}
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

