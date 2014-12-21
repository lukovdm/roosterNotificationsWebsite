from django.db import models

class User(models.Model):
    number = models.IntegerField(max_length=8, default=0000000)
    teacher = models.TextField(max_length=3, default="aaa")
    email = models.EmailField()
    updated = models.DateTimeField()
    student = models.BooleanField(default=True)
    lastText = models.TextField(default="")

    def __unicode__(self):
        return str(self.number) + str(self.email)
