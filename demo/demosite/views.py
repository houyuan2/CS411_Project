from django.shortcuts import render, redirect
from demosite.forms import KeyForm
from demosite.models import KeyTable
from demosite.models import ApartmentFeature
from json import dump
from django.db import connection
from django.core import serializers
from neo4j import GraphDatabase

import math
import json
from django.http import StreamingHttpResponse
import googlemaps
from googleplaces import GooglePlaces, types, lang

from demosite.models import KeyTable
from rest_framework import generics

import requests

from .serializers import KeyTableSerializer#, ApartmentFeatureSerializer

class KeyTableListCreate(generics.ListCreateAPIView):
    queryset = KeyTable.objects.all()
    serializer_class = KeyTableSerializer


class FindExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def apply_filter(self, message):
        message  = self.parse_filter(message)
        with self._driver.session() as session:
            filter_result = session.write_transaction(self._filter_result, message)
            output = []
            for room in filter_result:
                output.append(room[0])
            return output
    def parse_filter(self, message):
        if not message:
            return ["(r:Room)"]
        output = []
        example = "(f2:Feature12)<-[f10:f]-(r:Room)"
        for index, condition in enumerate(message):
            c = "(feature" + str(index) + ":Feature" + str(condition) + ")<-[f" + str(index) + ":f]-(r:Room)"
            output.append(c)
        return output

    def apply_recon(self, message):
        with self._driver.session() as session:
            recon = session.write_transaction(self._recon_result, str(message))
            output = {}
            for g in recon:
                print(g[0])
                output[g[0]] = g[2]
            return output
    @staticmethod
    def _filter_result(tx, message):

        condition = ""
        for i in range(len(message) - 1):
            condition += message[i] + ","
        condition += message[len(message) - 1]
        # print(condition)
        command = "MATCH " + condition + " \nRETURN DISTINCT r.apart_key, r.type"
        result = tx.run(command)
        return result

    @staticmethod
    def _recon_result(tx, message):
        command = "MATCH (n:Room)-[f]->()-[r]->(n2:Room)\n WHERE n.room_key = " + message + " AND n2.apart_key <> n.apart_key \nRETURN n2.apart_key, n2.room_key, count(n2.room_key)/13.0*0.8+((n2.size-n.size)*0.2/n.size) %0.2 as Freq\n ORDER BY Freq DESC\n LIMIT 3"
        result = tx.run(command)
        return result

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

def search(request):
    if request.method=='POST':
        try:
            search = json.loads(request.body.decode("utf-8"))['search']['apart_key']
            cursor = connection.cursor()
            query = "SELECT A.apart_key, A.apart_addr, R.env_rating, R.ppl_rating FROM demosite_apartmentfeature A JOIN demosite_ratingtable R on A.apart_key = R.apart_key_id "
            query += "WHERE A.apart_addr LIKE '%" + str(search) + "%' OR A.apart_key LIKE '%" + str(search) + "%'"
            cursor.execute(query)
            keytable_entry = cursor.fetchall()
            cursor.close()
            data=[]
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
                                WHERE       t.dest_addr = %s AND t.apart_key_id = %s", [dest, apart_key])
                entry = cursor.fetchall()
                distance = entry[0]
                cursor.close()
                return StreamingHttpResponse(distance)
            except Exception as e:
                #print(e)
                try:
                    gmaps = googlemaps.Client(key='AIzaSyD8Fru1q7cYQvzjRWlE5m9T3tAPlWGBowE')
                    matrix = gmaps.distance_matrix(origin, dest)
                    #print(matrix)
                    distanceInMile = float(matrix['rows'][0]['elements'][0]['distance']['text'].split(' ')[0])/1.6
                    #print(distanceInMile)
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO     demosite_distancetable(apart_key_id, dest_addr, distance) \
                                    VALUES          (%s, %s, %s)", [apart_key, dest, distanceInMile])
                    cursor.close()
                    return StreamingHttpResponse(distanceInMile)
                except Exception as e:
                    print(e)
                    return StreamingHttpResponse('1.00')
        except:
            return StreamingHttpResponse('1.00')
    return StreamingHttpResponse('it was GET request')

def update_nearby(request):
    if request.method=='GET':
        try: 
            cursor = connection.cursor()
            cursor.execute("SELECT apart_key_id FROM demosite_ratingtable")
            cursor.close()
            entry = cursor.fetchall()
            for apart in entry:
                id = apart[0]
                cursor = connection.cursor()
                cursor.execute("SELECT apart_addr FROM demosite_apartmentfeature WHERE apart_key=%s", id)
                cursor.close()
                addr = cursor.fetchall()[0][0]
                print(addr)
                gmaps = googlemaps.Client(key = 'AIzaSyD8Fru1q7cYQvzjRWlE5m9T3tAPlWGBowE')
                location = '309 E Green St Champaign IL'
                geocode_result = gmaps.geocode(addr)
                lat = geocode_result[0]['geometry']['location']['lat']
                lng = geocode_result[0]['geometry']['location']['lng']
                #05
                r05 = len(gmaps.places_nearby(location=(lat, lng), radius = 200, keyword = 'resturants')['results'])
                s05 = len(gmaps.places_nearby(location=(lat, lng), radius = 200, keyword = 'supermarket')['results'])
                #1
                r1 = len(gmaps.places_nearby(location=(lat, lng), radius = 500, keyword = 'resturants')['results'])
                s1 = len(gmaps.places_nearby(location=(lat, lng), radius = 500, keyword = 'supermarket')['results'])
                #2
                r2 = len(gmaps.places_nearby(location=(lat, lng), radius = 800, keyword = 'resturants')['results'])
                s2 = len(gmaps.places_nearby(location=(lat, lng), radius = 800, keyword = 'supermarket')['results'])
                print(r05, r1, r2, s05, s1, s2)
                envrating = max(5, (r05+r1+r2+s05+s1+s2)/100)
                cursor = connection.cursor()
                cursor.execute("UPDATE     demosite_ratingtable \
                                SET        env_rating = %s, rest_05_count = %s, rest_1_count = %s, rest_2_count = %s, \
                                           shop_05_count = %s, shop_1_count = %s, shop_2_count = %s \
                                WHERE      apart_key_id = %s", [envrating, r05, r1, r2, s05, s1, s2, apart])
                cursor.close()
                print('updated')
            return StreamingHttpResponse('success')
        except Exception as e:
            print(e)
            return StreamingHttpResponse('Error')
    return StreamingHttpResponse('it was POST request')

def AF1_comment_add_trigger():
    trigger = "CREATE TRIGGER auto_ratings_update \
                AFTER INSERT ON demosite_peoplerating \
                FOR EACH ROW \
	            BEGIN \
	            CALL update_ppl_rating(NEW.apart_key_id); \
	            END"
    cursor = connection.cursor()
    cursor.execute(trigger)
    cursor.close()

def AF1_comment_add_stored_procedure():
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

def test(request):
    key = '309'
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT     r.cover_internet_fee, r.cover_electricity_fee, r.private_washing_machine, r.number_of_bedroom, \
                                        r.number_of_bathroom, r.has_kitchen, r.has_refigerator, r.cover_water_fee, r.has_tv, r.size, r.room_key_id, k.apart_key_id \
                    FROM        (SELECT * FROM demosite_keytable WHERE apart_key_id = %s) k JOIN demosite_roomfeature r ON k.room_key = r.room_key_id", key)
    entry = cursor.fetchall()
    print(entry)
    cursor.close()
    return StreamingHttpResponse("done") 


def new_show(request):
    if request.method=='POST':
        try:
            key = json.loads(request.body.decode("utf-8"))['showinfo']['apart_key']
            data = []
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM demosite_ratingtable WHERE apart_key_id = %s", key)
            entry = cursor.fetchall()
            cursor.close()
            entry = tuple(entry)
            temparray = []
            for i in entry:
                temp_dictionary =  {}
                temp_dictionary['rest05']  =i[3]
                temp_dictionary['rest1'] = i[4]
                temp_dictionary['rest2'] = i[5]
                temp_dictionary['shop05'] = i[6]
                temp_dictionary['shop1'] = i[7]
                temp_dictionary['shop2'] = i[8]
                temparray.append(temp_dictionary)
            data.append(temparray)
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT     r.cover_internet_fee, r.cover_electricity_fee, r.private_washing_machine, r.number_of_bedroom, \
                                                r.number_of_bathroom, r.has_kitchen, r.has_refigerator, r.cover_water_fee, r.has_tv, r.size, r.room_key_id, k.apart_key_id, r.url \
                            FROM        (SELECT * FROM demosite_keytable WHERE apart_key_id = %s) k JOIN demosite_roomfeature r ON k.room_key = r.room_key_id", key)
            entry = cursor.fetchall()
            cursor.close()
            entry = tuple(entry)
            temparray = []
            for i in entry:
                temp_dictionary =  {}
                temp_dictionary['cover_internet_fee']  =i[0]
                temp_dictionary['cover_electricity_fee'] = i[1]
                temp_dictionary['private_washing_machine'] = i[2]
                temp_dictionary['number_of_bedroom'] = i[3]
                temp_dictionary['number_of_bathroom'] = i[4]
                temp_dictionary['has_kitchen'] = i[5]
                temp_dictionary['has_refigerator'] = i[6]
                temp_dictionary['cover_water_fee'] = i[7]
                temp_dictionary['has_tv'] = i[8]
                temp_dictionary['size'] = i[9]
                temp_dictionary['roomkey'] = i[10]
                temp_dictionary['url'] = i[12]
                temparray.append(temp_dictionary)
            data.append(temparray)
            cursor = connection.cursor()
            cursor.execute("SELECT      apart_addr, parking, study_room, lounge, front_desk, apart_key \
                            FROM        demosite_apartmentfeature \
                            WHERE       apart_key = %s", key)
            entry = cursor.fetchall()
            cursor.close()
            entry = tuple(entry)
            temparray = []
            for i in entry:
                temp_dictionary =  {}
                temp_dictionary['apart_addr']  =i[0]
                temp_dictionary['parking'] = i[1]
                temp_dictionary['study_room'] = i[2]
                temp_dictionary['lounge'] = i[3]
                temp_dictionary['front_desk'] = i[4]
                temparray.append(temp_dictionary)
            data.append(temparray)
            cursor = connection.cursor()
            cursor.execute("SELECT      env_rating, ppl_rating, apart_key_id \
                            FROM        demosite_ratingtable \
                            WHERE       apart_key_id = %s", key)
            entry = cursor.fetchall()
            cursor.close()
            entry = tuple(entry)
            temparray = []
            temparray = []
            for i in entry:
                temp_dictionary =  {}
                temp_dictionary['env_rating']  =i[0]
                temp_dictionary['ppl_rating'] = i[1]
                temparray.append(temp_dictionary)
            data.append(temparray)
            cursor = connection.cursor()
            cursor.execute("SELECT      rating, comment, nick_name, apart_key_id \
                            FROM        demosite_peoplerating \
                            WHERE       apart_key_id = %s", key)
            entry = cursor.fetchall()
            cursor.close()
            entry = tuple(entry)
            temparray = []
            for i in entry:
                temp_dictionary =  {}
                temp_dictionary['rating']  =i[0]
                temp_dictionary['comment'] = i[1]
                temp_dictionary['nick_name'] = i[2]
                temparray.append(temp_dictionary)
            data.append(temparray)
            print(data)
            return StreamingHttpResponse(json.dumps(data))
        except Exception as e:
            print(e)
            print("error")
            return StreamingHttpResponse("Error") 
    return StreamingHttpResponse('it was GET request')

def selectforyou(request):
    if request.method=='POST' or request.method=='GET':
        input = json.loads(request.body.decode("utf-8"))['Questions']
        #input = {'weights': {'washing': 1, 'nosharebath': 0, 'kitchen': 0, 'tv': 1, 'car': 0, 'study': 0, 'lounge': 0, 'shopping': 0}, 'dest1': '309 E Green St, Champaign IL 61820', 'dest2': '201 N Goodwin Ave, Urbana, IL 61801', 'dest3': '1401 W Green St, Urbana, IL 61801'}
        #print(input)
        weights = input['weights']
        total = 0
        for i in weights:
            weights[i] += 0.3
            total += weights[i]
        for i in weights:
            weights[i] /= total
            weights[i] *= 5
        #print(weights)
        #env_rating
        cursor = connection.cursor()
        cursor.execute("SELECT apart_key_id, room_key, private_washing_machine, number_of_bathroom, number_of_bedroom, has_kitchen, has_tv FROM demosite_keytable K JOIN demosite_roomfeature R on K.room_key = R.room_key_id")
        features = cursor.fetchall()
        env_rating = {}
        for i in features:
            name = i[0]
            washing = i[2]
            if(i[3] == i[4]):
                nosharebath = 1
            else:
                nosharebath = 0
            kitchen = i[5]
            tv = i[6]
            tempenvrating = washing * weights['washing'] + nosharebath * weights['nosharebath'] + kitchen * weights['kitchen'] + tv * weights['tv']
            if name not in env_rating:
                env_rating[name] = tempenvrating
            else:
                env_rating[name] = (env_rating[name] + tempenvrating) / 2
        cursor = connection.cursor()
        cursor.execute("SELECT apart_key, parking, study_room, lounge, front_desk FROM demosite_apartmentfeature")
        features = cursor.fetchall()
        for i in features:
            name = i[0]
            temppr = weights['car'] * i[1] + weights['study'] * i[2] + weights['lounge'] * i[3] + weights['shopping'] * i[4]
            env_rating[name] += temppr
        print(env_rating)
        cursor.close()
        #keytable_entry = tuple(keytable_entry)

        #pplrating
        cursor = connection.cursor()
        cursor.execute("SELECT apart_key_id, ppl_rating FROM demosite_ratingtable")
        pplrating = cursor.fetchall()
        ppl_rating = {}
        for i in pplrating:
            ppl_rating[i[0]] = i[1]
        print(ppl_rating)

        #locationrating
        l1 = input['dest1']
        l2 = input['dest2']
        l3 = input['dest3']
        locationrating = {}
        temploc = {}
        mindis = 50
        for i in env_rating:
            totaldis = 0.0
            d = {'distance':{'apart_key': i, 'dest': l1}}
            url = "http://18.217.253.58:8000/AF1Distance"
            r = requests.post(url, data=json.dumps(d))
            totaldis += float(r.text)
            d = {'distance':{'apart_key': i, 'dest': l2}}
            url = "http://18.217.253.58:8000/AF1Distance"
            r = requests.post(url, data=json.dumps(d))
            totaldis += float(r.text)
            d = {'distance':{'apart_key': i, 'dest': l3}}
            url = "http://18.217.253.58:8000/AF1Distance"
            r = requests.post(url, data=json.dumps(d))
            totaldis += float(r.text)
            print(i, totaldis)
            if mindis > totaldis:
                mindis = totaldis
            temploc[i] = totaldis
        print(temploc)
        print(mindis)
        for i in temploc:
            dis = temploc[i]
            rate = math.log(dis/mindis)
            locationrating[i] = 5 - rate * 3
        print(locationrating)
        data = []
        #print(env_rating)
        #print(ppl_rating)
        #print(locationrating)
        tempdict = {}
        for i in locationrating:
            smart = (env_rating[i] + ppl_rating[i] + locationrating[i])/3
            tempdict[i] = smart
        sorting = sorted(tempdict.keys())[::-1]
        print(sorting)
        for i in sorting:
            smart = (env_rating[i] + ppl_rating[i] + max(1,locationrating[i]))/3
            finaldict = {'apart': i, 'env': env_rating[i], 'ppl': ppl_rating[i], 'loc': min(max(1,locationrating[i]),5), 'smart': min(max(1,smart),5)}
            data.append(finaldict)
        print(data)
        return StreamingHttpResponse(json.dumps([data]))
    return StreamingHttpResponse('it was GET request')
def parse_json_filter(raw_input):
    output = []
    if raw_input['parking']:
        output.append(1)
    print("reach here1")
    if raw_input['study_room']:
        output.append(2)
    print("reach here2")
    if raw_input['lounge']:
        output.append(3)
    print("reach here3")
    if raw_input['front_desk']:
        output.append(4)
    print("reach here4")
    if raw_input['cover_internet_fee']:
        output.append(5)
    print("reach here5")
    if raw_input['cover_electricity_fee']:
        output.append(6)
    print("reach here6")
    if raw_input['private_washing_machine']:
        output.append(7)
    print("reach here7")
    if raw_input['has_kitchen']:
        output.append(8)
    print("reach here8")
    if raw_input['has_refrigerator']:
        output.append(9)
    print("reach here9")
    if raw_input['cover_water_fee']:
        output.append(10)
    print("reach here10")
    if raw_input['has_tv']:
        output.append(11)
    if raw_input['bedrooms'] != 0:
        output.append(str(raw_input['bedrooms']*10)+'bed')
    if raw_input['restrooms'] != 0:
        output.append(str(raw_input['restrooms']*10)+'bath')
        
    print("this is the: ", output)
    return output

def advance_filter(request):
    if request.method=='POST':
        try:
            Graph = FindExample("bolt://localhost", "matcha_squad", "matcha") #need to use a config file
            filter = json.loads(request.body.decode("utf-8"))['Filter']
            print("do we have filter?", filter)
            filter = parse_json_filter(filter)
            print(filter)
            result = Graph.apply_filter(filter)
            Graph.close()
            cursor = connection.cursor()
            query = "SELECT A.apart_key, A.apart_addr, R.env_rating, R.ppl_rating FROM demosite_apartmentfeature A JOIN demosite_ratingtable R on A.apart_key = R.apart_key_id "
            cursor.execute(query)
            keytable_entry = cursor.fetchall()
            cursor.close()
            data=[]
            keytable_entry = tuple(keytable_entry)
            for i in keytable_entry:
                if i[0] not in result:
                    continue
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

def similar_apart(request):
    if request.method=='POST':
        try:
            Graph = FindExample("bolt://localhost", "matcha_squad", "matcha") #need to use a config file
            filter = json.loads(request.body.decode("utf-8"))['similar_room']['room_key']
            print("the given: ", filter)
            result = Graph.apply_recon(filter)
            Graph.close()
            cursor = connection.cursor()
            query = "SELECT A.apart_key, A.apart_addr, R.env_rating, R.ppl_rating FROM demosite_apartmentfeature A JOIN demosite_ratingtable R on A.apart_key = R.apart_key_id "
            cursor.execute(query)
            keytable_entry = cursor.fetchall()
            cursor.close()
            data=[]
            keytable_entry = tuple(keytable_entry)
            for i in keytable_entry:
                if i[0] not in result:
                    continue
                temp_dictionary =  {}
                temp_dictionary['apart_key']  =i[0]
                temp_dictionary['apart_addr'] = i[1]
                temp_dictionary['overallrating'] = (float(i[2]) + float(i[3]))/2.0
                temp_dictionary['similarity'] = round(result[i[0]], 2)
                data.append(temp_dictionary)
            return StreamingHttpResponse(json.dumps(data))
        except Exception as e:
            print(e)
            print("error")
            return StreamingHttpResponse("Error") 
    return StreamingHttpResponse('it was POST request')