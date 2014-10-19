from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
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

def add(request):
    
    pb = registerPushbullet()
    user = User(number=request.POST["number"], email=request.POST["email"], updated=datetime.datetime.now() - datetime.timedelta(days=30))
    user.save()
    success, pb_user = pb.new_contact(str(user.number), str(user.email))
    pb_user.push_note("welcome", "to this site")
    return HttpResponseRedirect(reverse('register:index'))

def remove(request):
    pb = registerPushbullet()
    delete_user = [i for i in pb.contacts if i.name == str(request.POST["number"])]
    for delete_use in delete_user:
        pb.remove_contact(delete_use)
    User.objects.filter(number=request.POST["number"]).delete()
    return HttpResponseRedirect(reverse('register:index'))