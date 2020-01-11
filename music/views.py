from django.shortcuts import render

def welcome(request):
    return render(request,'music/welcome.html',{'title':'Welcome'})
