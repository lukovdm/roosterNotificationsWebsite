from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from models import User
from pushbullet import PushBullet
import datetime

def registerPushbullet():
    key = "PwmEg59jL6KjS2N0e6BjX3IEs2LpadYs"
    pb = PushBullet(key)
    return pb

class IndexView(generic.ListView):
    model = User
    template_name = 'register/index.html'

class InfoView(generic.TemplateView):
    template_name = 'register/info.html'

def add(request):
    user = User(number=request.POST["number"], email=request.POST["email"], updated=datetime.datetime.now() - datetime.timedelta(days=30))
    pb = registerPushbullet()
    success, pb_user = pb.new_contact(str(user.number), str(user.email))

    try:
        pb_user.push_note("Welcome to lesuitval.info " + str(request.POST["number"]), "Timetable updates will follow automatically.")
    except:
        messages.error(request, "Email already in use.", extra_tags="Add")
    else:
        user.save()
        messages.success(request, "%s succesfully added with email: %s" % (request.POST["number"], request.POST["email"]), extra_tags="AddSucces")
    return HttpResponseRedirect(reverse('register:index'))

def remove(request):
    pb = registerPushbullet()
    delete_users = [i for i in pb.contacts if (i.name == str(request.POST["number"]) and i.email == str(request.POST["email"]))]
    if not delete_users:
        messages.error(request, "User does not exit.", extra_tags="Delete")
    else:
        for delete_user in delete_users:
            delete_user.push_note("Thanks for using this site", "You have signed off.")
            pb.remove_contact(delete_user)
        User.objects.filter(number=request.POST["number"]).filter(email=request.POST["email"]).delete()
        messages.success(request, "%s succesfully deteled with email: %s" % (request.POST["number"], request.POST["email"]), extra_tags="DeleteSucces")
    return HttpResponseRedirect(reverse('register:index'))