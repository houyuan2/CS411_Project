from django.db import models

class KeyTable(models.Model):
    apart_name = models.CharField(max_length=200)
    room_key = models.AutoField(primary_key=True)
    apart_key = models.ForeignKey(
        'ApartmentFeature',
        on_delete=models.CASCADE,
    )

class ApartmentFeature(models.Model):
    apart_key = models.CharField(max_length=200, primary_key=True)
    apart_addr = models.CharField(max_length=200)
    parking = models.IntegerField()
    study_room = models.IntegerField()
    lounge = models.IntegerField()
    front_desk = models.IntegerField()

class RoomFeature(models.Model):
    room_key = models.ForeignKey(
        'KeyTable',
        on_delete=models.CASCADE,
        unique=True,
        primary_key=True
    )
    cover_internet_fee = models.IntegerField()
    cover_electricity_fee = models.IntegerField()
    private_washing_machine = models.IntegerField()
    number_of_bedroom = models.IntegerField()
    number_of_bathroom = models.IntegerField()
    has_kitchen = models.IntegerField()
    has_refigerator = models.IntegerField()
    cover_water_fee = models.IntegerField()
    has_tv = models.IntegerField()
    size = models.IntegerField()

class DistanceTable(models.Model):
    search_id = models.AutoField(primary_key=True)
    apart_key = models.ForeignKey(
        'ApartmentFeature',
        on_delete=models.CASCADE,
    )
    dest_addr = models.CharField(max_length=200)
    distance = models.FloatField()

class RatingTable(models.Model):
    apart_key = models.ForeignKey(
        'ApartmentFeature',
        on_delete=models.CASCADE,
        unique=True,
        primary_key=True
    )
    env_rating = models.FloatField()
    ppl_rating = models.FloatField()
    rest_05_count = models.IntegerField()
    rest_1_count = models.IntegerField()
    rest_2_count = models.IntegerField()
    shop_05_count = models.IntegerField()
    shop_1_count = models.IntegerField()
    shop_2_count = models.IntegerField()
    
class PeopleRating(models.Model):
    comment_id = models.AutoField(primary_key=True)
    apart_key = models.ForeignKey(
        'ApartmentFeature',
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField()
    comment = models.CharField(max_length=200)
    nick_name = models.CharField(max_length=200)