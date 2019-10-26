from django.shortcuts import render, redirect
from demosite.forms import KeyForm
from demosite.models import KeyTable

def room_key(request):
    # insert a room key_table entry into key_table
    # 
    if request.method == "POST": #and request.value == "Submit":
        form = KeyForm(request.POST)
        if form.is_valid():
            try:
                #obj = KeyTable(form)
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
        return render(request, 'show.html', {'keytables':keytables})


# Create your views here.
