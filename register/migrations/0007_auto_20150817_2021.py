# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from lxml import html
import requests
from pushbullet import PushBullet


def assign_class_code(apps, schema_editor):
    with open('/etc/api_key.txt') as f:
        key = f.read().strip()
    pb = PushBullet(key)

    users = apps.get_model("register", "User")
    for user in users.objects.all():
        if user.student:
            empty = True
            class_code = 0
            for i in range(3, 6):
                url = "http://gepro.nl/roosters/rooster.php?leerling=" + str(user.number) + \
                      "&type=Leerlingrooster&afdeling=" + "y" + str(i) + "&wijzigingen=1&school=1814&tabblad=1"
                page = requests.get(url)
                tree = html.fromstring(page.text)
                cells = tree.findall(".//td[@class='tableCell']")
                if cells is not None:
                    for cell in cells:
                        if cell.text is not None and cell.text != '&nbsp':
                            empty = False
                            class_code = i
                            break

            if not empty:
                user.class_code = class_code
                user.save()
                confirm_users = [i for i in pb.contacts if i.name == str(user.number)]
                print str(confirm_users) + ": not empty"
                for confirm_user in confirm_users:
                    confirm_user.push_note("You have been assigned to class %s" % (str(user.class_code)), "If this is wrong, please sign of and sign on again.")
            if empty:
                delete_users = [i for i in pb.contacts if i.name == str(user.number)]
                print str(delete_users) + ": empty"
                for delete_user in delete_users:
                    delete_user.push_note("You have been removed from lesuitval.info", "Due to some difficulties with the new time table system, user in class 1 or 2 have been signed of. If you wish to keep using this site please sign on again")
                    pb.remove_contact(delete_user)
                users.objects.filter(number=user.number).delete()

def assign_class_code_backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_user_lasttext'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='class_code',
            field=models.TextField(default=b'', max_length=2),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.RunPython(assign_class_code, assign_class_code_backwards),
    ]
