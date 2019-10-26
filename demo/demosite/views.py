from django.shortcuts import render, redirect
from demosite.forms import KeyForm
from demosite.models import KeyTable
from json import dump
from django.db import connection
from django.core import serializers

import json
from django.http import StreamingHttpResponse

from demosite.models import KeyTable
from demosite.serializers import KeyTableSerializer
from rest_framework import generics
class KeyTableListCreate(generics.ListCreateAPIView):
    queryset = KeyTable.objects.all()
    serializer_class = KeyTableSerializer

def room_key(request):
    # insert a room key_table entry into key_table
    # 
    if request.method == "POST": #and request.value == "Submit":
        form = KeyForm(request.POST)
        if form.is_valid():

            try:
                print(form.apart_name)
                form.save()
                return redirect('/show')  #to be implemented
            except:
                pass
    else:
        form = KeyForm()
    return render(request, 'front.html' , {'form':form})

def show(request):
    if request.method == "GET": 
        keytables = KeyTable.objects.all()
        data = serializers.serialize("json", KeyTable.objects.all())
        return render(request, 'show.html', {'keytables':keytables})

def test_insert(request):
    apart_name = "HERE"
    apart_addr = "308 East Green Street"
    apart_key = hash(apart_name)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO     demosite_keytable(apart_name, apart_addr, apart_key) \
                    VALUES          (%s, %s, %s)", [apart_name, apart_addr, apart_key])
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def test_delete(request):
    room_key = 4
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
    room_key = 1
    cursor = connection.cursor()
    cursor.execute("SELECT    * \
                    FROM      demosite_keytable \
                    WHERE     room_key = %s", [room_key])
    keytable_entry = cursor.fetchall()
    print(keytable_entry)
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def insert(request):
    if request.method=='POST':
            aptdata = json.loads(request.body.decode("utf-8"))
            apart_name = aptdata['aptname']
            apart_addr = aptdata['aptadd']
            apart_key = apart_name.upper()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO     demosite_keytable(apart_name, apart_addr, apart_key) \
                            VALUES          (%s, %s, %s)", [apart_name, apart_addr, apart_key])
            return StreamingHttpResponse('received')
    return StreamingHttpResponse('it was GET request')

# Create your views here.

def delete(request):
    if request.method=='POST':
            todo = json.loads(request.body.decode("utf-8"))
            room_key = todo['roomkey']
            cursor = connection.cursor()
            cursor.execute("DELETE FROM     demosite_keytable \
                            WHERE           demosite_keytable.room_key = %s", [room_key])
            cursor.close()
            return StreamingHttpResponse('deleted')
    return StreamingHttpResponse('it was GET request')