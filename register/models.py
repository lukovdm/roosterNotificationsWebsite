from django.db import models

class User(models.Model):
    number = models.IntegerField(max_length=8, default=0000000)
    email = models.EmailField()
    updated = models.DateTimeField()

    def __unicode__(self):
        return str(self.number)
