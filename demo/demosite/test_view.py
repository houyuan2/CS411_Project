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

## after midterm demo

def test_roomfeature_insert(request):
    room_key = 1
    cover_internet_fee = 1
    cover_electricity_fee = 0
    private_washing_machine = 1
    number_of_bedroom = 2
    number_of_bathroom = 1
    has_kitchen = 1
    has_refigerator = 1
    cover_water_fee = 0
    has_tv = 1
    size = 923
    column_list = [room_key, cover_internet_fee, cover_electricity_fee, private_washing_machine,
        number_of_bedroom, number_of_bathroom, has_kitchen, has_refigerator, cover_water_fee, has_tv,
        size]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO     demosite_roomfeature(room_key, cover_internet_fee, cover_electricity_fee, \
        private_washing_machine, number_of_bedroom, number_of_bathroom, has_kitchen, has_refigerator, \
        cover_water_fee, has_tv, size) \
                    VALUES          (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", column_list)
    keytables = KeyTable.objects.all()
    cursor.close()
    return render(request, 'show.html', {'keytables':keytables})

def test_roomfeature_delete(request):
    room_key = 1
    cursor = connection.cursor()
    cursor.execute("DELETE FROM     demosite_roomfeature \
                    WHERE           room_key = %s", [room_key])
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def test_distancetable_insert(request):
    apart_key = "HERE" 
    dest_addr = "siebel"
    distance = 3.7
    cursor = connection.cursor()
    cursor.execute("INSERT INTO     demosite_distancetable(apart_key, dest_addr, distance) \
                    VALUES          (%s, %s, %s)", [apart_key, dest_addr, distance])
    keytables = KeyTable.objects.all()
    cursor.close()
    return render(request, 'show.html', {'keytables':keytables})

def test_distancetable_delete(request):
    search_id = 1
    cursor = connection.cursor()
    cursor.execute("DELETE FROM     demosite_distancetable \
                    WHERE           search_id = %s", [search_id])
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def test_ratingtable_insert(request):
    apart_key = "HERE"
    env_rating = 1.1
    ppl_rating = 2.0
    rest_05_count = 0
    rest_1_count = 0
    rest_2_count = 0
    shop_05_count = 0
    shop_1_count = 0
    shop_2_count = 0
    column_list = [apart_key, env_rating, ppl_rating, rest_05_count, rest_1_count, rest_2_count,
        shop_05_count, shop_1_count, shop_2_count]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO     demosite_ratingtable(apart_key, env_rating, ppl_rating, rest_05_count, rest_1_count, \
        rest_2_count, shop_05_count, shop_1_count, shop_2_count) \
                    VALUES          (%s, %s, %s, %s, %s, %s, %s, %s, %s)", column_list)
    keytables = KeyTable.objects.all()
    cursor.close()
    return render(request, 'show.html', {'keytables':keytables})

def test_ratingtable_delete(request):
    apart_key = "HERE"
    cursor = connection.cursor()
    cursor.execute("DELETE FROM     demosite_ratingtable \
                    WHERE           apart_key = %s", [apart_key])
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def test_peoplerating_insert(request):
    apart_key = "HERE"
    rating = 3.4
    comment = "this is a test comment"
    nick_name = "test_nick_name"
    cursor = connection.cursor()
    cursor.execute("INSERT INTO     demosite_peoplerating(apart_key, rating, comment, nick_name) \
                    VALUES          (%s, %s, %s, %s)", [apart_key, rating, comment, nick_name])
    keytables = KeyTable.objects.all()
    cursor.close()
    return render(request, 'show.html', {'keytables':keytables})

def test_peoplerating_delete(request):
    comment_id = 1
    cursor = connection.cursor()
    cursor.execute("DELETE FROM     demosite_peoplerating \
                    WHERE           comment_id = %s", [comment_id])
    cursor.close()
    keytables = KeyTable.objects.all()
    return render(request, 'show.html', {'keytables':keytables})

def frankie_get_addr(apart_key):
    cursor = connection.cursor()
    cursor.execute("SELECT      f.apart_addr \
                    FROM        demosite_apartmentfeature f \
                    WHERE       f.apart_key = %s", apart_key)
    entry = cursor.fetchall()
    print(entry)
    cursor.close()
    return entry

def frankie_get_distance(origin, dest_addr):
    cursor = connection.cursor()
    cursor.execute("SELECT      t.distance \
                    FROM        demosite_distancetable t \
                    WHERE       t.dest_addr = %s AND t.apart_key_id = %s", [dest_addr, origin])
    entry = cursor.fetchall()
    print(entry)
    cursor.close()
    return entry

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