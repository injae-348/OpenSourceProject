import os
import json
import subprocess
import requests
from bs4 import BeautifulSoup

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from .forms import PetImageForm
from .models import PetBreed

from yolov5.detect import run

from gtts import gTTS
from django.http import FileResponse
import io

# 첫번째 페이지
def first_page(request):
    # POST 요청시(이미지를 올리고 결과 확인 버튼을 눌렀을 때)
    if request.method=='POST':
        form = PetImageForm(request.POST,request.FILES)
        if form.is_valid():
            # 폼을 확인해서 이미지를 저장
            image_instance = form.save(commit=False)
            image_instance.save()
            
            # Image 업로드 후 YOLOV5 모델 여기서 적용!
            upload_image_path = image_instance.image.path

            # yolov5s 에서 학습 시킨 가중치를 가지고 run 실행
            try:
                result = run(weights='yolov5/runs/train/pet_yolov5s_results/weights/best.pt',source=upload_image_path,imgsz=(640,640),conf_thres=0.5)
                print("result 결과 : ",result)
            except Exception as e:
                print("오류 발생:",e)
            
            # 객체 감지 결과 & 이미지 경로를 session에 저장
            request.session['detection_result'] = {
                'image_path':upload_image_path,
                'detections':result,
            }

            # 두번째 페이지로 redirect(연결: url 창에 주소를 넣어준다고 생각하면됨)
            return redirect('second_page')
    else:
        # POST 요청이 아닐시 => 폼 양식 생성
        form = PetImageForm()

    # render를 통해 first.html 템플릿을 생성
    return render(request,'first.html',{'form':form})

#==============================================================

def get_news_data(breed):
    try:
        search_query = breed  # 여기에 검색어를 breed로 바꿔 사용하세요
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={search_query}"
        
        # 네이버 뉴스 페이지에 GET 요청 보내기
        response = requests.get(url)
        
        # 페이지가 성공적으로 응답했는지 확인
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_list = soup.select("a.news_tit")

            news_data_combined = []
            for news in news_list:
                headline = news.text
                link = news['href']

                news_data_combined.append((headline, link))

            return news_data_combined

        else:
            print(f"네이버 뉴스에서 데이터를 가져오지 못했습니다. 상태 코드: {response.status_code}")
            return []

    except Exception as e:
        print(f"크롤링 중 에러 발생: {e}")
        return []
#==============================================================

# 두번째 페이지(결과 페이지)
def second_page(request):
    # 세션에 저장되어 있는 결과 & 이미지 경로를 가져옴
    detection_result = request.session.get('detection_result')

    # class.json 파일을 읽어와 영어로 출력된 클래스 이름을 한국어로 변환
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file_path = os.path.join(BASE_DIR, 'class.json')

    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        translated_classes = json.load(json_file)

    print("객체 탐지 결과 : ", detection_result)
    try:
        # 세션에 저장되어있던 이미지 경로
        uploaded_image = detection_result['image_path']
        # 세션에 저장되어있던 클래스 영어 이름 결과
        detected_class = detection_result['detections'][0]
        # 한국어로 변경한 값
        detected_class_kor = translated_classes.get(detected_class, "번역할 수 없는 값")
    except (KeyError, IndexError):
        # 만약 에러가 발생시 에러 페이지로 redirect(연결)
        return redirect('error_page')

    relative_path = uploaded_image.replace(settings.MEDIA_ROOT, '').replace('\\', '/')
    image_path = '/'.join([settings.MEDIA_URL.rstrip('/'), relative_path.lstrip('/')])

    # 품종에 대한 설명 만들어둔 DB에서 가져오기
    try:
        breed_object = PetBreed.objects.get(breed=detected_class)
        detected_class_description = breed_object.description

    # tts를 DB에 불러와서 읽기
        tts = gTTS(text=detected_class_description, lang='ko')
        tts_path = os.path.join(settings.MEDIA_ROOT, 'tts_output.mp3')
        tts.save(tts_path)

    # 파일을 읽어와서 응답에 사용
        with open(tts_path, 'rb') as audio_file:
            audio_content = audio_file.read()

    # 파일을 읽은 후에 파일을 닫아도 되기 때문에 with 블록 종료 후에 응답을 생성
        response = FileResponse(io.BytesIO(audio_content), content_type='audio/mp3')
        response['Content-Disposition'] = 'inline; filename=tts_output.mp3'
    
    except PetBreed.DoesNotExist:
        detected_class_description = "설명이 없습니다."
        tts_path = None

    relative_path = uploaded_image.replace(settings.MEDIA_ROOT, '').replace('\\', '/')
    image_path = '/'.join([settings.MEDIA_URL.rstrip('/'), relative_path.lstrip('/')])
    # 네이버 뉴스 헤드라인 가져오기

    # second.html 파일에서 사용할 정보 담아두는 객체
    # 품종에 대한 설명, 뉴스 등도 여기에 추가
    context = {
         'image_path':image_path,
         'detected_class':detected_class,
         'detected_class_kor':detected_class_kor,
         'detected_class_description':detected_class_description,
         'tts_path': tts_path,
    }

    return render(request,'second.html',context)
# Ajax 요청 처리
def get_news(request):
    if request.method == 'GET' and 'breed' in request.GET:
        breed = request.GET['breed']
        news_data_combined = get_news_data(breed)
        return JsonResponse({'news_data_combined': news_data_combined})
    return JsonResponse({'error': 'Invalid request'})
#==============================================================


#==============================================================

# 에러 페이지
def error_page(request):
    return render(request,'error.html')

#==============================================================

