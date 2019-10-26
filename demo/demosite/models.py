from django.db import models

class KeyTable(models.Model):
    apart_name = models.CharField(max_length=200)
    apart_addr = models.CharField(max_length=200)
    apart_key = models.CharField(max_length=200)
    room_key = models.AutoField(primary_key=True)

    # class Meta:
    #     db_table = "keytable"

    # def __init__(self, form):
    #     self.apart_name = form.apart_name
    #     self.apart_addr = form.apart_addr
    #     self.apart_key = hash(apart_name)

class ApartmentFeature(models.Model):
    apart_key = models.CharField(max_length=200, primary_key=True)
    parking = models.IntegerField()
    study_room = models.IntegerField()
    lounge = models.IntegerField()
    front_desk = models.IntegerField()
