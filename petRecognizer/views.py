import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from .forms import PetImageForm


from yolov5.detect import run

def first_page(request):
    if request.method=='POST':
        form = PetImageForm(request.POST,request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.save()
            
            # Image 업로드 후 YOLOV5 모델 여기서 적용!
            upload_image_path = image_instance.image.path

            try:
                result = run(weights='yolov5/runs/train/pet_yolov5s_results/weights/best.pt',source=upload_image_path,imgsz=(640,640),conf_thres=0.5)
                print("result 결과 : ",result)
            except Exception as e:
                print("오류 발생:",e)
            
            # 객체 감지 결과를 session에 저장
            request.session['detection_result'] = {
                'image_path':upload_image_path,
                'detections':result,
            }

            return redirect('second_page')

            # 객체 감지 결과를 query 매개변수로 전달
            # return redirect('second_page',detection_result=result)
    else:
        form = PetImageForm()

    return render(request,'first.html',{'form':form})


def second_page(request):
    detection_result = request.session.get('detection_result')

    print("객체 탐지 결과 : ",detection_result)

    uploaded_image = detection_result['image_path']
    detected_class = detection_result['detections'][0]

    relative_path = uploaded_image.replace(settings.MEDIA_ROOT,'').replace('\\','/') 
    # image_path = os.path.join(settings.MEDIA_URL,relative_path)
    image_path = '/'.join([settings.MEDIA_URL.rstrip('/'), relative_path.lstrip('/')])

    # 품종에 대한 설명 만들어둔 DB에서 가져오기

    # 네이버 뉴스 헤드라인 가져오기

    context = {
        'image_path':image_path,
        'detected_class':detected_class,
    }

    return render(request,'second.html',context)

