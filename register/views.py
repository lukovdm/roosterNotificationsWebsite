from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from models import User
from pushbullet import PushBullet
import datetime

def registerPushbullet():
    with open('/etc/api_key.txt') as f:
        key = f.read().strip()
    pb = PushBullet(key)
    return pb

class IndexView(generic.ListView):
    model = User
    template_name = 'register/index.html'

class InfoView(generic.TemplateView):
    template_name = 'register/info.html'

def add(request):
    if not unicode.isdigit(request.POST["number"]) and (not unicode.isalpha(request.POST["number"]) or not len(request.POST["number"]) == 3):
        if not unicode.isalpha(request.POST["number"]) or not len(request.POST["number"]) == 3:
            messages.error(request, "Please enter a valid 3 letter teacher code.", extra_tags="Add")
        else:
            messages.error(request, "Please enter a valid leerlingnumber.", extra_tags="Add")
    elif not "@" in request.POST["email"]:
        messages.error(request, "Please enter a valid email address.", extra_tags="Add")
    elif request.POST["email"] == u'luko.maas@hyperionlyceum.nl':
        messages.error(request, "You want to go to hell?", extra_tags="Add")
    else:
        if unicode.isalpha(request.POST["number"]) and len(request.POST["number"]) == 3:
            user = User(teacher=request.POST["number"], email=request.POST["email"], updated=datetime.datetime.now() - datetime.timedelta(days=30), student=False)
        else:
            user = User(number=request.POST["number"], email=request.POST["email"], updated=datetime.datetime.now() - datetime.timedelta(days=30), student=True)
        pb = registerPushbullet()
        success, pb_user = pb.new_contact(str(user.teacher) if unicode.isalpha(request.POST["number"]) and len(request.POST["number"]) == 3 else str(user.number), str(user.email))

        try:
            pb_user.push_note("Welcome to lesuitval.info " + str(request.POST["number"]), "Timetable updates will follow automatically.")
        except:
            messages.error(request, "Email already in use.", extra_tags="Add")
        else:
            user.save()
            messages.success(request, "%s succesfully added with email: %s" % (request.POST["number"], request.POST["email"]), extra_tags="AddSucces")
    return HttpResponseRedirect(reverse('register:index'))

def remove(request):
    if not unicode.isdigit(request.POST["number"]):
        if not unicode.isalpha(request.POST["number"]) or not len(request.POST["number"]) == 3:
            messages.error(request, "Please enter a valid 3 letter teacher code.", extra_tags="Delete")
        else:
            messages.error(request, "Please enter a valid leerlingnumber.", extra_tags="Delete")
    elif not "@" in request.POST["email"]:
        messages.error(request, "Please enter a valid email address.", extra_tags="Delete")
    else:
        pb = registerPushbullet()
        delete_users = [i for i in pb.contacts if (i.name == str(request.POST["number"]) and i.email == str(request.POST["email"]))]
        if not delete_users:
            messages.error(request, "User does not exit.", extra_tags="Delete")
        else:
            for delete_user in delete_users:
                delete_user.push_note("Thanks for using this site", "You have signed off.")
                pb.remove_contact(delete_user)
            if unicode.isalpha(request.POST["number"]) and len(request.POST["number"]) == 3:
                User.objects.filter(teacher=request.POST["number"]).filter(email=request.POST["email"]).delete()
            else:
                User.objects.filter(number=request.POST["number"]).filter(email=request.POST["email"]).delete()
            messages.success(request, "%s succesfully deteled with email: %s" % (request.POST["number"], request.POST["email"]), extra_tags="DeleteSucces")
    return HttpResponseRedirect(reverse('register:index'))