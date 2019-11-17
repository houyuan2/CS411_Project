from django.shortcuts import render, redirect
from demosite.forms import KeyForm
from demosite.models import KeyTable
from demosite.models import ApartmentFeature
from json import dump
from django.db import connection
from django.core import serializers

import json
from django.http import StreamingHttpResponse

from demosite.models import KeyTable
from rest_framework import generics

from .serializers import KeyTableSerializer#, ApartmentFeatureSerializer

#def room_key(request):
    # insert a room key_table entry into key_table
    # 
    #if request.method == "POST": #and request.value == "Submit":
    #    form = KeyForm(request.POST)
    #    if form.is_valid():

    #        try:
     #           print(form.apart_name)
    #            form.save()
    #            return redirect('/show')  #to be implemented
    #        except:
   #             pass
   # else:
   #     form = KeyForm()
   #  return render(request, 'front.html' , {'form':form})

class KeyTableListCreate(generics.ListCreateAPIView):
    queryset = KeyTable.objects.all()
    serializer_class = KeyTableSerializer

#class ApartmentFeatureListCreate(generics.ListCreateAPIView):
#    queryset = ApartmentFeature.objects.all()
#    serializer_class = ApartmentFeatureSerializer

def show(request):
    if request.method == "GET": 
        keytables = KeyTable.objects.all()
        apartmentfeatures = ApartmentFeature.objects.all()
        #data = serializers.serialize("json", keytables)
        #data2 = serializers.serialize("json", apartmentfeatures)
        return render(request, 'show.html', {'keytables':keytables, 'apartmentfeatures':apartmentfeatures})

def test_insert(request):
    apart_name = "Presby"
    apart_addr = "405 East John Street"
    apart_key = apart_name.upper()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO     demosite_keytable(apart_name, apart_addr, apart_key) \
                    VALUES          (%s, %s, %s)", [apart_name, apart_addr, apart_key])
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def test_delete(request):
    room_key = 6
    cursor = connection.cursor()
    cursor.execute("DELETE FROM     demosite_keytable \
                    WHERE           demosite_keytable.room_key = %s", [room_key])
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def test_update(request):
    room_key = 2
    apart_name = "Campus Center"
    apart_addr = "601 South 6TH Street"
    apart_key = apart_name.upper()
    cursor = connection.cursor()
    cursor.execute("UPDATE     demosite_keytable \
                    SET        apart_name = %s, apart_addr = %s, apart_key = %s \
                    WHERE      room_key = %s", [apart_name, apart_addr, apart_key, room_key])
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def test_get(request):
    room_key = 5
    cursor = connection.cursor()
    cursor.execute("SELECT    * \
                    FROM      demosite_keytable \
                    WHERE     room_key > %s", [room_key])
    keytable_entry = cursor.fetchall()
    print(keytable_entry)
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def test_apt_feature_insert(request):
    apart_key = "PRESBY" 
    parking = 0 
    study_room = 0
    lounge = 1 
    front_desk = 1
    cursor = connection.cursor()
    cursor.execute("INSERT INTO     demosite_apartmentfeature(apart_key, parking, study_room, lounge, front_desk) \
                    VALUES          (%s, %s, %s, %s, %s)", [apart_key, parking, study_room, lounge, front_desk])
    apartfeature = ApartmentFeature.objects.all()
    cursor.close()
    return render(request, 'show.html', {'apartmentfeatures':apartfeature})

def test_apt_feature_delete(request):
    apart_key = "PRESBY"
    cursor = connection.cursor()
    cursor.execute("DELETE FROM     demosite_apartmentfeature \
                    WHERE           apart_key = %s", [apart_key])
    cursor.close()
    apartfeature = ApartmentFeature.objects.all()
    return render(request, 'show.html', {'apartmentfeatures':apartfeature})

def test_get_rooms_count(request):
    num = 0
    try:
        apart_name = "latitude"
        apart_key = apart_name.upper()
        cursor = connection.cursor()
        cursor.execute("SELECT    COUNT(*) \
                        FROM      demosite_keytable\
                        GROUP BY  apart_key \
                        HAVING    apart_key = %s", [apart_key])
        result = cursor.fetchall()
        cursor.close()
        #print(result)
        num = tuple(result)[0][0]
    except:
        print("apartment doesn't exist")
    print(num)
    keytables = KeyTable.objects.all()
    apartfeature = ApartmentFeature.objects.all()
    return render(request, 'show.html', {'keytables':keytables, 'apartmentfeatures':apartfeature})

def test_get_apart_with_parking_and_study_room(request): 
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT a.apart_name FROM \
                    (SELECT            apart_name \
                    FROM              demosite_keytable k NATURAL JOIN demosite_apartmentfeature f \
                    GROUP BY          apart_key, apart_name, parking\
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
    keytables = KeyTable.objects.all()
    apartfeature = ApartmentFeature.objects.all()
    return render(request, 'show.html', {'keytables':keytables, 'apartmentfeatures':apartfeature})

def insert(request):
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
                cursor.execute("INSERT INTO     demosite_keytable(apart_name, apart_addr, apart_key) \
                            VALUES          (%s, %s, %s)", [apart_name, apart_addr, apart_key])
                return StreamingHttpResponse('received')
 #           else:
 #               form = NameForm()
    return StreamingHttpResponse('it was GET request') 
    #keytables = KeyTable.objects.all()
    #data = serializers.serialize("json", KeyTable.objects.all())   
 #   return render(request, 'show.html', {'keytables':form})

# Create your views here.

def delete(request):
    if request.method=='POST':
            todo = json.loads(request.body.decode("utf-8"))
            room_key = todo['deleteroom']['roomkey']
            cursor = connection.cursor()
            cursor.execute("DELETE FROM     demosite_keytable \
                            WHERE           demosite_keytable.room_key = %s", [room_key])
            cursor.close()
            return StreamingHttpResponse('deleted')
    return StreamingHttpResponse('it was GET request')
    
def update(request):
    if request.method=='POST':
            updatedata = json.loads(request.body.decode("utf-8"))
            apart_name = updatedata['changeapartment']['aptname']
            apart_addr = updatedata['changeapartment']['aptadd']
            apart_key = apart_name.upper()
            room_key = updatedata['changeapartment']['roomkey']
            cursor = connection.cursor()
            cursor.execute("UPDATE     demosite_keytable \
                            SET        apart_name = %s, apart_addr = %s, apart_key = %s \
                            WHERE      room_key = %s", [apart_name, apart_addr, apart_key, room_key])
            cursor.close()
            return StreamingHttpResponse('updated')
            
def apt_feature_insert(request):
    if request.method=='POST':
        aptdata = json.loads(request.body.decode("utf-8")) 
        apart_name = aptdata['newapartmentfeature']['aptname']
        parking = aptdata['newapartmentfeature']['parking']
        study_room = aptdata['newapartmentfeature']['study_room']
        lounge = aptdata['newapartmentfeature']['lounge']
        front_desk = aptdata['newapartmentfeature']['front_desk']
        apart_key = apart_name.upper()
        parking = int(parking)
        study_room = int(study_room)
        lounge = int(lounge)
        front_desk = int(front_desk)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO     demosite_apartmentfeature(apart_key, parking, study_room, lounge, front_desk) \
                        VALUES          (%s, %s, %s, %s, %s)", [apart_key, parking, study_room, lounge, front_desk])
        cursor.close()
        return StreamingHttpResponse('received')
    return StreamingHttpResponse('it was GET request') 

def apt_feature_delete(request):
    if request.method=='POST':
        aptdata = json.loads(request.body.decode("utf-8")) 
        apart_name = aptdata['deleteapartmentfeature']['aptname']
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
                            FROM      demosite_keytable\
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
                            GROUP BY          apart_key, apart_name, parking\
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