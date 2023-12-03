from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import PetImageForm

def index(request):
    return HttpResponse("어서오세요")

def first_page(request):
    if request.method=='POST':
        form = PetImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            
            # Image 업로드 후 YOLOV5 모델 여기서 적용!

            return redirect('second_page')
    else:
        form = PetImageForm()

    return render(request,'first.html',{'form':form})