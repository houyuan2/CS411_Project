# Generated by Django 2.2.6 on 2019-11-17 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demosite', '0004_delete_roomfeature'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomFeature',
            fields=[
                ('room_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='demosite.KeyTable', unique=True)),
                ('cover_internet_fee', models.IntegerField()),
                ('cover_electricity_fee', models.IntegerField()),
                ('private_washing_machine', models.IntegerField()),
                ('number_of_bedroom', models.IntegerField()),
                ('number_of_bathroom', models.IntegerField()),
                ('has_kitchen', models.IntegerField()),
                ('has_refigerator', models.IntegerField()),
                ('cover_water_fee', models.IntegerField()),
                ('has_tv', models.IntegerField()),
                ('size', models.IntegerField()),
            ],
        ),
    ]
