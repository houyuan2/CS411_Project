from django.db import models

class KeyTable(models.Model):
    apart_name = models.CharField(max_length=200)
    apart_addr = models.CharField(max_length=200)
    apart_key = models.BigIntegerField()
    room_key = models.AutoField(primary_key=True)

    # class Meta:
    #     db_table = "keytable"

    # def __init__(self, form):
    #     apart_name = form.apart_name
    #     apart_addr = form.apart_addr
    #     apart_key = hash(apart_name)
