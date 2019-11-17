from demosite.models import KeyTable
from django.views.generic import TemplateView
from django.db import connection

def test_insert(request):
    apart_name = "HERE"
    apart_addr = "308 East Green Street"
    apart_key = apart_name.upper()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO     demosite_keytable(apart_name, apart_addr, apart_key) \
                    VALUES          (%s, %s, %s)", [apart_name, apart_addr, apart_key])
    keytables = KeyTable.objects.all()
    cursor.close()
    return render(request, 'show.html', {'keytables':keytables})

def test_delete(request):
    room_key = 1
    cursor = connection.cursor()
    cursor.execute("DELETE FROM     demosite_keytable \
                    WHERE           demosite_keytable.room_key = %s", [room_key])
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})


def test_update(request):
    room_key = 1
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

def test_apt_feature_insert(request):
    apart_key = "HERE" 
    parking = 1 
    study_room = 1 
    lounge = 1 
    front_desk = 1
    cursor = connection.cursor()
    cursor.execute("INSERT INTO     demosite_apartmentfeature(apart_key, parking, study_room, lounge, front_desk) \
                    VALUES          (%s, %s, %s, %s, %s)", [apart_key, parking, study_room, lounge, front_desk])
    keytables = KeyTable.objects.all()
    cursor.close()
    return render(request, 'show.html', {'keytables':keytables})

def test_apt_feature_delete(request):
    apart_key = "HERE"
    cursor = connection.cursor()
    cursor.execute("DELETE FROM     demosite_apartmentfeature \
                    WHERE           apart_key = %s", [apart_key])
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def test_get_rooms_count(request):
    apart_name = "HERE"
    cursor = connection.cursor()
    cursor.execute("SELECT    COUNT(*) \
                    FROM      demosite_keytable k NATURAL JOIN demosite_apartmentfeature f \
                    GROUP BY  apart_name \
                    HAVING    apart_name = %s", [apart_name])
    result = cursor.fetchall()
    print(result)
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def test_get_apart_with_parking_and_study_room(request): 
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT   k.apart_name \
                    FROM              demosite_keytable k NATURAL JOIN demosite_apartmentfeature f \
                    GROUP BY          k.apart_name \
                    HAVING            f.parking = 1 \
                    INTERSECT \
                    SELECT DISTINCT   k.apart_name \
                    FROM              demosite_keytable k NATURAL JOIN demosite_apartmentfeature f \
                    GROUP BY          k.apart_name \
                    HAVING            f.study_room = 1")
    keytable_entry = cursor.fetchall()
    print(keytable_entry)
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})
