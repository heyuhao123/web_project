from django.shortcuts import render

# Create your views here.
def index(request):
    context={'title':'i am the king!'}
    return render(request,'index.html',context)