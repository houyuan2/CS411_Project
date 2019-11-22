from django.shortcuts import render, redirect
from demosite.forms import KeyForm
from demosite.models import KeyTable
from demosite.models import ApartmentFeature
from json import dump
from django.db import connection
from django.core import serializers

import json
from django.http import StreamingHttpResponse
import googlemaps
from googleplaces import GooglePlaces, types, lang

from demosite.models import KeyTable
from rest_framework import generics

from .serializers import KeyTableSerializer#, ApartmentFeatureSerializer

class KeyTableListCreate(generics.ListCreateAPIView):
    queryset = KeyTable.objects.all()
    serializer_class = KeyTableSerializer

def show(request):
    if request.method=='GET':
        try:
            data = []
            cursor = connection.cursor()
            cursor.execute("SELECT A.apart_key, A.apart_addr, R.env_rating, R.ppl_rating FROM demosite_apartmentfeature A JOIN demosite_ratingtable R on A.apart_key = R.apart_key_id")
            keytable_entry = cursor.fetchall()
            cursor.close()
            keytable_entry = tuple(keytable_entry)
            for i in keytable_entry:
                temp_dictionary =  {}
                temp_dictionary['apart_key']  =i[0]
                temp_dictionary['apart_addr'] = i[1]
                temp_dictionary['overallrating'] = (float(i[2]) + float(i[3]))/2.0
                data.append(temp_dictionary)
            return StreamingHttpResponse(json.dumps(data))
        except Exception as e:
            print(e)
            print("error")
            return StreamingHttpResponse("Error") 
    return StreamingHttpResponse('it was POST request')

def oldfiltershow(request):
    if request.method=='POST':
        try:
            filter = json.loads(request.body.decode("utf-8"))['Filter']
            print(filter)
            query = "SELECT DISTINCT apart_key, apart_addr, env_rating, ppl_rating FROM (SELECT * FROM (demosite_apartmentfeature A JOIN demosite_ratingtable R on A.apart_key = R.apart_key_id)) temp NATURAL JOIN demosite_keytable, demosite_roomfeature WHERE apart_key <> 'test'"
            if(filter['parking'] > 0):
                query += " AND parking = %d" % filter["parking"]
            if(filter['lounge'] > 0):
                query += " AND lounge = %d" % filter["lounge"]
            if(filter['study_room'] > 0):
                query += " AND study_room = %d" % filter["study_room"]
            if(filter['front_desk'] > 0):
                query += " AND front_desk = %d" % filter["front_desk"]
            print(query)
            data = []
            cursor = connection.cursor()
            cursor.execute(query)
            keytable_entry = cursor.fetchall()
            print(keytable_entry)
            cursor.close()
            keytable_entry = tuple(keytable_entry)
            for i in keytable_entry:
                temp_dictionary =  {}
                temp_dictionary['apart_key']  =i[0]
                temp_dictionary['apart_addr'] = i[1]
                temp_dictionary['overallrating'] = (float(i[2]) + float(i[3]))/2.0
                data.append(temp_dictionary)
            return StreamingHttpResponse(json.dumps(data))
        except Exception as e:
            print(e)
            print("error")
            return StreamingHttpResponse("Error") 
    return StreamingHttpResponse('it was GET request')

def keytable_insert(request):
    if request.method=='POST': #and request.value == "insert":
            #aptdata = request.POST.copy() #ProfileForm(request.POST, instance=request.user)
            #aptdata = json.loads(request.body.decode("utf-8"))
#            form = NameForm(request.POST)
#            if form.is_valid():
                aptdata = json.loads(request.body.decode("utf-8")) 
                apart_name = aptdata['newapartment']['aptname']
                apart_addr = aptdata['newapartment']['aptadd']
                apart_key = apart_name.upper()
                cursor = connection.cursor()
                cursor.execute("INSERT INTO     demosite_keytable(apart_name, apart_addr, apart_key_id) \
                            VALUES          (%s, %s, %s)", [apart_name, apart_addr, apart_key])
                return StreamingHttpResponse('received')
 #           else:
 #               form = NameForm()
    return StreamingHttpResponse('it was GET request') 
    #keytables = KeyTable.objects.all()
    #data = serializers.serialize("json", KeyTable.objects.all())   
 #   return render(request, 'show.html', {'keytables':form})

# Create your views here.

def keytable_delete(request):
    if request.method=='POST':
            todo = json.loads(request.body.decode("utf-8"))
            room_key = todo['deleteroom']['roomkey']
            cursor = connection.cursor()
            cursor.execute("DELETE FROM     demosite_keytable \
                            WHERE           demosite_keytable.room_key = %s", [room_key])
            cursor.close()
            return StreamingHttpResponse('deleted')
    return StreamingHttpResponse('it was GET request')
    
def keytable_update(request):
    if request.method=='POST':
            updatedata = json.loads(request.body.decode("utf-8"))
            apart_name = updatedata['changeapartment']['aptname']
            apart_addr = updatedata['changeapartment']['aptadd']
            apart_key = apart_name.upper()
            room_key = updatedata['changeapartment']['roomkey']
            cursor = connection.cursor()
            cursor.execute("UPDATE     demosite_keytable \
                            SET        apart_name = %s, apart_addr = %s, apart_key_id = %s \
                            WHERE      room_key = %s", [apart_name, apart_addr, apart_key, room_key])
            cursor.close()
            return StreamingHttpResponse('updated')
            
def apartfeature_insert(request):
    if request.method=='POST':
        aptdata = json.loads(request.body.decode("utf-8")) 
        apart_name = aptdata['newapartmentfeature']['apt_name']
        parking = aptdata['newapartmentfeature']['parking']
        study_room = aptdata['newapartmentfeature']['study_room']
        lounge = aptdata['newapartmentfeature']['lounge']
        front_desk = aptdata['newapartmentfeature']['front_desk']
        apart_addr = aptdata['newapartmentfeature']['apart_addr']
        apart_key = apart_name.upper()
        parking = int(parking)
        study_room = int(study_room)
        lounge = int(lounge)
        front_desk = int(front_desk)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO     demosite_apartmentfeature(apart_key, parking, study_room, lounge, front_desk, apart_addr) \
                        VALUES          (%s, %s, %s, %s, %s, %s)", [apart_key, parking, study_room, lounge, front_desk, apart_addr])
        cursor.close()
        return StreamingHttpResponse('received')
    return StreamingHttpResponse('it was GET request') 

def apartfeature_delete(request):
    if request.method=='POST':
        aptdata = json.loads(request.body.decode("utf-8")) 
        apart_name = aptdata['deleteapartmentfeature']['apt_name']
        apart_key = apart_name.upper()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM     demosite_apartmentfeature \
                        WHERE           apart_key = %s", [apart_key])
        cursor.close()
        return StreamingHttpResponse('deleted')
    return StreamingHttpResponse('it was GET request') 

def get_rooms_count(request):
    if request.method=='POST':
        num = 0
        try:
            aptdata = json.loads(request.body.decode("utf-8")) 
            apart_key = aptdata['roomscount']['apart_key']
            apart_key = apart_key.upper()
            cursor = connection.cursor()
            cursor.execute("SELECT    COUNT(*) \
                            FROM      demosite_keytable k NATURAL JOIN demosite_apartmentfeature f \
                            GROUP BY  apart_key \
                            HAVING    apart_key = %s", [apart_key])
            result = cursor.fetchall()
            cursor.close()
            #print(result)
            num = tuple(result)[0][0]
        except:
            print("apartment doesn't exist")
        print(num)
        return StreamingHttpResponse(json.dumps([{"num":str(num)}]))
    return StreamingHttpResponse('it was GET request')

def get_apart_with_parking_and_study_room(request): 
    if request.method=='GET':
        try:
            data = {"apartments":[]}
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT a.apart_name FROM \
                            (SELECT            apart_name \
                            FROM              demosite_keytable k NATURAL JOIN demosite_apartmentfeature f \
                            GROUP BY          apart_key_id, apart_name, parking\
                            HAVING            parking = 1) a \
                            INNER JOIN \
                            (SELECT            apart_name \
                            FROM              demosite_keytable k NATURAL JOIN demosite_apartmentfeature f \
                            GROUP BY          apart_key, apart_name, study_room \
                            HAVING            study_room = 1) b \
                            ON (a.apart_name = b.apart_name)")
            keytable_entry = cursor.fetchall()
            print(keytable_entry)
            cursor.close()
            keytable_entry = tuple(keytable_entry)
            for i in keytable_entry:
                data["apartments"].append(i[0])
            return StreamingHttpResponse(json.dumps([data]))
        except:
            print("error")
            return StreamingHttpResponse("Error") 
    return StreamingHttpResponse('it was POST request')

def roomfeature_insert(request):
    if request.method != 'GET':
        return StreamingHttpResponse('it was POST request')
    try: 
        aptdata = json.loads(request.body.decode("utf-8")) 
        room_key = int(aptdata['newroomfeature']['room_key'])
        cover_internet_fee = int(aptdata['newroomfeature']['cover_internet_fee'])
        cover_electricity_fee = int(aptdata['newroomfeature']['cover_electricity_fee'])
        private_washing_machine = int(aptdata['newroomfeature']['private_washing_machine'])
        number_of_bedroom = int(aptdata['newroomfeature']['number_of_bedroom'])
        number_of_bathroom = int(aptdata['newroomfeature']['number_of_bathroom'])
        has_kitchen = int(aptdata['newroomfeature']['has_kitchen'])
        has_refigerator = int(aptdata['newroomfeature']['has_refigerator'])
        cover_water_fee = int(aptdata['newroomfeature']['cover_water_fee'])
        has_tv = int(aptdata['newroomfeature']['has_tv'])
        size = int(aptdata['newroomfeature']['size'])
        column_list = [room_key, cover_internet_fee, cover_electricity_fee, private_washing_machine,
            number_of_bedroom, number_of_bathroom, has_kitchen, has_refigerator, cover_water_fee, has_tv,
            size]
        cursor = connection.cursor()
        cursor.execute("INSERT INTO     demosite_roomfeature(room_key, cover_internet_fee, cover_electricity_fee, \
            private_washing_machine, number_of_bedroom, number_of_bathroom, has_kitchen, has_refigerator, \
            cover_water_fee, has_tv, size) \
                        VALUES          (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", column_list)
        cursor.close()
        return StreamingHttpResponse('received')
    except:
        print("insert fails")
        return StreamingHttpResponse('Error')

def roomfeature_delete(request):
    if request.method=='POST':
        try: 
            aptdata = json.loads(request.body.decode("utf-8")) 
            room_key = int(aptdata['deleteroomfeature']['room_key'])
            cursor = connection.cursor()
            cursor.execute("DELETE FROM     demosite_roomfeature \
                            WHERE           room_key = %s", [room_key])
            cursor.close()
            return StreamingHttpResponse('deleted')
        except:
            print("delete fails")
            return StreamingHttpResponse('Error')
    return StreamingHttpResponse('it was GET request') 

def distancetable_insert(request):
    if request.method=='POST':
        try:
            aptdata = json.loads(request.body.decode("utf-8"))
            search_id = aptdata['newdistancetable']['search_id']
            apart_key = aptdata['newdistancetable']['apart_key'].upper()
            dest_addr = aptdata['newdistancetable']['dest_addr']
            distance = float(aptdata['newdistancetable']['distance'])
            print(aptdata['newdistancetable'])
            cursor = connection.cursor()
            cursor.execute("INSERT INTO     demosite_distancetable(search_id, apart_key_id, dest_addr, distance) \
                            VALUES          (%s, %s, %s, %s)", [search_id, apart_key, dest_addr, distance])
            cursor.close()
            return StreamingHttpResponse('received')
        except:
            print("insert fails")
            return StreamingHttpResponse('Error')
    return StreamingHttpResponse('it was GET request')

def distancetable_delete(request):
    if request.method=='POST':
        try: 
            aptdata = json.loads(request.body.decode("utf-8")) 
            search_id = int(aptdata['deleteroomfeature']['search_id'])
            cursor = connection.cursor()
            cursor.execute("DELETE FROM     demosite_distancetable \
                            WHERE           search_id = %s", [search_id])
            cursor.close()
            return StreamingHttpResponse('deleted')
        except:
            print("delete fails")
            return StreamingHttpResponse('Error')
    return StreamingHttpResponse('it was GET request')

def ratingtable_insert(request):
    if request.method=='POST':
        try:
            aptdata = json.loads(request.body.decode("utf-8"))
            apart_key = aptdata['newratingtable']['apart_key'].upper()
            env_rating = float(aptdata['newratingtable']['env_rating'])
            ppl_rating = float(aptdata['newratingtable']['ppl_rating'])
            rest_05_count = int(aptdata['newratingtable']['rest_05_count'])
            rest_1_count = int(aptdata['newratingtable']['rest_1_count'])
            rest_2_count = int(aptdata['newratingtable']['rest_2_count'])
            shop_05_count = int(aptdata['newratingtable']['shop_05_count'])
            shop_1_count = int(aptdata['newratingtable']['shop_1_count'])
            shop_2_count = int(aptdata['newratingtable']['shop_2_count'])
            column_list = [apart_key, env_rating, ppl_rating, rest_05_count, rest_1_count, rest_2_count,
                        shop_05_count, shop_1_count, shop_2_count]
            cursor = connection.cursor()
            cursor.execute("INSERT INTO     demosite_ratingtable(apart_key_id, env_rating, ppl_rating, rest_05_count, rest_1_count, \
                    rest_2_count, shop_05_count, shop_1_count, shop_2_count) \
                            VALUES          (%s, %s, %s, %s, %s, %s, %s, %s, %s)", column_list)
            return StreamingHttpResponse('received')
        except:
            print("insert fails")
            return StreamingHttpResponse('Error')
    return StreamingHttpResponse('it was GET request')

def ratingtable_delete(request):
    if request.method=='POST':
        try: 
            aptdata = json.loads(request.body.decode("utf-8")) 
            apart_key = aptdata['deleteratingtable']['apart_key'].upper()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM     demosite_ratingtable \
                            WHERE           apart_key_id = %s", [apart_key])
            cursor.close()
            return StreamingHttpResponse('deleted')
        except:
            print("delete fails")
            return StreamingHttpResponse('Error')
    return StreamingHttpResponse('it was GET request')

def peoplerating_insert(request):
    if request.method=='POST':
        try:
            aptdata = json.loads(request.body.decode("utf-8"))
            apart_key = aptdata['newpeoplerating']['apart_key'].upper()
            rating = float(aptdata['newpeoplerating']['rating'])
            comment = aptdata['newpeoplerating']['comment']
            nick_name = aptdata['newpeoplerating']['nick_name']
            cursor = connection.cursor()
            print(aptdata['newpeoplerating'])
            cursor.execute("INSERT INTO     demosite_peoplerating(apart_key_id, rating, comment, nick_name) \
                            VALUES          (%s, %s, %s, %s)", [apart_key, rating, comment, nick_name])
            cursor.close()
            return StreamingHttpResponse('received')
        except:
            print("insert fails")
            return StreamingHttpResponse('Error')
    return StreamingHttpResponse('it was GET request')

def peoplerating_delete(request):
    if request.method=='POST':
        try: 
            aptdata = json.loads(request.body.decode("utf-8")) 
            comment_id = int(aptdata['deletepeoplerating']['comment_id'])
            cursor = connection.cursor()
            cursor.execute("DELETE FROM     demosite_peoplerating \
                            WHERE           comment_id = %s", [comment_id])
            cursor.close()
            return StreamingHttpResponse('deleted')
        except:
            print("delete fails")
            return StreamingHttpResponse('Error')
    return StreamingHttpResponse('it was GET request')
    
def AF1Distance(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            apart_key = data['distance']['apart_key']
            dest = data['distance']['dest']
            cursor = connection.cursor()
            cursor.execute("SELECT      f.apart_addr \
                            FROM        demosite_apartmentfeature f \
                            WHERE       f.apart_key = %s", apart_key)
            entry = cursor.fetchall()
            origin = entry[0][0]
            cursor.close()
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT      t.distance \
                                FROM        demosite_distancetable t \
                                WHERE       t.dest_addr = %s", dest)
                entry = cursor.fetchall()
                distance = entry[0]
                cursor.close()
                return StreamingHttpResponse(distance)
            except:
                try:
                    gmaps = googlemaps.Client(key='AIzaSyD8Fru1q7cYQvzjRWlE5m9T3tAPlWGBowE')
                    matrix = gmaps.distance_matrix(origin, dest)
                    distanceInMile = float(matrix['rows'][0]['elements'][0]['distance']['text'].split(' ')[0])/1.6
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO     demosite_distancetable(apart_key_id, dest_addr, distance) \
                                    VALUES          (%s, %s, %s)", [apart_key, dest, distanceInMile])
                    cursor.close()
                    return StreamingHttpResponse(distanceInMile)
                except Exception as e:
                    print(e)
                    return StreamingHttpResponse('inaccurate address')
        except:
            return StreamingHttpResponse('failed')
    return StreamingHttpResponse('it was GET request')

def add_trigger():
    trigger = "CREATE TRIGGER auto_ratings_update \
                AFTER INSERT ON demosite_peoplerating \
                FOR EACH ROW \
	            BEGIN \
	            CALL update_ppl_rating(NEW.apart_key_id); \
	            END"
    cursor = connection.cursor()
    cursor.execute(trigger)
    cursor.close()

def add_stored_procedure():
    procedure = "CREATE PROCEDURE update_ppl_rating(IN update_key varchar(128)) \
                BEGIN \
                DECLARE total INT DEFAULT 0; \
                DECLARE sum_rating INT DEFAULT 0; \
                DECLARE avg_rating DOUBLE DEFAULT 0; \
                SELECT COUNT(*) INTO total \
                FROM demosite_peoplerating \
                GROUP BY apart_key_id \
                HAVING apart_key_id = update_key; \
                SELECT SUM(rating) INTO sum_rating \
                FROM demosite_peoplerating \
                GROUP BY apart_key_id \
                HAVING apart_key_id = update_key; \
                SET avg_rating = sum_rating / total; \
                UPDATE demosite_ratingtable \
                SET ppl_rating = avg_rating \
                WHERE apart_key_id = update_key; \
                END"
    cursor = connection.cursor()
    cursor.execute(procedure)
    cursor.close()